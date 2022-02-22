from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User

class ProfileInline(admin.StackedInline): 
    model = Profile
    con_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# admin.site.unregister(MyUser)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)