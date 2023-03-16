from secrets import choice
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from category.models import Category
from orders.models import Order, OrderProduct
from sellers.apps import SellersConfig
from sellers.forms import UpdateSalerAccountDetailForm, UpdateSalerDetailForm, variationform
from sellers.models import Product, Seller, Variation, VariationManager
from django.contrib import messages
from django.contrib.auth.hashers import  check_password
from django.contrib.auth  import authenticate
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
def sellers_register(request):
	return render(request, "sellers/login_register.html")

def sellers_registration(request):
	if request.method=="POST":
		username=request.POST["username"]
		fname=request.POST["name"]
		lname=request.POST["lname"]
		phone=request.POST["phone"]
		email=request.POST["email"]
		password=request.POST["pass"]
		
		value = {
			'username':username,
			'first_name': fname,
			'last_name': lname,
			'mobile': phone,
			'email': email
		}
		error_message = None

		seller = Seller(username=username,
							first_name=fname,
							last_name=lname,
							mobile=phone,
							email=email,
							password=password)
		error_message = validateCustomer(seller)

		if not error_message:
			print(fname, lname, phone, email, password)
			seller.password = make_password(seller.password)
			seller.register()
			return redirect("sellers_register")
		else:
			data = {
				'error': error_message,
				'values': value
			}
			return render(request,  "sellers/login_register.html", data)
	

def validateCustomer(seller):
		error_message = None;
		if (not seller.first_name):
			error_message = "First Name Required !!"
		elif len(seller.first_name) < 4:
			error_message = 'First Name must be 4 char long or more'
		elif not seller.last_name:
			error_message = 'Last Name Required'
		elif len(seller.last_name) < 4:
			error_message = 'Last Name must be 4 char long or more'
		elif not seller.mobile:
			error_message = 'Phone Number required'
		elif len(seller.mobile) < 10:
			error_message = 'Phone Number must be 10 char Long'
		elif len(seller.password) < 6:
			error_message = 'Password must be 6 char long'
		elif len(seller.email) < 5:
			error_message = 'Email must be 5 char long'
		elif seller.isExists():
			error_message = 'Email Address Already Registered..'
		elif seller.isExistsusername():
			error_message='username already exists'

		# saving

		return error_message  
#sellers login
def sellers_login(request):   #seller login attempt
	if request.method=="POST":
		email=request.POST["email"] 
		password=request.POST["your_pass"]
		seller=Seller.get_seller_by_email(email)
		error_message =None
		if seller:
			flag =check_password(password,seller.password)
			if flag:
				request.session['seller'] =seller.id
				messages.success(request,"login successful")
			return redirect('dashboard') 
		else:
			return redirect("sellers_register")

#sellers logout
def logout_seller(request):
	request.session.clear()
	return redirect("sellers_register")

def sellers_dashboard(request) :
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		orders=OrderProduct.get_orders_by_seller(seller)
		print(seller_details)
		print(orders)
		paginator3 = Paginator(orders, 6)
		page3= request.GET.get('page3')
		paged_products3 = paginator3.get_page(page3)
		product_count=orders.count()
		co=OrderProduct.objects.filter(seller=Seller(id=seller),order__status__contains="Cancelled")
		do=OrderProduct.objects.filter(seller=Seller(id=seller),order__status__contains="Delivered")
		c_count=co.count()
		d_count=do.count()
		context={   'orders' : paged_products3,
					'data':seller_details,
					'product_count' : product_count,
					'c_count':c_count,
					'd_count':d_count
					}

		return render(request, "sellers/dashboard.html",context)
	else:
		return  redirect("sellers_register")


#mange order
def manageorder(request):
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		if request.method == 'GET':
			odrr = request.GET.get('odrr')
			st = request.GET.get('st')
			if st == 'Cancelled':
				o = Order.objects.filter(id=odrr).first()
				o.status = 'Cancelled'
				o.save()
			if st == 'Accepted':
				o = Order.objects.filter(id=odrr).first()
				o.status = 'Accepted'
				o.save()
			if st == 'Packed':
				o = Order.objects.filter(id=odrr).first()
				o.status = 'Packed'
				o.save()
			if st == 'Delivered':
				o = Order.objects.filter(id=odrr).first()
				o.status = 'Delivered'
				o.save()
		ordr = [i for i in OrderProduct.objects.filter(seller=Seller(id=seller)) if i.order.status != 'Cancel' and i.order.status != 'On The Way' and i.order.status != 'Delivered'][::-1]
		

		paginator5 = Paginator(ordr, 6)
		page5= request.GET.get('page5')
		paged_products2 = paginator5.get_page(page5)
		print(ordr)
		params = {
				'orders':paged_products2,
				'dorders': [i for i in OrderProduct.objects.filter(seller=Seller(id=seller)) if i.order.status != 'Cancel' and i.order.status != 'On The Way' and i.order.status != 'Delivered'][::-1],
				'data':seller_details,
				}

		return render(request,"sellers/manageorder.html",params)
	else:
		return  redirect("sellers_register")


