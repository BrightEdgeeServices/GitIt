# rtedb

| **Category** | **Links**                                                                                                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| General      | [![][maintenance_y_img]][maintenance_y_lnk] [![][semver_pic]][semver_link]                                                                                                                 |
| CI           | [![][gha_tests_img]][gha_tests_lnk] [![][pre_commit_ci_img]][pre_commit_ci_lnk] [![][codestyle_img]][codestyle_lnk] <br/>[![][codecov_img]][codecov_lnk] [![][gha_docu_img]][gha_docu_lnk] |
| Github       | [![][gh_issues_img]][gh_issues_lnk] [![][gh_language_img]][gh_language_lnk] [![][gh_last_commit_img]][gh_last_commit_lnk] [![][gh_deployment_img]][gh_deployment_lnk]                      |

\[!\[\]gha_docu_img\]\][gha_docu_lnk]
Create the database used by the RTE system.

# Installation and Setup

1. If you have access to this project you most probably have
   done \[Installation, Setup and Environment Configuration\]<https://brightedgeeservices.atlassian.net/wiki/spaces/DE/overview>.
   If not, follow these steps first.
2. Set environment variables in IDE and virtual environment
3. Local Dvelopment environment
4. Add to the `%SCRIPTS_DIR%\venv_rte-db_setup_custom.bat` file.
   ```
   SET MYSQL_DB_NAME=rte_01
   SET MYSQL_HOST=localhost
   SET MYSQL_INSTALLER_PWD=N0tS0S3curePassw0rd
   SET MYSQL_INSTALLER_USERID=rtinstall
   SET MYSQL_PWD=N0tS0S3curePassw0rd
   SET MYSQL_ROOT_PWD=%MYSQL_PWD%
   ```
5. Add to the pytest environment vairaibles in your IDE. In PyCharm you will have to add it fear each and every test.
   ```
   MYSQL_DB_NAME=rte_01
   MYSQL_HOST=localhost
   MYSQL_INSTALLER_PWD=N0tS0S3curePassw0rd
   MYSQL_INSTALLER_USERID=rtinstall
   MYSQL_PWD=N0tS0S3curePassw0rd
   MYSQL_ROOT_PWD=%MYSQL_PWD%
   MYSQL_TCP_PORT_RTE=50001
   PROJECT_DIR=%PROJECTS_BASE_DIR%\RTE\rte-db
   ```
6. Quality Assurance Environment
7. Production Environment
8. In a command window:
   ```commandline
   vi rte-db
   ```

## References

1. [RTE Design and Specifications](https://brightedgeeservices.atlassian.net/wiki/spaces/RDAS/overview)

2. [Policies & Procedures](https://brightedgeeservices.atlassian.net/wiki/spaces/PP/overview%3E)

[codecov_img]: https://img.shields.io/codecov/c/gh/RealTimeEvents/rtedb "CodeCov"
[codecov_lnk]: (https://app.codecov.io/gh/RealTimeEvents/rtedb) "CodeCov"
[codestyle_img]: https://img.shields.io/badge/code%20style-black-000000.svg "Code Style Black"
[codestyle_lnk]: https://github.com/psf/black "Code Style Black"
[gha_docu_img]: https://img.shields.io/readthedocs/rtedb "Read the Docs"
[gha_docu_lnk]: https://github.com/RealTimeEvents/rtedb/blob/master/.github/workflows/02-check-documentation.yml "Read the Docs"
[gha_tests_img]: https://img.shields.io/github/actions/workflow/status/RealTimeEvents/rtedb/03-ci.yml?label=ci "Test status"
[gha_tests_lnk]: https://github.com/RealTimeEvents/rtedb/blob/master/.github/workflows/03-ci.yml "Test status"
[gh_deployment_img]: https://img.shields.io/github/deployments/RealTimeEvents/rtedb/pypi "PiPy Deployment"
[gh_deployment_lnk]: https://github.com/RealTimeEvents/rtedb/deployments/pypi "PiPy Deployment"
[gh_issues_img]: https://img.shields.io/github/issues-raw/RealTimeEvents/rtedb "GitHub - Issue Counter"
[gh_issues_lnk]: https://github.com/RealTimeEvents/rtedb/issues "GitHub - Issue Counter"
[gh_language_img]: https://img.shields.io/github/languages/top/RealTimeEvents/rtedb "GitHub - Top Language"
[gh_language_lnk]: https://github.com/RealTimeEvents/rtedb "GitHub - Top Language"
[gh_last_commit_img]: https://img.shields.io/github/last-commit/RealTimeEvents/rtedb/master "GitHub - Last Commit"
[gh_last_commit_lnk]: https://github.com/RealTimeEvents/rtedb/commit/master "GitHub - Last Commit"
[maintenance_y_img]: https://img.shields.io/badge/Maintenance%20Intended-%E2%9C%94-green.svg?style=flat-square "Maintenance - intended"
[maintenance_y_lnk]: http://unmaintained.tech/ "Maintenance - intended"
[pre_commit_ci_img]: https://img.shields.io/github/actions/workflow/status/RealTimeEvents/rtedb/01-pre-commit.yml?label=pre-commit "Pre-Commit"
[pre_commit_ci_lnk]: https://github.com/RealTimeEvents/rtedb/blob/master/.github/workflows/01-pre-commit.yml "Pre-Commit"
[semver_link]: https://semver.org/ "Sentic Versioning - 2.0.0"
[semver_pic]: https://img.shields.io/badge/Semantic%20Versioning-2.0.0-brightgreen.svg?style=flat-square "Sentic Versioning - 2.0.0"
