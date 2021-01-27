from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=250, null=True, unique = True)
	
	def __str__(self):
		return self.name


class Vendor(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=250, null=True, unique=True)
	location = models.CharField(max_length=250,null=True,blank=True)
	phone = PhoneField(blank=True, help_text='Contact phone number')

	def __str__(self):
		return self.name

	# def save(self,*args,**kwargs):
	# 	self.name = "Rojesh"
	# 	super(Customer,self).save(*args,**kwargs)




class Product(models.Model):
	name = models.CharField(max_length=250, null=True)
	vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE, null=True)
	category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
	price  = models.IntegerField(null=True)
	description  = models.CharField(max_length=250, null=True)
	image = models.ImageField(upload_to='products/', null=True)
	originalprice = models.IntegerField(null=True, blank=True)
	quantity = models.IntegerField(null=True, default=0) 
	sales = models.IntegerField(null=True, default=0)
	post_date = models.DateTimeField(auto_now_add=True, null=True)
	unit = models.CharField(max_length=250, null=True) 

	def __str__(self):
		return self.name

	# @property
	# def get_discount(self):
	# 	dis = self.price - self.discount
	# 	return dis

		


class Order(models.Model):
	order_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	order_date = models.DateTimeField(auto_now_add=True, null=True)
	status = models.BooleanField(default=False,null=True,blank=False)
	phone = PhoneField(blank=True, help_text='Contact phone number')
	location = models.CharField(max_length=250,null=True)
	# landmark = models.CharField(max_length=250, null=True)

	def __str__(self):
		return self.order_by.first_name 
class OrderItem(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
	quantity = models.IntegerField(null=True)
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	deliveryCharge = models.IntegerField(null=True, blank=True)
	total = models.IntegerField(null=True)
	def __str__(self):
		return self.product.name
# class Contact(models.Model):
# 	name
# 	email
# 	subject
# 	message