import requests
import argparse
import base64

API_URL = 'https://cloud.illum.io/api/v1/integrations/cloud_credentials'

def create_cloud_credentials(tenant_id, service_account_key_id, service_account_token, type, **kwargs):

    auth_str = f"{service_account_key_id}:{service_account_token}"
    auth_bytes = auth_str.encode('utf-8')  # Encode string into bytes
    auth_encoded = base64.b64encode(auth_bytes).decode('utf-8')  # Encode bytes to base64 and decode to string


    headers = {
        'X-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + auth_encoded
    }
    data = {'type': type}
    data.update(kwargs)
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Script to interact with Illumio CloudSecure API")
    parser.add_argument('--tenant-id', required=True, help="CloudSecure Tenant ID")
    parser.add_argument('--service-account-key-id', required=True, help="CloudSecure Service Account Key ID")
    parser.add_argument('--service-account-token', required=True, help="CloudSecure Service Account Token")
    parser.add_argument('--type', required=True, help="Cloud Credential Type (e.g., AzureRole or AzureFlow)")
    parser.add_argument('--client-id', help="Azure Illumio Registered App Client ID")
    parser.add_argument('--client-secret', help="Azure Illumio Registered App Client Secret (base64 encoded)")
    parser.add_argument('--subscription-id', help="Subscription ID")
    parser.add_argument('--azure-tenant-id', help="Azure Tenant ID")
    parser.add_argument('--destinations', nargs='+', help="List of destinations (required for AzureFlow)")

    args = parser.parse_args()

    if args.type == "AzureFlow":
        if not args.destinations:
            parser.error("For AzureFlow type, destinations are required.")
        response = create_cloud_credentials(args.tenant_id, args.service_account_key_id, args.service_account_token, args.type,
                                             subscription_id=args.subscription_id, azure_tenant_id=args.azure_tenant_id,
                                             destinations=args.destinations)
    else:
        response = create_cloud_credentials(args.tenant_id, args.service_account_key_id, args.service_account_token, args.type,
                                             client_id=args.client_id, client_secret=args.client_secret, subscription_id=args.subscription_id, azure_tenant_id=args.azure_tenant_id)
    
    print("Response:", response)

if __name__ == "__main__":
    main()

