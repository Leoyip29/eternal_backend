from rest_framework import serializers
from django.utils import timezone
from core.serializers import TranslatedCharField
from catalogue.models import Product, ProductSize, ProductColor
from catalogue.serializers import ProductListSerializer
from .models import DiscountCode, EngravingDetail, Order, OrderItem, DeliveryDetail, PaymentRecord


# ── Engraving ─────────────────────────────────────────────────────────────────

class EngravingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngravingDetail
        fields = ("id", "line_1", "line_2", "line_3", "line_4", "font_choice", "photo", "special_notes")


# ── Discount ──────────────────────────────────────────────────────────────────

class DiscountCodeValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        try:
            dc = DiscountCode.objects.get(code__iexact=data["code"])
        except DiscountCode.DoesNotExist:
            raise serializers.ValidationError({"code": "Invalid discount code."})

        valid, reason = dc.is_valid()
        if not valid:
            raise serializers.ValidationError({"code": reason})

        if data["subtotal"] < dc.min_order_amount:
            raise serializers.ValidationError({
                "code": f"Minimum order amount for this code is HKS {dc.min_order_amount:,.0f}."
            })

        data["discount_code"] = dc
        data["discount_amount"] = dc.calculate_discount(data["subtotal"])
        return data


# ── Order Items ───────────────────────────────────────────────────────────────

class OrderItemInputSerializer(serializers.Serializer):
    """Validates one line item sent from the frontend during order creation."""
    product_slug = serializers.SlugField()
    size_id = serializers.IntegerField(required=False, allow_null=True)
    color_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)
    engraving = EngravingDetailSerializer(required=False, allow_null=True)

    def validate_product_slug(self, value):
        try:
            return Product.objects.get(slug=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product '{value}' not found.")

    def validate(self, data):
        product = data["product_slug"]   # already resolved to Product object
        size_id = data.get("size_id")
        color_id = data.get("color_id")

        if size_id:
            try:
                data["size"] = ProductSize.objects.get(id=size_id, product=product)
            except ProductSize.DoesNotExist:
                raise serializers.ValidationError({"size_id": "Invalid size for this product."})
        else:
            data["size"] = None

        if color_id:
            try:
                data["color"] = ProductColor.objects.get(id=color_id, product=product)
            except ProductColor.DoesNotExist:
                raise serializers.ValidationError({"color_id": "Invalid color for this product."})
        else:
            data["color"] = None

        data["product"] = product
        return data


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    size_label = serializers.SerializerMethodField()
    color_name = serializers.SerializerMethodField()
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    engraving = EngravingDetailSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "size_label", "color_name", "quantity", "unit_price", "line_total", "engraving")

    def get_size_label(self, obj):
        if not obj.size:
            return None
        lbl = obj.size.label
        lang = self.context.get("lang", "en")
        return lbl.get(lang) or lbl.get("en", "") if isinstance(lbl, dict) else str(lbl)

    def get_color_name(self, obj):
        if not obj.color:
            return None
        n = obj.color.name
        lang = self.context.get("lang", "en")
        return n.get(lang) or n.get("en", "") if isinstance(n, dict) else str(n)


# ── Delivery ──────────────────────────────────────────────────────────────────

class DeliveryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDetail
        exclude = ("order",)


# ── Payment ───────────────────────────────────────────────────────────────────

class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = ("method", "status", "paid_at", "amount")


# ── Order Read ────────────────────────────────────────────────────────────────

class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    delivery = DeliveryDetailSerializer(read_only=True)
    payment = PaymentRecordSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "order_number", "status", "status_display",
            "subtotal", "shipping_cost", "discount_amount", "total",
            "items", "delivery", "payment",
            "created_at",
        )


# ── Order Create ──────────────────────────────────────────────────────────────

class OrderCreateSerializer(serializers.Serializer):
    """
    Full checkout payload — received in one POST.

    {
      "items": [
        {
          "product_slug": "sapphire-shimmer-estate-columbarium",
          "size_id": 2,
          "color_id": 1,
          "quantity": 1,
          "engraving": {
            "line_1": "In Loving Memory",
            "line_2": "John Smith",
            "line_3": "1945 – 2024",
            "line_4": "",
            "font_choice": "classic",
            "special_notes": "Gold colour text please"
          }
        }
      ],
      "discount_code": "SAVE10",
      "delivery": {
        "country": "Hong Kong",
        "full_name": "Jane Smith",
        "address_line_1": "123 Main Street",
        "address_line_2": "Flat 5A",
        "city": "Hong Kong",
        "zip_code": "000000",
        "email": "jane@example.com",
        "whatsapp_number": "+852 9876 5432",
        "payment_method": "card",
        "save_for_next_time": true
      }
    }
    """
    items = OrderItemInputSerializer(many=True)
    discount_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    delivery = DeliveryDetailSerializer()

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def validate(self, data):
        # Resolve discount code if provided
        code_str = data.get("discount_code", "").strip()
        data["resolved_discount"] = None
        if code_str:
            try:
                dc = DiscountCode.objects.get(code__iexact=code_str)
                valid, reason = dc.is_valid()
                if not valid:
                    raise serializers.ValidationError({"discount_code": reason})
                data["resolved_discount"] = dc
            except DiscountCode.DoesNotExist:
                raise serializers.ValidationError({"discount_code": "Invalid discount code."})
        return data

    def create(self, validated_data):
        items_data = validated_data["items"]
        delivery_data = validated_data["delivery"]
        discount = validated_data.get("resolved_discount")

        # 1. Create order shell
        order = Order.objects.create(discount_code=discount)

        # 2. Create items
        for item_data in items_data:
            product = item_data["product"]
            engraving_data = item_data.get("engraving")
            engraving = None
            if engraving_data:
                engraving = EngravingDetail.objects.create(**engraving_data)

            OrderItem.objects.create(
                order=order,
                product=product,
                size=item_data.get("size"),
                color=item_data.get("color"),
                quantity=item_data["quantity"],
                unit_price=product.effective_price,
                engraving=engraving,
            )

        # 3. Recalculate totals
        order.refresh_from_db()
        order.recalculate_totals()
        order.save()

        # 4. Create delivery
        DeliveryDetail.objects.create(order=order, **delivery_data)

        # 5. Create payment record
        PaymentRecord.objects.create(
            order=order,
            method=delivery_data["payment_method"],
            amount=order.total,
            status=PaymentRecord.PENDING,
        )

        # 6. Mark discount as used
        if discount:
            discount.used_count += 1
            discount.save(update_fields=["used_count"])

        return order