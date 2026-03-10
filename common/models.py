from django.db import models
from django.contrib.auth.models import Group, User
import uuid
from datetime import datetime

"""
    Esta tabela será usada para armazenar os dados por id do usuario. 
    Os dados serão separados por usuários para facilitar a diferenca de dados no momento de exibir.
    A data de criacão será usada para pegar os dados mais recentes.

"""


class DataDashboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(default=datetime.now)
    ref_date = models.DateTimeField(blank=True, null=True)
    info = models.JSONField()

    def __str__(self):
        return f"{self.creation_date}"

# Modelo de Fundo
class Fund(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Liga Fundo à Instituição (Group)
class FundAccess(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fund.name} - {self.group.name}"

# Tabelas de Dados
class CreditStock(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    data = models.JSONField()
    ref_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fund.name} - {self.ref_date}"

class TransactionHistory(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    data = models.JSONField()
    ref_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fund.name} - {self.ref_date}"

class CashFlow(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    data = models.JSONField()
    ref_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fund.name} - {self.ref_date}"
