from panel.dto.dashboard_dto import DashboardDTO
from panel.dto.return_default_dto import ReturnDefault
from typing import Optional
from panel.repositories.dashboard_repository.abstract_dashboard_repository import AbstractDashboardRepository
from panel.validator.validator_data_info_frame import ValidatorDataInfoFrame
from panel.validator.validator_data_info_statistics import ValidatorDataInfoStatistics

class DashboardService:
    def __init__(self, dashboardRepository: AbstractDashboardRepository):
        self.dashboardRepository = dashboardRepository

    def get_dashboard_date(self,type) -> Optional[DashboardDTO]:
        
        dash = self.dashboardRepository.get_date(type)

        if not dash:
            print('Dados do dashboard não enconotrados.')
            return None

        return dash
    
    def create_dashboard(self,data):
        type =  data.get('type')
        if type == 'statistics':
            info={
                "user_id":data.get('user_id'),
                "type": data.get('type'),
                "data_statistics": data.get("data_statistics"),
                "current_box": data.get("current_box"),
                "cumulative_expected_flow": data.get("cumulative_expected_flow"),
            }
        
        else:
            info={
                "user_id":data.get('user_id'),
                "type": data.get('type'),
                "data_frame" : data.get('data_frame'),
                "rank_common_debtor" : data.get('rank_common_debtor'),
                "rank_special_debtor" : data.get('rank_special_debtor'),
                "common_debtor" : data.get('common_debtor'),
                "common_debtor_transform" : data.get('common_debtor_transform'),
                "special_debtor" : data.get('special_debtor'),
                "special_debtor_transform" : data.get('special_debtor_transform'),
                "data_statistics" : data.get('data_statistics'),
                "current_box" : data.get('current_box'),
                "cumulative_expected_flow" : data.get('cumulative_expected_flow')
            }

        print(info)
        
        if info['type'] == 'statistics':
            validator = ValidatorDataInfoStatistics()
            verify = validator.validate_statistics(info)
        else:
            print('dentro do frame')
            validator = ValidatorDataInfoFrame()
            verify = validator.validate_frame(info)            

        if verify.get('error'):
            return_default = ReturnDefault(success=False,message=verify)
            return return_default.to_dict()
        
        if self.dashboardRepository.create_data(info):
            return_default = ReturnDefault(success=True,message='Data registered successfully')
            return return_default.to_dict()
        else:
            return_default = ReturnDefault(success=False,message='Error registering with the bank')
            return return_default.to_dict()
