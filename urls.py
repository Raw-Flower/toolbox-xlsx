from django.urls import path
from .views import *

app_name = 'xlsx'
urlpatterns = [
    path(route='index/',view=index_view,name='index'),
]
