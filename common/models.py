from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

"""
    Esta tabela será usada para armazenar os dados por id do usuario. 
    Os dados serão separados por usuários para facilitar a diferenca de dados no momento de exibir.
    A data de criacão será usada para pegar os dados mais recentes.

"""

class DataDashboard(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    creation_date = models.DateTimeField(default=datetime.now)
    ref_date = models.DateTimeField(blank=True, null=True) 
    info =models.JSONField()

    def __str__(self):
        return f"{self.creation_date}"