from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import get_products_by_category
from django.core.cache import cache

# CBV реализации

class ProductListView(ListView):
    """Главная страница с отображением списка товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


    def get_queryset(self):
        
        cache_key = 'product_list'
        products = cache.get(cache_key)
        if products is None:
            products = super().get_queryset()
            cache.set(cache_key, products, 60 * 5)
        return products

@method_decorator(cache_page(60 * 5), name='dispatch')
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

    def form_valid(self, form):
        # Автоматически устанавливаем владельца продукта
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('index')
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        
        # Проверяем, является ли пользователь владельцем продукта
        if product.owner != request.user:
            messages.error(request, 'У вас нет прав для редактирования этого продукта.')
            return redirect('index')
        
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('index')
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        
        # Проверяем, является ли пользователь владельцем продукта или модератором
        if not (product.owner == request.user or request.user.has_perm('catalog.delete_product')):
            messages.error(request, 'У вас нет прав для удаления этого продукта.')
            return redirect('index')
        
        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, View):
    """Представление для отмены публикации продукта"""
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        # Проверяем права пользователя
        if not request.user.has_perm('catalog.can_unpublish_product'):
            messages.error(request, 'У вас нет прав для отмены публикации продуктов.')
            return redirect('index')
        
        # Отменяем публикацию
        product.is_published = False
        product.save()
        
        messages.success(request, f'Публикация продукта "{product.name}" отменена.')
        return redirect('index')

class CategoryProductsView(ListView):
    """Представление для отображения списка продуктов по категории"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        print("CategoryProductsView вызван!")
        # Получаем ID категории из URL
        category_id = self.kwargs.get('category_id')
        print(f"Category ID: {category_id}")
        # Возвращаем список продуктов по категории
        return Product.objects.filter(category_id=category_id, is_published=True)