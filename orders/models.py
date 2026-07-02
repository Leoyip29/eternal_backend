import uuid
from django.db import models
from django.core.validators import MinValueValidator
from catalogue.models import Product, ProductSize, ProductColor


def generate_order_number():
    return "ORD-" + uuid.uuid4().hex[:8].upper()


# ──────────────────────────────────────────────────────────────────────────────
# DISCOUNT CODE
# ──────────────────────────────────────────────────────────────────────────────

class DiscountCode(models.Model):
    PERCENT = "percent"
    FIXED = "fixed"
    DISCOUNT_TYPE_CHOICES = [
        (PERCENT, "Percentage (%)"),
        (FIXED,   "Fixed Amount (HKD)"),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank for unlimited uses.")
    used_count = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Discount Code"
        verbose_name_plural = "Discount Codes"

    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False, "This discount code is inactive."
        if self.expiry_date and self.expiry_date < timezone.now().date():
            return False, "This discount code has expired."
        if self.max_uses and self.used_count >= self.max_uses:
            return False, "This discount code has reached its usage limit."
        return True, None

    def calculate_discount(self, subtotal):
        if self.discount_type == self.PERCENT:
            return round(subtotal * self.value / 100, 2)
        return min(self.value, subtotal)

    def __str__(self):
        return f"{self.code} ({self.get_discount_type_display()}: {self.value})"


# ──────────────────────────────────────────────────────────────────────────────
# ENGRAVING DETAIL
# ──────────────────────────────────────────────────────────────────────────────

class EngravingDetail(models.Model):
    FONT_CHOICES = [
        ("classic",    "Classic Serif"),
        ("modern",     "Modern Sans-Serif"),
        ("script",     "Elegant Script"),
        ("chinese",    "Chinese Traditional"),
        ("block",      "Block Letter"),
    ]

    line_1 = models.CharField(max_length=100, blank=True)
    line_2 = models.CharField(max_length=100, blank=True)
    line_3 = models.CharField(max_length=100, blank=True)
    line_4 = models.CharField(max_length=100, blank=True)
    font_choice = models.CharField(max_length=20, choices=FONT_CHOICES, default="classic")
    photo = models.ImageField(upload_to="orders/engraving/", blank=True, null=True)
    special_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Engraving Detail"
        verbose_name_plural = "Engraving Details"

    def __str__(self):
        return f"Engraving: {self.line_1} {self.line_2}".strip()


# ──────────────────────────────────────────────────────────────────────────────
# ORDER
# ──────────────────────────────────────────────────────────────────────────────

class Order(models.Model):
    PENDING    = "pending"
    CONFIRMED  = "confirmed"
    PROCESSING = "processing"
    COMPLETED  = "completed"
    CANCELLED  = "cancelled"

    STATUS_CHOICES = [
        (PENDING,    "Pending"),
        (CONFIRMED,  "Confirmed"),
        (PROCESSING, "Processing"),
        (COMPLETED,  "Completed"),
        (CANCELLED,  "Cancelled"),
    ]

    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="orders"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def recalculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items.all())
        if self.discount_code:
            self.discount_amount = self.discount_code.calculate_discount(self.subtotal)
        else:
            self.discount_amount = 0
        self.total = max(self.subtotal - self.discount_amount + self.shipping_cost, 0)

    def __str__(self):
        return f"{self.order_number} — {self.get_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    engraving = models.OneToOneField(
        EngravingDetail, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="order_item"
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    @property
    def line_total(self):
        size_mod = self.size.price_modifier if self.size else 0
        return (self.unit_price + size_mod) * self.quantity

    def __str__(self):
        return f"{self.order.order_number} — {self.product}"


# ──────────────────────────────────────────────────────────────────────────────
# DELIVERY DETAIL
# ──────────────────────────────────────────────────────────────────────────────

class DeliveryDetail(models.Model):
    CARD = "card"
    COD  = "cod"
    PAYMENT_CHOICES = [
        (CARD, "Debit / Credit Card (PayMe)"),
        (COD,  "Cash on Delivery (COD)"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    country = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=CARD)
    save_for_next_time = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Delivery Detail"
        verbose_name_plural = "Delivery Details"

    def __str__(self):
        return f"{self.order.order_number} — {self.full_name}"


# ──────────────────────────────────────────────────────────────────────────────
# PAYMENT RECORD
# ──────────────────────────────────────────────────────────────────────────────

class PaymentRecord(models.Model):
    PENDING   = "pending"
    PAID      = "paid"
    FAILED    = "failed"
    REFUNDED  = "refunded"

    STATUS_CHOICES = [
        (PENDING,  "Pending"),
        (PAID,     "Paid"),
        (FAILED,   "Failed"),
        (REFUNDED, "Refunded"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=10)
    reference = models.CharField(max_length=100, blank=True, help_text="PayMe transaction reference")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Payment Record"
        verbose_name_plural = "Payment Records"

    def __str__(self):
        return f"{self.order.order_number} — {self.get_status_display()} ({self.method})"