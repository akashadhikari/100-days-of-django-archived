from django.urls import path
from .views import profile_page, follow_user, unfollow_user, profile_edit

app_name = 'profile'
urlpatterns = [
    path('<username>/', profile_page, name='profile'),
    path('<username>/follow/', follow_user, name='follow'),
    path('<username>/unfollow/', unfollow_user, name='unfollow'),
    path('<username>/edit/', profile_edit, name='edit'),

]
