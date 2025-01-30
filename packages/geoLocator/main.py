import json
import urllib.request
from typing import Dict, Any
import os

def main(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to handle IP information requests using ipapi.co (free, no token needed)
    """
    try:
        print("Starting function execution with args:", json.dumps(args))
        
        # Get client IP from headers
        headers = args.get('__ow_headers', {})
        ip_address = None

        # Try different header fields where the client IP might be
        for header in ['x-forwarded-for', 'x-real-ip', 'remote-addr']:
            if header in headers:
                ip_address = headers[header].split(',')[0].strip()
                break

        if not ip_address:
            print("No client IP found in headers, using default")
            ip_address = '8.8.8.8'

        print(f"Processing IP address: {ip_address}")

        # Make request to ipapi.co
        url = f'https://ipapi.co/{ip_address}/json/'
        print(f"Requesting data from: {url}")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print("Successfully got IP details")

        # Format response
        response = {
            "ip": ip_address,  # Added IP to response
            "range": [0, 0],  # Simplified range
            "country": data.get('country_code', ''),
            "region": data.get('region', ''),
            "eu": "1" if data.get('in_eu', False) else "0",
            "timezone": data.get('timezone', ''),
            "city": data.get('city', ''),
            "ll": [
                float(data.get('latitude', 0)),
                float(data.get('longitude', 0))
            ],
            "metro": 0,  # Simplified metro code
            "area": 1000  # Default area code
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        } 