from django.contrib import admin
from .models import (
    CataloguePage, Category, Material,
    Product, ProductImage, ProductSize, ProductColor, ProductReview,
)


@admin.register(CataloguePage)
class CataloguePageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero Banner", {"fields": ("hero_title", "hero_subtitle", "hero_background_image")}),
    )

    def has_add_permission(self, request):
        return not CataloguePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("__str__",)
    prepopulated_fields = {}
    fieldsets = (
        ("Identity", {"fields": ("name", "slug", "image")}),
        ("Content", {"fields": ("description",)}),
        ("Display", {"fields": ("order", "is_active")}),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("__str__", "slug")
    fieldsets = (
        (None, {"fields": ("name", "slug")}),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "is_primary", "order")


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ("label", "dimensions", "price_modifier", "is_default", "order")


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ("name", "hex_code", "swatch_image", "is_default", "order")


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    fields = ("customer_name", "review_text", "star_rating", "is_active")
    readonly_fields = ("customer_name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "material", "price", "sale_price", "is_active", "is_featured", "is_new", "is_sale")
    list_editable = ("is_active", "is_featured", "is_new", "is_sale")
    list_display_links = ("__str__",)
    list_filter = ("category", "material", "is_active", "is_featured", "is_new", "is_sale")
    search_fields = ("slug",)
    fieldsets = (
        ("Identity",     {"fields": ("name", "slug", "category", "material")}),
        ("Pricing",      {"fields": ("price", "sale_price")}),
        ("Content",      {"fields": ("short_description", "full_description", "shipping_info")}),
        ("Flags",        {"fields": ("is_active", "is_featured", "is_new", "is_sale")}),
    )
    inlines = [ProductImageInline, ProductSizeInline, ProductColorInline, ProductReviewInline]