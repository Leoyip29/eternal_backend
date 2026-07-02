from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils import get_language_from_request
from .models import Order, DeliveryDetail
from .serializers import (
    OrderCreateSerializer,
    OrderReadSerializer,
    DiscountCodeValidateSerializer,
    EngravingDetailSerializer,
    DeliveryDetailSerializer,
)


class CreateOrderView(APIView):
    """
    POST /api/orders/
    Accepts the full checkout payload in one call:
      items (with optional engraving) + discount_code + delivery details.
    Returns the created order with order_number for the confirmation screen.
    """

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save()
        lang = get_language_from_request(request)
        return Response(
            OrderReadSerializer(order, context={"request": request, "lang": lang}).data,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    """
    GET /api/orders/<order_number>/
    Returns full order detail — used for the Order Complete confirmation screen.
    """

    def get(self, request, order_number):
        try:
            order = Order.objects.prefetch_related(
                "items__product__images",
                "items__size",
                "items__color",
                "items__engraving",
            ).select_related("delivery", "payment", "discount_code").get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        lang = get_language_from_request(request)
        return Response(OrderReadSerializer(order, context={"request": request, "lang": lang}).data)


class ValidateDiscountView(APIView):
    """
    POST /api/orders/discount/validate/
    Body: { "code": "SAVE10", "subtotal": 52000 }
    Returns the discount amount if valid.
    """

    def post(self, request):
        serializer = DiscountCodeValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dc = serializer.validated_data["discount_code"]
        return Response({
            "code":            dc.code,
            "discount_type":   dc.discount_type,
            "value":           dc.value,
            "discount_amount": serializer.validated_data["discount_amount"],
            "message":         f"Discount code applied: HKS {serializer.validated_data['discount_amount']:,.0f} off",
        })


class SaveEngravingView(APIView):
    """
    POST /api/orders/engraving/
    Saves engraving details before checkout and returns an engraving_id
    that can be passed with the order items in the full checkout call.
    """

    def post(self, request):
        serializer = EngravingDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        engraving = serializer.save()
        return Response({"engraving_id": engraving.id}, status=status.HTTP_201_CREATED)


class SavedAddressView(APIView):
    """
    GET /api/orders/saved-address/?email=<email>
    Returns the last saved delivery address for a given email
    (for the 'Auto fill previous information' checkbox in the UI).
    """

    def get(self, request):
        email = request.query_params.get("email", "").strip()
        if not email:
            return Response({})

        delivery = DeliveryDetail.objects.filter(
            email=email, save_for_next_time=True
        ).order_by("-order__created_at").first()

        if not delivery:
            return Response({})

        return Response(DeliveryDetailSerializer(delivery).data)