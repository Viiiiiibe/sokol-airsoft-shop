from django.contrib import admin
from mptt.fields import TreeManyToManyField
from .models import Product, Category
from mptt.admin import DraggableMPTTAdmin
from django.forms import CheckboxSelectMultiple


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'categories', 'name', 'price', 'items_left', 'recommend')
    search_fields = ('name', 'description',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'
    list_editable = ('recommend',)
    formfield_overrides = {
        TreeManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug',)
    mptt_level_indent = 20

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
