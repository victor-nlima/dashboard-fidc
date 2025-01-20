from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
# from .factories.dashboard_factory import DashboardFactory
import logging



@login_required(login_url='login')
@never_cache
def dashboard_frame(request):
    message = None
    # uso da factory na views

    # factory = DashboardFactory()
    # dashboard_data = factory.execute_get_dashboard(dashboard_id)
    
    #exemplo de definicao de dados para usuarios diferentes 

    # if request.user.groups.filter(name='Admin').exists():
    #     #monta os dados para o admin 
    #     pass
    
    # if request.user.groups.filter(name='BV').exists():
    #     #monta os dados para o bv
    #     pass 
    
    data_frame = [
        {
            'title': "Prazo Médio",
            'value': "27.54 dias",
            'info': "Enquadrado"
        },
        {
            'title': "Subordinação",
            'value':'21.25%',
            'info':"Enquadrado"
        },
        {
            'title': "Devedor",
            'value':'Comum',
            'info':"Alerta"
        },
        {
            'title': "Devedor",
            'value':'Especial',
            'info':"Enquadrado"
        },
        {
            'title': "Recompra",
            'value':"2.54%",
            'info':"Enquadrado"
        },
    ]

    rank_common_debtor = [
        {
            'title': "TOP 1",
            'value':"3.57%",
            'info':"Alerta"
        },
        {
            'title': "TOP 5",
            'value':"10.41%",
            'info':"Enquadrado"
        },{
            'title': "TOP 10",
            'value':"16.93%",
            'info':"Enquadrado"
        },
    ]

    rank_special_debtor = [
        {
            'title': "TOP 1",
            'value':"3.57%",
            'info':"Enquadrado"
        },
        {
            'title': "TOP 5",
            'value':"10.41%",
            'info':"Enquadrado"
        },
    ]

    common_debtor = [0, 3.57, 5.62, 7.3, 8.88, 0, 10.41, 11.86, 13.25, 14.54, 15.76, 0]

    special_debtor =  [{
        "value": 3.57,
        "itemStyle": {
          "color": '#c39b56'
        }
      }, 2.05, 1.68, 1.58, 1.53, {
        "value": 10.41,
        "itemStyle": {
          "color": '#c39b56'
        }
      }, 1.45, 1.39, 1.29, 1.22, 1.17, {
        "value": 16.93,
        "itemStyle": {
          "color": '#c39b56'
        }
      }]

    return render(request,'dashboard_frame.html',{
        'message':message,
        'data_frame':data_frame,
        'rank_common_debtor':rank_common_debtor,
        'rank_special_debtor':rank_special_debtor,
        'common_debtor':common_debtor,
        'special_debtor':special_debtor,
        })


@login_required(login_url='login')
@never_cache
def dashboard_statistics(request):
    message = None
    # uso da factory na views

    # factory = DashboardFactory()
    # dashboard_data = factory.execute_get_dashboard(dashboard_id)
    
    #exemplo de definicao de dados para usuarios diferentes 

    # if request.user.groups.filter(name='Admin').exists():
    #     #monta os dados para o admin 
    #     pass
    
    # if request.user.groups.filter(name='BV').exists():
    #     #monta os dados para o bv
    #     pass

    data_statistics = [
        {
            'title': "Número de boletos",
            'value':1191,
            'info':" 5248 desde início"
        },
        {
            'title': "Total à Receber",
            'value':'R$25.251.214,99',
            'info':"94.25% do PL"
        },
        {
            'title': "Valor de Face Comprado",
            'value':'R$25.123.456,78',
            'info':"R$1.972.184.145,78 desde início"
        },
        {
            'title': "Número de cessões",
            'value':9,
            'info':"Última 2025-01-16"
        },
        {
            'title': "PL Senior",
            'value':"R$24.123.456,78",
            'info':" base 2025-01-16"
        },
        {
            'title': "PMT esperada",
            'value':"R$254.567,78",
            'info':"Em 2025-02-15"
        },
    ]

    current_box = [4523, 4523, 4523, 4523, 4523, 4523, 4523, 4523]

    cumulative_expected_flow = [0, 125, 254, 357, 687, 913, 1234, 1321]

    return render(request,'dashboard_statistics.html',{
        'message':message,
        "data_statistics": data_statistics,
        "current_box": current_box,
        "cumulative_expected_flow": cumulative_expected_flow,
        })