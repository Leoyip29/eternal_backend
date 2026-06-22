from django.db import models
from django.core.exceptions import ValidationError


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Gravestone Memorials")
    logo = models.ImageField(upload_to="cms/", blank=True, null=True)
    favicon = models.ImageField(upload_to="cms/", blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    copyright_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Only one Site Settings instance is allowed.")

    def __str__(self):
        return self.site_name


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("whatsapp", "WhatsApp"),
        ("twitter", "Twitter / X"),
        ("linkedin", "LinkedIn"),
    ]

    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.ImageField(upload_to="cms/social/", blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.get_platform_display()


class FooterColumn(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Footer Column"
        verbose_name_plural = "Footer Columns"

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    column = models.ForeignKey(FooterColumn, on_delete=models.CASCADE, related_name="links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=0)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return f"{self.column.title} — {self.label}"


class NewsletterSection(models.Model):
    headline = models.CharField(max_length=200, default="Join Our Newsletter")
    subtext = models.TextField(blank=True)
    button_label = models.CharField(max_length=50, default="Subscribe")
    background_image = models.ImageField(upload_to="cms/newsletter/", blank=True, null=True)

    class Meta:
        verbose_name = "Newsletter Section"
        verbose_name_plural = "Newsletter Section"

    def clean(self):
        if not self.pk and NewsletterSection.objects.exists():
            raise ValidationError("Only one Newsletter Section instance is allowed.")

    def __str__(self):
        return self.headline