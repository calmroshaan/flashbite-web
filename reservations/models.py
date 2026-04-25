import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from stores.models import Store
from bags.models import SurpriseBag

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('picked_up', 'Picked Up'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bag = models.ForeignKey(SurpriseBag, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pickup_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reservation_code = models.CharField(max_length=8, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            self.reservation_code = uuid.uuid4().hex[:8].upper()
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(self.reservation_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.qr_code.save(f'qr_{self.reservation_code}.png', File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.reservation_code}"