from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Customer testimonial / review."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    reviewer_name = models.CharField(max_length=100)
    rating        = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    body          = models.TextField(help_text='The review text.')
    source        = models.CharField(
        max_length=50, blank=True,
        help_text='e.g. Google, Zomato, Walk-in',
    )
    is_approved   = models.BooleanField(
        default=False,
        help_text='Only approved reviews appear on the website.',
    )
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer_name} — {self.rating}★'
