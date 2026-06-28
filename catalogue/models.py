from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from core.fields import TranslatedField


class CataloguePage(models.Model):
    """Singleton — controls the hero banner on the Stone Catalogue page."""
    hero_title = TranslatedField()
    hero_subtitle = TranslatedField()
    hero_background_image = models.ImageField(upload_to="catalogue/hero/", blank=True, null=True)

    class Meta:
        verbose_name = "Catalogue Page"
        verbose_name_plural = "Catalogue Page"

    def clean(self):
        if not self.pk and CataloguePage.objects.exists():
            raise ValidationError("Only one Catalogue Page instance is allowed.")

    def __str__(self):
        t = self.hero_title
        return t.get("en", "") if isinstance(t, dict) else str(t)


class Category(models.Model):
    name = TranslatedField()
    slug = models.SlugField(max_length=100, unique=True)
    description = TranslatedField(long_text=True)
    image = models.ImageField(upload_to="catalogue/categories/", blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            en_name = self.name.get("en", "") if isinstance(self.name, dict) else str(self.name)
            self.slug = slugify(en_name)
        super().save(*args, **kwargs)

    def __str__(self):
        n = self.name
        return n.get("en", "") if isinstance(n, dict) else str(n)


class Material(models.Model):
    name = TranslatedField()
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["slug"]
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def save(self, *args, **kwargs):
        if not self.slug:
            en_name = self.name.get("en", "") if isinstance(self.name, dict) else str(self.name)
            self.slug = slugify(en_name)
        super().save(*args, **kwargs)

    def __str__(self):
        n = self.name
        return n.get("en", "") if isinstance(n, dict) else str(n)


class Product(models.Model):
    name = TranslatedField()
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")

    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    short_description = TranslatedField()
    full_description = TranslatedField(long_text=True)
    shipping_info = TranslatedField(long_text=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            en_name = self.name.get("en", "") if isinstance(self.name, dict) else str(self.name)
            self.slug = slugify(en_name)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price else self.price

    def __str__(self):
        n = self.name
        return n.get("en", "") if isinstance(n, dict) else str(n)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="catalogue/products/")
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product} — Image #{self.order}"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")
    label = TranslatedField()
    dimensions = models.CharField(max_length=100, blank=True, help_text='e.g. "200 x 60 cm"')
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"

    def __str__(self):
        lbl = self.label
        lbl_en = lbl.get("en", "") if isinstance(lbl, dict) else str(lbl)
        return f"{self.product} — {lbl_en}"


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    name = TranslatedField()
    hex_code = models.CharField(max_length=7, blank=True, help_text='e.g. "#1a1a1a"')
    swatch_image = models.ImageField(upload_to="catalogue/swatches/", blank=True, null=True)
    is_default = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"

    def __str__(self):
        n = self.name
        n_en = n.get("en", "") if isinstance(n, dict) else str(n)
        return f"{self.product} — {n_en}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    customer_name = models.CharField(max_length=100)
    review_text = TranslatedField(long_text=True)
    star_rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"{self.product} — {self.customer_name} ({self.star_rating}★)"