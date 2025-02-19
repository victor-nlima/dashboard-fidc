from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

@csrf_exempt
def login(request):
    
    message = None
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request,username=username,password=password)
        
        if user:
            auth_login(request,user)
            next_url = request.GET.get('next','dashboard_frame')
            return redirect(next_url)
        else:   
            message = {'success': False, 'message': f'Email ou Senha incorretos'}

        
    return render(request,'login.html',{"form":form,'message':message})

def logout_views(request):
    
    logout(request)
    request.session.flush()
    
    return redirect('login')