from products.models import Product
from django.core.cache import cache


def bestsellers_data(request):
    recommended_products = cache.get_or_set("recommended_products_cache",
                                            Product.objects.all().filter(recommend=True).order_by('-pub_date'), 10 * 60)
    return {'recommended_products': recommended_products}
