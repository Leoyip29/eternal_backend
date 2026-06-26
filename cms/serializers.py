from rest_framework import serializers
from core.serializers import TranslatedCharField
from .models import SiteSettings, SocialLink, FooterColumn, FooterLink, NewsletterSection


class SiteSettingsSerializer(serializers.ModelSerializer):
    copyright_text = TranslatedCharField()

    class Meta:
        model = SiteSettings
        fields = "__all__"


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_label = serializers.CharField(source="get_platform_display", read_only=True)

    class Meta:
        model = SocialLink
        fields = ("id", "platform", "platform_label", "url", "icon", "order")


class FooterLinkSerializer(serializers.ModelSerializer):
    label = TranslatedCharField()

    class Meta:
        model = FooterLink
        fields = ("id", "label", "url", "order", "open_in_new_tab")


class FooterColumnSerializer(serializers.ModelSerializer):
    title = TranslatedCharField()
    links = FooterLinkSerializer(many=True, read_only=True)

    class Meta:
        model = FooterColumn
        fields = ("id", "title", "order", "links")


class NewsletterSectionSerializer(serializers.ModelSerializer):
    headline = TranslatedCharField()
    subtext = TranslatedCharField()
    button_label = TranslatedCharField()

    class Meta:
        model = NewsletterSection
        fields = "__all__"