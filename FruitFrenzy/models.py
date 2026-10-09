from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from decimal import Decimal


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField()
    product_ingredients = models.TextField()
    product_image = models.ImageField(upload_to='media/images/')
    allergen = models.ForeignKey('Allergen', on_delete=models.CASCADE)

    class Meta:
        ordering = ['product_name']

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Allergen(models.Model):
    allergen_id = models.AutoField(primary_key=True)
    allergen_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.allergen_name

    def get_absolute_url(self):
        return reverse('allergen_detail', args=[str(self.id)])


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def tax(self):
        return round(self.subtotal() * Decimal(0.07), 2)

    def price_tax(self):
        return self.subtotal() + self.tax()

    def prod_count(self):
        return sum(item.quantity for item in CartItem.objects.filter(cart=self.product))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.price * self.quantity

    def tax(self):
        return round(self.subtotal() * Decimal(0.07), 2)

    def price_tax(self):
        return self.subtotal() + self.tax()


class Reviews(models.Model):
    RATING_CHOICES = [
        (5, '5 Stars'),
        (4, '4 Stars'),
        (3, '3 Stars'),
        (2, '2 Stars'),
        (1, '1 Star'),
    ]

    review_title = models.CharField(max_length=255)
    review_content = models.TextField()
    review_rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    product_image = models.ImageField(upload_to='product_images/')

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.review_title
