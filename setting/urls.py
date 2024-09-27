from django.urls import  path
from setting import views

app_name = 'setting'
urlpatterns = [
    path('', views.home, name='home'),
]