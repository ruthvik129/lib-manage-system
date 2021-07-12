from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import BooksMaster , InventoryMaster , Issues

admin.site.register(BooksMaster)
admin.site.register(InventoryMaster)
admin.site.register(Issues)
