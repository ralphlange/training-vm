# Molecule tests for the phoebus role

Functional tests: the `default` scenario builds Phoebus in a plain
`ubuntu:22.04` container (roles `initial_setup` + `phoebus`), then runs the
testinfra tests in `resources/tests/test_phoebus.py`:

| Test | Checks |
|---|---|
| `test_run_phoebus_wrapper_is_installed` | `/usr/local/bin/run-phoebus` is executable and its JDK exists |
| `test_javafx_matches_architecture` | the product contains `javafx-graphics-<version>-linux.jar` (x86_64) or `…-linux-aarch64.jar` (aarch64), with `<version>` = `phoebus_openjfx_version` from the role defaults |
| `test_phoebus_runs_and_lists_applications` | the built product starts with the installed `preferences.ini`, and `-list` prints `databrowser`, `display_runtime` and `probe` (no display needed) |
| `test_documentation_is_built` | `docs/build/html/index.html` exists |
| `test_documentation_is_included_in_product` | the product's `doc/index.html` exists and matches `phoebus_version` ("Phoebus 6.0.0 documentation"), and the Data Browser help page is included |

CI runs the scenario on x86_64 and aarch64 (`.github/workflows/molecule.yml`).
To run it locally (needs Docker):

```bash
cd ansible/roles/phoebus
molecule test
```
