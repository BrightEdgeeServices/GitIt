# Release 2.1.0

## ER Diagram Version

- [Version 005](https://brightedgeeservices.atlassian.net/wiki/spaces/RDAS/overview)

## General Changes

- Implemented Reahl and configure
- Rename environment variable RTE_ENVIRONEMTN to VENV_ENVIRONMENT.
- Reorganized .gitignore.
- Update pre-commit configuration
- Implement an improved version of `docker-rebuild.ps1`
- Removed the redundant `Docker` file.
- Implement an approved version of initdb.ps1.
- Implement Poetry.

## GitHub

- Rename .yml to .yaml
- Fixed and improved the ISSUE_TEMPLATE's
- Add `release` ISSUE_TEMPLATE
- Merged 01-pre-commit.yml and 02-check-documentation.yml workflow into 01-pre-commit-and-document-check.yaml. Removed
  02-check-documentation.yml
- Enable correct usage of GitHub `secrets`.
- Improved and implemented Poetry in 03-ci.yaml workflow

______________________________________________________________________

# Release 2.0.0

## ER Diagram Version

- [Version 005](https://brightedgeeservices.atlassian.net/wiki/spaces/RDAS/overview)

## General Changes

- Add a `queries` directory to store SQL scripts used in MySQL Workbench or other db tools.
- Implemented `rtecommon`.
- Changed the contents of the `table_test_data.py` from class definition to JSON definitions.
- Changed all the tests to use the dbdef module functions.
- Updated install.ps1 to install rtecommon.
- Corrections to the pyproject.toml file.
- Update the README.MD file.

## Pre-commit

- Updated pre-commit configuration file.
- Introduced `isort` in favour of `reorder-python-imports` due to `black` conflicts.

## GitHub Workflows

- Removed `gitit` Environment requirement from `.github\\workflow\\bugfix.md` and `.github\\workflow\\hotfix.md`.
- Add and update `New Release Checks` in `.github\\workflow\\bugfix.md` and `.github\\workflow\\hotfix.md and`
  `.github\\workflow\\enhancement.md`.
- Changed all the spelling of `organisation` to `organization` to satisfy the spellchecker.

## GitHub CI Workflow

- Add `RTE_ENVIRONMENT`
- Remove 'Set PYTHONPATH' step.
- Remove the `Create Reahl db user` step

## Remove Reahl

- Remove `etc` directory.
- Remove all Reahl code from all code files.
- Removed `main.py`.
- Created a substitution table for real table
- Added `dbdef.py` with database utilities.
- Removed the pytest LoginFixture
- Created replacement functions for Reahl fixtures to clean the db etc.

## Table Changes

### event_worker

- Rename `person_organisation_org_type_id` column to `person_organization_org_type_id`.

### identification

- `nr` column to `nr`

### organization_org_type

- Rename `member` relationship definition to `child`.
- Reference in `phone_s` relationship from `PhoneOrg` to `PhoneOrganizationOrgType`.

### organization_structure

- Removed the id primary key and replaced with `member_type_id`, `parent_id` and `member_id` composite primanry key.
- Change `member` relationship definition to `child`.
- Enable index on

### org_type_registration_type

- New table. See DbDescription.md for details.

### person

- Rename `title` to `social_title` to resolve confusion with chess titles.

### person_organisation_org_type

- Rename `PersonOrganisationOrgType` class to `PersonOrganizationOrgType`
- Rename `person_organisation_org_type` table to `person_organization_org_type`

### person_org_type_registration

- Rename `person_organisation_org_type_id` column to `person_organization_org_type_id`
- Rename person_organization_org_type relationship to person_organization_org_type

### phone_organization_org_type

- Rename `phone_org` table to `phone_organization_org_type`

______________________________________________________________________

# Release 1.1.0

## ER Diagram Version

- [Version 004](https://brightedgeeservices.atlassian.net/wiki/spaces/RDAS/overview)

## General

- Removed some redundant code.
- Develop Phone
- Develop PhonePerson
- Develop PhoneType
- Add .vscode to .gitignore

## Table Changes

### emailaddr_org

- Rename EmailaddrOrg to EmailaddrOrganizationOrgType

### organization_structure_definition

- New table. See DbDescription.md for details.

### sport_discipline

- New table. See DbDescription.md for details.

______________________________________________________________________

# Release 1.0.0

## ER Diagram Version

- [Version 004](https://brightedgeeservices.atlassian.net/wiki/spaces/RDAS/overview)

## General

- Upgrade to Reahl 7
- Disabled the rstcheck in GitHub Workflow due to the README now in Markdown format and updated it.
- Added code for test_table_person_system_account but then disabled it.
  See [GitHub Issue 64](https://github.com/RealTimeEvents/rtedb/issues/64).
- Removed unnecessary code in the test code.
- Updated pre-commit revision hooks
- pyproject.toml
  - Reorganized options alphabetically for better comparison with other versions.
  - Updated Python version to be \<3.13
  - Add mdformat to dev requirements
  - Update persisted list

# Release 0.1.6

## ER Diagram Version

- [Version 004](https://brightedgeeservices.atlassian.net/wiki/spaces/RDAS/overview)

## General

- Pin MySQL to 8.0.34

## Relationship Changes

- Configured Person \<-> OrganizationOrgType as unidirectional relationship.
- Configure OrganizationOrgType \<-> Portfolio as unidirectional relationship.
- Configured Identification \<-> IdentificationType as unidirectional relationship.

## Table Changes

### federation

- Deleted. The federation the person is affiliated to is now stored in `person_organisation_org_type.home_federation.`

### acc_type

- Deleted. Supplier/Customer relationship will be split into different tables and not be governed by AccType.

### bank_acc_detail

- New table. See DbDescription.md for details.

### bank_acc_detail_billing_unit

- New table. See DbDescription.md for details.

### bank_acc_detail_organization_org_type

- New table. See DbDescription.md for details.

### bank_acc_detail_person

- Rename from `bank_acc_detail_person`. See DbDescription.md for details.

### billing_unit_desc

- New table. See DbDescription.md for details.

### family_unit_person

- New table. See DbDescription.md for details.

### billing_unit_person_role

- New table. See DbDescription.md for details.

### family_unit_role

- New table. See DbDescription.md for details.

### identification

- New column `document_path`. The actual document will be stored in the file storage
  and the path to the file in the db field.

### person

- Removed column `system_account_id`. The column was moved to the `person_system_account` table.

### person_bank_acc

- Rename table to `bank_acc_detail_person`.

### organization

- Change `entry_date` to `registration_date`

### organization_org_type

- Remove (replace) `entry_date` and `active`. The combination of the two fields is not
  convenient since an organization is deregistered as a type and then register again.
- Add `registration_date`, `deregistration_date` to replace `entry_date` and `active`.
- Add `federation_country_id` to indicate which country the federation represents.
- See `DbDescription.md` for more.

### person_organisation_org_type

- Remove (replace) `entry_date` and `active`. The combination of the two fields is not
  convenient since a person can resign from an organization and then register again.
- Add `registration_date`, `deregistration_date' to replace `entry_date`and`active\`.
- Add `home_federation` to replace the deleted `federation` table.
- See `DbDescription.md` for more.

### person_org_portfolio

- The `appointment` and `active` field combinations do not sufficiently indicate since
  when the person does not fill the portfolio and when he/she left the portfolio.
  It was replaced with `term_start` and `term_end`.

- Add `term_start`

- Add `term_end`

- Remove `appointment`

- Remove \`active'

### person_system_account

- New table. See DbDescription.md for details.

### portfolio_status

- New table. See DbDescription.md for details.

### relationship

- Moved from "accounting" to "person" group.
- The billing_unit will not be used to define the relationship in a family, but a specific table will be created.

______________________________________________________________________
