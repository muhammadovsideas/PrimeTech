from .serializers import *
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# HTML views
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from urllib.parse import quote






class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    @swagger_auto_schema(
        operation_description="List all categories with search and ordering",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by title or description',
                              type=openapi.TYPE_STRING),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description='Order by id or title',
                type=openapi.TYPE_STRING,
                enum=['title', '-title']
            ),
        ]
    )
    def get(self, request):
        categories = Category.objects.all()

        search = request.GET.get('search')
        if search:
            categories = categories.filter(title__icontains=search) | categories.filter(description__icontains=search)

        ordering = request.GET.get('ordering')
        if ordering in ['title', '-title']:
            categories = categories.order_by(ordering)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    @swagger_auto_schema(
        operation_description="List all products with search, price filtering and ordering",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by title, description, or brand',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description='Filter by minimum price',
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description='Filter by maximum price',
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('category', openapi.IN_QUERY, description='Filter by category id',
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description='Order by price, created_at or title',
                type=openapi.TYPE_STRING,
                enum=['price', '-price',  'title', '-title']
            ),
        ]
    )
    def get(self, request):
        products = Product.objects.all()

        search = request.GET.get('search')
        if search:
            products = products.filter(title__icontains=search) | products.filter(
                description__icontains=search) | products.filter(brand__icontains=search)

        min_price = request.GET.get('min_price')
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass

        max_price = request.GET.get('max_price')
        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass

        category_id = request.GET.get('category')
        if category_id:
            try:
                products = products.filter(category_id=int(category_id))
            except ValueError:
                pass

        ordering = request.GET.get('ordering')
        if ordering in ['price', '-price','title', '-title']:
            products = products.order_by(ordering)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



# ------------------ HTML PAGES ------------------
def home(request):
    """Homepage: product list with search and filtering."""
    products = Product.objects.all()

    search = request.GET.get('q')
    if search:
        products = products.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(brand__icontains=search)
        )

    category_id = request.GET.get('category')
    if category_id:
        try:
            products = products.filter(category_id=int(category_id))
        except (TypeError, ValueError):
            pass

    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand__iexact=brand)

    min_price = request.GET.get('min')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max')
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    ordering = request.GET.get('order')
    if ordering in ['price', '-price', 'title', '-title', 'created_at', '-created_at']:
        products = products.order_by(ordering)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Product.objects.order_by('brand').values_list('brand', flat=True).distinct(),
        'qs': request.GET,
    }
    return render(request, 'home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Telegram buy link to admin with prefilled message
    message = (
        f"Assalomu alaykum! Men {product.title} mahsulotini xarid qilmoqchiman. "
        f"Narxi: {product.discount_price or product.price}. ID: {product.pk}"
    )
    telegram_buy_link = f"https://t.me/muhammadov_developer?text={quote(message)}"

    context = {
        'product': product,
        'telegram_buy_link': telegram_buy_link,
        'categories': Category.objects.all(),
        'brands': Product.objects.order_by('brand').values_list('brand', flat=True).distinct(),
        'qs': request.GET,
    }
    return render(request, 'product_detail.html', context)

