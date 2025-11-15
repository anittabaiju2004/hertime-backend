from django.db import models

# Create your models here.


class tbl_register(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    age = models.IntegerField(default=1)
    user_type = models.CharField(default='user', max_length=50)


    def __str__(self):
        return self.name



from django.db import models
from userapp.models import tbl_register   # import your user table

class CycleInput(models.Model):

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name="cycle_inputs")
    last_day_of_period = models.DateField()
    duration = models.IntegerField(help_text="Duration of period in days")
    flow_intensity = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True, help_text="List symptoms like cramps, headache, etc.")
    description = models.TextField(blank=True, null=True)
    average_cycle_length = models.IntegerField(help_text="Average cycle length in days", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cycle input for {self.user.name} on {self.last_day_of_period}"






#Product purchase and cart purhase
from django.db import models
from adminapp.models import Category, Product
from userapp.models import tbl_register

class ProductBooking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()   # Flutter sends this
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.name}"


class BookingPayment(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash on Delivery'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    payment_choice = models.CharField(max_length=20, default='booking_payment')

    booking = models.OneToOneField(ProductBooking, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')

    # Card only
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)  # last 4 digits only
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)

    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)



class Cart(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()  # Flutter sends
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.name}"


class CartPayment(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash on Delivery'),
    ]

    payment_choice = models.CharField(max_length=20, default='cart_payment')

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    cart_ids = models.JSONField(default=list)   # [1,2,3]

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, default='completed')

    # Card only
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)

    total_amount = models.FloatField(default=0)   # Flutter sends
    created_at = models.DateTimeField(auto_now_add=True)
