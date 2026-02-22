"""
Template-rendered views for the /menu/ page.
"""
from django.shortcuts import render
from .models import Category


def menu_page(request):
    """Public menu page — renders a full menu driven by the JS/API."""
    categories = Category.objects.all().order_by('display_order')
    return render(request, 'menu/menu.html', {'categories': categories})
