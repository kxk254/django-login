from django.urls import  path
from vertical import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'vertical'
urlpatterns = [
    path('', views.home, name='home'),

]