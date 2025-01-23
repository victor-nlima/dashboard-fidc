class ReturnDefault:
    def __init__(self, success: bool = False , message:str = '' ):
        self.success = success,
        self.message = message
    
    def to_dict(self):
        return{
            'success':self.success,
            'message':self.message
        }
