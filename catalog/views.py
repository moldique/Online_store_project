from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'catalog/home.html')

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
