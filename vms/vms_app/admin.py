from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product

# Register your models here.
admin.site.register(CustomUser, UserAdmin)

 # Create a custom admin class for the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview')
    search_fields = ('name',)
    list_filter = ('price',)
    fields = ('name', 'price', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image and '<img src="{0}" width="100" height="100" />'.format(obj.image.url)
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

admin.site.register(Product, ProductAdmin)