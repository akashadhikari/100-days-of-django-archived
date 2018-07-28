from django.urls import path
from .views import (search_list,
                    )
app_name = 'search'

urlpatterns = [
    path('', search_list, name='query'),

]
