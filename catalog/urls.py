from django.urls import path
from .views import ProductListView, ProductDetailView, ContactsView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
