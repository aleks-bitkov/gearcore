from django.db import models
from django.urls import reverse

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

class Motorcycle(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(verbose_name='Опис', blank=True)

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Ціна')
    discount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Знижка у %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість')

    is_new = models.BooleanField("Товар новий?", default=False, help_text="Позначити як новий товар")

    category = models.ForeignKey(Categories, on_delete=models.RESTRICT, verbose_name='Категорія')
    brand = models.ForeignKey(Brands, on_delete=models.RESTRICT, verbose_name='Бренд')

    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100),3)
        return self.price

    @property
    def main_image_obj(self):
        return self.images.filter(is_main=True).first()

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = f"для \"{self.name}\" ще не було додано опису, вибачте за незручності"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("goods:product", kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            models.Index(fields=['category', 'brand']),  # Композитний індекс
        ]
        verbose_name = "Мотоцикл"
        verbose_name_plural = "Мотоцикли"
        ordering = ['-created_at']

    def __str__(self):
        return self.name



class Engine(models.Model):
    """Характеристики двигуна"""
    FUEL_SYSTEM_CHOICES = [
        ('карбюраторна', 'Карбюраторна'),
        ('інжекторна', 'Інжекторна'),
    ]

    COOLING_CHOICES = [
        ('повітряне', 'Повітряне'),
        ('рідинне', 'Рідинне'),
        ('комбіноване', 'Комбіноване'),
    ]

    motorcycle = models.OneToOneField(Motorcycle, on_delete=models.CASCADE, related_name='engine',
                                      verbose_name="Мотоцикл")

    # Основні характеристики
    engine_type = models.CharField("Тип двигуна", max_length=100,
                                   help_text="Наприклад: бензиновий, 4-х тактний, FT163FML")
    cylinder_description = models.CharField("Опис циліндрів", max_length=200,
                                            help_text="Наприклад: 1-циліндровий, з верхнім розташуванням розподільного валу SOHC")
    max_power_hp = models.FloatField("Максимальна потужність (к.с.)")
    max_power_rpm = models.IntegerField("Обороти при макс. потужності (об./хв.)")
    torque_nm = models.FloatField("Обертаючий момент (Нм)")
    torque_rpm = models.IntegerField("Обороти при макс. моменті (об./хв.)")
    displacement = models.IntegerField("Об'єм двигуна (см³)")
    cooling = models.CharField("Охолодження двигуна", max_length=20, choices=COOLING_CHOICES)
    start_type = models.CharField("Тип запуску", max_length=200,
                                  help_text="Наприклад: електростартер [з ключа/кнопки] та механічний стартер")
    balance_shaft = models.BooleanField("Балансувальний вал", default=False)
    fuel_system = models.CharField("Система упорскування палива", max_length=20, choices=FUEL_SYSTEM_CHOICES)

    class Meta:
        verbose_name = "Двигун"
        verbose_name_plural = "Двигуни"

    def __str__(self):
        return f"Двигун {self.motorcycle}"


class Transmission(models.Model):
    """Характеристики трансмісії"""
    GEARBOX_TYPE_CHOICES = [
        ('механічна', 'Механічна'),
        ('автоматична', 'Автоматична'),
        ('CVT', 'CVT'),
    ]

    DRIVE_TYPE_CHOICES = [
        ('ланцюговий', 'Ланцюговий'),
        ('ременевий', 'Ременевий'),
        ('кардановий', 'Кардановий'),
    ]

    motorcycle = models.OneToOneField(Motorcycle, on_delete=models.CASCADE, related_name='transmission',
                                      verbose_name="Мотоцикл")

    gearbox_type = models.CharField("Тип КПП", max_length=20, choices=GEARBOX_TYPE_CHOICES)
    gears_count = models.IntegerField("Кількість передач")
    gearbox_description = models.CharField("Опис КПП", max_length=200,
                                           help_text="Наприклад: послідовна (схема 1-0-2-3-4-5)")
    drive_type = models.CharField("Тип приводу", max_length=20, choices=DRIVE_TYPE_CHOICES)
    clutch_description = models.CharField("Зчеплення", max_length=200,
                                          help_text="Наприклад: механічне, багатодискове, в масляній ванні")

    class Meta:
        verbose_name = "Трансмісія"
        verbose_name_plural = "Трансмісії"

    def __str__(self):
        return f"Трансмісія {self.motorcycle}"


