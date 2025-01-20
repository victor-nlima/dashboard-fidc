from typing import List, Optional
from panel.dto.dashboard_dto import DashboardDTO
from .abstract_dashboard_repository import AbstractDashboardRepository
from common.models import DataDashboard # importacao do models

class DashboardRepository(AbstractDashboardRepository):
    def _to_dto(self, dashboard: DataDashboard) -> DashboardDTO:
        return DashboardDTO(
            id = id,
            creation_date = dashboard.creation_date,
            user = dashboard.user_id,
            info = dashboard.info
        )

    def get_all(self) -> List[DashboardDTO]:
        all_dashboard_registers = DataDashboard.objects.all()
        return [self._to_dto(dash) for dash in all_dashboard_registers]

    def get_by_id(self, document_id: int) -> Optional[DashboardDTO]:
        dash = DataDashboard.objects.filter(id=document_id).first()
        return self._to_dto(dash) if dash else None

