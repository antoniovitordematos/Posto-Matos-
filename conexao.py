import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="posto_matos",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )
