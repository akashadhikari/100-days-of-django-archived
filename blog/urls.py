from django.urls import path
from .views import blogs_list, blog_create, blog_detail, blog_edit, blog_delete


app_name = 'blog'
urlpatterns = [
    path('', blogs_list, name='list'),
    path('new/', blog_create, name='create'),
    path('s/<pk>/', blog_detail, name='detail'),
    path('s/<pk>/edit/', blog_edit, name='edit'),
    path('093fbd18-c370-4dcd-bd69-199311edb878/<pk>/delete/', blog_delete, name='delete'),
]
