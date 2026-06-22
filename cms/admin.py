from django.contrib import admin
from .models import SiteSettings, SocialLink, FooterColumn, FooterLink, NewsletterSection


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "logo", "favicon")}),
        ("Contact", {"fields": ("phone", "email", "whatsapp_number", "address")}),
        ("Footer", {"fields": ("copyright_text",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("platform",)


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ("label", "url", "order", "open_in_new_tab")


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    inlines = [FooterLinkInline]


@admin.register(NewsletterSection)
class NewsletterSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("headline", "subtext", "button_label", "background_image")}),
    )

    def has_add_permission(self, request):
        return not NewsletterSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False