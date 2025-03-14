from typing import List, Optional
from panel.dto.dashboard_dto import DashboardDTO
from .abstract_dashboard_repository import AbstractDashboardRepository
from common.models import DataDashboard 
from django.contrib.auth.models import User

class DashboardRepository(AbstractDashboardRepository):
    def _to_dto(self, dashboard: DataDashboard) -> DashboardDTO:
        return DashboardDTO(
            id = dashboard.id,
            creation_date = dashboard.creation_date,
            info = dashboard.info
        )

    # def get_by_id(self, dash_id: int) -> Optional[DashboardDTO]:
    #     dash = DataDashboard.objects.filter(id=dash_id).first()
    #     return self._to_dto(dash) if dash else None

    def get_date(self):
        dash = DataDashboard.objects.all().order_by('-creation_date').first()
        return self._to_dto(dash) if dash else None

    def create_data(self,data) -> bool:
        try:
            
            dataDashboard = DataDashboard(
                info = data
            )

            
            
            dataDashboard.save()
            return True
        
        except Exception as e:
            print(f'Erro ao salvar: {e}')
            return False
    
    def delete_last_date(self):
        try:
            last_date = DataDashboard.objects.all().order_by('-creation_date').first()
            date_remove = last_date.creation_date
            last_date.delete()

            return date_remove

        except Exception as e:
            return False
