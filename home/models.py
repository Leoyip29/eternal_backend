from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from core.fields import TranslatedField


# ──────────────────────────────────────────────────────────────────────────────
# HERO SECTION
# ──────────────────────────────────────────────────────────────────────────────

class HeroSection(models.Model):
    headline = TranslatedField()
    subtext = TranslatedField(long_text=True)
    cta1_label = TranslatedField(verbose_name="CTA 1 Label")
    cta1_url = models.CharField(max_length=255, verbose_name="CTA 1 URL")
    cta2_label = TranslatedField(verbose_name="CTA 2 Label")
    cta2_url = models.CharField(max_length=255, verbose_name="CTA 2 URL")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def clean(self):
        if not self.pk and HeroSection.objects.exists():
            raise ValidationError("Only one Hero Section is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class HeroImage(models.Model):
    hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="home/hero/")
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Hero Image"
        verbose_name_plural = "Hero Images"

    def __str__(self):
        return f"Hero Image #{self.order}"


# ──────────────────────────────────────────────────────────────────────────────
# OUR PRODUCTS
# ──────────────────────────────────────────────────────────────────────────────

class ProductsSectionHeading(models.Model):
    headline = TranslatedField()
    subtext = TranslatedField()

    class Meta:
        verbose_name = "Products Section Heading"
        verbose_name_plural = "Products Section Heading"

    def clean(self):
        if not self.pk and ProductsSectionHeading.objects.exists():
            raise ValidationError("Only one Products Section Heading is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class FeaturedProduct(models.Model):
    name = TranslatedField()
    description = TranslatedField(long_text=True)
    image = models.ImageField(upload_to="home/products/", blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Featured Product"
        verbose_name_plural = "Featured Products"

    def __str__(self):
        n = self.name
        return n.get("en", "") if isinstance(n, dict) else str(n)


# ──────────────────────────────────────────────────────────────────────────────
# OUR SERVICES
# ──────────────────────────────────────────────────────────────────────────────

class ServicesSectionHeading(models.Model):
    headline = TranslatedField()
    subtext = TranslatedField()
    background_image = models.ImageField(upload_to="home/services/", blank=True, null=True)

    class Meta:
        verbose_name = "Services Section Heading"
        verbose_name_plural = "Services Section Heading"

    def clean(self):
        if not self.pk and ServicesSectionHeading.objects.exists():
            raise ValidationError("Only one Services Section Heading is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class ServiceStep(models.Model):
    section = models.ForeignKey(ServicesSectionHeading, on_delete=models.CASCADE, related_name="steps")
    icon = models.ImageField(upload_to="home/services/icons/", blank=True, null=True)
    title = TranslatedField()
    description = TranslatedField(long_text=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Service Step"
        verbose_name_plural = "Service Steps"

    def __str__(self):
        t = self.title
        return f"{self.order}. {t.get('en', '') if isinstance(t, dict) else t}"


# ──────────────────────────────────────────────────────────────────────────────
# HOW IT WORKS
# ──────────────────────────────────────────────────────────────────────────────

class HowItWorksHeading(models.Model):
    headline = TranslatedField()
    subtext = TranslatedField()

    class Meta:
        verbose_name = "How It Works Heading"
        verbose_name_plural = "How It Works Heading"

    def clean(self):
        if not self.pk and HowItWorksHeading.objects.exists():
            raise ValidationError("Only one How It Works Heading is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class HowItWorksStep(models.Model):
    section = models.ForeignKey(HowItWorksHeading, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveSmallIntegerField()
    title = TranslatedField()
    description = TranslatedField(long_text=True)
    icon = models.ImageField(upload_to="home/how-it-works/", blank=True, null=True)

    class Meta:
        ordering = ["step_number"]
        verbose_name = "How It Works Step"
        verbose_name_plural = "How It Works Steps"

    def __str__(self):
        t = self.title
        return f"Step {self.step_number}: {t.get('en', '') if isinstance(t, dict) else t}"


# ──────────────────────────────────────────────────────────────────────────────
# STONE GALLERY
# ──────────────────────────────────────────────────────────────────────────────

class StoneGallerySection(models.Model):
    headline = TranslatedField()
    subtext = TranslatedField()
    explore_more_label = TranslatedField()
    explore_more_url = models.CharField(max_length=255, default="/stone-catalogue")

    class Meta:
        verbose_name = "Stone Gallery Section"
        verbose_name_plural = "Stone Gallery Section"

    def clean(self):
        if not self.pk and StoneGallerySection.objects.exists():
            raise ValidationError("Only one Stone Gallery Section is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class StoneGalleryImage(models.Model):
    section = models.ForeignKey(StoneGallerySection, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="home/stone-gallery/")
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Stone Gallery Image"
        verbose_name_plural = "Stone Gallery Images"

    def __str__(self):
        return f"Gallery Image #{self.order}"


# ──────────────────────────────────────────────────────────────────────────────
# ABOUT US
# ──────────────────────────────────────────────────────────────────────────────

class AboutUsSection(models.Model):
    headline = TranslatedField()
    body_text = TranslatedField(long_text=True)

    class Meta:
        verbose_name = "About Us Section"
        verbose_name_plural = "About Us Section"

    def clean(self):
        if not self.pk and AboutUsSection.objects.exists():
            raise ValidationError("Only one About Us Section is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class AboutUsImage(models.Model):
    section = models.ForeignKey(AboutUsSection, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="home/about/")
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "About Us Image"
        verbose_name_plural = "About Us Images"

    def __str__(self):
        return f"About Image #{self.order}"


# ──────────────────────────────────────────────────────────────────────────────
# FAQ
# ──────────────────────────────────────────────────────────────────────────────

class FAQSection(models.Model):
    headline = TranslatedField()

    class Meta:
        verbose_name = "FAQ Section Heading"
        verbose_name_plural = "FAQ Section Heading"

    def clean(self):
        if not self.pk and FAQSection.objects.exists():
            raise ValidationError("Only one FAQ Section is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class FAQ(models.Model):
    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, related_name="faqs")
    question = TranslatedField()
    answer = TranslatedField(long_text=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        q = self.question
        return q.get("en", "") if isinstance(q, dict) else str(q)


# ──────────────────────────────────────────────────────────────────────────────
# TESTIMONIALS
# ──────────────────────────────────────────────────────────────────────────────

class TestimonialsSection(models.Model):
    headline = TranslatedField()
    subtext = TranslatedField()

    class Meta:
        verbose_name = "Testimonials Section Heading"
        verbose_name_plural = "Testimonials Section Heading"

    def clean(self):
        if not self.pk and TestimonialsSection.objects.exists():
            raise ValidationError("Only one Testimonials Section is allowed.")

    def __str__(self):
        h = self.headline
        return h.get("en", "") if isinstance(h, dict) else str(h)


class Testimonial(models.Model):
    section = models.ForeignKey(TestimonialsSection, on_delete=models.CASCADE, related_name="testimonials")
    customer_name = models.CharField(max_length=100)
    review_text = TranslatedField(long_text=True)
    star_rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.customer_name} — {self.star_rating}★"