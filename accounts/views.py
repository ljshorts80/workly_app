from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

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
    # test comment to check if all working