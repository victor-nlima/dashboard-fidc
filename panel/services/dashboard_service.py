from panel.dto.dashboard_dto import DashboardDTO
from panel.dto.return_default_dto import ReturnDefault
from typing import Optional
from panel.repositories.dashboard_repository.abstract_dashboard_repository import AbstractDashboardRepository
from panel.validator.validator_data_info import ValidatorDataInfo

class DashboardService:
    def __init__(self, dashboardRepository: AbstractDashboardRepository):
        self.dashboardRepository = dashboardRepository

    def get_dashboard_date(self) -> Optional[DashboardDTO]:
        
        dash = self.dashboardRepository.get_date()

        if not dash:
            print('Dados do dashboard não enconotrados.')
            return None

        return dash
    
    def create_dashboard(self,data):
        
        print('=================================================\n')
        print('entrando na funcao de criacao....................\n')
        print('=================================================\n')

        info={
            "data_frame" : data.get('data_frame'),
            "rank_common_debtor" : data.get('rank_common_debtor'),
            "rank_special_debtor" : data.get('rank_special_debtor'),
            "common_debtor" : data.get('common_debtor'),
            "common_debtor_transform" : data.get('common_debtor_transform'),
            "special_debtor" : data.get('special_debtor'),
            "special_debtor_transform" : data.get('special_debtor_transform'),
            "data_statistics" : data.get('data_statistics'),
            "current_box" : data.get('current_box'),
            "cumulative_expected_flow" : data.get('cumulative_expected_flow'),
            "data_statistics": data.get("data_statistics"),
            "current_box": data.get("current_box"),
            "cumulative_expected_flow": data.get("cumulative_expected_flow"),
        }

        print('=====================================\n')
        print('antes de validar ')
        print('=====================================\n')
        
        validator = ValidatorDataInfo()
        verify = validator.validate(info)
                 

        if verify.get('error'):
            return_default = ReturnDefault(success=False,message=verify)
            return return_default.to_dict()
        
        if self.dashboardRepository.create_data(info):
            return_default = ReturnDefault(success=True,message='Data registered successfully')
            return return_default.to_dict()
        else:
            return_default = ReturnDefault(success=False,message='Error registering with the bank')
            return return_default.to_dict()
