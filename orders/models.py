from django.db import models
from django.contrib.auth.models import User
from sellers.models import Product, Seller, Variation

# Create your models here.
class Payment(models.Model):
	METHOD =(
		('CASH ON DELIVERY','CASH ON DELIVERY'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	payment_id = models.CharField(max_length=100,default='NULL')
	payment_method = models.CharField(max_length=100,choices=METHOD)
	amount_paid = models.CharField(max_length=100) # this is the total amount paid
	status = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.User.first_name
		
class Order(models.Model):
	STATUS = (
		
		("Accepted",'Accepted'),
		("Packed",'Packed'),
		("On The Way",'On The Way'),
		("Delivered",'Delivered'),
		('Cancelled', 'Cancelled'),
	)

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
	order_number = models.CharField(max_length=20)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)
	email = models.EmailField(max_length=50)
	address_line_1 = models.CharField(max_length=50)
	address_line_2 = models.CharField(max_length=50, blank=True)
	pincode = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	order_note = models.CharField(max_length=100, blank=True)
	order_total = models.FloatField()
	tax = models.FloatField()
	status = models.CharField(max_length=10, choices=STATUS, default='')
	ip = models.CharField(blank=True, max_length=20)
	is_ordered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def full_name(self):
		return f'{self.first_name} {self.last_name}'

	def full_address(self):
		return f'{self.address_line_1} {self.address_line_2}'

	def __str__(self):
		return self.first_name
	



class OrderProduct(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	seller =models.ForeignKey(Seller,on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variations = models.ManyToManyField(Variation, blank=True)
	quantity = models.IntegerField()
	product_price = models.FloatField()
	ordered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product.product_name
	   
	def get_orders_by_seller(seller_id):
		return OrderProduct.objects.filter(seller=seller_id).order_by('-created_at')
	
	def save(self,*args, **kwargs): 
		self.seller = (self.product.Seller)
		super(OrderProduct, self).save(*args, **kwargs)