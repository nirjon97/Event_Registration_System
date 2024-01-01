from django.contrib import admin
from .models import Event,Registration,Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Registration)
