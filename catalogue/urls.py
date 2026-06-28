from django.urls import path
from .views import (
    CataloguePageView,
    CatalogueView,
    CategoryListView,
    MaterialListView,
    ProductListView,
    ProductDetailView,
    RelatedProductsView,
)

urlpatterns = [
    path("page/",                         CataloguePageView.as_view(),   name="catalogue-page"),
    path("",                              CatalogueView.as_view(),       name="catalogue"),
    path("categories/",                   CategoryListView.as_view(),    name="categories"),
    path("materials/",                    MaterialListView.as_view(),    name="materials"),
    path("products/",                     ProductListView.as_view(),     name="product-list"),
    path("products/<slug:slug>/",         ProductDetailView.as_view(),   name="product-detail"),
    path("products/<slug:slug>/related/", RelatedProductsView.as_view(), name="product-related"),
]