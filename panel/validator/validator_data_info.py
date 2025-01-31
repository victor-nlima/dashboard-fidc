from cerberus import Validator

class ValidatorDataInfo:
    def __init__(self):

        self.data_info= {
            'data_statistics':{'type':'list','required':True},
            "current_box":{'type':'list','required':True},
            "cumulative_expected_flow":{'type':'list','required':True},
            'data_frame': {'type': 'list','required':True },
            'rank_common_debtor': {'type': 'list', 'required':True},
            'rank_special_debtor': {'type': 'list','required':True },
            'common_debtor': {'type': 'list','required':True },
            'common_debtor_transform': {'type': 'list', 'required':True},
            'special_debtor': {'type': 'list', 'required':True},
            'special_debtor_transform': {'type': 'list','required':True },
            'data_statistics': {'type': 'list','required':True },
            'current_box': {'type': 'list','required':True },
            'cumulative_expected_flow': {'type': 'list', 'required':True},
            'buyback': {'type': 'list', 'required':True}
        }

    def validate(self,data):
            
        v = Validator(self.data_info)
        
        if not v.validate(data):
            return {'error': 'Dados inválidos', 'details': v.errors}

        return {'message': 'Dados válidos!', 'data': v.document}
      