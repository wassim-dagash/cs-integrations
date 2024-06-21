# cs-integrations

# Scripts to onboard AWS and Azure Accounts to CS. 

aws_onboard.py and azure_onboard.py:

## Overview

The scripts are designed to interact with the CloudSecure API to create cloud credentials. It supports creating credentials for different types of clouds like AWS and Azure such as AWSRole and AWSFlow. The script accepts various parameters through command-line arguments and sends a POST request to the Illum.io API with the provided data.

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)
- `argparse` library (standard with Python 3.x)
- `json` library (standard with Python 3.x)
- `base64` library (standard with Python 3.x)

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required `requests` library:
   ```sh
   pip install requests
   ```

## Azure Usage 


## AWS Usage

To run the script, use the following command format:

```sh
python script_name.py --tenant-id TENANT_ID --service-account-key SERVICE_ACCOUNT_KEY --service-account-token SERVICE_ACCOUNT_TOKEN --type TYPE --account-id ACCOUNT_ID [additional parameters based on type]
```

### Required Arguments

- `--tenant-id`: CloudSecure Tenant ID.
- `--service-account-key`: CloudSecure Service Account Key.
- `--service-account-token`: CloudSecure Service Account Token.
- `--type`: Type of cloud credential (either `AWSRole` or `AWSFlow`).
- `--account-id`: Customer Account ID.

### Additional Arguments

#### For `AWSRole` Type

- `--role-arn`: ARN of IAM Role (required).
- `--external-id`: CS External ID for trust relationship, usually equals CloudSecure Service Account Key (required).
- `--org-id`: Organization ID, required only when onboarding an organization.
- `--management-account-id`: Master Account ID, required only when onboarding an organization.

#### For `AWSFlow` Type

- `--destinations`: List of S3 ARNs (required).

## Examples

### Creating AWSRole Credentials

```sh
python script_name.py --tenant-id your_tenant_id --service-account-key your_service_account_key --service-account-token your_service_account_token --type AWSRole --account-id your_account_id --role-arn your_role_arn --external-id your_external_id --org-id your_org_id --management-account-id your_management_account_id
```

### Creating AWSFlow Credentials

```sh
python script_name.py --tenant-id your_tenant_id --service-account-key your_service_account_key --service-account-token your_service_account_token --type AWSFlow --account-id your_account_id --destinations arn1 arn2 arn3
```


To run the Azure script, use the following command format:

```sh
python script_name.py --tenant-id TENANT_ID --service-account-key-id SERVICE_ACCOUNT_KEY_ID --service-account-token SERVICE_ACCOUNT_TOKEN --type TYPE [additional parameters based on type]
```

### Additional Arguments

#### For `AzureRole` Type

- `--client-id`: Azure Illumio Registered App Client ID.
- `--client-secret`: Azure Illumio Registered App Client Secret (base64 encoded).
- `--subscription-id`: Subscription ID.
- `--azure-tenant-id`: Azure Tenant ID.

#### For `AzureFlow` Type

- `--subscription-id`: Subscription ID.
- `--azure-tenant-id`: Azure Tenant ID.
- `--destinations`: List of destinations (required).

## Examples

### Creating AzureRole Credentials

```sh
python script_name.py --tenant-id your_tenant_id --service-account-key-id your_service_account_key_id --service-account-token your_service_account_token --type AzureRole --client-id your_client_id --client-secret your_client_secret --subscription-id your_subscription_id --azure-tenant-id your_azure_tenant_id
```

### Creating AzureFlow Credentials

```sh
python script_name.py --tenant-id your_tenant_id --service-account-key-id your_service_account_key_id --service-account-token your_service_account_token --type AzureFlow --subscription-id your_subscription_id --azure-tenant-id your_azure_tenant_id --destinations destination1 destination2
```
