# users/models.py
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', _('Покупатель')
        ADMIN = 'admin', _('Администратор')
        SUPERADMIN = 'superadmin', _('Супер-админ')

    phone = models.CharField('Телефон', max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    email_verified = models.BooleanField(_('Email подтверждён'), default=False)
    
    role = models.CharField(
        _('Роль'),
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    balance = models.DecimalField(
        _('Баланс'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_index=True
    )
    phone = models.CharField(
        _('Телефон'),
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # Автоматически устанавливаем права доступа на основе роли
        if self.role in [self.Role.ADMIN, self.Role.SUPERADMIN]:
            self.is_staff = True
        if self.role == self.Role.SUPERADMIN:
            self.is_superuser = True
        
        super().save(*args, **kwargs)
        
        # Назначаем права после сохранения
        if self.role == self.Role.ADMIN:
            self._assign_admin_permissions()

    # Добавленный метод
    def _assign_admin_permissions(self):
        """Назначает права администратора."""
        permissions = Permission.objects.filter(
            content_type__app_label__in=['orders', 'products'],
            codename__in=[
                'view_order', 'change_order',
                'view_book', 'change_book',
                'view_review', 'delete_review'
            ]
        )
        self.user_permissions.set(permissions)
