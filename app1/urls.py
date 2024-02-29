from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='employee_list'),
    path('search_result',views.search_result,name='search_result')
]
