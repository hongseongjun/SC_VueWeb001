from django.contrib import admin
from .models import User, UserLoginLog

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'level', 'is_staff', 'is_admin', 'is_superuser', 'jdate')
    search_fields = ('user_id', 'name')
#admin.site.register(User, UserAdmin)


@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_ip', 'loginout')
    search_fields = ('user_id', 'user_name')
