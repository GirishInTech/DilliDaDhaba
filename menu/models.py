from django.db import models


class Category(models.Model):
    """
    Top-level grouping for menu items (e.g. Starters, Main Course, Breads).
    """
    name          = models.CharField(max_length=100, unique=True)
    display_order = models.PositiveSmallIntegerField(default=0, db_index=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'
        ordering            = ['display_order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Individual dish on the menu.
    """
    category           = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='items',
    )
    name               = models.CharField(max_length=200)
    description        = models.TextField(blank=True)
    veg                = models.BooleanField(
        default=True,
        help_text='Green dot = veg, Red dot = non-veg',
    )
    egg                = models.BooleanField(
        default=False,
        help_text='Contains egg but no meat (e.g. egg curry, egg bhurji). Set veg=False when this is True.',
    )

    # Prices — at least one must be filled in
    price_half         = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text='Half portion price (₹)',
    )
    price_full         = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text='Full portion price (₹)',
    )
    price_regular      = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text='Regular / single price (₹)',
    )

    image              = models.ImageField(
        upload_to='menu/',
        null=True, blank=True,
        help_text='Upload a square food photo (min 600×600 px)',
    )

    featured           = models.BooleanField(
        default=False,
        help_text='Show on homepage featured section',
    )
    needs_verification = models.BooleanField(
        default=False,
        help_text='Flag item for chef / admin review',
    )
    is_available       = models.BooleanField(
        default=True,
        help_text='Uncheck to hide item from the public menu',
    )

    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering            = ['category__display_order', 'name']
        indexes             = [
            models.Index(fields=['featured']),
            models.Index(fields=['is_available']),
        ]

    def __str__(self):
        return f'{self.name} [{self.category.name}]'

    # ------------------------------------------------------------------
    # Convenience helpers (used in templates / serializers)
    # ------------------------------------------------------------------
    @property
    def display_price(self) -> str:
        """Return a human-friendly price string."""
        parts = []
        if self.price_regular is not None:
            parts.append(f'₹{self.price_regular}')
        else:
            if self.price_half is not None:
                parts.append(f'Half ₹{self.price_half}')
            if self.price_full is not None:
                parts.append(f'Full ₹{self.price_full}')
        return '  /  '.join(parts) if parts else 'Price on request'

    @property
    def has_half_full(self) -> bool:
        return self.price_half is not None and self.price_full is not None
