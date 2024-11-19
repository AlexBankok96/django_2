from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactsPageView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="catalog_list"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    path("catalog/<int:pk>/", ProductDetailView.as_view(), name="catalog_detail"),
    path('create/', ProductCreateView.as_view(), name="create_product"),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),
]