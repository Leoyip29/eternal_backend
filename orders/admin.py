from django.contrib import admin
from django.utils.html import format_html
from .models import DiscountCode, EngravingDetail, Order, OrderItem, DeliveryDetail, PaymentRecord


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "value", "min_order_amount", "used_count", "max_uses", "expiry_date", "is_active")
    list_editable = ("is_active",)
    list_display_links = ("code",)
    list_filter = ("discount_type", "is_active")
    fieldsets = (
        ("Code",     {"fields": ("code", "is_active")}),
        ("Discount", {"fields": ("discount_type", "value", "min_order_amount")}),
        ("Limits",   {"fields": ("max_uses", "used_count", "expiry_date")}),
    )
    readonly_fields = ("used_count",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "size", "color", "quantity", "unit_price", "line_total_display", "engraving")
    fields = ("product", "size", "color", "quantity", "unit_price", "line_total_display", "engraving")

    def line_total_display(self, obj):
        return f"HKS {obj.line_total:,.0f}"
    line_total_display.short_description = "Line Total"


class DeliveryDetailInline(admin.StackedInline):
    model = DeliveryDetail
    extra = 0
    readonly_fields = ("order",)


class PaymentRecordInline(admin.StackedInline):
    model = PaymentRecord
    extra = 0
    readonly_fields = ("order", "paid_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "status_badge", "subtotal_display", "discount_amount", "total_display", "created_at")
    list_display_links = ("order_number",)
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "delivery__full_name", "delivery__email")
    readonly_fields = ("order_number", "subtotal", "shipping_cost", "discount_amount", "total", "created_at", "updated_at")
    fieldsets = (
        ("Order",    {"fields": ("order_number", "status", "discount_code")}),
        ("Totals",   {"fields": ("subtotal", "shipping_cost", "discount_amount", "total")}),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )
    inlines = [OrderItemInline, DeliveryDetailInline, PaymentRecordInline]

    def status_badge(self, obj):
        colours = {
            "pending":    "#f0ad4e",
            "confirmed":  "#5bc0de",
            "processing": "#337ab7",
            "completed":  "#5cb85c",
            "cancelled":  "#d9534f",
        }
        colour = colours.get(obj.status, "#999")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;">{}</span>',
            colour, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def subtotal_display(self, obj):
        return f"HKS {obj.subtotal:,.0f}"
    subtotal_display.short_description = "Subtotal"

    def total_display(self, obj):
        return f"HKS {obj.total:,.0f}"
    total_display.short_description = "Total"


@admin.register(EngravingDetail)
class EngravingDetailAdmin(admin.ModelAdmin):
    list_display = ("__str__", "font_choice", "created_at")
    readonly_fields = ("created_at",)