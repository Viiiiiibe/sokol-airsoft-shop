from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category
from products.tasks import rebuild_product_cache, rebuild_category_cache


@receiver(post_save, sender=Product)
def create_product(instance, **kwargs):
    category_slugs = [y for y, *z in list(instance.category.all().values_list('slug'))]
    rebuild_product_cache.delay(category_slugs)


@receiver(post_delete, sender=Product)
def delete_product(instance, **kwargs):
    category_slugs = [y for y, *z in list(instance.category.all().values_list('slug'))]
    rebuild_product_cache.delay(category_slugs)


@receiver(post_save, sender=Category)
def create_category(instance, **kwargs):
    rebuild_category_cache.delay(instance.parent.slug if instance.parent else None)


@receiver(post_delete, sender=Category)
def delete_category(instance, **kwargs):
    rebuild_category_cache.delay(instance.parent.slug if instance.parent else None)
