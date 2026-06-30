import socket
import psycopg2
import urllib.parse
from pathlib import Path

password = "DN3rPZ2YUq+YiR&"
encoded_password = urllib.parse.quote_plus(password)
project_ref = "eznsvreplkrydhmerrzi"

all_regions = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
    'ap-south-1', 'ap-south-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-southeast-3',
    'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3',
    'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1', 'eu-central-2', 'eu-north-1',
    'eu-south-1', 'eu-south-2',
    'ca-central-1', 'sa-east-1', 'me-central-1', 'me-south-1', 'af-south-1', 'il-central-1'
]

print("Scanning regions with encoded password...")
for region in all_regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    try:
        ip = socket.gethostbyname(host)
        conn_str = f"postgresql://postgres.{project_ref}:{encoded_password}@{host}:6543/postgres"
        try:
            conn = psycopg2.connect(conn_str, connect_timeout=3)
            print(f"\nSUCCESS! Connected to {region} on 6543!")
            conn.close()
            break
        except Exception as e:
            err = str(e).strip().replace("\n", " ")
            print(f"{region}: {err[:150]}")
    except Exception:
        # Region does not resolve
        pass
