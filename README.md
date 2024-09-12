# Jenkins Pipeline Documentation

This Jenkins pipeline is designed to automate the process of deploying infrastructure using Terraform. The pipeline includes stages for checking out source code from Git, initializing and applying Terraform configurations, and handling failures by cleaning up resources. Below is a detailed explanation of each stage and how the pipeline operates.

---

## Overview

- **Pipeline Type**: Declarative
- **Agent**: `any` (runs on any available Jenkins agent)
- **Primary Tools Used**: Git, Terraform
- **Credentials**: AWS credentials for Terraform operations

## Pipeline Stages

### 1. Checkout SCM
- **Purpose**: This stage checks out the code from the specified Git repository and branch.
- **Configuration**:
  - Uses `GitSCM` plugin for checking out the code.
  - Branch: `*/main`
  - Repository URL: `https://github.com/Ahmedyehia12/LibraryManagmentSystem`
  - Credentials ID: `c6d6be8b-c4b5-450b-a13c-1b8aca95fc69` (used for authentication with the Git repository).

### 2. Setup Plugin Cache Directory
- **Purpose**: This stage sets up a directory for caching Terraform plugins, which can speed up the Terraform operations by avoiding repeated downloads.
- **Configuration**:
  - Creates a cache directory at `/var/lib/jenkins/.terraform.d/plugin-cache` using the `mkdir` command.

### 3. Terraform Init - Backend
- **Purpose**: Initializes the Terraform configuration for the backend, which is responsible for managing the remote state.
- **Configuration**:
  - Runs within the `Terraform/backend-init` directory.
  - Uses AWS credentials (`aws-creds`) to access AWS resources needed for the backend setup.
  - Executes `terraform init` to initialize the backend configuration.

### 4. Terraform Apply - Backend
- **Purpose**: Applies the Terraform configuration for the backend to set up the remote state storage.
- **Configuration**:
  - Runs within the `Terraform/backend-init` directory.
  - Uses AWS credentials (`aws-creds`).
  - Executes `terraform apply -auto-approve` to automatically apply the configuration without manual approval.
- **Post Action**: 
  - On failure, the stage will:
    - Set the build result to `FAILURE`.
    - Echo a failure message.
    - Destroy the resources created during this stage using `terraform destroy -auto-approve`.

### 5. Terraform Init - Main Creation
- **Purpose**: Initializes the main Terraform configuration responsible for creating infrastructure.
- **Conditions**:
  - Only runs if the previous stages did not result in failure.
- **Configuration**:
  - Runs within the `Terraform/main_creation` directory.
  - Uses AWS credentials (`aws-creds`).
  - Executes `terraform init` to initialize the main creation configuration.
- **Post Action**:
  - On failure, the stage will:
    - Set the build result to `FAILURE`.
    - Echo a failure message.
    - Clean up resources created in the backend stage by destroying them using `terraform destroy -auto-approve`.

### 6. Terraform Apply - Main Creation
- **Purpose**: Applies the main Terraform configuration to create the required infrastructure.
- **Conditions**:
  - Only runs if the previous stages did not result in failure.
- **Configuration**:
  - Runs within the `Terraform/main_creation` directory.
  - Uses AWS credentials (`aws-creds`).
  - Executes `terraform apply -auto-approve` to automatically apply the configuration.
- **Post Action**:
  - On failure, the stage will:
    - Set the build result to `FAILURE`.
    - Echo a failure message.
    - Destroy the resources created in the main creation and backend stages using `terraform destroy -auto-approve`.

## Post Actions

- **Always**:
  - Cleans up the workspace (`cleanWs()`), ensuring that the workspace is clean after every pipeline run. This helps to avoid issues caused by leftover files from previous builds.
- **Failure**:
  - Echoes 'Pipeline failed!' to indicate that the pipeline encountered errors.
- **Success**:
  - Echoes 'Pipeline succeeded!' to indicate that all stages were completed successfully.

## Key Points

- **Error Handling**: Each `Terraform Apply` stage includes error handling through the `post` block, which attempts to clean up resources created if the stage fails.
- **Credential Management**: The pipeline uses AWS credentials (`aws-creds`) bound in stages that interact with AWS services through Terraform. These credentials must be configured in Jenkins with the correct access rights.
- **Conditional Execution**: The `when` directive is used to ensure that certain stages only run if previous stages were successful (`currentBuild.result != 'FAILURE'`).
- **Clean-Up Strategy**: The pipeline is designed to clean up resources upon failure to ensure that the AWS environment does not contain unintended or partially deployed resources.

## Requirements

- **Jenkins Plugins**:
  - `Pipeline: AWS Steps`
  - `Git`
  - `Terraform`
- **Credentials**:
  - AWS credentials (`aws-creds`) configured in Jenkins for accessing AWS services.
  - Git credentials (`c6d6be8b-c4b5-450b-a13c-1b8aca95fc69`) for accessing the Git repository.

## Recommendations

- Ensure that the AWS credentials have sufficient permissions to create, modify, and destroy the resources specified in the Terraform configurations.
- Regularly review the pipeline logs to monitor for potential issues, especially in the clean-up steps during failure scenarios.
- Test the pipeline in a non-production environment before applying it in a production setting to ensure that all stages perform as expected.

This detailed documentation should help understand and maintain the pipeline effectively. If there are any changes in the repository structure or AWS configuration, the pipeline will need adjustments accordingly.
