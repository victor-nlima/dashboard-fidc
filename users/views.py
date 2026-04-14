from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from common.models import LoginAttempt
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

@csrf_protect
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

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("="*50)
        print("DEntrod dA VIEW")
        print("="*50)
        ip = self.get_client_ip(request)
        print(ip)
        print("="*50)
        attempt, _ = LoginAttempt.objects.get_or_create(ip_address=ip)
        try:
            response = super().post(request, *args, **kwargs)
            print("Validar requisicao")
            attempt.attempts = 0
            attempt.blocked_until = None
            attempt.save()
            return response
        
        except Exception:
            print("Erro na autenticação")
            attempt.attempts += 1
            if attempt.attempts >= 10:
                attempt.blocked_until = timezone.now() + timedelta(hours=1)
            attempt.save()
            raise AuthenticationFailed("Usuário ou senha inválidos.")

    def get_client_ip(self, request):
        remote_addr = request.META.get('REMOTE_ADDR', '')
        trusted_proxies = getattr(settings, 'TRUSTED_PROXIES', [])
        if remote_addr in trusted_proxies:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0].strip()
        return remote_addr