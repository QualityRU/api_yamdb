from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import CustomUser


class CustomUserResource(ModelResource):
    """Модель ресурсов пользователей."""

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    """Модель пользователей."""

    resource_classes = (CustomUserResource,)
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
