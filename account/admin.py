from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employer, Jobseeker, EmployerProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "role"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("role",)}),)
    ordering = ["email"]  # Update ordering to use 'email'


class EmployerProfileInline(admin.StackedInline):
    model = EmployerProfile
    can_delete = False
    verbose_name_plural = "EmployerProfile"


class EmployerAdmin(CustomUserAdmin):
    inlines = (EmployerProfileInline,)
    ordering = ["email"]  # Update ordering to use 'email'


class JobseekerAdmin(CustomUserAdmin):
    ordering = ["email"]  # Update ordering to use 'email'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Jobseeker, JobseekerAdmin)
