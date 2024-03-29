from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
	category_name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	subcategory = models.TextField(max_length=255, blank=True)
	cat_image = models.ImageField(upload_to='products/categories', blank=True)

	def save(self,*args, **kwargs): 
		self.slug = slugify(self.category_name)
		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def get_url(self):
			return reverse('products_by_category', args=[self.slug])

	def __str__(self):
		return self.category_name
