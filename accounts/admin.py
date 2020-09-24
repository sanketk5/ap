from django.contrib import admin
from . models import Profile, User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('username','first_name','email', 'is_staff','is_superuser','is_active',)
    list_editable=('is_active','is_staff','is_superuser',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'refer_code', 'refer_order',)
    list_display_links = ('user', 'refer_code', 'refer_order',)


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
