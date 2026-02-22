from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('reviewer_name', 'rating', 'source', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter   = ('is_approved', 'rating', 'source')
    search_fields = ('reviewer_name', 'body')
    readonly_fields = ('created_at',)
    actions = ['approve_reviews']

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
