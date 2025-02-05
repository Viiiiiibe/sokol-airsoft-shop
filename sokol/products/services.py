from django.core.cache import cache
from django.db.models import Q, Max, Min
from .models import Product

CACHE_TIMEOUT = 10 * 60  # 10 минут


def get_cached_products(key, queryset):
    return cache.get_or_set(key, queryset, CACHE_TIMEOUT)


def get_filtered_products(category, request):
    filters = {
        "product_type": "product_type__in",
        "compatibility": "compatibility__in",
        "thread_type": "thread_type__in",
        "mounting_type": "mounting_type__in",
        "imitation_of_a_shot": "imitation_of_a_shot__in",
        "laser_sight": "laser_sight__in",
        "weight": "weight__in",
        "principle_of_operation": "principle_of_operation__in",
        "diameter": "diameter__in",
        "gearbox": "gearbox__in",
    }

    queryset = Q(category=category)
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price or max_price:
        price_range = get_cached_products(
            f"price_data_for_filters_in_{category.slug}_cache",
            Product.objects.filter(category=category).aggregate(Max("price"), Min("price"))
        )
        queryset &= Q(price__range=(min_price or price_range["price__min"], max_price or price_range["price__max"]))

    min_length_get = request.GET.get("min_length", '')
    max_length_get = request.GET.get("max_length", '')

    if min_length_get or max_length_get:
        length_range = get_cached_products(
            f"length_data_for_filters_in_{category.slug}_cache",
            Product.objects.filter(category=category).aggregate(Max("length"), Min("length"))
        )
        queryset &= Q(
            length__range=(min_price or length_range["length__min"], max_price or length_range["length__max"]))

    for param, field in filters.items():
        values = request.GET.getlist(param)
        if values:
            queryset &= Q(**{field: values})

    return Product.objects.filter(queryset).order_by(request.GET.get("sort_by", "-pub_date"))


def get_category_filters(category):
    """Получает данные для фильтров по категории с кешированием."""
    filter_fields = [
        ("price", Max, Min),
        "product_type",
        "compatibility",
        "thread_type",
        "mounting_type",
        "imitation_of_a_shot",
        "laser_sight",
        "weight",
        "principle_of_operation",
        ("length", Max, Min),
        "diameter",
        "gearbox",
    ]

    filters_data = {}
    for field in filter_fields:
        if isinstance(field, tuple):
            field_name, max_func, min_func = field
            filters_data[f"{field_name}_data_for_filters"] = get_cached_products(
                f"{field_name}_data_for_filters_in_{category.slug}_cache",
                Product.objects.filter(category=category).aggregate(max_func(field_name), min_func(field_name))
            )
        else:
            # Если поле числовое, исключаем `None`, а не `""`
            exclude_value = None if field in ["weight", "diameter", "length", "price"] else ""
            filters_data[f"{field}_data_for_filters"] = get_cached_products(
                f"{field}_data_for_filters_in_{category.slug}_cache",
                Product.objects.filter(category=category).values(field).distinct().exclude(**{field: exclude_value})
            )

    return filters_data
