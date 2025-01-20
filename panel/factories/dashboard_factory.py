from panel.repositories.dashboard_repository.dashboard_repository import DashboardRepository
from panel.services.dashboard_service import DashboardService

class DashboardFactory:
    def __init__(self):
        # self.session = next(get_db())
        self.dashboardRepository = DashboardRepository()

    def execute_get_dashboard(self, dashboard_id: int):
        dashboardService = DashboardService(self.dashboardRepository)
        response = dashboardService.get_dashboard(dashboard_id)
        return response

