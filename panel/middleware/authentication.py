from django.http import JsonResponse
from functools import wraps
from panel.dto.return_default_dto import ReturnDefault
from decouple import config
import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError

def validate_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        token = request.headers.get('Authorization')
        token = str(token).split(' ')[1]
        if not token:
            return_default = ReturnDefault(success=False,message='The token was missing.')
            return JsonResponse(return_default.to_dict(), status=401)
        
        try:
            key = config('SECRET_KEY') 
            
            jwt.decode(token, key , algorithms=["HS256"])
        except InvalidSignatureError:

            return_default = ReturnDefault(success=False,message='invalid token')
            return JsonResponse(return_default.to_dict(), status=401)
        
        except ExpiredSignatureError:

            return_default = ReturnDefault(success=False,message='expired token')
            return  JsonResponse(return_default.to_dict(), status=401)
        
        except Exception as e:
            return_default = ReturnDefault(success=False,message=str(e))
            return JsonResponse(return_default.to_dict(), status=401)

        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view