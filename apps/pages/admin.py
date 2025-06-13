from django.contrib import admin
from .models import Slide


# Register your models here.
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')