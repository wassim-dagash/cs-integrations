import requests
import argparse
import json
import base64

def create_cloud_credentials(tenant_id, service_account_key, service_account_token, account_id, type, **kwargs):
    url = 'https://cloud.illum.io/api/v1/integrations/cloud_credentials'
    
    auth_str = f"{service_account_key}:{service_account_token}"
    auth_bytes = auth_str.encode('utf-8')  # Encode string into bytes
    auth_encoded = base64.b64encode(auth_bytes).decode('utf-8')  # Encode bytes to base64 and decode to string

    headers = {
        'X-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + auth_encoded 
    }
    data = {
        "account_id": account_id,
        "type": type
    }

    data.update(kwargs)
    print(kwargs)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Script to interact with Illum.io API")
    parser.add_argument('--tenant-id', required=True, help="CloudSecure Tenant ID")
    parser.add_argument('--service-account-key', required=True, help="CloudSecure Service Account Key")
    parser.add_argument('--service-account-token', required=True, help="CloudSecure Service Account Token")
    parser.add_argument('--type', required=True, help="Type of cloud credential (AWSRole or AWSFlow)")
    parser.add_argument('--account-id', required=True, help="Customer Account ID")
    parser.add_argument('--role-arn', help="ARN of IAM Role (required for AWSRole type)")
    parser.add_argument('--external-id', help="CS External ID for trust relationship, usually equals CloudSecure Service Account Key")
    parser.add_argument('--org-id', help="Organization ID , Required only when onboarding an org")
    parser.add_argument('--management-account-id', help="Master Account ID, required only when onboarding an org")
    parser.add_argument('--destinations', nargs='+', help="List of S3 ARNs (required for AWSFlow type)")
    
    args = parser.parse_args()

    if args.type == "AWSRole":
        if not args.role_arn or not args.external_id or not args.org_id or not args.management_account_id:
            parser.error("For AWSRole type, role-arn and external-id are required . If onboarding or, then org-id, and management-account-id are required.")
        response = create_cloud_credentials(args.tenant_id, args.service_account_key, args.service_account_token, args.account_id, args.type,
                                             role_arn=args.role_arn, external_id=args.external_id, org_id=args.org_id, management_account_id=args.management_account_id)
    elif args.type == "AWSFlow":
        if not args.destinations:
            parser.error("For AWSFlow type, destinations are required.")
        response = create_cloud_credentials(args.tenant_id, args.service_account_key, args.service_account_token, args.account_id, args.type,
                                             destinations=args.destinations)
    else:
        parser.error("Invalid type. Supported types are AWSRole and AWSFlow.")

    print("Response:", response)

if __name__ == "__main__":
    main()

