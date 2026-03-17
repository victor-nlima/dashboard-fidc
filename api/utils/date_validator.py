from datetime import datetime
from rest_framework.response import Response

def date_validator(date):
    try:
        data_ref = datetime.strptime(date, '%Y-%m-%d').date()
        return data_ref
    except ValueError:
        return Response({'detail': 'Formato de data inválido. Use YYYY-MM-DD.'}, status=400)
    except Exception as e:
        return Response({'detail': 'Erro na data de referência. Use YYYY-MM-DD.'}, status=400)
        