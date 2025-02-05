from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from cart.cart import Cart
from .models import Product, Category
from .services import get_cached_products, get_filtered_products, get_category_filters


def index(request):
    products = get_cached_products("10_new_products_cache", Product.objects.order_by("-pub_date")[:10])
    context = {"products": products}
    return render(request, "products/index.html", context)


def all_products(request):
    keyword = request.GET.get("q")
    if keyword:
        products = Product.objects.filter(name__icontains=keyword).order_by("-pub_date")
    else:
        products = get_cached_products("all_products_cache", Product.objects.order_by("-pub_date"))

    paginator = Paginator(products, 24)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"page_obj": page_obj, "keyword": keyword}
    return render(request, "products/all_products.html", context)


def categories(request):
    categories = get_cached_products("categories_without_parents_cache",
                                     Category.objects.filter(parent=None).order_by("title"))
    context = {"categories": categories}
    return render(request, "products/categories.html", context)


def subcategories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = get_cached_products(f"{slug}_subcategories_cache", Category.objects.filter(parent=category))
    context = {"subcategories": subcategories, "category": category}
    return render(request, "products/subcategories.html", context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    filters_data = get_category_filters(category)
    products = get_filtered_products(category, request)

    paginator = Paginator(products, request.GET.get("prod_count", 24))
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {"category": category, "page_obj": page_obj, "sort_parameter": request.GET.get("sort_by", "-pub_date"),
               **filters_data}
    return render(request, "products/category_list.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    in_cart = str(product_id) in Cart(request).cart
    context = {"product": product, "in_cart": in_cart}
    return render(request, "products/product_detail.html", context)
