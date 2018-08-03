from django.urls import path
from .views import (home,
                    blogs_following_list,
                    blog_create,
                    blog_detail,
                    blog_edit,
                    blog_delete,
                    like_trigger,
                    unlike_trigger,
                    )


app_name = 'blog'
urlpatterns = [
    path('', home, name='list'),
    path('new/', blog_create, name='create'),
    path('s/<pk>/', blog_detail, name='detail'),
    path('s/<pk>/edit/', blog_edit, name='edit'),
    path('s/<pk>/delete/', blog_delete, name='delete'),
    path('s/<pk>/like/', like_trigger, name='like'),
    path('s/<pk>/unlike/', unlike_trigger, name='unlike'),
    path('following/', blogs_following_list, name='following'),
]
