from django.db import models
import uuid
from django.utils.text import slugify

# Función para generar SKU
def generate_sku(name, category_name):
    prefix = category_name[:3].upper()
    name_part = ''.join(e for e in name if e.isalnum())[:3].upper()
    unique_part = uuid.uuid4().hex[:4].upper()
    return f"{prefix}-{name_part}-{unique_part}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Hombre'),
        ('F', 'Mujer'),
        ('U', 'Unisex'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category', 'active']),
            models.Index(fields=['gender']),
        ]

    def __str__(self):
        return (f"{self.name} ({self.sku}) - {self.created.date()} - {self.price} - "
                f"{dict(self.GENDER_CHOICES).get(self.gender)} - "
                f"{'disponible' if self.active else 'No disponible'}")

    def save(self, *args, **kwargs):
        if not self.sku and self.category and self.name:
            self.sku = generate_sku(self.name, self.category.name)
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    @property
    def is_available(self):
        return self.active and self.stock > 0

    @property
    def is_low_stock(self):
        return self.stock > 0 and self.stock < 3
