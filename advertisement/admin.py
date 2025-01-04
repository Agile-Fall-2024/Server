from django.contrib import admin

from advertisement.models import Advertisement, Category


# Register your models here.
@admin.register(Advertisement)
class AdvertiseAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass