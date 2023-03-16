from django.http import HttpResponse
from math import ceil
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from category.models import Category
from sellers.models import Product, ReviewRating, Variation
from .models import Cart,CartItem
from orders.models import Order, Payment, OrderProduct
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
import requests
from .forms import ReviewForm, UpdateUserDetailForm, UserUpdateForm
# Create your views here.
def index(request):
		# products = Product.objects.all()
	# print(products)
	# n = len(products)
	# nSlides = n//4 + ceil((n/4)-(n//4))
	reviews = ReviewRating.objects.all()
	allProds = []
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = Product.objects.filter(category=cat)
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		allProds.append([prod, range(1, nSlides), nSlides])

	# params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
	# allProds = [[products, range(1, nSlides), nSlides],
	#             [products, range(1, nSlides), nSlides]]
	params = {'allProds':allProds,'reviews': reviews}
	return render(request, 'index.html', params)

def productView(request,category_slug,product_slug):

	# Fetch the product using the product_id
	try:
		product = Product.objects.get(category__slug=category_slug, slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
		subcat=[]
		for cat in Variation.objects.all():
			x = cat.variation_value.split(',')
			x.insert(0, cat)
			subcat.append(x)
		print(subcat)
	except Exception as e:
		raise e
	if request.user.is_authenticated:
		try:
			orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
		except OrderProduct.DoesNotExist:
			orderproduct = None    
	else:
		orderproduct = None
	reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
	reviews2 = ReviewRating.objects.all()
	allProds = []
	related_prod=Product.objects.filter(category=product.category)
	n = len(related_prod)
	nSlides = n//4 + ceil((n/4)-(n//4))
	allProds.append([related_prod, range(1, nSlides), nSlides])
	print(related_prod)
	
	context = {
		'product': product,
		'in_cart'       : in_cart,
		'orderproduct': orderproduct,
		'reviews': reviews,
		
		'subcat':subcat,
		
		'allProds':allProds,
	}   
	
	

	return render(request, 'prodView.html', context)
	
def login_register(request):
	return render(request,"customer/login_register.html")

def cust_registration(request):
	if request.method == "POST":
		fname=request.POST["name"]
		lname=request.POST["lname"]
		email=request.POST["email"]
		password=request.POST["password_input"]
		username=request.POST["username"]
		myuser = User.objects.create_user(username, email, password)
		myuser.first_name= fname
		myuser.last_name= lname
		myuser.save()

		return redirect("/")
	else:
		return HttpResponse('fail')

def customer_login_attempt(request):
	if request.method=="POST":
		email=request.POST["email"]
		password=request.POST["password"]
		user=authenticate(username = email, password= password)
		if user is not None:
			try:
				cart = Cart.objects.get(cart_id=_cart_id(request))
				is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
				if is_cart_item_exists:
					cart_item = CartItem.objects.filter(cart=cart)

					# Getting the product variations by cart id
					product_variation = []
					for item in cart_item:
						variation = item.variations.all()
						product_variation.append(list(variation))

					# Get the cart items from the user to access his product variations
					cart_item = CartItem.objects.filter(user=user)
					ex_var_list = []
					id = []
					for item in cart_item:
						existing_variation = item.variations.all()
						ex_var_list.append(list(existing_variation))
						id.append(item.id)

					# product_variation = [1, 2, 3, 4, 6]
					# ex_var_list = [4, 6, 3, 5]

					for pr in product_variation:
						if pr in ex_var_list:
							index = ex_var_list.index(pr)
							item_id = id[index]
							item = CartItem.objects.get(id=item_id)
							item.quantity += 1
							item.user = user
							item.save()
						else:
							cart_item = CartItem.objects.filter(cart=cart)
							for item in cart_item:
								item.user = user
								item.save()
			except:
				pass
			auth.login(request, user)
			messages.success(request, 'You are now logged in.')
			url = request.META.get('HTTP_REFERER')
			try:
				query = requests.utils.urlparse(url).query
				# next=/cart/checkout/
				params = dict(x.split('=') for x in query.split('&'))
				if 'next' in params:
					nextPage = params['next']
					return redirect(nextPage)                
			except:
				return redirect('/')
		else:
			messages.error(request, 'Invalid login credentials')
			return redirect('login_register')
	return render(request, 'login_register.html')



def logout_cust(request):
	logout(request) #session end
	return redirect("login_register")


def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart

def add_cart(request, product_id):
	current_user = request.user
	product = Product.objects.get(id=product_id) #get the product
	# If the user is authenticated
	if current_user.is_authenticated :
		product_variation = []
		if request.method == 'POST':
			for item in request.POST:
				key = item
				value = request.POST[key]

				try:
					pass
					variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
					product_variation.append(variation)
				except:
					pass


		is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
		if is_cart_item_exists:
			cart_item = CartItem.objects.filter(product=product, user=current_user)
			ex_var_list = []
			id = []
			for item in cart_item:
				existing_variation = item.variations.all()
				ex_var_list.append(list(existing_variation))
				id.append(item.id)

			if product_variation in ex_var_list:
				# increase the cart item quantity
				index = ex_var_list.index(product_variation)
				item_id = id[index]
				item = CartItem.objects.get(product=product, id=item_id)
				item.quantity += 1
				item.save()

			else:
				item = CartItem.objects.create(product=product, quantity=1, user=current_user)
				if len(product_variation) > 0:
					item.variations.clear()
					item.variations.add(*product_variation)
				item.save()
		else:
			cart_item = CartItem.objects.create(
				product = product,
				quantity = 1,
				user = current_user,
			)
			if len(product_variation) > 0:
				cart_item.variations.clear()
				cart_item.variations.add(*product_variation)
			cart_item.save()
		return redirect('cart')
	# If the user is not authenticated
	else:
		product_variation = []
		if request.method == 'POST':
			for item in request.POST:
				key = item
				value = request.POST[key]

				try:
					variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
					product_variation.append(variation)
				except:
					pass


		try:
			cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
		except Cart.DoesNotExist:
			cart = Cart.objects.create(
				cart_id = _cart_id(request)
			)
		cart.save()

		is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
		if is_cart_item_exists:
			cart_item = CartItem.objects.filter(product=product, cart=cart)
			# existing_variations -> database
			# current variation -> product_variation
			# item_id -> database
			ex_var_list = []
			id = []
			for item in cart_item:
				existing_variation = item.variations.all()
				ex_var_list.append(list(existing_variation))
				id.append(item.id)

			print(ex_var_list)

			if product_variation in ex_var_list:
				# increase the cart item quantity
				index = ex_var_list.index(product_variation)
				item_id = id[index]
				item = CartItem.objects.get(product=product, id=item_id)
				item.quantity += 1
				item.save()

			else:
				item = CartItem.objects.create(product=product, quantity=1, cart=cart)
				if len(product_variation) > 0:
					item.variations.clear()
					item.variations.add(*product_variation)
				item.save()
		else:
			cart_item = CartItem.objects.create(
				product = product,
				quantity = 1,
				cart = cart,
			)
			if len(product_variation) > 0:
				cart_item.variations.clear()
				cart_item.variations.add(*product_variation)
			cart_item.save()
		return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

	product = get_object_or_404(Product, id=product_id)
	try:
		if request.user.is_authenticated:
			cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
		if cart_item.quantity > 1:
			cart_item.quantity -= 1
			cart_item.save()
		else:
			cart_item.delete()
	except:
		pass
	return redirect('cart')
		

def remove_cart_item(request, product_id, cart_item_id):
	product = get_object_or_404(Product,id=product_id)
	if request.user.is_authenticated:
		cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
	else:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
	cart_item.delete()
	return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
	try:
		tax = 0
		grand_total = 0
		if request.user.is_authenticated:
			cart_items = CartItem.objects.filter(user=request.user, is_active=True)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			quantity += cart_item.quantity
		tax = (2 * total)/100
		grand_total = total + tax
	except ObjectDoesNotExist:
		pass #just ignore

	context = {
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
		'tax'       : tax,
		'grand_total': grand_total,
	}
	return render(request, 'cart.html', context)


def search(request):
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		if keyword:
			products = Product.objects.order_by('-created_date').filter(Q(desc__icontains=keyword) | Q(product_name__icontains=keyword))
			product_count = products.count()
	context = {
		'products': products,
		'product_count': product_count,
	}
	return render(request, 'store.html', context)


def store(request, category_slug=None):
	categories = None
	products = None
	reviews = ReviewRating.objects.all()
	if category_slug != None:
		categories = get_object_or_404(Category, slug=category_slug)
		products = Product.objects.filter(category=categories, is_available=True)
		paginator = Paginator(products, 6)
		page = request.GET.get('page')
		paged_products = paginator.get_page(page)
		product_count = products.count()
	else:
		products = Product.objects.all().filter(is_available=True).order_by('id')
		paginator = Paginator(products, 6)
		page = request.GET.get('page')
		paged_products = paginator.get_page(page)
		product_count = products.count()

	context = {
		'products': paged_products,
		'product_count': product_count,
		'reviews':reviews,
	}
	return render(request, 'store.html', context)


@login_required(login_url='login_register')
def checkout(request, total=0, quantity=0, cart_items=None):
	try:
		tax = 0
		grand_total = 0
		if request.user.is_authenticated:
			cart_items = CartItem.objects.filter(user=request.user, is_active=True)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			quantity += cart_item.quantity
		tax = (2 * total)/100
		grand_total = total + tax
	except ObjectDoesNotExist:
		pass #just ignore

	context = {
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
		'tax'       : tax,
		'grand_total': grand_total,
	}
	return render(request, 'checkout.html', context)

def submit_review(request, product_id):
	url = request.META.get('HTTP_REFERER')
	if request.method == 'POST':
		try:
			reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
			form = ReviewForm(request.POST, instance=reviews)
			form.save()
			messages.success(request, 'Thank you! Your review has been updated.')
			return redirect(url)
		except ReviewRating.DoesNotExist:
			form = ReviewForm(request.POST)
			if form.is_valid():
				data = ReviewRating()
				data.subject = form.cleaned_data['subject']
				data.rating = form.cleaned_data['rating']
				data.review = form.cleaned_data['review']
				data.ip = request.META.get('REMOTE_ADDR')
				data.product_id = product_id
				data.user_id = request.user.id
				data.save()
				messages.success(request, 'Thank you! Your review has been submitted.')
				return redirect(url)

def account_settings(request):
	if request.method == 'POST':
		#User Details Update
		s_form = UpdateUserDetailForm(request.POST, request.FILES, instance=request.user.customerdetails)
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if s_form.is_valid() and u_form.is_valid():
			s_form.save()
			u_form.save()
			messages.success(request, f'Your Account has been Updated!')
			return redirect("custaccount_settings")

		
			
		else:
			messages.error(request, 'Please correct the error below.')

	else:
		s_form = UpdateUserDetailForm(instance=request.user.customerdetails)
		u_form = UserUpdateForm(instance=request.user)
		
	detl = {
		'u_form':u_form,
		's_form':s_form,
		
		'title':'User Account Settings',
		
		'category':Category.objects.all(),
		}
	return render(request, 'customer/account_settings.html', detl)
