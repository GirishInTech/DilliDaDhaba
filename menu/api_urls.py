"""
URL routes that live under /api/
"""
from django.urls import path
from .api_views import category_list, menu_list, featured_items

urlpatterns = [
    path('categories', category_list,  name='api-categories'),
    path('menu',       menu_list,       name='api-menu'),
    path('featured',   featured_items,  name='api-featured'),
]
