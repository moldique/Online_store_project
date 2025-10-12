from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

# CBV реализации

class ProductListView(ListView):
    """Главная страница с отображением списка товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Страница детального просмотра товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = '/users/login/'  # URL для перенаправления неавторизованных пользователей


class ContactsView(TemplateView):
    """Страница контактов с обработкой формы через POST."""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')

        if name and phone and message_text:
            messages.success(request, 'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля формы.')

        # Перерисовываем ту же страницу, чтобы показать сообщения
        return render(request, self.template_name)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('index')
    login_url = '/users/login/'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('index')
    login_url = '/users/login/'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('index')
    login_url = '/users/login/'
