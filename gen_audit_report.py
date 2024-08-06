import requests
import base64
import argparse
import json
import csv

def create_report(api_key, api_secret, tenant_id, file_name, file_format, from_time, to_time):
    url = 'https://cloud.illum.io/api/v1/report'
    
    # Encode the API key and secret
    credentials = f"{api_key}:{api_secret}"
    credentials_bytes = credentials.encode('utf-8')
    encoded_credentials = base64.b64encode(credentials_bytes).decode('utf-8')
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en-AU;q=0.9,en;q=0.8,ar;q=0.7',
        'content-type': 'application/json',
        'Authorization': 'Basic ' + encoded_credentials, 
        'origin': 'https://console.illum.io',
        'priority': 'u=1, i',
        'referer': 'https://console.illum.io/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-tenant-id': tenant_id
    }
    
    data = {
        "fileName": file_name,
        "fileFormat": f"FILE_FORMAT_{file_format.upper()}",
        "auditReportRequest": {
            "from_time": from_time,
            "to_time": to_time
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    return response.status_code, response.text



def create_flow_report(api_key, api_secret, tenant_id, file_name, file_format, from_time, to_time, max_results):
    url = 'https://cloud.illum.io/api/v1/flows'

    # Encode the API key and secret
    credentials = f"{api_key}:{api_secret}"
    credentials_bytes = credentials.encode('utf-8')
    encoded_credentials = base64.b64encode(credentials_bytes).decode('utf-8')

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en-AU;q=0.9,en;q=0.8,ar;q=0.7',
        'content-type': 'application/json',
        'Authorization': 'Basic ' + encoded_credentials,
        'origin': 'https://console.illum.io',
        'priority': 'u=1, i',
        'referer': 'https://console.illum.io/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-tenant-id': tenant_id
    }

    data = {
        "fileName": file_name,
        "fileFormat": f"FILE_FORMAT_{file_format.upper()}",
        "period": {
            "start_time": from_time,
            "end_time": to_time
        },
        "max_results": max_results
    }

    response = requests.post(url, headers=headers, json=data)


    if response.status_code == 200:
        resp_json = response.json()
        flows = resp_json['flows']
        
        with open('data.csv', 'w', newline='') as f:
            csv_file = csv.writer(f)

            # Assuming the response content is a list of dictionaries
            
            if flows:
                # Write header row
                header = flows[0].keys()
                csv_file.writerow(header)

                # Write data rows
                for item in flows:
                    csv_file.writerow(item.values())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response content: {response.content}")

    # Uncomment the return statement if needed
    return response.status_code, response.text


def main():
    parser = argparse.ArgumentParser(description='Generate audit report from Illumio API.')
    parser.add_argument('--api_key', required=True, help='API key for authentication')
    parser.add_argument('--api_secret', required=True, help='API secret for authentication')
    parser.add_argument('--tenant_id', required=True, help='Tenant ID')
    parser.add_argument('--file_name', required=True, help='File name for the report')
    parser.add_argument('--file_format', choices=['csv', 'json'], required=True, help='File format for the report')
    parser.add_argument('--from_time', required=True, help='Start time for the report (e.g., 2024-08-04T00:01:18Z)')
    parser.add_argument('--to_time', required=True, help='End time for the report (e.g., 2024-08-05T00:01:18Z)')
    parser.add_argument('--max_results', required=True, help='The returned maxmimum limit for entries of flows')

    args = parser.parse_args()
    
    #status_code, response_text = create_report(args.api_key, args.api_secret, args.tenant_id, args.file_name, args.file_format, args.from_time, args.to_time)
    status_code, response_text = create_flow_report(args.api_key, args.api_secret, args.tenant_id, args.file_name, args.file_format, args.from_time, args.to_time, args.max_results)
    
    #print(f"Status Code: {status_code}")
    #print(f"Response: {response_text}")

if __name__ == "__main__":
    main()
