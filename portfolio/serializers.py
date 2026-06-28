from rest_framework import serializers
from core.serializers import TranslatedCharField
from .models import OurWorkPage, WorkCategory, WorkItem


class OurWorkPageSerializer(serializers.ModelSerializer):
    title = TranslatedCharField()
    subtitle = TranslatedCharField()

    class Meta:
        model = OurWorkPage
        fields = "__all__"


class WorkCategorySerializer(serializers.ModelSerializer):
    name = TranslatedCharField()

    class Meta:
        model = WorkCategory
        fields = ("id", "name", "slug", "order")


class WorkItemSerializer(serializers.ModelSerializer):
    title = TranslatedCharField()
    description = TranslatedCharField()
    category = WorkCategorySerializer(read_only=True)

    class Meta:
        model = WorkItem
        fields = ("id", "title", "category", "image", "description", "order")


class WorkCategoryWithItemsSerializer(serializers.ModelSerializer):
    """Category with all its active work items nested — used for the filtered gallery view."""
    name = TranslatedCharField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = WorkCategory
        fields = ("id", "name", "slug", "order", "items")

    def get_items(self, obj):
        active = obj.items.filter(is_active=True)
        return WorkItemSerializer(active, many=True, context=self.context).data