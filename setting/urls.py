from django.urls import  path
from setting import views

app_name = 'setting'
urlpatterns = [
    path('', views.home, name='home'),
    path("<int:pk>/", views.SettingUpdateView.as_view(), name="setting-update"),
    path('avatar/update/', views.AvatarUpdateView.as_view(), name='avatar-update'),
]