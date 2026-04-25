from django.db import models
from stores.models import Store

class SurpriseBag(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='bags')
    title = models.CharField(max_length=255)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_total = models.IntegerField()
    quantity_left = models.IntegerField()
    pickup_start = models.TimeField()
    pickup_end = models.TimeField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='bag_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.store.name}"