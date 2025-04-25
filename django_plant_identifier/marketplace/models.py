from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class PlantSale(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='market_plants/')
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants_sold')
    is_sold = models.BooleanField(default=False)
    date_listed = models.DateTimeField(default=timezone.now)
    quantity_available = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    @property
    def is_out_of_stock(self):
        return self.quantity_available <= 0

    @property
    def total_sold(self):
        return sum(purchase.quantity for purchase in self.purchases.all())

    def __str__(self):
        return self.name

class Purchase(models.Model):
    plant = models.ForeignKey(PlantSale, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.TextField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    status_choices = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    @property
    def total_price(self):
        return self.plant.price * self.quantity

    def __str__(self):
        return f"{self.buyer.username} purchased {self.quantity} {self.plant.name}"
