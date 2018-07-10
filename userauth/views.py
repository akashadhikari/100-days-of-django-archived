from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

# Create your views here.


def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
        'login_form': login_form,
        'page_title': 'Login - TheShelve'
    }
    if login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            if request.user.is_authenticated:
                return redirect(reverse('blog:list'))
            else:
                print('Bhai vayena')
                messages.add_message(request, messages.INFO, 'Hello world.')
        else:
            print("Username and password doesn't match.")
            messages.add_message(request, messages.INFO, 'Hello world.')
    if not request.user.is_authenticated:
        return render(request, 'userauth/login.html', context)
    else:
        return redirect(reverse('blog:list'))

def logout_view(request):
    logout(request)
    return redirect(reverse('userauth:login'))
