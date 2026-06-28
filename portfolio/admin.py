from django.contrib import admin
from .models import OurWorkPage, WorkCategory, WorkItem


@admin.register(OurWorkPage)
class OurWorkPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Page Header", {"fields": ("title", "subtitle")}),
    )

    def has_add_permission(self, request):
        return not OurWorkPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class WorkItemInline(admin.TabularInline):
    model = WorkItem
    extra = 1
    fields = ("title", "image", "description", "order", "is_active")


@admin.register(WorkCategory)
class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("__str__",)
    fieldsets = (
        ("Identity", {"fields": ("name", "slug")}),
        ("Display",  {"fields": ("order", "is_active")}),
    )
    inlines = [WorkItemInline]


@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("__str__",)
    list_filter = ("category", "is_active")
    fieldsets = (
        ("Content", {"fields": ("title", "category", "image", "description")}),
        ("Display", {"fields": ("order", "is_active")}),
    )