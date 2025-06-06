from django.db import models
from django.contrib.auth.models import User
import uuid


class Product(models.Model):
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    price=models.FloatField()
    image=models.CharField(max_length=500,default="https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")
    file=models.FileField(upload_to='uploads')
    total_sales_amount=models.IntegerField(default=0)
    total_sales=models.IntegerField(default=0)

    def __str__(self) :
        return self.name

class OrderDetail(models.Model):
    customer_email=models.EmailField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    amount=models.IntegerField()
    stripe_payment_intent=models.CharField(max_length=200)
    has_paid=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now_add=True)

    def _generate_unique_order_number(self):
        while True:
            order_number = str(uuid.uuid4()).replace('-', '').upper()[:10]
            if not OrderDetail.objects.filter(order_number=order_number).exists():
                return order_number
    
    

    

    
    
    