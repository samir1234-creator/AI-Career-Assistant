import urllib.request
import json
import ipaddress

db_ip = "2406:da1c:4c7:f801:9927:ed93:aab3:ceb7"
target_addr = ipaddress.ip_address(db_ip)

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
print("Downloading AWS IP ranges...")
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    # Check IPv6 prefixes
    found = False
    for prefix in data.get("ipv6_prefixes", []):
        net = ipaddress.ip_network(prefix["ipv6_prefix"])
        if target_addr in net:
            print(f"MATCH FOUND!")
            print(f"Network: {prefix['ipv6_prefix']}")
            print(f"Region: {prefix['region']}")
            print(f"Service: {prefix['service']}")
            found = True
            
    if not found:
        print("No matching AWS IPv6 range found in the published JSON.")
except Exception as e:
    print(f"Error checking AWS IP ranges: {e}")
