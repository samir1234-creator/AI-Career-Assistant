import psycopg2
import urllib.parse

password = "DN3rPZ2YUq+YiR&"
encoded_password = urllib.parse.quote_plus(password)
project_ref = "eznsvreplkrydhmerrzi"
host = "aws-1-ap-southeast-2.pooler.supabase.com"

# Test port 6543 (transaction pooling)
print("Testing port 6543...")
try:
    conn_str_6543 = f"postgresql://postgres.{project_ref}:{encoded_password}@{host}:6543/postgres"
    conn = psycopg2.connect(conn_str_6543, connect_timeout=5)
    print("SUCCESS on 6543!")
    conn.close()
except Exception as e:
    print(f"Failed on 6543: {e}")

# Test port 5432 (session pooling)
print("\nTesting port 5432...")
try:
    conn_str_5432 = f"postgresql://postgres.{project_ref}:{encoded_password}@{host}:5432/postgres"
    conn = psycopg2.connect(conn_str_5432, connect_timeout=5)
    print("SUCCESS on 5432!")
    conn.close()
except Exception as e:
    print(f"Failed on 5432: {e}")
