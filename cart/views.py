from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Book
from .models import Cart, CartItem
from payments.models import Payment

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('book')
    total = cart.total_price()
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, pk):
    try:
        book = get_object_or_404(Book, pk=pk)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart:cart')
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('cart:cart')

@login_required
def remove_from_cart(request, pk):
    cart = request.user.cart
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=pk)
    cart_item.delete()
    return redirect('cart:cart')

from django.db import DatabaseError
from django.contrib import messages

@login_required
def increment_cart(request, pk):
    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, book_id=pk)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart:cart')     
    except DatabaseError as e:
        error_message = str(e).split('CONTEXT:')[0].strip()
        messages.error(request, error_message)
        return redirect('book_detail', pk=pk)

@login_required
def decrement_cart(request, pk):  # <-- Добавленная функция
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=pk)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('cart:cart')

@login_required
@transaction.atomic
def process_payment(request):
    if request.method == 'POST':
        try:
            cart = request.user.cart
            cart_items = CartItem.objects.filter(cart=cart).select_related('book')
            for item in cart_items:
                if item.book.stock < item.quantity:
                    raise Exception(f"Недостаточно товара: {item.book.title}")  
                item.book.stock -= item.quantity
                item.book.save()
            Payment.objects.create(
                user=request.user,
                amount=cart.total_price(),
                card_number=request.POST.get('card_number'),
                card_expiry=request.POST.get('card_expiry'),
                card_cvc=request.POST.get('card_cvc')
            )
            cart_items.delete()
            messages.success(request, "Оплата прошла успешно! Количество книг обновлено.")
            return redirect('cart:cart')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('cart:cart')
    
    return redirect('cart:cart')
