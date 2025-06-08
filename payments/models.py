# payments/models.py
from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=32)
    card_expiry = models.CharField(max_length=8)
    card_cvc = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Платёж {self.id} ({self.user.username})"
    
    class Meta:
        managed = True
        db_table = 'payments_payment'
