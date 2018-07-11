from django.shortcuts import render, get_object_or_404
from .models import UserProfile
# Create your views here.

def profile_page(request, username):
    user = get_object_or_404(UserProfile, username=username)
    full_name = user.first_name + " " +user.last_name
    last_login = user.last_login
    profile_pic = user.profile_pic
    address = user.address
    context = {
        'fullname': full_name,
        'last_login': last_login,
        'profile_pic': profile_pic,
        'address': address

    }
    return render(request, "userprofile/profile_home.html", context)
