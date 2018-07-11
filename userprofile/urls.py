from django.urls import path
from .views import profile_page

app_name = 'profile'
urlpatterns = [
    path('<username>/', profile_page, name='profile'),

]
