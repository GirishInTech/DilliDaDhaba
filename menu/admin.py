from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'display_order', 'item_count', 'created_at')
    list_editable = ('display_order',)
    ordering      = ('display_order',)
    search_fields = ('name',)

    @admin.display(description='Items')
    def item_count(self, obj):
        return obj.items.count()


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'veg_badge',
        'price_display',
        'featured',
        'is_available',
        'needs_verification',
        'image_preview',
    )
    list_filter  = (
        'category',
        'veg',
        'featured',
        'is_available',
        'needs_verification',
    )
    list_editable = ('featured', 'is_available')
    search_fields = ('name', 'description')
    autocomplete_fields = ('category',)
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'name', 'description', 'veg'),
        }),
        ('Pricing', {
            'fields': ('price_regular', 'price_half', 'price_full'),
            'description': 'Fill price_regular for single-portion items, '
                           'or price_half + price_full for half/full portions.',
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
        }),
        ('Flags', {
            'fields': ('featured', 'is_available', 'needs_verification'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Type', ordering='veg')
    def veg_badge(self, obj):
        color = '#16a34a' if obj.veg else '#dc2626'
        label = '● Veg' if obj.veg else '● Non-Veg'
        return format_html('<span style="color:{}">{}</span>', color, label)

    @admin.display(description='Price')
    def price_display(self, obj):
        return obj.display_price

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'
