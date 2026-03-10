from django.contrib import admin
from common.models import DataDashboard, Fund, FundAccess, CreditStock, TransactionHistory, CashFlow

admin.site.register(DataDashboard)
admin.site.register(Fund)
admin.site.register(FundAccess)
admin.site.register(CreditStock)
admin.site.register(TransactionHistory)
admin.site.register(CashFlow)

