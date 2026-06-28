from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import OurWorkPage, WorkCategory, WorkItem
from .serializers import (
    OurWorkPageSerializer,
    WorkCategorySerializer,
    WorkCategoryWithItemsSerializer,
    WorkItemSerializer,
)


class OurWorkPageView(APIView):
    """Singleton page header — title and subtitle."""

    def get(self, request):
        obj = OurWorkPage.objects.first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        return Response(OurWorkPageSerializer(obj, context={"request": request}).data)


class WorkCategoryListView(ListAPIView):
    """Flat list of active categories — used to populate the filter tabs."""
    queryset = WorkCategory.objects.filter(is_active=True)
    serializer_class = WorkCategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}


class OurWorkView(APIView):
    """
    Full portfolio gallery.

    Without filter:  returns all categories with their work items nested.
    ?category=<slug>: returns only items for that category (flat list).
    """

    def get(self, request):
        ctx = {"request": request}
        slug = request.query_params.get("category")

        if slug:
            # Return flat list of items for a single category
            try:
                category = WorkCategory.objects.get(slug=slug, is_active=True)
            except WorkCategory.DoesNotExist:
                return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

            items = WorkItem.objects.filter(category=category, is_active=True)
            return Response({
                "category": WorkCategorySerializer(category, context=ctx).data,
                "items": WorkItemSerializer(items, many=True, context=ctx).data,
            })

        # Return all categories with nested items
        categories = WorkCategory.objects.filter(is_active=True).prefetch_related("items")
        return Response(WorkCategoryWithItemsSerializer(categories, many=True, context=ctx).data)


class OurWorkFullPageView(APIView):
    """
    Single endpoint that returns everything the Our Work page needs:
    page header + all categories + all items.
    """

    def get(self, request):
        ctx = {"request": request}
        page = OurWorkPage.objects.first()
        categories = WorkCategory.objects.filter(is_active=True).prefetch_related("items")

        return Response({
            "page": OurWorkPageSerializer(page, context=ctx).data if page else {},
            "gallery": WorkCategoryWithItemsSerializer(categories, many=True, context=ctx).data,
        })