from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Store(models.Model):
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('bakery', 'Bakery'),
        ('cafe', 'Cafe'),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    city = models.CharField(max_length=100)
    address = models.TextField()
    cover_image = models.ImageField(upload_to='store_covers/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) # Converts "Ali Bakery" to "ali-bakery" for clean URLs
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name