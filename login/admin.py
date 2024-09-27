from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Avatar, UserSetting, DarkMode

# Register your models here.


admin.site.register(User, UserAdmin)

admin.site.register(Avatar)
admin.site.register(UserSetting)
admin.site.register(DarkMode)
