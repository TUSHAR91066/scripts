import sys
import socket
import requests
import json
import os
from config import IPINFO_TOKEN


IPINFO_TOKEN = os.getenv('d86a0c3fcea0bd')
if not IPINFO_TOKEN:
    print("Warning: IPINFO_TOKEN environment variable not set")

def get_ip():
    """Get the local machine's IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error getting local IP: {str(e)}"

def get_public_ip():
    """Get the public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        return f"Error getting public IP: {str(e)}"

def get_ip_info(ip_address=None):
    """Get location information for an IP address using ipinfo.io"""
    try:
        if not IPINFO_TOKEN:
            raise ValueError("API token not configured. Please set your token in config.py")
            
        if ip_address is None:
            ip_address = get_public_ip()
            
        headers = {
            'Authorization': f'Bearer {IPINFO_TOKEN}',
            'Accept': 'application/json',
        }
            
        url = f'https://ipinfo.io/{ip_address}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 401:
            return "Error: Invalid API token. Please check your configuration."
        elif response.status_code != 200:
            return f"Error: API request failed with status code {response.status_code}"
            
        data = response.json()
        
        return {
            'IP': data.get('ip', 'N/A'),
            'City': data.get('city', 'N/A'),
            'Region': data.get('region', 'N/A'),
            'Country': data.get('country', 'N/A'),
            'Location': data.get('loc', 'N/A'),
            'Organization': data.get('org', 'N/A'),
            'Postal': data.get('postal', 'N/A'),
            'Timezone': data.get('timezone', 'N/A')
        }
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"Error getting IP info: {str(e)}"

def main():
    """Main function to run the IP information tool"""
    print("\n=== IP Information Tool ===\n")
    
    
    local_ip = get_ip()
    print(f"Local IP Address: {local_ip}")
    
    
    public_ip = get_public_ip()
    print(f"Public IP Address: {public_ip}")
    
    
    print("\nGathering location information...")
    ip_info = get_ip_info()
    
    if isinstance(ip_info, dict):
        print("\nLocation Information:")
        print("-" * 20)
        for key, value in ip_info.items():
            print(f"{key}: {value}")
    else:
        print(ip_info)

if __name__ == "__main__":
    main() 