class ChassisAndBrakes(models.Model):
    """Ходова частина і гальма"""
    BRAKE_TYPE_CHOICES = [
        ('дисковий', 'Дисковий'),
        ('барабанний', 'Барабанний'),
    ]

    SUSPENSION_TYPE_CHOICES = [
        ('телескопічна вилка', 'Телескопічна вилка'),
        ('маятникова', 'Маятникова'),
        ('моноаморт', 'Моноаморт'),
    ]

    motorcycle = models.OneToOneField(Motorcycle, on_delete=models.CASCADE, related_name='chassis',
                                      verbose_name="Мотоцикл")

    # Гальма
    front_brake_type = models.CharField("Тип переднього гальма", max_length=20, choices=BRAKE_TYPE_CHOICES)
    rear_brake_type = models.CharField("Тип заднього гальма", max_length=20, choices=BRAKE_TYPE_CHOICES)
    front_brake_description = models.CharField("Опис переднього гальма", max_length=200,
                                               help_text="Наприклад: дисковий, гідравлічний")
    rear_brake_description = models.CharField("Опис заднього гальма", max_length=200,
                                              help_text="Наприклад: дисковий, гідравлічний")

    # Підвіска
    front_suspension = models.CharField("Передня підвіска", max_length=50, choices=SUSPENSION_TYPE_CHOICES)
    rear_suspension = models.CharField("Задня підвіска", max_length=200,
                                       help_text="Наприклад: маятникова, два амортизатори")

    # Колеса
    front_wheel = models.CharField("Переднє колесо", max_length=50, help_text="Розмір у форматі 90/90-17 R")
    rear_wheel = models.CharField("Заднє колесо", max_length=50, help_text="Розмір у форматі 120/80-17 R")
    wheelbase = models.IntegerField("Колісна база (мм)")
    ground_clearance = models.IntegerField("Дорожній просвіт (мм)")

    class Meta:
        verbose_name = "Ходова частина і гальма"
        verbose_name_plural = "Ходова частина і гальма"

    def __str__(self):
        return f"Ходова {self.motorcycle}"


class PerformanceSpecs(models.Model):
    """Експлуатаційні характеристики"""
    motorcycle = models.OneToOneField(Motorcycle, on_delete=models.CASCADE, related_name='performance',
                                      verbose_name="Мотоцикл")

    max_speed = models.IntegerField("Максимальна швидкість (км/год)")
    fuel_tank_volume = models.FloatField("Об'єм паливного бака (л)")
    fuel_consumption = models.FloatField("Витрати палива (л/100км)")
    curb_weight = models.IntegerField("Вага споряджена (кг)")
    seat_height = models.IntegerField("Висота по сидінню (мм)")
    length = models.IntegerField("Довжина (мм)")
    width = models.IntegerField("Ширина (мм)")
    height = models.IntegerField("Висота (мм)")
    warranty_months = models.IntegerField("Гарантія (місяців)")
    load_capacity = models.IntegerField("Вантажопідйомність (кг)")
    country_of_origin = models.CharField("Країна виробництва", max_length=100)

    class Meta:
        verbose_name = "Експлуатаційні характеристики"
        verbose_name_plural = "Експлуатаційні характеристики"

    def __str__(self):
        return f"Характеристики {self.motorcycle}"


class AdditionalFeatures(models.Model):
    """Інші характеристики"""
    motorcycle = models.OneToOneField(Motorcycle, on_delete=models.CASCADE, related_name='features',
                                      verbose_name="Мотоцикл")

    dashboard_description = models.TextField("Приладова панель", help_text="Опис приладової панелі та її функцій")
    lighting_description = models.TextField("Світло", help_text="Опис системи освітлення")
    lubrication_system = models.CharField("Система змазки", max_length=200,
                                          help_text="Наприклад: тиском та розбризкуванням, з мокрим картером")
    recommended_oil = models.TextField("Рекомендована олія", help_text="Рекомендації по моторній оливі")

    class Meta:
        verbose_name = "Додаткові характеристики"
        verbose_name_plural = "Додаткові характеристики"

    def __str__(self):
        return f"Додаткові характеристики {self.motorcycle}"


# Додаткова модель для зберігання зображень мотоцикла
class MotorcycleImage(models.Model):
    """Зображення мотоцикла"""
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, related_name='images', verbose_name="Мотоцикл")
    image = models.ImageField("Зображення", upload_to='motorcycles/')
    title = models.CharField("Назва зображення", max_length=200, blank=True)
    is_main = models.BooleanField("Основне зображення", default=False)
    created_at = models.DateTimeField("Дата додавання", auto_now_add=True)

    class Meta:
        verbose_name = "Зображення мотоцикла"
        verbose_name_plural = "Зображення мотоциклів"
        ordering = ['-is_main', '-created_at']

    def __str__(self):
        return f"Зображення {self.motorcycle} - {self.title}"

    def save(self, *args, **kwargs):
        # Забезпечуємо, що тільки одне зображення може бути основним
        if self.is_main:
            MotorcycleImage.objects.filter(motorcycle=self.motorcycle, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
