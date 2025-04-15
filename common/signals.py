# common/signals.py

from django.db.models.signals import post_migrate
from django.db import connection
from django.dispatch import receiver

@receiver(post_migrate)
def testar_alter_column_timestamp(sender, **kwargs):
    with connection.cursor() as cursor:
        print("[Signal] Rodando alteração de tipo só para teste...")

        cursor.execute("""
            ALTER TABLE common_datadashboard
            ALTER COLUMN creation_date TYPE timestamp(0) WITHOUT time zone,
            ALTER COLUMN ref_date TYPE timestamp(0) WITHOUT time zone;
        """)
    