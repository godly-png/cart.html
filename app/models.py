# from django.db import models
# from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.
# class Product(models.Model):
#     name=models.CharField(max_length=200)
#     description=models.TextField()
#     price=models.DecimalField(max_digits=10,decimal_places=2)
#     image=models.ImageField(upload_to='products/')


#     def __str__(self):
#         return self.name
    

# class Cartitems(models.Model):
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity=models.PositiveBigIntegerField(default=1)

#     @property
#     def total_price(self):
#         return self.product.price * self.quantity
    


#     def __str__(self):
#         return f"{self.quantity} of {self.product.name}"
    

# # class Order(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     total_amount = models.FloatField()
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"Order {self.id}"
    












# # -----------------------------
# # Billing Details Model
# # -----------------------------
# # models.py
# from django.db import models
# from django.contrib.auth.models import User

# # class BillingDetails(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     full_name = models.CharField(max_length=100)
# #     email = models.EmailField()
# #     phone_number = models.CharField(max_length=20)
# #     address = models.TextField()        # <-- make sure this exists
# #     city = models.CharField(max_length=50)
# #     state = models.CharField(max_length=50)
# #     pincode = models.CharField(max_length=10)
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.full_name} - {self.user.username}"
    




# # class Order(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
# #     date = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"Order #{self.id} - {self.user.username}"

# # class OrderItem(models.Model):
# #     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
# #     product_name = models.CharField(max_length=200)
# #     quantity = models.IntegerField(default=1)
# #     price = models.DecimalField(max_digits=10, decimal_places=2)  # price * quantity

# #     def __str__(self):
# #         return f"{self.product_name} ({self.quantity})"    
# class BillingDetails(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=20)
#     address = models.TextField()  
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     pincode = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.full_name} - {self.user.username}"


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     billing_details = models.ForeignKey(
#         BillingDetails, on_delete=models.SET_NULL, null=True, blank=True
#     )
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} - {self.user.username}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product_name = models.CharField(max_length=200)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # single item price

#     def __str__(self):
#         return f"{self.product_name} ({self.quantity})"

from django.db import models
from django.contrib.auth.models import User

# --------- Product & Cart ---------
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Cartitems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ⚠ Must link to user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# --------- Billing & Orders ---------
class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_details = models.ForeignKey(
        BillingDetails, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # subtotal per line

    def __str__(self):
        return f"{self.product_name} ({self.quantity})"


