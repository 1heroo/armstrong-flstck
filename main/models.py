from django.db import models


class ProductCategory(models.Model):
    image_url = models.URLField(blank=True, null=True, verbose_name='Изображение')
    
    def __str__(self):
        tranlatiion = self.get_translation_json('ru')
        if tranlatiion.get('name'):
            return tranlatiion.get('name')
        return ''
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_translation_json(self, lang):
        translation = self.translations.filter(language=lang).first()
        if not translation:
            translation = self.translations.first()
        return {
            'id': self.id,
            'name': translation.name if translation else None,
            'description': translation.description if translation else None,
        }


class ProductCategoryTranslation(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('ru', 'Русский'),
        ('ky', 'Кыргызча'),
    ]
    
    product_category = models.ForeignKey(ProductCategory, related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='ru')
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Перевод категории"
        verbose_name_plural = "Переводы категорий"
        unique_together = ('product_category', 'language')
    
    def __str__(self):
        return self.name


class ProductType(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='product_types', on_delete=models.CASCADE, null=True)

    def __str__(self):
        translation = self.translations.first()
        return translation.name if translation else 'Без названия'
    
    def get_name(self, lang='ru'):
        translation = self.translations.filter(language=lang).first()
        if translation:
            return translation.name
        return self.translations.first().name if self.translations.exists() else 'Без названия'
    
    class Meta:
        verbose_name = "Модель вид"
        verbose_name_plural = "Модель виды"

    def get_translation_json(self, lang):
        translation = self.translations.filter(language=lang).first()
        if not translation:
            translation = self.translations.first()
        return {
            'id': self.id,
            'name': translation.name if translation else None,
        }


class ProductTypeTranslation(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('ru', 'Русский'),
        ('ky', 'Кыргызча'),
    ]

    product_type = models.ForeignKey(ProductType, related_name='translations', on_delete=models.CASCADE, null=True)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='ru')
    name = models.CharField(max_length=100, verbose_name='Название', default='Без названия')

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE, null=True)
    
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за м²")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    
    image_url = models.URLField(verbose_name='Основное изображение')
    tags = models.CharField(max_length=200, blank=True, verbose_name='Теги (через запятую)',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"
        ordering = ['-in_stock', '-created_at']

    def __str__(self):
        translation = self.translations.first()
        return translation.name if translation else 'Без названия'

    def get_translation_json(self, lang):
        translation = self.translations.filter(language=lang).first()
        if not translation:
            translation = self.translations.first()

        images = self.images.all()
        type_name = None
        if hasattr(self, 'product_type') and self.product_type:
            type_translation = self.product_type.get_translation_json(lang)
            type_name = type_translation['name'] if type_translation else None

        product_name = translation.name if translation else None
        type_product_name = product_name
        if type_name and product_name:
            type_product_name = f"{product_name} - ({type_name})"

        return {
            'id': self.id,
            'name': translation.name if translation else None,
            'type_name': type_product_name,
            'description': translation.description if translation else None,
            'price_per_sqm': float(self.price_per_sqm.normalize()),
            'in_stock': self.in_stock,
            'image_url': images[0].image_url if images else None,
            'additional_images': [img.image_url for img in images[1:]] if images.count() > 1 else [],
            'tags': self.tags,
            'characteristics': [char.get_translation_json(lang) for char in self.characteristics.all()]
        }

    def get_name(self, lang='ru'):
        translation = self.translations.filter(language=lang).first()
        if translation:
            return translation.name
        return self.translations.first().name if self.translations.exists() else 'Без названия'


class ProductTranslation(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('ru', 'Русский'),
        ('ky', 'Кыргызча'),
    ]

    product = models.ForeignKey(Product, related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='ru', verbose_name='Язык')
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        verbose_name = "Перевод продукта"
        verbose_name_plural = "Переводы продуктов"

        unique_together = ('product', 'language')

    def __str__(self):
        return f"id: {self.id}"


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = "Характеристика модели"
        verbose_name_plural = "Характеристики моделей"
        ordering = ['order']

    def __str__(self):
        return f"{self.product} - {self.translations.first().name if self.translations.exists() else 'Характеристика'}"

    def get_translation_json(self, lang='ru'):
        translation = self.translations.filter(language=lang).first()
        if not translation:
            translation = self.translations.first()
        return {
            "id": self.id,
            "name": translation.name if translation else None,
            "value": translation.value if translation else None
        }


class ProductCharacteristicTranslation(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('ru', 'Русский'),
        ('ky', 'Кыргызча'),
    ]

    characteristic = models.ForeignKey(ProductCharacteristic, related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='ru')
    name = models.CharField(max_length=200, verbose_name='Название характеристики')
    value = models.CharField(max_length=200, verbose_name='Значение характеристики', blank=True)

    class Meta:
        verbose_name = "Перевод характеристики"
        verbose_name_plural = "Переводы характеристик"
        unique_together = ('characteristic', 'language')

    def __str__(self):
        return f"{self.name}: {self.value} ({self.language})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(verbose_name='URL изображения')

    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Альтернативный текст')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product} - Image {self.order}"


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)
    message = models.TextField(verbose_name='Сообщение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    checked = models.BooleanField(default=False, verbose_name='Проверено')    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        verbose_name = "Контактный запрос"
        verbose_name_plural = "Контактные запросы"

        ordering = ['-created_at']

