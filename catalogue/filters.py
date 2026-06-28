import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    material = django_filters.CharFilter(field_name="material__slug", lookup_expr="exact")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    is_featured = django_filters.BooleanFilter(field_name="is_featured")
    is_new = django_filters.BooleanFilter(field_name="is_new")
    is_sale = django_filters.BooleanFilter(field_name="is_sale")

    class Meta:
        model = Product
        fields = ["category", "material", "min_price", "max_price", "is_featured", "is_new", "is_sale"]