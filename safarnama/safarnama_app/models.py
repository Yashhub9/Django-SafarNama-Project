from django.db import models
from django.contrib.auth.models import User
# Create your models here.  
class product(models.Model):
    
    name = models.CharField(max_length=50, verbose_name='Package Name')
    price = models.FloatField(verbose_name='Package Price')
    
    original_price = models.FloatField(verbose_name='Original Price', default=0.0)  # New Field
    pdetails = models.CharField(max_length=100)
    duration=models.CharField(max_length=100, verbose_name='Duration')
    is_active = models.BooleanField(default=True, verbose_name='Available')
    pimage = models.ImageField(upload_to='image')
    itinery=models.CharField(default='null', verbose_name="itinery",max_length=1000)
    notes=models.CharField(max_length=100, verbose_name="notes",default='null')


    # Method to calculate discount percentage
    def discount_percentage(self):
        if self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return 0

   


    def _str_(self):
        return self.name
class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")   
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid") 
    qty=models.IntegerField(default=1)   
class orders(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")   
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")  
    qty=models.IntegerField(default=1)


class Review(models.Model):
    name = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}"
    



class Itinerary(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='itineraries')
    day = models.PositiveIntegerField(verbose_name="Day Number")
    activities = models.TextField(verbose_name="Activities for the Day")

    class Meta:
        unique_together = ('product', 'day')  # Ensure unique day entries for a product
        ordering = ['day']  # Order itineraries by day

    def __str__(self):
        return f"Day {self.day}: {self.product.name}"
    

class Booking(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    passenger_count = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Passenger(models.Model):
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        from datetime import timedelta, timezone
        return self.created_at >= timezone.now() - timedelta(minutes=10)
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customers = models.TextField(help_text="Comma-separated customer names")  # Store multiple names
    customer_count = models.IntegerField(default=1)  # Number of customers
    amount_per_customer = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)  # Price per customer
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.total_amount}"
    

# models.py
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
