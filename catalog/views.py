from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Product

# Create your views here.

def index(request):
    """Контроллер главной страницы с отображением товаров"""
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def product_detail(request, pk):
    """Контроллер для отображения страницы товара"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        if name and phone and message:
            # Здесь можно добавить логику сохранения в базу данных
            # или отправки email
            messages.success(request, 'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля формы.')
    
    return render(request, 'catalog/contacts.html')
