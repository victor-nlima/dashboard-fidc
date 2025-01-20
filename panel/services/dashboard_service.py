from panel.dto.dashboard_dto import DashboardDTO
from typing import Optional
from panel.repositories.dashboard_repository.abstract_dashboard_repository import AbstractDashboardRepository

class DashboardService:
    def __init__(self, dashboardRepository: AbstractDashboardRepository):
        self.dashboardRepository = dashboardRepository

    def get_dashboard(self, dashboard_id: int) -> Optional[DashboardDTO]:
        if not dashboard_id:
            return None

        dash = self.dashboardRepository.get_by_id(dashboard_id)

        if not dash:
            print('Dados do dashboard não enconotrados.')
            return None

        return dash

