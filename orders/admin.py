# orders/admin.py
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_date', 'status', 'total_price', 'created_at')
    actions = ['set_status_processing']

    def set_status_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f"Статус 'В обработке' установлен для {updated} заказов.")
    set_status_processing.short_description = "Изменить статус на 'В обработке'"
