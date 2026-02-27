## Configuration Setups

This folder contains collections of configurations and user setups.

*File: `configs/ci-base-image.yml`*

Setup used to create the container image
that runs container-based CI on GitHub Actions.
This saves time by
starting from a common container image with the initial setup
and running independent VM installs in parallel.

*File: `configs/ci-*.yml`*

Setups for the different container-based CI runs
that are used on GitHub Actions.
This saves time by running independent builds in parallel.

*File: `configs/container.yml`*

Small setup for running inside containers.

*File: `configs/everything.yml`*

Full setup that tries to install as many roles/modules as possible.
Does not work inside containers.

*File: `configs/local.yml`*

Reasonably small setup - used as default when `setup` is not defined on the command line.

*File: `configs/local.yml.sample`*

Commented sample of a setup file.
Copy the content to `local.yml` or a new setup file
and change the content as required.

---

## Differences Between Flavors

Rocky is the only flavor that builds everything.

Ubuntu builds everything except `pvaPy`.

- `bluesky` cannot build in CI because that would need containers inside containers.
  (There are ways to do that, though.)
- EPICS module `pvaPy` - downgrading to 5.3.1 makes it build on Rocky.
  The later versions try to check for boost 1.78.0 and fail.
  5.3.1 won't build on distros with Python 3.12.
  5.3.1 also fails on Ubuntu for different boost version reasons.
- `areaDetector` uses a deprecated function in `xmllib2`;
  Fedora's version is too new.
- `areaDetector` also fails on debian because its version of ansible does not support 'search_string' in lineinfile which is used in adcore_prep.yml. Trying to get an new ansible from the ubuntu ppa (as per ansible docs) fails with dependecy conflicts.
