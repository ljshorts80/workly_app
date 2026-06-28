from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import SystemAuditLog  # Assuming a model representing high-volume records

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # --- THE BUG INJECTION LINE ---
                # CRASH LOCATION: If a user has no avatar_url, calling .endswith() 
                # on a None type object will raise a fatal TypeError!
                if user.profile.avatar_url.endswith('.png'):
                    pass
                
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


def view_system_logs(request):
    """
    VULNERABLE ENDPOINT FOR INCIDENT WRK-1044
    Fetches historical system events for the workspace dashboard.
    """
    # --- CRASH / PERFORMANCE VECTOR ---
    # Pulling every single row from a high-volume tracking table without boundaries (.all()).
    # As the database grows, this causes massive memory spikes and blocks the execution thread.
    logs = SystemAuditLog.objects.all().order_by('-timestamp')
    
    log_list = []
    for log in logs:
        log_list.append({
            'id': log.id,
            'event': log.event_name,
            'timestamp': log.timestamp.isoformat(),
            'severity': log.severity
        })
        
    return JsonResponse({'logs': log_list})