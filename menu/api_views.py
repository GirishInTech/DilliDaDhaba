"""
DRF API views for the public-facing Menu API.
All endpoints are read-only and unauthenticated.
"""
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Category, MenuItem
from .serializers import (
    CategoryListSerializer,
    MenuItemSerializer,
)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def category_list(request):
    """GET /api/categories — list all categories ordered by display_order."""
    qs = Category.objects.all()
    serializer = CategoryListSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def menu_list(request):
    """
    GET /api/menu              — full available menu
    GET /api/menu?category=<id> — items filtered by category id
    GET /api/menu?veg=true      — veg-only items
    """
    qs = (
        MenuItem.objects.filter(is_available=True)
        .select_related('category')
        .order_by('category__display_order', 'name')
    )

    category_id = request.query_params.get('category')
    if category_id:
        qs = qs.filter(category_id=category_id)

    veg_param = request.query_params.get('veg')
    if veg_param is not None:
        qs = qs.filter(veg=veg_param.lower() == 'true')

    serializer = MenuItemSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def featured_items(request):
    """GET /api/featured — items marked as featured and available."""
    qs = (
        MenuItem.objects.filter(featured=True, is_available=True)
        .select_related('category')
    )
    serializer = MenuItemSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)
