from rest_framework import serializers
from core.serializers import TranslatedCharField
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


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = ("id", "image", "alt_text", "order")


class HeroSectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()
    cta1_label = TranslatedCharField()
    cta2_label = TranslatedCharField()
    images = HeroImageSerializer(many=True, read_only=True)

    class Meta:
        model = HeroSection
        fields = "__all__"


class ProductsSectionHeadingSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()

    class Meta:
        model = ProductsSectionHeading
        fields = "__all__"


class FeaturedProductSerializer(serializers.ModelSerializer):
    name = TranslatedCharField()
    description = TranslatedCharField()

    class Meta:
        model = FeaturedProduct
        fields = ("id", "name", "description", "image", "order")


class ServiceStepSerializer(serializers.ModelSerializer):
    title = TranslatedCharField()
    description = TranslatedCharField()

    class Meta:
        model = ServiceStep
        fields = ("id", "icon", "title", "description", "order")


class ServicesSectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()
    steps = ServiceStepSerializer(many=True, read_only=True)

    class Meta:
        model = ServicesSectionHeading
        fields = ("id", "headline", "subtext", "background_image", "steps")


class HowItWorksStepSerializer(serializers.ModelSerializer):
    title = TranslatedCharField()
    description = TranslatedCharField()

    class Meta:
        model = HowItWorksStep
        fields = ("id", "step_number", "title", "description", "icon")


class HowItWorksSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()
    steps = HowItWorksStepSerializer(many=True, read_only=True)

    class Meta:
        model = HowItWorksHeading
        fields = ("id", "headline", "subtext", "steps")


class StoneGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoneGalleryImage
        fields = ("id", "image", "alt_text", "order")


class StoneGallerySectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()
    explore_more_label = TranslatedCharField()
    images = StoneGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = StoneGallerySection
        fields = ("id", "headline", "subtext", "explore_more_label", "explore_more_url", "images")


class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = ("id", "image", "alt_text", "order")


class AboutUsSectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    body_text = TranslatedCharField()
    images = AboutUsImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUsSection
        fields = ("id", "headline", "body_text", "images")


class FAQSerializer(serializers.ModelSerializer):
    question = TranslatedCharField()
    answer = TranslatedCharField()

    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "order")


class FAQSectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = FAQSection
        fields = ("id", "headline", "faqs")


class TestimonialSerializer(serializers.ModelSerializer):
    review_text = TranslatedCharField()

    class Meta:
        model = Testimonial
        fields = ("id", "customer_name", "review_text", "star_rating", "order")


class TestimonialsSectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()
    testimonials = TestimonialSerializer(many=True, read_only=True)

    class Meta:
        model = TestimonialsSection
        fields = ("id", "headline", "subtext", "testimonials")