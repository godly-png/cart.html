from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products/')


    def __str__(self):
        return self.name
    

class Cartitems(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    


    def __str__(self):
        return f"{self.quantity} of {self.product.name}"