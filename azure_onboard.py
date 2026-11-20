import argparse
import base64
import json
import sys

import requests

API_URL = 'https://cloud.illum.io/api/v1/integrations/cloud_credentials'


def b64(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')


def create_cloud_credentials(tenant_id, service_account_key_id, service_account_token, type, api_url=API_URL, **kwargs):
    headers = {
        'X-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + b64(f"{service_account_key_id}:{service_account_token}"),
    }
    data = {'type': type}
    # Only send fields that were actually provided. For tenant-level onboarding this
    # omits subscription_id entirely (same as illumio-init.ps1) instead of sending null.
    data.update({k: v for k, v in kwargs.items() if v not in (None, '', [])})

    response = requests.post(api_url, headers=headers, json=data, timeout=60)
    try:
        body = response.json()
    except ValueError:
        body = response.text
    return response.status_code, body


def main():
    parser = argparse.ArgumentParser(description="Onboard an Azure subscription or tenant to Illumio CloudSecure")
    parser.add_argument('--tenant-id', required=True, help="CloudSecure Tenant ID")
    parser.add_argument('--service-account-key-id', required=True, help="CloudSecure Service Account Key ID")
    parser.add_argument('--service-account-token', required=True, help="CloudSecure Service Account Token")
    parser.add_argument('--type', required=True, choices=['AzureRole', 'AzureFlow'], help="Cloud Credential Type")
    parser.add_argument('--client-id', help="Azure Illumio Registered App Client ID")
    secret = parser.add_mutually_exclusive_group()
    secret.add_argument('--client-secret', help="Azure app client secret, already base64 encoded")
    secret.add_argument('--client-secret-raw', help="Azure app client secret as shown in Azure (encoded for you)")
    parser.add_argument('--subscription-id', help="Azure Subscription ID (omit for tenant-level onboarding)")
    parser.add_argument('--azure-tenant-id', help="Azure (Entra) Tenant ID")
    parser.add_argument('--destinations', nargs='+',
                        help="Storage account resource IDs for flow logs (required for AzureFlow)")
    parser.add_argument('--api-url', default=API_URL, help="Override the CloudSecure API URL")

    args = parser.parse_args()

    if args.type == "AzureFlow":
        if not args.destinations:
            parser.error("For AzureFlow type, --destinations is required.")
        payload = dict(subscription_id=args.subscription_id, azure_tenant_id=args.azure_tenant_id,
                       destinations=args.destinations)
    else:
        client_secret = args.client_secret or (b64(args.client_secret_raw) if args.client_secret_raw else None)
        if not (args.client_id and client_secret and args.azure_tenant_id):
            parser.error("For AzureRole type, --client-id, --client-secret(-raw) and --azure-tenant-id are required.")
        payload = dict(client_id=args.client_id, client_secret=client_secret,
                       azure_tenant_id=args.azure_tenant_id, subscription_id=args.subscription_id)

    scope = f"subscription {args.subscription_id}" if args.subscription_id else f"tenant {args.azure_tenant_id}"
    print(f"Onboarding Azure {scope} ({args.type})")

    status, body = create_cloud_credentials(args.tenant_id, args.service_account_key_id, args.service_account_token,
                                            args.type, api_url=args.api_url, **payload)
    print(f"HTTP {status}")
    print(json.dumps(body, indent=2) if isinstance(body, (dict, list)) else body)
    sys.exit(0 if 200 <= status < 300 else 1)


if __name__ == "__main__":
    main()
