from django.db import models


class Product(models.Model):
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за м²")
    image_url = models.URLField(verbose_name='Основное изображение')
    tags = models.CharField(max_length=200, blank=True, verbose_name='Теги (через запятую)',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']

    def __str__(self):
        translation = self.translations.first()
        return translation.name if translation else 'Без названия'

    def get_translation_json(self, lang):
        print(self.translations.all())

        translation = self.translations.filter(language=lang).first()
        print(translation)
        if not translation:
            translation = self.translations.first()

        images = self.images.all()
        print(images.count())
        return {
            'id': self.id,
            'name': translation.name if translation else None,
            'description': translation.description if translation else None,
            'price_per_sqm': str(self.price_per_sqm),
            'image_url': images[0].image_url if images else None,
            'additional_images': images[1:] if images.count() > 1 else [],
            'tags': self.tags,
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
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        verbose_name = "Контактный запрос"
        verbose_name_plural = "Контактные запросы"

        ordering = ['-created_at']

