# products/views.py
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from orders.models import Order, OrderItem
from .models import Book

def book_detail(request, pk):
    book = Book.objects.annotate(annotated_rating=Coalesce(Avg('reviews__rating'), 0.0)).get(pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    return render(request, 'products/book_detail.html', {
        'book': book,
        'reviews': reviews,
    })

@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if book.reviews.filter(user=request.user).exists():
                messages.error(request, "Вы уже оставляли отзыв на эту книгу.")
            else:
                review = form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                messages.success(request, "Спасибо за ваш отзыв!")
                return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'products/add_review.html', {
        'book': book,
        'reviews': reviews,
        'form': form
    })

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
