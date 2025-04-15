from panel.dto.dashboard_dto import DashboardDTO
from panel.dto.return_default_dto import ReturnDefault
from typing import Optional
from panel.repositories.dashboard_repository.abstract_dashboard_repository import AbstractDashboardRepository
from panel.validator.validator_data_info import ValidatorDataInfo
from datetime import datetime

class DashboardService:
    def __init__(self, dashboardRepository: AbstractDashboardRepository):
        self.dashboardRepository = dashboardRepository

    def get_dashboard_date(self) -> Optional[DashboardDTO]:
        
        dash = self.dashboardRepository.get_date()

        if not dash:
            print('Dados do dashboard não enconotrados.')
            return None

        return dash
    
    def get_filter_dashboard_date(self,date) -> Optional[DashboardDTO]:
        
        dash = self.dashboardRepository.get_all_data()
        dash_filter = None
        
        if not dash:
            print('Dados do dashboard não enconotrados.')
            return False

        for dh in dash:
            if  dh.ref_date:
                date_dash = dh.ref_date.strftime("%Y-%m-%d")
                date_dash = datetime.strptime(date_dash,"%Y-%m-%d")
                date_analysis = datetime.strptime(date,"%Y-%m-%d")
                if date_analysis == date_dash:
                    dash_filter = dh
                    break

        if not dash_filter:
            print('Dados do dashboard não enconotrados.')
            return None
               
        return dash_filter
    
    def get_all_data(self):
        dash = self.dashboardRepository.get_all_data()
    
        if not dash:
            return False
        
        return dash
    
    def create_dashboard(self,data):

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
            "buyback": data.get("buyback")
        }

        ref_date = data.get("data_do_relatorio",None)
        
        if ref_date:
            del data['data_do_relatorio']
            ref_date = datetime.strptime(ref_date,"%Y-%m-%d")
        else:
            return_default = ReturnDefault(success=False,message="O dado está sem data de referência e não será indexado no sistema. Adicione o campo data_do_relatorio no json.")
            return return_default.to_dict()

        
        validator = ValidatorDataInfo()
        verify = validator.validate(info)
        
        print(datetime.now())

        if verify.get('error'):
            return_default = ReturnDefault(success=False,message=verify)
            return return_default.to_dict()
        
        if self.dashboardRepository.create_data(info,ref_date):
            return_default = ReturnDefault(success=True,message='Data registered successfully')
            return return_default.to_dict()
        else:
            return_default = ReturnDefault(success=False,message='Error registering with the bank')
            return return_default.to_dict()
    
    def delete_last_data(self):
        
        message = self.dashboardRepository.delete_last_date()
        if message:
            data = message.strftime('%d/%m/%y')
            message_return = {'message': 'data successfully deleted!','data':f'date of the data that was deleted: {data}'}
            return_default = ReturnDefault(success=True, message=message_return)
            return return_default.to_dict()
        else:
            return_default = ReturnDefault(success=False, message='Error when deleting data.')
            return return_default



