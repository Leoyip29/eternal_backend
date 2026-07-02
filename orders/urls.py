from django.urls import path
from .views import (
    CreateOrderView,
    OrderDetailView,
    ValidateDiscountView,
    SaveEngravingView,
    SavedAddressView,
)

urlpatterns = [
    path("",                        CreateOrderView.as_view(),      name="order-create"),
    path("<str:order_number>/",     OrderDetailView.as_view(),      name="order-detail"),
    path("discount/validate/",      ValidateDiscountView.as_view(), name="discount-validate"),
    path("engraving/",              SaveEngravingView.as_view(),    name="engraving-save"),
    path("saved-address/",          SavedAddressView.as_view(),     name="saved-address"),
]