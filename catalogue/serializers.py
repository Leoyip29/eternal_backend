from rest_framework import serializers
from core.serializers import TranslatedCharField
from .models import (
    CataloguePage, Category, Material,
    Product, ProductImage, ProductSize, ProductColor, ProductReview,
)


class CataloguePageSerializer(serializers.ModelSerializer):
    hero_title = TranslatedCharField()
    hero_subtitle = TranslatedCharField()

    class Meta:
        model = CataloguePage
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    name = TranslatedCharField()
    description = TranslatedCharField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "image", "order")


class MaterialSerializer(serializers.ModelSerializer):
    name = TranslatedCharField()

    class Meta:
        model = Material
        fields = ("id", "name", "slug")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_primary", "order")


class ProductSizeSerializer(serializers.ModelSerializer):
    label = TranslatedCharField()

    class Meta:
        model = ProductSize
        fields = ("id", "label", "dimensions", "price_modifier", "is_default", "order")


class ProductColorSerializer(serializers.ModelSerializer):
    name = TranslatedCharField()

    class Meta:
        model = ProductColor
        fields = ("id", "name", "hex_code", "swatch_image", "is_default", "order")


class ProductReviewSerializer(serializers.ModelSerializer):
    review_text = TranslatedCharField()

    class Meta:
        model = ProductReview
        fields = ("id", "customer_name", "review_text", "star_rating", "created_at")


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for catalogue listing — no nested reviews."""
    name = TranslatedCharField()
    short_description = TranslatedCharField()
    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "category", "material",
            "price", "sale_price", "effective_price",
            "short_description",
            "images", "sizes", "colors",
            "is_featured", "is_new", "is_sale",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail page — includes reviews and full description."""
    name = TranslatedCharField()
    short_description = TranslatedCharField()
    full_description = TranslatedCharField()
    shipping_info = TranslatedCharField()
    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True, source="reviews.filter")
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "category", "material",
            "price", "sale_price", "effective_price",
            "short_description", "full_description", "shipping_info",
            "images", "sizes", "colors", "reviews",
            "is_featured", "is_new", "is_sale",
            "average_rating", "review_count",
            "created_at",
        )

    def get_average_rating(self, obj):
        active = obj.reviews.filter(is_active=True)
        if not active.exists():
            return None
        total = sum(r.star_rating for r in active)
        return round(total / active.count(), 1)

    def get_review_count(self, obj):
        return obj.reviews.filter(is_active=True).count()

    def to_representation(self, instance):
        # override reviews source to filter active only
        ret = super().to_representation(instance)
        ctx = self.context
        active_reviews = instance.reviews.filter(is_active=True)
        ret["reviews"] = ProductReviewSerializer(active_reviews, many=True, context=ctx).data
        return ret


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    """Used on the catalogue page — each category with its products nested."""
    name = TranslatedCharField()
    description = TranslatedCharField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "image", "order", "products")

    def get_products(self, obj):
        active = obj.products.filter(is_active=True).prefetch_related("images", "sizes", "colors")
        return ProductListSerializer(active, many=True, context=self.context).data