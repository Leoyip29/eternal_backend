from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from orders.models import (
    DiscountCode, EngravingDetail, Order,
    OrderItem, DeliveryDetail, PaymentRecord,
)
from catalogue.models import Product, ProductSize, ProductColor


class Command(BaseCommand):
    help = "Seed Phase 5 orders data: discount codes + one sample order"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing data.")

    def handle(self, *args, **kwargs):
        force = kwargs["force"]
        self.seed_discount_codes(force)
        self.seed_sample_order(force)
        self.stdout.write(self.style.SUCCESS("\nPhase 5 orders data seeded successfully."))

    # ── Discount Codes ────────────────────────────────────────────────────────

    def seed_discount_codes(self, force):
        if DiscountCode.objects.exists() and not force:
            self.stdout.write("  DiscountCodes exist — skipping.")
            return

        DiscountCode.objects.all().delete()
        codes = [
            {
                "code": "WELCOME10",
                "discount_type": "percent",
                "value": 10,
                "min_order_amount": 0,
                "max_uses": None,
                "expiry_date": date(2026, 12, 31),
                "is_active": True,
            },
            {
                "code": "SAVE5000",
                "discount_type": "fixed",
                "value": 5000,
                "min_order_amount": 30000,
                "max_uses": 100,
                "expiry_date": date(2026, 12, 31),
                "is_active": True,
            },
            {
                "code": "MEMORIAL15",
                "discount_type": "percent",
                "value": 15,
                "min_order_amount": 50000,
                "max_uses": 50,
                "expiry_date": date(2026, 12, 31),
                "is_active": True,
            },
            {
                "code": "FAMILY2000",
                "discount_type": "fixed",
                "value": 2000,
                "min_order_amount": 10000,
                "max_uses": None,
                "expiry_date": None,
                "is_active": True,
            },
            {
                "code": "EXPIRED",
                "discount_type": "percent",
                "value": 20,
                "min_order_amount": 0,
                "max_uses": None,
                "expiry_date": date(2024, 1, 1),
                "is_active": True,
            },
        ]
        for c in codes:
            DiscountCode.objects.create(**c)
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(codes)} DiscountCodes created."))

    # ── Sample Order ──────────────────────────────────────────────────────────

    def seed_sample_order(self, force):
        if Order.objects.exists() and not force:
            self.stdout.write("  Sample Order exists — skipping.")
            return

        Order.objects.all().delete()

        try:
            product = Product.objects.get(slug="sapphire-shimmer-estate-columbarium")
            size = ProductSize.objects.filter(product=product, is_default=True).first()
            color = ProductColor.objects.filter(product=product, is_default=True).first()
        except Product.DoesNotExist:
            self.stdout.write(self.style.WARNING("  Product not found — skipping sample order. Run seed_catalogue first."))
            return

        discount = DiscountCode.objects.get(code="WELCOME10")

        # 1. Create order
        order = Order.objects.create(
            order_number="ORD-SAMPLE01",
            status=Order.CONFIRMED,
            discount_code=discount,
        )

        # 2. Engraving
        engraving = EngravingDetail.objects.create(
            line_1="In Loving Memory",
            line_2="John Smith",
            line_3="1945 – 2024",
            line_4="Forever in Our Hearts",
            font_choice="classic",
            special_notes="Please use gold colour for all text.",
        )

        # 3. Order item
        OrderItem.objects.create(
            order=order,
            product=product,
            size=size,
            color=color,
            quantity=1,
            unit_price=product.effective_price,
            engraving=engraving,
        )

        # 4. Recalculate totals
        order.recalculate_totals()
        order.save()

        # 5. Delivery
        DeliveryDetail.objects.create(
            order=order,
            country="Hong Kong",
            full_name="Jane Smith",
            address_line_1="123 Memorial Lane",
            address_line_2="Flat 5A",
            city="Kowloon",
            zip_code="000000",
            email="jane.smith@example.com",
            whatsapp_number="+852 9876 5432",
            payment_method=DeliveryDetail.CARD,
            save_for_next_time=True,
        )

        # 6. Payment
        PaymentRecord.objects.create(
            order=order,
            method=DeliveryDetail.CARD,
            amount=order.total,
            status=PaymentRecord.PAID,
            paid_at=timezone.now(),
            reference="PAYME-REF-SAMPLE01",
        )

        # 7. Mark discount used
        discount.used_count += 1
        discount.save(update_fields=["used_count"])

        self.stdout.write(self.style.SUCCESS(
            f"  ✓ Sample order {order.order_number} created — "
            f"Subtotal: HKS {order.subtotal:,.0f} | "
            f"Discount: HKS {order.discount_amount:,.0f} | "
            f"Total: HKS {order.total:,.0f}"
        ))