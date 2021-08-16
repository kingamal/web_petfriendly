from django.db import models

# Create your models here.

ACTIVE = 1
DISABLED = 0
CHOICES = [
    (DISABLED, 'Disabled'),
    (ACTIVE, 'Active')
]

class HotelsLocation(models.Model):
    hotel_name = models.CharField(max_length=120)
    city = models.CharField(max_length=64)
    url_hotel = models.CharField(max_length=1024)
    latitude = models.DecimalField(decimal_places=12, max_digits=15)
    longitude = models.DecimalField(decimal_places=12, max_digits=15)
    active = models.SmallIntegerField(default=1, choices=CHOICES)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    def __str__(self):
        return "Hotel: {}".format(self.hotel_name)
