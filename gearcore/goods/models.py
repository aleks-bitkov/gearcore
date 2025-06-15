import logging

from django.db import models

log = logging.getLogger(__name__)

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        # db_table = "category"
        verbose_name = "категорію"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Назва бренду')
    slug = models.SlugField(max_length=70, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'brand'
        verbose_name = "бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name


class CategoryBrand(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.RESTRICT, verbose_name='Категорія')
    brand = models.ForeignKey(Brands, on_delete=models.RESTRICT, verbose_name='Бренд')

    class Meta:
        db_table = 'category_brand'
        verbose_name = "категорію-бренд"
        verbose_name_plural = "Категорії-бренди"

    def __str__(self):
        return f"{self.category.name}-{self.brand.name}"


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    description = models.TextField(verbose_name='Опис', blank=True)
    main_image = models.ImageField(upload_to='products/', verbose_name='Головне зображення',
                                   blank=True, default='products/default.jpg')

    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Ціна')
    discount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Знижка у %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість')

    category = models.ForeignKey(Categories, on_delete=models.RESTRICT, verbose_name='Категорія')
    brand = models.ForeignKey(Brands, on_delete=models.RESTRICT, verbose_name='Бренд')

    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100),3)
        return self.price

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = f"для \"{self.name}\" ще не було додано опису, вибачте за незручності"

        category_brand = CategoryBrand.objects.filter(category=self.category, brand=self.brand)

        if not category_brand.exists():
            CategoryBrand.objects.create(category=self.category, brand=self.brand)
            log.debug('create a new entry category-brand: %s-%s', self.category.name, self.brand.name)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "product"
        verbose_name = "продукт"
        verbose_name_plural = "Продукти"
