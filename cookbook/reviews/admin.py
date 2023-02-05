from django.contrib import admin
from reviews.models import (Dish, Review)


class DishAdmin(admin.ModelAdmin):
  model = Dish
  list_display = ('name', 'description','publication_date')
  search_fields = ['name']

# Register your models here.
admin.site.register(Dish, DishAdmin)
admin.site.register(Review)
