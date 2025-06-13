from django.db import models

# Create your models here.
class Slide(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='slides/%Y/%m/%d', null=True, blank=True)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.order == 0:  # Solo asignar si no se definió manualmente
            last_order = Slide.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f"Slide {self.id}"