def orderview(request):
	seller = request.session.get('seller')
	orders=OrderProduct.get_orders_by_seller(seller)
	print(OrderProduct)
	return render(request , 'dashboard.html'  , {'orders' : orders})

def allproduct(request):
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		allproduct=Product.get_orders_by_seller(seller)
		product_count = allproduct.count()
		paginator4 = Paginator(allproduct, 6)
		page4= request.GET.get('page4')
		paged_products4 = paginator4.get_page(page4)
		print(seller_details)
		print(allproduct)
		return render(request, "sellers/allproducts.html",{'allproduct' : paged_products4,'data':seller_details,'product_count' : product_count,})
	else:
		return  redirect("sellers_register")

def addproduct(request):
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		
		if request.method =='POST':
			prod_name = request.POST.get('prod_name')
			brand=request.POST.get('brand_name')
			desc = request.POST.get('desc')
			cat = request.POST.get('category')
			subcategory = request.POST.get('subcategory')
			price = request.POST.get('price')
			price_not = request.POST.get('price_not')
			stock=request.POST.get('stock')
			image1 = request.FILES.get("image1")
			image2 = request.FILES.get("image2")
			image3 = request.FILES.get("image3")
			image4 = request.FILES.get("image4")
			image5 = request.FILES.get("image5")


			Product(Seller=Seller(id=seller),brand=brand,product_name=prod_name,category=Category.objects.get(id=int(cat)),subcategory=subcategory,price=price,price_not=price_not,stock=stock,desc=desc,image1=image1).save()
			p= Product.objects.filter(product_name=prod_name)[0]
			if image2:
				p.image2=image2
			if image3:
				p.image3=image3
			if image4:
				p.image4=image4
			if image5:
				p.image5=image5
			p.save()
			messages.success(request, f'Product Added successfully!')
		
		
		subcat=[]
		for cat in Category.objects.all():
			x = cat.subcategory.split(',')
			x.insert(0, cat)
			subcat.append(x)
		print(subcat)
		context={
				'data' : seller_details,
				'subcat': subcat,
		}
		
		return render(request, "sellers/add_product.html",context)
	else:
		return  redirect("sellers_register")

def addvariation(request):
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		product=Product.objects.filter(Seller=seller)
		if request.method =='POST':
			prod_name = request.POST.get('prod_name')
			variation=request.POST.get('variation')
			varvalue=request.POST.get('varvalue')
			Variation(product=Product.objects.get(id=int(prod_name)),variation_category=str(variation),variation_value=varvalue).save()

			messages.success(request, f'Product variations added successfully!')
		
		context={'data' :seller_details,
				 'product':product,
				
				}
	return render(request,"sellers/add_variation.html",context)


def delete_product(request):
	id=request.GET["id"]
	Product.objects.filter(id=id).delete()
	return redirect("allproduct")

def edit_product(request):
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		id=request.GET["id"]
		prod=Product.objects.filter(id=id)
		subcat=[]
		if request.method =='POST':
			prod_name = request.POST.get('prod_name')
			brand=request.POST.get('brand_name')
			desc = request.POST.get('desc')
			cat = request.POST.get('category')
			subcategory = request.POST.get('subcategory')
			price = request.POST.get('price')
			price_not = request.POST.get('price_not')
			stock=request.POST.get('stock')
			image1 = request.FILES.get("image1")
			image2 = request.FILES.get("image2")
			image3 = request.FILES.get("image3")
			image4 = request.FILES.get("image4")
			image5 = request.FILES.get("image5")


			Product.objects.filter(id=id).update(Seller=Seller(id=seller),brand=brand,product_name=prod_name,category=Category.objects.get(id=int(cat)),subcategory=subcategory,price=price,price_not=price_not,stock=stock,desc=desc)
			p= Product.objects.filter(product_name=prod_name)[0]
			if image1:
				p.image1=image1
			if image2:
				p.image2=image2
			if image3:
				p.image3=image3
			if image4:
				p.image4=image4
			if image5:
				p.image5=image5
			p.save()
			messages.success(request, f'Product updated successfully!')
		for cat in Category.objects.all():
			x = cat.subcategory.split(',')
			x.insert(0, cat)
			subcat.append(x)
		print(subcat)
		
		context={
				'data' : seller_details,
				'prod':prod,
				'subcat':subcat
		}
		
		return render(request,"sellers/edit_product.html",context)
	else:
		return  redirect("sellers_register")

def account_settings(request):
	if request.session.get("seller") is not None:
		seller = request.session.get('seller')
		seller_details=Seller.objects.filter(id=seller)
		
		if request.method=="POST":

			username=request.POST["username"]
			fname=request.POST["name"]
			lname=request.POST["lname"]
			phone=request.POST["phone"]
			email=request.POST["email"]
			password=request.POST["pass"]
		
			

			Seller.objects.filter(id=seller).update(username=username,
							first_name=fname,
							last_name=lname,
							mobile=phone,
							email=email,
							password=password)
			

			
			print(fname, lname, phone, email, password)
			seller.password = make_password(seller.password)
			seller.register()
			
				
		
		context = {
	
					'data':seller_details,
				}
		return render(request,  "sellers/account_settings.html", context)
	else:
			return redirect("sellers_register")