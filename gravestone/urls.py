from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cms/", include("cms.urls")),
    path("api/home/", include("home.urls")),
    path("api/catalogue/", include("catalogue.urls")),
    path("api/portfolio/", include("portfolio.urls")),
    path("api/orders/",    include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)