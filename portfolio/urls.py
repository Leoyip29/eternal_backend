from django.urls import path
from .views import (
    OurWorkPageView,
    WorkCategoryListView,
    OurWorkView,
    OurWorkFullPageView,
)

urlpatterns = [
    path("",             OurWorkFullPageView.as_view(),  name="our-work-full"),
    path("page/",        OurWorkPageView.as_view(),      name="our-work-page"),
    path("categories/",  WorkCategoryListView.as_view(), name="work-categories"),
    path("gallery/",     OurWorkView.as_view(),          name="our-work-gallery"),
]