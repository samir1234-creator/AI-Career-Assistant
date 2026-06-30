import socket
import psycopg2

password = "DN3rPZ2YUq+YiR&"
project_ref = "eznsvreplkrydhmerrzi"

all_regions = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
    'ap-south-1', 'ap-south-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-southeast-3',
    'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3',
    'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1', 'eu-central-2', 'eu-north-1',
    'eu-south-1', 'eu-south-2',
    'ca-central-1', 'sa-east-1', 'me-central-1', 'me-south-1', 'af-south-1', 'il-central-1'
]

print("Checking which regions exist and testing connections...")
for region in all_regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    try:
        ip = socket.gethostbyname(host)
        print(f"Region {region} exists at {ip}")
        # Try port 6543
        conn_str = f"postgresql://postgres.{project_ref}:{password}@{host}:6543/postgres"
        try:
            conn = psycopg2.connect(conn_str, connect_timeout=3)
            print(f"---> SUCCESS! Connected to {region} on 6543")
            conn.close()
            break
        except Exception as e:
            err = str(e).strip().replace("\n", " ")
            if "tenant/user" not in err.lower() and "tenant or user" not in err.lower():
                print(f"     Failed {region} 6543: {err[:120]}")
    except Exception as e:
        # Host name doesn't resolve
        pass
