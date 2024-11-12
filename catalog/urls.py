from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryListView, ProductListByCategoryView, ContactsView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', ProductListByCategoryView.as_view(), name='product_list_by_category'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]

#     # Блоговые маршруты
#     path('blog/', BlogPostListView.as_view(), name='blog_post_list'),
#     path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
#     path('blog/new/', BlogPostCreateView.as_view(), name='blog_post_create'),
#     path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog_post_edit'),
#     path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_post_delete'),  # Удаление записи блога
# ]
