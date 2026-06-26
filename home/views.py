from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    HeroSection, ProductsSectionHeading, FeaturedProduct,
    ServicesSectionHeading, HowItWorksHeading,
    StoneGallerySection, AboutUsSection,
    FAQSection, TestimonialsSection,
)
from .serializers import (
    HeroSectionSerializer, ProductsSectionHeadingSerializer, FeaturedProductSerializer,
    ServicesSectionSerializer, HowItWorksSerializer,
    StoneGallerySectionSerializer, AboutUsSectionSerializer,
    FAQSectionSerializer, TestimonialsSectionSerializer,
)


class HomePageView(APIView):
    """Single endpoint that returns the full homepage content in one call."""

    def get(self, request):
        ctx = {"request": request}

        hero = HeroSection.objects.prefetch_related("images").filter(is_active=True).first()
        products_heading = ProductsSectionHeading.objects.first()
        featured_products = FeaturedProduct.objects.filter(is_active=True)
        services_heading = ServicesSectionHeading.objects.prefetch_related("steps").first()
        hiw_heading = HowItWorksHeading.objects.prefetch_related("steps").first()
        gallery = StoneGallerySection.objects.prefetch_related("images").first()
        about = AboutUsSection.objects.prefetch_related("images").first()
        faq_section = FAQSection.objects.prefetch_related("faqs").first()
        testimonials_section = TestimonialsSection.objects.prefetch_related("testimonials").first()

        return Response({
            "hero": HeroSectionSerializer(hero, context=ctx).data if hero else {},
            "products_section": {
                "heading": ProductsSectionHeadingSerializer(products_heading, context=ctx).data if products_heading else {},
                "products": FeaturedProductSerializer(featured_products, many=True, context=ctx).data,
            },
            "services_section": ServicesSectionSerializer(services_heading, context=ctx).data if services_heading else {},
            "how_it_works": HowItWorksSerializer(hiw_heading, context=ctx).data if hiw_heading else {},
            "stone_gallery": StoneGallerySectionSerializer(gallery, context=ctx).data if gallery else {},
            "about_us": AboutUsSectionSerializer(about, context=ctx).data if about else {},
            "faq": FAQSectionSerializer(faq_section, context=ctx).data if faq_section else {},
            "testimonials": TestimonialsSectionSerializer(testimonials_section, context=ctx).data if testimonials_section else {},
        })


class HeroView(APIView):
    def get(self, request):
        obj = HeroSection.objects.prefetch_related("images").filter(is_active=True).first()
        return Response(HeroSectionSerializer(obj, context={"request": request}).data if obj else {})


class FeaturedProductsView(APIView):
    def get(self, request):
        qs = FeaturedProduct.objects.filter(is_active=True)
        return Response(FeaturedProductSerializer(qs, many=True, context={"request": request}).data)


class StoneGalleryView(APIView):
    def get(self, request):
        obj = StoneGallerySection.objects.prefetch_related("images").first()
        return Response(StoneGallerySectionSerializer(obj, context={"request": request}).data if obj else {})


class AboutUsView(APIView):
    def get(self, request):
        obj = AboutUsSection.objects.prefetch_related("images").first()
        return Response(AboutUsSectionSerializer(obj, context={"request": request}).data if obj else {})


class FAQView(APIView):
    def get(self, request):
        obj = FAQSection.objects.prefetch_related("faqs").first()
        return Response(FAQSectionSerializer(obj, context={"request": request}).data if obj else {})


class TestimonialsView(APIView):
    def get(self, request):
        obj = TestimonialsSection.objects.prefetch_related("testimonials").first()
        return Response(TestimonialsSectionSerializer(obj, context={"request": request}).data if obj else {})