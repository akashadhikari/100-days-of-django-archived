from django.urls import path
from .views import login_page, register_page, logout_view

app_name = 'userauth'
urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_view, name='logout')

]
