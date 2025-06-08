from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Book
from .models import Order, OrderItem

@login_required
def create_order(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        delivery_date = request.POST.get('delivery_date')
        if not delivery_date:
            delivery_date = None  # <-- Ключевая строка!
        book = get_object_or_404(Book, pk=book_id)
        order = Order.objects.create(
            user=request.user,
            delivery_date=delivery_date
        )
        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=1,
            price=book.price
        )   
        messages.success(request, 'Заказ успешно оформлен!')
        return redirect('orders:orders')
    return redirect('home')

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/orders.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
