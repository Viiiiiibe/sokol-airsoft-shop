from sokol.celery import app
from .models import Product, Category
from django.core.cache import cache
from django.db.models import Max, Min


@app.task
def rebuild_product_cache(category_slugs):
    cache.set("10_new_products_cache", Product.objects.all().order_by('-pub_date')[:10], 10 * 60)
    cache.set("all_products_cache", Product.objects.all().order_by('-pub_date'), 10 * 60)
    cache.set("recommended_products_cache", Product.objects.all().filter(recommend=True).order_by('-pub_date'), 10 * 60)
    if category_slugs is not None:
        for slug in category_slugs:
            cache.set(f"price_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).aggregate(Max('price'), Min('price')), 10 * 60)
            cache.set(f"product_type_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('product_type').distinct().exclude(
                          product_type=''), 10 * 60)
            cache.set(f"compatibility_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('compatibility').distinct().exclude(
                          compatibility=''), 10 * 60)
            cache.set(f"thread_type_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('thread_type').distinct().exclude(
                          thread_type=''), 10 * 60)
            cache.set(f"mounting_type_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('mounting_type').distinct().exclude(
                          mounting_type=''), 10 * 60)
            cache.set(f"imitation_of_a_shot_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values(
                          'imitation_of_a_shot').distinct().exclude(imitation_of_a_shot=''), 10 * 60)
            cache.set(f"laser_sight_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('laser_sight').distinct().exclude(
                          laser_sight=''), 10 * 60)
            cache.set(f"weight_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('weight').distinct().exclude(
                          weight=None),
                      10 * 60)
            cache.set(f"principle_of_operation_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values(
                          'principle_of_operation').distinct().exclude(principle_of_operation=''), 10 * 60)
            cache.set(f"length_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).aggregate(Max('length'), Min('length')),
                      10 * 60)
            cache.set(f"diameter_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('diameter').distinct().exclude(
                          diameter=None), 10 * 60)
            cache.set(f"gearbox_data_for_filters_in_{slug}_cache",
                      Product.objects.all().filter(category__slug=slug).values('gearbox').distinct().exclude(
                          gearbox=''),
                      10 * 60)


@app.task
def rebuild_category_cache(parent_slug):
    cache.set("categories_without_parents_cache", Category.objects.all().filter(parent=None).order_by('title'), None)
    if parent_slug is not None:
        cache.set(f"{parent_slug}_subcategories_cache",
                  Category.objects.all().filter(parent=Category.objects.get(slug=parent_slug)), None)
