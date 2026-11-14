"""Functional tests for the phoebus role: the product is built for the
target architecture and runs, and its online help (Sphinx docs) is built
and included in the product."""

import os
import re

import pytest
import yaml

PHOEBUS_SRC = "/opt/epics-tools/lib/phoebus"
PRODUCT = f"{PHOEBUS_SRC}/phoebus-product/target"
PREFERENCES = "/opt/epics-tools/config/preferences.ini"
RUN_PHOEBUS = "/usr/local/bin/run-phoebus"

# JavaFX platform classifier per architecture (see the openjfx parent POM)
JAVAFX_PLATFORM = {"x86_64": "linux", "aarch64": "linux-aarch64"}


@pytest.fixture(scope="module")
def role_defaults():
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "defaults", "main.yml"
    )
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def java(host):
    """The java binary of the JDK that run-phoebus uses."""
    wrapper = host.file(RUN_PHOEBUS).content_string
    match = re.search(r"^export JAVA_HOME=(\S+)", wrapper, re.MULTILINE)
    assert match, f"no JAVA_HOME in {RUN_PHOEBUS}"
    return f"{match.group(1)}/bin/java"


def test_run_phoebus_wrapper_is_installed(host, java):
    assert host.file(RUN_PHOEBUS).mode & 0o111
    assert host.file(java).exists


def test_javafx_matches_architecture(host, role_defaults):
    platform = JAVAFX_PLATFORM[host.system_info.arch]
    version = role_defaults["phoebus_openjfx_version"]
    jar = f"{PRODUCT}/lib/javafx-graphics-{version}-{platform}.jar"
    assert host.file(jar).exists


def test_phoebus_runs_and_lists_applications(host, java):
    # -list loads all application descriptors from the product's classpath
    # and exits without starting the UI
    cmd = host.run(
        "cd %s && %s -Djava.awt.headless=true -jar product-*.jar"
        " -settings %s -list",
        PRODUCT,
        java,
        PREFERENCES,
    )
    assert cmd.rc == 0, cmd.stdout + cmd.stderr
    for app in ("databrowser", "display_runtime", "probe"):
        assert f"'{app}'" in cmd.stdout


def test_documentation_is_built(host):
    assert host.file(f"{PHOEBUS_SRC}/docs/build/html/index.html").exists


def test_documentation_is_included_in_product(host, role_defaults):
    index = host.file(f"{PRODUCT}/doc/index.html")
    assert index.exists
    version = role_defaults["phoebus_version"].lstrip("v")
    assert f"Phoebus {version} documentation" in index.content_string
    assert host.file(f"{PRODUCT}/doc/app/databrowser/doc/index.html").exists
