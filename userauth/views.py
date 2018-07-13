from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm
from userprofile.models import Profile

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
        else:
            print("Username and password doesn't match.")
    if not request.user.is_authenticated:
        return render(request, 'userauth/login.html', context)
    else:
        return redirect(reverse('blog:list'))


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        'register_form': register_form
    }
    if register_form.is_valid():
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        password = request.POST.get('password')
        User.objects.create_user(username=username,
                            first_name=first_name,
                            last_name=last_name,
                            password=password)
        created_profile = Profile.objects.last()
        created_profile.location = address
        created_profile.save()
    if request.method == 'POST':
        return redirect('userauth:login')
    else:
        print('Bhai vayena')
    if not request.user.is_authenticated:
        return render(request, 'userauth/register.html', context)
    else:
        return redirect('blog:list')

def logout_view(request):
    logout(request)
    return redirect(reverse('userauth:login'))
