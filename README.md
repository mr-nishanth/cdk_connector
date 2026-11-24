# CDK Connector

## Overview

The `cdk-connector` repository contains the vendor-specific integration responsible for extracting dealership data from the CDK DMS and preparing it for migration into Tekion ARC.

The connector owns its CDK-specific authentication, navigation, extraction workflows, data handling, transformation and migration behaviour.

CDK extraction logic must remain isolated from other vendor-specific implementations.

## Responsibilities

- Connect to the authorized CDK DMS environment.
- Authenticate using the existing supported authentication mechanism.
- Navigate CDK-specific workflows.
- Extract supported dealership data.
- Handle CDK-specific extraction failures.
- Transform extracted data into the required ARC-compatible format.
- Preserve data integrity during migration.
- Report extraction and processing errors.

## Vendor Identity

| Property | Value |
|---|---|
| Vendor | CDK |
| Repository | cdk-connector |
| Target platform | Tekion ARC |
| Connector type | Vendor-specific DMS connector |

## Architecture

Document the actual implementation here:

- Authentication mechanism: To be documented
- Navigation mechanism: To be documented
- Extraction workflow: To be documented
- Supported data entities: To be documented
- Transformation and mapping: To be documented
- Error-handling strategy: To be documented

## Vendor-Specific Workflow

Document the actual CDK extraction sequence.

| Workflow | Extraction steps | Status |
|---|---|---|
| Customer data | To be documented | Pending |
| Vehicle data | To be documented | Pending |
| Deal data | To be documented | Pending |
| Service data | To be documented | Pending |

Do not reuse extraction step numbering or workflow assumptions from other DMS vendors.

## Repository Development Guidelines

1. Preserve existing CDK extraction behaviour.
2. Investigate the actual affected code path before making changes.
3. Keep modifications limited to the Jira Story scope.
4. Follow established repository architecture and conventions.
5. Add or update tests for changed behaviour.
6. Avoid unnecessary dependency upgrades and refactoring.
7. Do not modify other vendor repositories.

## AI Migration Agent Integration

This repository is registered under the logical vendor identifier `CDK`.

The central repository registry must resolve `CDK` to `cdk-connector`.

The AI Migration Agent may:

- Investigate CDK extraction failures.
- Analyze relevant source files and dependencies.
- Use Graphify to understand code relationships.
- Identify the probable root cause.
- Prepare a targeted implementation plan.
- Modify relevant source files in an isolated Docker workspace.
- Execute available tests.
- Generate a Git diff for deterministic validation.

The AI agent must not determine repository authorization itself.

## Testing and Validation

Before creating a pull request:

- Run relevant unit tests.
- Run relevant integration tests where available.
- Execute configured lint and type checks.
- Inspect the complete Git diff.
- Verify that modifications are within the approved connector scope.
- Check for unintended extraction or mapping regressions.

Actual commands must be verified from the repository configuration.

## Security

- Never commit dealership credentials, cookies or API tokens.
- Redact sensitive values from logs.
- Use approved secure credential handling.
- Preserve existing authentication and authorization controls.

## Documentation Maintenance

Update this README when the CDK extraction architecture, supported workflows, dependencies or test procedures change.

**Note:** This README describes intended responsibilities. Actual CDK implementation details must be verified from the source code.
