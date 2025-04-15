from decouple import config
import psycopg2

NAME = config('DB_NAME')
USER = config('DB_USER')
PASSWORD = config('DB_PASSWORD')
HOST = config('DB_HOST')
PORT = config('DB_PORT', default='5432')

connect = psycopg2.connect(
    host=HOST,
    database=NAME,
    user=USER,
    password=PASSWORD,
    port=PORT,
)

connect.autocommit = True
cursor = connect.cursor()

try:
    print("🔄 Alterando campos para timestamp WITHOUT time zone...")
    cursor.execute("""
        ALTER TABLE common_datadashboard
        ALTER COLUMN creation_date TYPE timestamp WITHOUT time zone USING creation_date::timestamp,
        ALTER COLUMN ref_date TYPE timestamp WITHOUT time zone USING ref_date::timestamp;
    """)
    print("Campos alterados com sucesso!")
except Exception as e:
    print("Erro ao executar ALTER TABLE:", e)
finally:
    cursor.close()
    connect.close()
