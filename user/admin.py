from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Visit


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0  
    readonly_fields = ("timestamp",)
    can_delete = False  


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("profile_picture",)}),
    )
    inlines = [VisitInline]  


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    model = Visit
    list_display = ("user", "timestamp")
    search_fields = ("user__username", "user__email")
    ordering = ("-timestamp",)
