from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import CataloguePage, Category, Material, Product
from .serializers import (
    CataloguePageSerializer,
    CategorySerializer,
    CategoryWithProductsSerializer,
    MaterialSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)
from .filters import ProductFilter


class CataloguePageView(APIView):
    """Hero banner singleton for the catalogue page."""

    def get(self, request):
        obj = CataloguePage.objects.first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        return Response(CataloguePageSerializer(obj, context={"request": request}).data)


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}


class CatalogueView(APIView):
    """
    Full catalogue — all active categories with their products nested.
    Supports ?category=<slug> to return a single category with its products.
    """

    def get(self, request):
        ctx = {"request": request}
        slug = request.query_params.get("category")

        qs = Category.objects.filter(is_active=True).prefetch_related(
            "products", "products__images", "products__sizes", "products__colors", "products__material"
        )
        if slug:
            qs = qs.filter(slug=slug)

        return Response(CategoryWithProductsSerializer(qs, many=True, context=ctx).data)


class ProductListView(ListAPIView):
    """
    Flat product list with filtering, search, and ordering.

    Filters: ?category=<slug>  ?material=<slug>  ?min_price=  ?max_price=
             ?is_featured=true  ?is_new=true  ?is_sale=true
    Search:  ?search=<name>
    Order:   ?ordering=price | -price | created_at | -created_at
    """
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = []   # name is JSON — handled below
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related(
            "category", "material"
        ).prefetch_related("images", "sizes", "colors")

        # JSON name search — filter in Python after DB fetch for SQLite compat
        search = self.request.query_params.get("search", "").strip().lower()
        if search:
            qs = [
                p for p in qs
                if search in (p.name.get("en", "") + p.name.get("zh_hans", "") + p.name.get("zh_hant", "")).lower()
            ]
        return qs

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).select_related(
        "category", "material"
    ).prefetch_related("images", "sizes", "colors", "reviews")
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_serializer_context(self):
        return {"request": self.request}


class RelatedProductsView(APIView):
    """Returns up to 4 products from the same category (excluding current product)."""

    def get(self, request, slug):
        try:
            product = Product.objects.select_related("category").get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        related = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(slug=slug).prefetch_related("images", "sizes", "colors")[:4]

        return Response(
            ProductListSerializer(related, many=True, context={"request": request}).data
        )


class MaterialListView(ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get_serializer_context(self):
        return {"request": self.request}