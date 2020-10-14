from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login



def profile(request):
    if request.user.is_authenticated:
        if request.user.is_candidate:
            return redirect('candidate-profile')
        else:
            if request.user.is_employer:
                return redirect('employer-profile')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    context = {

    }
    return render(request, 'registration/signup.html', context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'accounts/login.html', {'error': 'Your account has been disabled'})
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    context = {

    }
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('sign-in')
