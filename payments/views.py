from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from cart.models import Cart, CartItem

@login_required
@transaction.atomic
def pay_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.book.price * item.quantity for item in cart_items)
        
        if request.method == 'POST':
            # Данные шифруются автоматически триггером PostgreSQL
            Payment.objects.create(
                user=request.user,
                amount=total,
                card_number=request.POST['card_number'],
                card_expiry=request.POST['card_expiry'],
                card_cvc=request.POST['card_cvc'],
                status='completed'
            )
            cart_items.delete()
            return render(request, 'payments/payment_success.html', {'amount': total})
            
        return render(request, 'payments/payment.html', {'cart_items': cart_items, 'total': total})
    
    except Exception as e:
        messages.error(request, f"Ошибка оплаты: {str(e)}")
        return redirect('cart:cart')
