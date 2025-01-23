from typing import List, Optional
from panel.dto.dashboard_dto import DashboardDTO
from .abstract_dashboard_repository import AbstractDashboardRepository
from common.models import DataDashboard # importacao do models
from django.contrib.auth.models import User

class DashboardRepository(AbstractDashboardRepository):
    def _to_dto(self, dashboard: DataDashboard) -> DashboardDTO:
        return DashboardDTO(
            id = dashboard.id,
            creation_date = dashboard.creation_date,
            type = dashboard.type,
            user = dashboard.user_id,
            info = dashboard.info
        )

    # def get_by_id(self, dash_id: int) -> Optional[DashboardDTO]:
    #     dash = DataDashboard.objects.filter(id=dash_id).first()
    #     return self._to_dto(dash) if dash else None

    def get_date(self,type):
        dash = DataDashboard.objects.filter(type=type).order_by('-creation_date').first()
        return self._to_dto(dash) if dash else None

    def create_data(self,data) -> bool:
        try:

            if data['type'] != 'framing' and data['type'] != 'statistics' :
                return False
            
            dataDashboard = DataDashboard(
                user_id = data['user_id'],
                type = data['type'],
                info = data
            )
            
            dataDashboard.save()
            return True
        
        except Exception as e:
            print(f'Erro ao salvar: {e}')
            return False
