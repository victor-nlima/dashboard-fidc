# common/signals.py

from django.db.models.signals import post_migrate
from django.db import connection
from django.dispatch import receiver

@receiver(post_migrate)
def alterar_timestamp_sem_timezone(sender, **kwargs):
    def precisa_alterar(coluna):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT data_type, datetime_precision
                FROM information_schema.columns
                WHERE table_name = 'common_datadashboard'
                AND column_name = %s;
            """, [coluna])
            result = cursor.fetchone()
            if not result:
                return False
            tipo = result[0]
            return tipo == 'timestamp with time zone'

    print("[Signal] Verificação de tipos de timestamp executada.")

    colunas = ['creation_date', 'ref_date']
    if any(precisa_alterar(coluna) for coluna in colunas):
        with connection.cursor() as cursor:
            print("[Signal] Alterando tipo de coluna para timestamp WITHOUT time zone...")
            cursor.execute("""
                ALTER TABLE common_datadashboard
                ALTER COLUMN creation_date TYPE timestamp WITHOUT time zone,
                ALTER COLUMN ref_date TYPE timestamp WITHOUT time zone;
            """)
