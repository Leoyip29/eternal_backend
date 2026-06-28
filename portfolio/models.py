from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from core.fields import TranslatedField


class OurWorkPage(models.Model):
    """Singleton — controls the page header for the Our Work page."""
    title = TranslatedField()
    subtitle = TranslatedField()

    class Meta:
        verbose_name = "Our Work Page"
        verbose_name_plural = "Our Work Page"

    def clean(self):
        if not self.pk and OurWorkPage.objects.exists():
            raise ValidationError("Only one Our Work Page instance is allowed.")

    def __str__(self):
        t = self.title
        return t.get("en", "") if isinstance(t, dict) else str(t)


class WorkCategory(models.Model):
    """e.g. Christian Companion, Jewish Companion, Asian/Chinese Grave, Italian Grave."""
    name = TranslatedField()
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Work Category"
        verbose_name_plural = "Work Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            en_name = self.name.get("en", "") if isinstance(self.name, dict) else str(self.name)
            self.slug = slugify(en_name)
        super().save(*args, **kwargs)

    def __str__(self):
        n = self.name
        return n.get("en", "") if isinstance(n, dict) else str(n)


class WorkItem(models.Model):
    """A single portfolio piece shown in the Our Work grid."""
    title = TranslatedField()
    category = models.ForeignKey(WorkCategory, on_delete=models.PROTECT, related_name="items")
    image = models.ImageField(upload_to="portfolio/work/")
    description = TranslatedField(long_text=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Work Item"
        verbose_name_plural = "Work Items"

    def __str__(self):
        t = self.title
        return t.get("en", "") if isinstance(t, dict) else str(t)