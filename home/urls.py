from django.urls import path
from .views import (
    HomePageView,
    HeroView,
    FeaturedProductsView,
    StoneGalleryView,
    AboutUsView,
    FAQView,
    TestimonialsView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("hero/", HeroView.as_view(), name="hero"),
    path("featured-products/", FeaturedProductsView.as_view(), name="featured-products"),
    path("stone-gallery/", StoneGalleryView.as_view(), name="stone-gallery"),
    path("about/", AboutUsView.as_view(), name="about"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("testimonials/", TestimonialsView.as_view(), name="testimonials"),
]