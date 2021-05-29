from django.db import models

# Create your models here.
class PizzaModel(models.Model):
    name=models.CharField(max_length=200)
    price=models.CharField(max_length=100)
    image=models.ImageField(null=True, blank=True)

class OrderModel(models.Model):
    username=models.CharField(max_length=10)
    phone=models.CharField(max_length=30)
    address=models.CharField(max_length=200)
    ordereditems=models.CharField(max_length=500)
    totalamount=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=20)

class usercart(models.Model):
    username=models.CharField(max_length=10)
    item_name=models.CharField(max_length=200)
    item_price=models.IntegerField(null=True,blank=True)
    item_image=models.ImageField(null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    amount=models.IntegerField(null=True,blank=True)
    