
from django.contrib import admin
from common.models import DataDashboard, PositionHistory

admin.site.register(DataDashboard)

@admin.register(PositionHistory)
class PositionHistoryAdmin(admin.ModelAdmin):
	list_display = ('user', 'ref_date', 'creation_date')

