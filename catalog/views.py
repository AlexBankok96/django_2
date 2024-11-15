from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Product, Category, Version
from .forms import ProductForm  # Импортируем нашу форму

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            current_version = product.versions.filter(is_current=True).first()
            product.current_version = current_version
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

class ProductListByCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_list_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Product.objects.filter(category=category)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

# Новые представления для CRUD

class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionCreateView(CreateView):
    model = Version
    template_name = 'catalog/version_form.html'
    fields = ['product', 'version_name', 'version_number', 'description']  # Поля для формы
    success_url = reverse_lazy('catalog:product_list')  # После создания версии перенаправляем на список товаров

    def form_valid(self, form):
        # Можно добавить дополнительную логику для обработки данных формы
        return super().form_valid(form)

# Класс для редактирования версии товара
class VersionUpdateView(UpdateView):
    model = Version
    template_name = 'catalog/version_form.html'
    fields = ['version_name', 'version_number', 'description']  # Поля для формы
    success_url = reverse_lazy('catalog:product_list')  # После редактирования версии перенаправляем на список товаров

    def form_valid(self, form):
        # Можно добавить дополнительную логику для обработки данных формы
        return super().form_valid(form)