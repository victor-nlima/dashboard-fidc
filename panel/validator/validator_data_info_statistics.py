from cerberus import Validator

class ValidatorDataInfoStatistics:
    def __init__(self):

        self.data_info_statistics = {
            'user_id':{'type':'integer','required':True},
            'type':{'type':'string','required':True},
            'data_statistics':{'type':'list','required':True},
            "current_box":{'type':'list','required':True},
            "cumulative_expected_flow":{'type':'list','required':True} 
        }

    def validate_statistics(self,data):
            
        v = Validator(self.data_info_statistics)
        
        if not v.validate(data):
            return {'error': 'Dados inválidos', 'details': v.errors}

        return {'message': 'Dados válidos!', 'data': v.document}
      