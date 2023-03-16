from asyncio.windows_events import NULL
from django.db import models
from sqlalchemy import null
from PIL import Image
from category.models import Category
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Avg, Count
from django.utils.text import slugify
# Create your models here.
class Seller(models.Model):
	SEX_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
	STATE_CHOICES = (
		("Andaman & Nicobar Islands",'Andaman & Nicobar Islands'),
		("Andhra Pradesh",'Andhra Pradesh'),
		("Arunachal Pradesh",'Arunachal Pradesh'),
		("Assam",'Assam'),
		("Bihar",'Bihar'),
		("Chandigarh",'Chandigarh'),
		("Chhattisgarh",'Chhattisgarh'),
		("Dadra & Nagar Haveli",'Dadra & Nagar Haveli'),
		("Daman and Diu",'Daman and Diu'),
		("Delhi",'Delhi'),
		("Goa",'Goa'),
		("Gujarat",'Gujarat'),
		("Haryana",'Haryana'),
		("Himachal Pradesh",'Himachal Pradesh'),
		("Jammu & Kashmir",'Jammu & Kashmir'),
		("Jharkhand",'Jharkhand'),
		("Karnataka",'Karnataka'),
		("Kerala",'Kerala'),
		("Lakshadweep",'Lakshadweep'),
		("Madhya Pradesh",'Madhya Pradesh'),
		("Maharashtra",'Maharashtra'),
		("Manipur",'Manipur'),
		("Meghalaya",'Meghalaya'),
		("Mizoram",'Mizoram'),
		("Nagaland",'Nagaland'),
		("Odisha",'Odisha'),
		("Puducherry",'Puducherry'),
		("Punjab",'Punjab'),
		("Rajasthan",'Rajasthan'),
		("Sikkim",'Sikkim'),
		("Tamil Nadu",'Tamil Nadu'),
		("Telangana",'Telangana'),
		("Tripura",'Tripura'),
		("Uttarakhand",'Uttarakhand'),
		("Uttar Pradesh",'Uttar Pradesh'),
		("West Bengal",'West Bengal'),
		)
	username=models.CharField(max_length=10,unique=True)
	first_name=models.CharField(default='',max_length=10)
	last_name=models.CharField(default='',max_length=10)
	password=models.CharField(max_length=500)
	email=models.EmailField()
	photo = models.ImageField(default='default.png',upload_to='user_photos')
	mobile = models.CharField(max_length=10,null=True)
	gst_Number = models.CharField(max_length=15,null=True)
	shop_Name = models.CharField(max_length=500,null=True)
	alternate_mobile = models.CharField(max_length=10,null=True,blank=True)
	shop_Address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	account_Holder_Name = models.CharField(max_length=50, null=True)
	account_Number = models.CharField(max_length=20, null=True)
	ifsc_Code = models.CharField(max_length=11, null=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.photo.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.photo.path)
			
	def register(self):
		self.save()

	@staticmethod
	def get_seller_by_email(email):
		try:
			return Seller.objects.get(email=email)
		except:
			return False
	def get_seller_by_id(seller_id):
		try:
			return Seller.objects.get(seller_id=seller_id)
		except:
			return False

	def isExists(self):
		if Seller.objects.filter(email = self.email):
			return True

		return  False
	
	def isExistsusername(self):
		if Seller.objects.filter(username = self.username):
			return True

		return  False
	def __str__(self):
		return "seller-"  + self.first_name + '-'+ self.email


class Product(models.Model):
	product_name = models.CharField(max_length=100)
	slug = models.CharField(max_length=200, unique=True)
	Seller =models.ForeignKey(Seller,on_delete=models.CASCADE,default='')
	brand = models.CharField(max_length=50, default="")
	category        = models.ForeignKey(Category, on_delete=models.CASCADE)
	subcategory = models.CharField(max_length=50, default="")
	price = models.IntegerField(default=0)
	price_not = models.IntegerField(default=999)
	desc = models.TextField()
	is_available    = models.BooleanField(default=True)
	stock=models.IntegerField(default="0")
	created_date = models.DateField(auto_now=True)
	image1 = models.ImageField(upload_to='products/images', default="",null=True)
	image2 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image3 = models.ImageField(upload_to='products/images', default="",null=True,blank=True) 
	image4 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image5 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img1 = Image.open(self.image1.path)
		if img1.height > 1500 or img1.width > 1500:
			output_size = (1500, 1500)
			img1.thumbnail(output_size)
			img1.save(self.image1.path)	
			
		if self.image2:
			img2 = Image.open(self.image2.path)
			if img2.height > 1500 or img2.width > 1500:
				output_size = (1500, 1500)
				img2.thumbnail(output_size)
				img2.save(self.image2.path)

		if self.image3:
			img3 = Image.open(self.image3.path)
			if img3.height > 1500 or img3.width > 1500:
				output_size = (1500, 1500)
				img3.thumbnail(output_size)
				img3.save(self.image3.path)

		if self.image4:
			img4 = Image.open(self.image4.path)
			if img4.height > 1500 or img4.width > 1500:
				output_size = (1500, 1500)
				img4.thumbnail(output_size)
				img4.save(self.image4.path)

		if self.image5:
			img5 = Image.open(self.image5.path)
			if img5.height > 1500 or img5.width > 1500:
				output_size = (1500, 1500)
				img5.thumbnail(output_size)
				img5.save(self.image5.path)

	def save(self,*args, **kwargs): 
		self.slug = slugify(self.product_name)
		super(Product, self).save(*args, **kwargs)

	def get_url(self):
		return reverse('productView', args=[self.category.slug, self.slug])

	def __str__(self):
		return self.product_name

	def averageReview(self):
		reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
		avg = 0
		if reviews['average'] is not None:
			avg = float(reviews['average'])
		return avg

	def countReview(self):
		reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
		count = 0
		if reviews['count'] is not None:
			count = int(reviews['count'])
		return count

	def get_orders_by_seller(seller_id):
		return Product.objects.filter(Seller=seller_id).order_by('-created_date')



class VariationManager(models.Manager):
	def colors(self):
		return super(VariationManager, self).filter(variation_category='color', is_active=True)

	def sizes(self):
		return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
	('color', 'color'),
	('size', 'size'),
)


class Variation(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variation_category = models.CharField(max_length=100, choices=variation_category_choice)
	variation_value     = models.CharField(max_length=100)
	is_active           = models.BooleanField(default=True)
	created_date        = models.DateTimeField(auto_now=True)

	objects = VariationManager()

	def __str__(self):
		return self.variation_value

class Choice(models.Model):
	varname=models.CharField(max_length=100)
	def __str__(self):
		return self.varname
		
class ReviewRating(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(max_length=100, blank=True)
	review = models.TextField(max_length=500, blank=True)
	rating = models.FloatField()
	ip = models.CharField(max_length=20, blank=True)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.subject

