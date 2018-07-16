from django.urls import path
from .views import profile_page, follow_user

app_name = 'profile'
urlpatterns = [
    path('<username>/', profile_page, name='profile'),
    path('<username>/follow/', follow_user, name='follow'),

]
