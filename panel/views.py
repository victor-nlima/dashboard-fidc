from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .factories.dashboard_factory import DashboardFactory
import logging
from panel.middleware.authentication import validate_token
from decouple import config
import json
#pip install cryptography
from cryptography.fernet import Fernet



@login_required(login_url='login')
@never_cache
def dashboard_frame(request):
    message = None

    factory = DashboardFactory()
    
    try:
        dashboard_data = factory.execute_get_dashboard_data(type='framing')
        info = dashboard_data.info
    except Exception as e:
        message = {'success':False,"message":'Nenhum dado encontrado'}
        info = None
    
    data_frame = [frame for frame in info['data_frame']] if info else None
    rank_common_debtor = [rank for rank in info['rank_common_debtor']] if info else None
    rank_special_debtor = [rank for rank in info['rank_special_debtor']] if info else None
    common_debtor = [cn for cn in info['common_debtor']] if info else None
    common_debtor_transform = [cdt for cdt in info['common_debtor_transform']] if info else None
    special_debtor = [sd for sd in info['special_debtor']] if info else None
    special_debtor_transform = [sdt for sdt in info['special_debtor_transform']] if info else None
    data_statistics = [ds for ds in info['data_statistics']] if info else None 
    current_box = [cb for cb in info['current_box']] if info else None
    cumulative_expected_flow = [cef for cef in info['cumulative_expected_flow']] if info else None
    user_id = info['user_id'] if info else None
    

    return render(request,'dashboard_frame.html',{
        'message':message,
        'data_frame':data_frame,
        'rank_common_debtor':rank_common_debtor,
        'rank_special_debtor':rank_special_debtor,
        'common_debtor':common_debtor,
        'common_debtor_transform':common_debtor_transform,
        'special_debtor':special_debtor,
        'special_debtor_transform':special_debtor_transform,
        'data_statistics':data_statistics,
        'current_box':current_box,
        'cumulative_expected_flow':cumulative_expected_flow,
        'user_id':user_id
    })


@login_required(login_url='login')
@never_cache
def dashboard_statistics(request):
    message = None

    factory = DashboardFactory()

    try:
        dashboard_data = factory.execute_get_dashboard_data(type='statistics')
        info = dashboard_data.info
    except Exception as e:
        message = {'success':False,"message":'Nenhum dado encontrado'}
        info = None

    data_statistics = [ds for ds in info['data_statistics']] if info else None
    current_box = [cb for cb in info['current_box']] if info else None
    cumulative_expected_flow = [cef for cef in info['cumulative_expected_flow']] if info else None

    return render(request,'dashboard_statistics.html',{
        'message':message,
        "data_statistics": data_statistics,
        "current_box": current_box,
        "cumulative_expected_flow": cumulative_expected_flow,
    })

@csrf_exempt
@validate_token
def created_data(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            data_encrypted = str(payload['data'])
            key = config('KEY')
            
            fernet = Fernet(key)
            
            data_decrypted = fernet.decrypt(data_encrypted)
            data_json = json.loads(data_decrypted.decode('utf-8'))
            factory = DashboardFactory()
            response_data = factory.execute_create_data(data=data_json)
        except Exception as e:

            return JsonResponse({"message": f"Houve algum erro na requisicao: {str(e)}"},status=400)
        
        
        return JsonResponse(response_data)
