from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CategoryListView,
    ProductListByCategoryView,
    ContactsView,
    VersionCreateView,   # Добавлен класс для создания версий
    VersionUpdateView    # Добавлен класс для обновления версий
)

app_name = 'catalog'

urlpatterns = [
    # Товары
    path('', ProductListView.as_view(), name='product_list'),  # Список товаров
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Детали товара
    path('product/create/', ProductCreateView.as_view(), name='product_create'),  # Создание товара
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),  # Редактирование товара
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),  # Удаление товара

    # Категории
    path('categories/', CategoryListView.as_view(), name='category_list'),  # Список категорий
    path('category/<int:pk>/', ProductListByCategoryView.as_view(), name='product_list_by_category'),  # Список товаров по категории

    # Контакты
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # Версии продуктов (новые пути)
    path('version/create/', VersionCreateView.as_view(), name='version_create'),  # Создание версии продукта
    path('version/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_edit'),  # Редактирование версии продукта
]
