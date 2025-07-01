from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Назва")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL",
    )

    class Meta:
        db_table = "category"
        verbose_name = "категорію"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва бренду")
    slug = models.SlugField(
        max_length=70, unique=True, blank=True, null=True, verbose_name="URL",
    )

    class Meta:
        db_table = "brand"
        verbose_name = "бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name


class Color(models.Model):
    """Модель для цветов"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Назва кольору")
    hex_code = models.CharField(
        max_length=7,
        verbose_name="HEX код",
        help_text="Наприклад: #FF0000",
    )

    class Meta:
        verbose_name = "Колір"
        verbose_name_plural = "Кольори"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Motorcycle(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Назва")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL",
    )
    description = models.TextField(verbose_name="Опис", blank=True)

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    price = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, verbose_name="Ціна",
    )
    discount = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, verbose_name="Знижка у %",
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")

    is_new = models.BooleanField(
        "Товар новий?", default=False, help_text="Позначити як новий товар",
    )

    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, verbose_name="Категорія",
    )
    brand = models.ForeignKey(Brand, on_delete=models.RESTRICT, verbose_name="Бренд")
    colors = models.ManyToManyField(
        Color, through="MotorcycleVariant", verbose_name="Доступні кольори",
    )

    class Meta:
        indexes = [
            models.Index(fields=["category", "brand"]),
        ]
        verbose_name = "Мотоцикл"
        verbose_name_plural = "Мотоцикли"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = (
                f'для "{self.name}" ще не було додано опису, вибачте за незручності'
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("goods:product", kwargs={"slug": self.slug})

    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100), 3)
        return self.price

    @property
    def default_variant(self):
        """Возвращает вариант по умолчанию (первый доступный)"""
        return self.variants.filter(is_available=True).first()

    @property
    def available_colors(self):
        """Возвращает доступные цвета для мотоцикла"""
        return self.colors.filter(motorcyclevariant__is_available=True)

    @property
    def main_image_obj(self):
        """Возвращает главное изображение варианта по умолчанию"""
        default_variant = self.default_variant
        if default_variant:
            return default_variant.images.filter(is_main=True).first()
        return None



class Engine(models.Model):
    """Характеристики двигуна"""

    FUEL_SYSTEM_CHOICES = [
        ("карбюраторна", "Карбюраторна"),
        ("інжекторна", "Інжекторна"),
    ]

    COOLING_CHOICES = [
        ("повітряне", "Повітряне"),
        ("рідинне", "Рідинне"),
        ("комбіноване", "Комбіноване"),
    ]

    motorcycle = models.OneToOneField(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="engine",
        verbose_name="Мотоцикл",
    )

    # Основні характеристики
    engine_type = models.CharField(
        "Тип двигуна",
        max_length=100,
        help_text="Наприклад: бензиновий, 4-х тактний, FT163FML",
    )
    cylinder_description = models.CharField(
        "Опис циліндрів",
        max_length=200,
        help_text="Наприклад: 1-циліндровий, з верхнім розташуванням розподільного валу SOHC",
    )
    max_power_hp = models.FloatField("Максимальна потужність (к.с.)")
    max_power_rpm = models.IntegerField("Обороти при макс. потужності (об./хв.)")
    torque_nm = models.FloatField("Обертаючий момент (Нм)")
    torque_rpm = models.IntegerField("Обороти при макс. моменті (об./хв.)")
    displacement = models.IntegerField("Об'єм двигуна (см³)")
    cooling = models.CharField(
        "Охолодження двигуна", max_length=20, choices=COOLING_CHOICES,
    )
    start_type = models.CharField(
        "Тип запуску",
        max_length=200,
        help_text="Наприклад: електростартер [з ключа/кнопки] та механічний стартер",
    )
    balance_shaft = models.BooleanField("Балансувальний вал", default=False)
    fuel_system = models.CharField(
        "Система упорскування палива", max_length=20, choices=FUEL_SYSTEM_CHOICES,
    )

    class Meta:
        verbose_name = "Двигун"
        verbose_name_plural = "Двигуни"

    def __str__(self):
        return f"Двигун {self.motorcycle}"


class Transmission(models.Model):
    """Характеристики трансмісії"""

    GEARBOX_TYPE_CHOICES = [
        ("механічна", "Механічна"),
        ("автоматична", "Автоматична"),
        ("CVT", "CVT"),
    ]

    DRIVE_TYPE_CHOICES = [
        ("ланцюговий", "Ланцюговий"),
        ("ременевий", "Ременевий"),
        ("кардановий", "Кардановий"),
    ]

    motorcycle = models.OneToOneField(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="transmission",
        verbose_name="Мотоцикл",
    )

    gearbox_type = models.CharField(
        "Тип КПП", max_length=20, choices=GEARBOX_TYPE_CHOICES,
    )
    gears_count = models.IntegerField("Кількість передач")
    gearbox_description = models.CharField(
        "Опис КПП",
        max_length=200,
        help_text="Наприклад: послідовна (схема 1-0-2-3-4-5)",
    )
    drive_type = models.CharField(
        "Тип приводу", max_length=20, choices=DRIVE_TYPE_CHOICES,
    )
    clutch_description = models.CharField(
        "Зчеплення",
        max_length=200,
        help_text="Наприклад: механічне, багатодискове, в масляній ванні",
    )

    class Meta:
        verbose_name = "Трансмісія"
        verbose_name_plural = "Трансмісії"

    def __str__(self):
        return f"Трансмісія {self.motorcycle}"


class SuspensionSystem(models.Model):
    SUSPENSION_TYPE_CHOICES = [
        ("телескопічна вилка", "Телескопічна вилка"),
        ("маятникова", "Маятникова"),
        ("моноаморт", "Моноаморт"),
    ]

    motorcycle = models.OneToOneField(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="chassis",
        verbose_name="Мотоцикл",
    )
    # Підвіска
    front_suspension = models.CharField(
        "Передня підвіска", max_length=50, choices=SUSPENSION_TYPE_CHOICES,
    )
    rear_suspension = models.CharField(
        "Задня підвіска",
        max_length=200,
        help_text="Наприклад: маятникова, два амортизатори",
    )

    # Колеса
    front_wheel = models.CharField(
        "Переднє колесо", max_length=50, help_text="Розмір у форматі 90/90-17 R",
    )
    rear_wheel = models.CharField(
        "Заднє колесо", max_length=50, help_text="Розмір у форматі 120/80-17 R",
    )
    wheelbase = models.IntegerField("Колісна база (мм)")
    ground_clearance = models.IntegerField("Дорожній просвіт (мм)")

    class Meta:
        verbose_name = "Ходова частина"
        verbose_name_plural = "Ходові частини"

    def __str__(self):
        return f"Ходові частини мотоциклу {self.motorcycle}"

class BreakSystem(models.Model):
    BRAKE_TYPE_CHOICES = [
        ("дисковий", "Дисковий"),
        ("барабанний", "Барабанний"),
    ]

    motorcycle = models.OneToOneField(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="brakes",
        verbose_name="Мотоцикл",
    )

    # Гальма
    front_brake_type = models.CharField(
        "Тип переднього гальма", max_length=20, choices=BRAKE_TYPE_CHOICES,
    )
    rear_brake_type = models.CharField(
        "Тип заднього гальма", max_length=20, choices=BRAKE_TYPE_CHOICES,
    )
    front_brake_description = models.CharField(
        "Опис переднього гальма",
        max_length=200,
        help_text="Наприклад: дисковий, гідравлічний",
    )
    rear_brake_description = models.CharField(
        "Опис заднього гальма",
        max_length=200,
        help_text="Наприклад: дисковий, гідравлічний",
    )

    class Meta:
        verbose_name = "гальма"
        verbose_name_plural = "гальма"

    def __str__(self):
        return f"Гальма {self.motorcycle}"


class PerformanceSpecs(models.Model):
    """Експлуатаційні характеристики"""

    motorcycle = models.OneToOneField(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="performance",
        verbose_name="Мотоцикл",
    )

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

    motorcycle = models.OneToOneField(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Мотоцикл",
    )

    dashboard_description = models.TextField(
        "Приладова панель", help_text="Опис приладової панелі та її функцій",
    )
    lighting_description = models.TextField(
        "Світло", help_text="Опис системи освітлення",
    )
    lubrication_system = models.CharField(
        "Система змазки",
        max_length=200,
        help_text="Наприклад: тиском та розбризкуванням, з мокрим картером",
    )
    recommended_oil = models.TextField(
        "Рекомендована олія", help_text="Рекомендації по моторній оливі",
    )

    class Meta:
        verbose_name = "Додаткові характеристики"
        verbose_name_plural = "Додаткові характеристики"

    def __str__(self):
        return f"Додаткові характеристики {self.motorcycle}"


class MotorcycleVariant(models.Model):
    """Вариант мотоцикла (конкретный цвет)"""

    motorcycle = models.ForeignKey(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Мотоцикл",
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Колір")

    # Специфические для варианта поля
    price_modifier = models.DecimalField(
        default=0.00,
        max_digits=10,
        decimal_places=2,
        verbose_name="Модифікатор ціни",
        help_text="Додаткова вартість за цей колір (може бути від'ємною)",
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Кількість на складі",
    )
    is_available = models.BooleanField(
        default=True, verbose_name="Доступний для замовлення",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("motorcycle", "color")
        verbose_name = "Варіант мотоцикла"
        verbose_name_plural = "Варіанти мотоциклів"
        ordering = ["motorcycle", "color"]

    def __str__(self):
        return f"{self.motorcycle.name} - {self.color.name}"

    def final_price(self):
        """Отримання фінальної оцінки з можифікацією"""
        base_price = self.motorcycle.price + self.price_modifier
        if self.motorcycle.discount:
            return round(base_price - (base_price * self.motorcycle.discount / 100), 3)
        return base_price

    @property
    def main_image(self):
        """Главное изображение этого варианта"""
        return self.images.filter(is_main=True).first()





class VariantImage(models.Model):
    """Изображения для конкретного варианта мотоцикла"""

    variant = models.ForeignKey(
        MotorcycleVariant,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Варіант",
    )
    image = models.ImageField("Зображення", upload_to="motorcycle_variants/")
    title = models.CharField("Назва зображення", max_length=200, blank=True)
    is_main = models.BooleanField("Основне зображення", default=False)
    sort_order = models.PositiveIntegerField(
        default=0, verbose_name="Порядок сортування",
    )
    created_at = models.DateTimeField("Дата додавання", auto_now_add=True)

    class Meta:
        verbose_name = "Зображення варіанту"
        verbose_name_plural = "Зображення варіантів"
        ordering = ["sort_order", "-is_main", "-created_at"]

    def __str__(self):
        return f"Зображення {self.variant} - {self.title}"

    def save(self, *args, **kwargs):
        if self.is_main:
            VariantImage.objects.filter(variant=self.variant, is_main=True).update(
                is_main=False,
            )
        super().save(*args, **kwargs)
