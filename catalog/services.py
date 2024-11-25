from django.core.cache import cache
from catalog.models import Product, Category


def get_cached_product_details(product_id):
    cache_key = f'product_{product_id}_details'
    cached_data = cache.get(cache_key)

    if cached_data is None:
        product = Product.objects.filter(id=product_id).first()
        if product:
            cached_data = {
                'name': product.name,
                'description': product.description,
                'purchase_price': product.purchase_price,
                'image': product.image.url if product.image else None,
            }
            cache.set(cache_key, cached_data, timeout=60)
    return cached_data


def get_categories_from_cache():
    cache_key = 'product_categories'
    cached_data = cache.get(cache_key)

    if cached_data is None:
        categories = Category.objects.all()
        cached_data = {
            'categories': [category.name for category in categories]
        }
        cache.set(cache_key, cached_data, timeout=60)
    return cached_data
