from django.urls import  path
from setting import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'setting'
urlpatterns = [
    path('', views.home, name='home'),
    path("<int:pk>/", views.SettingUpdateView.as_view(), name="setting-update"),
    path('avatar/update/', views.AvatarUpdateView.as_view(), name='avatar-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)