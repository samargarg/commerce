from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024, blank=True)
    basePrice = models.DecimalField(max_digits=7, decimal_places=2)
    photo = models.URLField(blank=True)
    options=[
        'fashion',
        'appliances',
        'automotive',
        'collectibles',
        'electronics',
        'furniture',
        'kitchen',
        'jewelry',
        'software',
        'toys'
    ]
    category = models.CharField(max_length=64, choices=[(option, option.capitalize()) for option in options])
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bids")
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.amount} On {self.listing} By {self.user}"

class Comment(models.Model):
    content = models.CharField(max_length=2048)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment By {self.user} On {self.listing}"

