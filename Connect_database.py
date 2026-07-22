import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = connection.cursor()

cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()