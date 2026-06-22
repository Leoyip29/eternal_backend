from django.urls import path
from .views import (
    SiteSettingsView,
    SocialLinksView,
    FooterView,
    NewsletterSectionView,
    SiteConfigView,
)

urlpatterns = [
    path("site-settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("social-links/", SocialLinksView.as_view(), name="social-links"),
    path("footer/", FooterView.as_view(), name="footer"),
    path("newsletter-section/", NewsletterSectionView.as_view(), name="newsletter-section"),
    path("site-config/", SiteConfigView.as_view(), name="site-config"),
]