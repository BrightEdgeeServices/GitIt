# Release 5.2.0

- Remove the ISSUE_TEMPLATE relying on the .github repository for the defaults.
- Add new workflows:
  - py-temp-fork-pvt_merge_with_local-def.yaml
  - py-temp-fork-scheduled_sync_with_upstream-def.yaml
- Removed workflow:
  - python-template-pypi-public-no-docker.yaml
- Updated config files
  - .gitignore
  - pre-commit-config.yaml
- Updated scripts
  - SetupDotEnv.ps1
  - SetupGitHubAccess.ps1
  - SetupPrivateRepoAccess.ps1

______________________________________________________________________

# Release 5.1.0

## General

- Updated the workflows to the latest versions
- Update the issue templates
- Update to the latest version of `beetools`
- Implemented pydantic_settings
- Add tests for code missed.
- Implemented Poetry and removed unnecessary configuration files.
