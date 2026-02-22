from django.shortcuts import render
from menu.models import MenuItem
from reviews.models import Review


def home(request):
    featured_items = (
        MenuItem.objects.filter(featured=True, is_available=True)
        .select_related('category')[:8]
    )
    testimonials = Review.objects.filter(is_approved=True).order_by('-created_at')[:6]
    return render(request, 'core/home.html', {
        'featured_items': featured_items,
        'testimonials': testimonials,
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')
