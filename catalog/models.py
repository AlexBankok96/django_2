from django.db import models
from users.models import User

class Product(models.Model):
    NOT_PUBLISHED = 'not_published'
    PUBLISHED = 'published'

    STATUS_CHOICES = [
        (NOT_PUBLISHED, 'Не опубликован'),
        (PUBLISHED, 'Опубликован'),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        max_length=1000, verbose_name="Описание", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        blank=True,
        related_name="Product",
    )
    purchase_price = models.IntegerField(
        null=True, blank=True, verbose_name="Цена за покупку", help_text="Введите цену"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    # Новое поле для статуса публикации
    published = models.BooleanField(default=False, verbose_name="Публикация", help_text="Статус публикации продукта")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]

    def save(self, *args, **kwargs):
        # Убираем логику с version_number
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        max_length=1000,
        verbose_name="Описание категории",
        help_text="Введите описание категории",
    )

    def __str__(self):
        return f"{self.name}{self.description}"

    class Meta:
        verbose_name = "Категорию продукта"
        verbose_name_plural = "Категории"


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Продукт", blank=True, null=True,
                                related_name="versions"
                                )
    version_number = models.IntegerField(verbose_name="номер версии")
    name = models.CharField(
        max_length=200,
        verbose_name="наименование версии",
        default="Default Version Name",
    )
    version_flag = models.BooleanField(default=False, verbose_name="признак версии")

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["product", "version_number", "name", "version_flag"]
        constraints = [
            models.UniqueConstraint(fields=['product', 'version_flag'],
                                    condition=models.Q(version_flag=True),
                                    name='unique_active_version')
        ]

    def __str__(self):
        return f'{self.name} - {self.version_number}'

    def save(self, *args, **kwargs):
        if not self.version_number:
            max_version = Version.objects.filter(product=self).aggregate(models.Max('version_number'))['version_number__max']
            self.version_number = (max_version + 1) if max_version is not None else 1
        if self.version_flag:
            Version.objects.filter(product=self.product, version_flag=True).update(version_flag=False)
        super().save(*args, **kwargs)
