from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=255)
    is_current = models.BooleanField(default=False)
    description = models.TextField(default="Нет описания")

    class Meta:
        ordering = ['-is_current', 'version_number']

    def __str__(self):
        return f'{self.product.name} - {self.version_name} ({self.version_number})'


# class BlogPost(models.Model):
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)  # уникальное поле для slug
#     content = models.TextField()
#     preview_image = models.ImageField(upload_to='blog_previews/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     published = models.BooleanField(default=False)
#     views_count = models.PositiveIntegerField(default=0)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return self.title