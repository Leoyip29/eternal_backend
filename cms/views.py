from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SiteSettings, SocialLink, FooterColumn, NewsletterSection
from .serializers import (
    SiteSettingsSerializer,
    SocialLinkSerializer,
    FooterColumnSerializer,
    NewsletterSectionSerializer,
)


class SiteSettingsView(APIView):
    def get(self, request):
        obj = SiteSettings.objects.first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        return Response(SiteSettingsSerializer(obj, context={"request": request}).data)


class SocialLinksView(APIView):
    def get(self, request):
        qs = SocialLink.objects.filter(is_active=True)
        return Response(SocialLinkSerializer(qs, many=True, context={"request": request}).data)


class FooterView(APIView):
    def get(self, request):
        columns = FooterColumn.objects.prefetch_related("links").all()
        return Response(FooterColumnSerializer(columns, many=True, context={"request": request}).data)


class NewsletterSectionView(APIView):
    def get(self, request):
        obj = NewsletterSection.objects.first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        return Response(NewsletterSectionSerializer(obj, context={"request": request}).data)


class SiteConfigView(APIView):
    """Single endpoint that returns all global site config in one call."""

    def get(self, request):
        ctx = {"request": request}
        settings_obj = SiteSettings.objects.first()
        social_qs = SocialLink.objects.filter(is_active=True)
        footer_qs = FooterColumn.objects.prefetch_related("links").all()
        newsletter_obj = NewsletterSection.objects.first()

        return Response(
            {
                "site_settings": SiteSettingsSerializer(settings_obj, context=ctx).data if settings_obj else {},
                "social_links": SocialLinkSerializer(social_qs, many=True, context=ctx).data,
                "footer": FooterColumnSerializer(footer_qs, many=True, context=ctx).data,
                "newsletter_section": NewsletterSectionSerializer(newsletter_obj, context=ctx).data if newsletter_obj else {},
            }
        )
