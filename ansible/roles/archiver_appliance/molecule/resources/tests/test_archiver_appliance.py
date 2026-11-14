"""Functional tests: the Phoebus Data Browser can fetch data from the
Archiver Appliance.

The Data Browser reads archived data over the pbraw protocol, which is an
HTTP request to <retrieval URL>/data/getData.raw. The tests take that URL
from the installed Phoebus preferences, archive a counter PV served by a
temporary IOC, and fetch its data from there.
"""

import json
import time
from datetime import datetime, timedelta, timezone

import pytest

PREFERENCES = "/opt/epics-tools/config/preferences.ini"
ARCHIVES_KEY = "org.csstudio.trends.databrowser3/archives="
MGMT_URL = "http://localhost:17665/mgmt/bpl"
APPLIANCE_ID = "appliance0"
TEST_DIR = "/tmp/ci-aa-test"
TEST_PV = "ci:aa:counter"
TEST_DB = (
    f'record(calc, "{TEST_PV}") {{\n'
    '  field(SCAN, "1 second")\n'
    f'  field(INPA, "{TEST_PV}")\n'
    '  field(CALC, "A+1")\n'
    '}\n'
)


def wait_for(check, timeout, interval=5):
    """Call check() until it returns a truthy value or timeout expires."""
    deadline = time.monotonic() + timeout
    while True:
        result = check()
        if result or time.monotonic() > deadline:
            return result
        time.sleep(interval)


def http_get_json(host, url):
    """GET url inside the container; return the parsed JSON or None."""
    cmd = host.run("curl -sf %s", url)
    if cmd.rc != 0:
        return None
    try:
        return json.loads(cmd.stdout)
    except ValueError:
        return None


def databrowser_archive(host):
    """First default archive of the Data Browser, as a plain URL."""
    for line in host.file(PREFERENCES).content_string.splitlines():
        if line.startswith(ARCHIVES_KEY):
            first = line[len(ARCHIVES_KEY):].split("*")[0]
            return first.split("|")[0].replace("\\:", ":").strip()
    return ""


def time_range():
    fmt = "%Y-%m-%dT%H:%M:%S.000Z"
    now = datetime.now(timezone.utc)
    start = (now - timedelta(minutes=10)).strftime(fmt)
    end = (now + timedelta(minutes=10)).strftime(fmt)
    return f"from={start}&to={end}"


@pytest.fixture(scope="module")
def test_ioc(host):
    """Run a temporary IOC serving TEST_PV over PV Access (the Archiver
    Appliance's default protocol)."""
    host.run_expect([0], "mkdir -p %s", TEST_DIR)
    host.run_expect([0], "printf '%%s' %s > %s/test.db", TEST_DB, TEST_DIR)
    host.run_expect(
        [0],
        "bash -lc 'cd %s && setsid nohup softIocPVA -S -d test.db"
        " </dev/null >ioc.log 2>&1 & echo $! >%s/ioc.pid'",
        TEST_DIR,
        TEST_DIR,
    )
    yield
    host.run("kill $(cat %s/ioc.pid)", TEST_DIR)
    print(host.run("cat %s/ioc.log", TEST_DIR).stdout)


def test_databrowser_uses_local_archiver(host):
    assert databrowser_archive(host) == "pbraw://localhost:17665/retrieval"


def test_appliance_is_running(host):
    url = f"{MGMT_URL}/getApplianceInfo?id={APPLIANCE_ID}"
    info = http_get_json(host, url)
    assert info and info.get("identity") == APPLIANCE_ID


def test_databrowser_can_fetch_archived_data(host, test_ioc):
    # The IOC serves the PV
    assert wait_for(
        lambda: host.run("bash -lc 'pvget -w 2 %s'", TEST_PV).rc == 0,
        timeout=30,
        interval=2,
    ), "test IOC does not serve " + TEST_PV

    # The appliance archives it
    host.run_expect(
        [0],
        "curl -sf %s",
        f"{MGMT_URL}/archivePV?pv={TEST_PV}"
        "&samplingperiod=1&samplingmethod=MONITOR",
    )

    def being_archived():
        status = http_get_json(host, f"{MGMT_URL}/getPVStatus?pv={TEST_PV}")
        return bool(status) and status[0].get("status") == "Being archived"

    assert wait_for(being_archived, timeout=180), TEST_PV + " not archived"

    # The Data Browser's archive URL delivers its samples
    retrieval = databrowser_archive(host).replace("pbraw://", "http://", 1)
    query = f"pv={TEST_PV}&{time_range()}"

    def samples():
        data = http_get_json(host, f"{retrieval}/data/getData.json?{query}")
        return data[0].get("data", []) if data else []

    found = wait_for(lambda: len(samples()) >= 3, timeout=120)
    assert found, f"no samples of {TEST_PV} from {retrieval}"

    # ...also in the pbraw format the Data Browser actually requests
    raw = host.run(
        "curl -sf -o /dev/null -w '%%{size_download}' %s",
        f"{retrieval}/data/getData.raw?{query}",
    )
    assert raw.rc == 0 and int(raw.stdout) > 0
