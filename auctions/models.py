from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from django.core.validators import MinValueValidator

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)


class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    CATEGORY_CHOICES = (
        ('BOOKS', 'Books'),
        ('ELECTRONICS', 'Electronics'),
        ('FASHION', 'Fashion'),
        ('HOME', 'Home'),
        ('SPORTS', 'Sports'),
        ('TOYS', 'Toys'),
        ('OTHER', 'Other'),
        ('BEAUTY', 'Beauty & Personal Care'),
        ('FOOD', 'Food & Beverage'),
        ('HEALTH', 'Health & Wellness'),
        ('JEWELRY', 'Jewelry & Accessories'),
        ('MUSIC', 'Music & Entertainment'),
        ('OFFICE', 'Office & Stationery'),
        ('PETS', 'Pet Supplies'),
        ('TRAVEL', 'Travel & Leisure'),
        ('VEHICLES', 'Vehicles & Automotive'),
    )
    CATEGORY_CHOICES = sorted(CATEGORY_CHOICES, key=lambda x: x[1] if x[0] != 'OTHER' else 'ZZZ')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    date_created = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return self.title
    
    def close_listing(self):
        if self.status == 'active':
            self.status = 'closed'
            # Set the winner of the auction to the highest bidder (if any)
            highest_bid = self.bids.order_by('-amount').first()
            
            
            if highest_bid:
                self.winner = highest_bid.bidder
            # Set the date_ended to the current time
            self.date_ended = datetime.now(timezone.utc)
            self.save()


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid of {self.amount} by {self.bidder.username} on {self.listing.title}'
