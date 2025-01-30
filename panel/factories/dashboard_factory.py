from panel.repositories.dashboard_repository.dashboard_repository import DashboardRepository
from panel.services.dashboard_service import DashboardService

class DashboardFactory:
    def __init__(self):
        # self.session = next(get_db())
        self.dashboardRepository = DashboardRepository()

    def execute_get_dashboard_data(self):
        dashboardService = DashboardService(self.dashboardRepository)
        response = dashboardService.get_dashboard_date()
        return response

    def execute_create_data(self,data):
        dashboardService = DashboardService(self.dashboardRepository)
        response = dashboardService.create_dashboard(data)
        return response
    
    def delete_last_data(self):
        dashboardService = DashboardService(self.dashboardRepository)
        response = dashboardService.delete_last_data()
        return response
