from cerberus import Validator

class ValidatorDataInfoFrame:
    def __init__(self):
        self.data_info_frame = {
            'user_id':{'type':'integer', 'required':True},
            'type':{'type':'string','required':True},
            'data_frame': {'type': 'list','required':True },
            'rank_common_debtor': {'type': 'list', 'required':True},
            'rank_special_debtor': {'type': 'list','required':True },
            'common_debtor': {'type': 'list','required':True },
            'common_debtor_transform': {'type': 'list', 'required':True},
            'special_debtor': {'type': 'list', 'required':True},
            'special_debtor_transform': {'type': 'list','required':True },
            'data_statistics': {'type': 'list','required':True },
            'current_box': {'type': 'list','required':True },
            'cumulative_expected_flow': {'type': 'list', 'required':True}
        }
    
    def validate_frame(self,data):
        
        v = Validator(self.data_info_frame)
        
        if not v.validate(data):
            return {'error': 'Dados inválidos', 'details': v.errors}

        return {'message': 'Dados válidos!', 'data': v.document}

      