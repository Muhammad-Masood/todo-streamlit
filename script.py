import psycopg2

# Optional: tell psycopg2 to cancel the query on Ctrl-C
import psycopg2.extras; psycopg2.extensions.set_wait_callback(psycopg2.extras.wait_select)

# You can set the password to None if it is specified in a ~/.pgpass file
USERNAME = "Muhammad Masood"
PASSWORD = "M@s00d.123"
HOST = "@ep-cool-darkness-123456.us-east-2.aws.neon.tech"
PORT = "5432"
PROJECT = "TodoApp"

conn_str = f"dbname={PROJECT} user={USERNAME} password={PASSWORD} host={HOST} port={PORT} sslmode=require"

conn = psycopg2.connect(conn_str)

with conn.cursor() as cur:
 cur.execute("SELECT 'hello neon';")
 print(cur.fetchall())