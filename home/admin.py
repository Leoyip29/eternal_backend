from django.contrib import admin
from .models import (
    HeroSection, HeroImage,
    ProductsSectionHeading, FeaturedProduct,
    ServicesSectionHeading, ServiceStep,
    HowItWorksHeading, HowItWorksStep,
    StoneGallerySection, StoneGalleryImage,
    AboutUsSection, AboutUsImage,
    FAQSection, FAQ,
    TestimonialsSection, Testimonial,
)


# ── Hero ──────────────────────────────────────────────────────────────────────

class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1
    fields = ("image", "alt_text", "order")


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Copy", {"fields": ("headline", "subtext")}),
        ("Call to Action", {"fields": ("cta1_label", "cta1_url", "cta2_label", "cta2_url")}),
        ("Status", {"fields": ("is_active",)}),
    )
    inlines = [HeroImageInline]

    def has_add_permission(self, request):
        return not HeroSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Products ──────────────────────────────────────────────────────────────────

@admin.register(ProductsSectionHeading)
class ProductsSectionHeadingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ProductsSectionHeading.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("name",)


# ── Services ──────────────────────────────────────────────────────────────────

class ServiceStepInline(admin.TabularInline):
    model = ServiceStep
    extra = 1
    fields = ("icon", "title", "description", "order")


@admin.register(ServicesSectionHeading)
class ServicesSectionHeadingAdmin(admin.ModelAdmin):
    inlines = [ServiceStepInline]

    def has_add_permission(self, request):
        return not ServicesSectionHeading.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── How It Works ──────────────────────────────────────────────────────────────

class HowItWorksStepInline(admin.TabularInline):
    model = HowItWorksStep
    extra = 1
    fields = ("step_number", "icon", "title", "description")


@admin.register(HowItWorksHeading)
class HowItWorksHeadingAdmin(admin.ModelAdmin):
    inlines = [HowItWorksStepInline]

    def has_add_permission(self, request):
        return not HowItWorksHeading.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Stone Gallery ──────────────────────────────────────────────────────────────

class StoneGalleryImageInline(admin.TabularInline):
    model = StoneGalleryImage
    extra = 1
    fields = ("image", "alt_text", "order")


@admin.register(StoneGallerySection)
class StoneGallerySectionAdmin(admin.ModelAdmin):
    inlines = [StoneGalleryImageInline]

    def has_add_permission(self, request):
        return not StoneGallerySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── About Us ──────────────────────────────────────────────────────────────────

class AboutUsImageInline(admin.TabularInline):
    model = AboutUsImage
    extra = 1
    fields = ("image", "alt_text", "order")


@admin.register(AboutUsSection)
class AboutUsSectionAdmin(admin.ModelAdmin):
    inlines = [AboutUsImageInline]

    def has_add_permission(self, request):
        return not AboutUsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── FAQ ───────────────────────────────────────────────────────────────────────

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ("question", "answer", "order", "is_active")


@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    inlines = [FAQInline]

    def has_add_permission(self, request):
        return not FAQSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Testimonials ──────────────────────────────────────────────────────────────

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    fields = ("customer_name", "review_text", "star_rating", "order", "is_active")


@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(admin.ModelAdmin):
    inlines = [TestimonialInline]

    def has_add_permission(self, request):
        return not TestimonialsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False