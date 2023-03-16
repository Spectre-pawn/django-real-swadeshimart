from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from ecommerce.models import CartItem
import datetime
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import json
from sellers.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def payments(request):
	body = json.loads(request.body)
	order = Order.objects.get(user=request.user, is_ordered=False,order_number= body['orderID'])

	order.is_ordered = True
	order.save()

	# Move the cart items to Order Product table
	cart_items = CartItem.objects.filter(user=request.user)

	for item in cart_items:
		orderproduct = OrderProduct()
		orderproduct.order_id = order.id
		
		orderproduct.user_id = request.user.id
		orderproduct.product_id = item.product_id
		orderproduct.quantity = item.quantity
		orderproduct.product_price = item.product.price
		orderproduct.ordered = True
		orderproduct.save()

		cart_item = CartItem.objects.get(id=item.id)
		product_variation = cart_item.variations.all()
		orderproduct = OrderProduct.objects.get(id=orderproduct.id)
		orderproduct.variations.set(product_variation)
		orderproduct.save()


		# Reduce the quantity of the sold products
		product = Product.objects.get(id=item.product_id)
		product.stock -= item.quantity
		product.save()

	# Clear cart
	CartItem.objects.filter(user=request.user).delete()




def place_order(request, total=0, quantity=0,):
	current_user = request.user

	# If the cart count is less than or equal to 0, then redirect back to shop
	cart_items = CartItem.objects.filter(user=current_user)
	cart_count = cart_items.count()
	if cart_count <= 0:
		return redirect('store')

	grand_total = 0
	tax = 0
	for cart_item in cart_items:
		total += (cart_item.product.price * cart_item.quantity)
		quantity += cart_item.quantity
	tax = (2 * total)/100
	grand_total = total + tax

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			# Store all the billing information inside Order table
			data = Order()
			data.user = current_user
			data.first_name = form.cleaned_data['first_name']
			data.last_name = form.cleaned_data['last_name']
			data.phone = form.cleaned_data['phone']
			data.email = form.cleaned_data['email']
			data.address_line_1 = form.cleaned_data['address_line_1']
			data.address_line_2 = form.cleaned_data['address_line_2']
			data.pincode = form.cleaned_data['pincode']
			data.state = form.cleaned_data['state']
			data.city = form.cleaned_data['city']
			data.order_note = form.cleaned_data['order_note']
			data.order_total = grand_total

			data.tax = tax
			data.ip = request.META.get('REMOTE_ADDR')
			data.save()
			# Generate order number
			yr = int(datetime.date.today().strftime('%Y'))
			dt = int(datetime.date.today().strftime('%d'))
			mt = int(datetime.date.today().strftime('%m'))
			d = datetime.date(yr,mt,dt)
			current_date = d.strftime("%Y%m%d") #20210305
			order_number = current_date + str(data.id)
			data.order_number = order_number
			data.save()

			
			#clear cart
			#CartItem.objects.filter(user=request.user).delete()

			order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
			order.is_ordered = True
			order.save()

			# Move the cart items to Order Product table
			cart_items = CartItem.objects.filter(user=request.user)

			for item in cart_items:
				orderproduct = OrderProduct()
				orderproduct.order_id = order.id
		
				orderproduct.user_id = request.user.id
				orderproduct.product_id = item.product_id
				orderproduct.quantity = item.quantity
				orderproduct.product_price = item.product.price
				orderproduct.ordered = True
				orderproduct.save()

				cart_item = CartItem.objects.get(id=item.id)
				product_variation = cart_item.variations.all()
				orderproduct = OrderProduct.objects.get(id=orderproduct.id)
				orderproduct.variations.set(product_variation)
				orderproduct.save()


				# Reduce the quantity of the sold products
				product = Product.objects.get(id=item.product_id)
				product.stock -= item.quantity
				product.save()

			# Clear cart
			CartItem.objects.filter(user=request.user).delete()
			context = {
				'order': order,
				'cart_items': cart_items,
				'total': total,
				'tax': tax,
				'grand_total': grand_total,
			}
			return render(request, 'payments.html', context)
	else:
		return redirect('checkout')

def my_orders(request):
	if request.user.is_authenticated:
		
		orders = OrderProduct.objects.filter(user=request.user).order_by('-created_at')
		print(orders)
		paginator2 = Paginator(orders, 6)
		page2= request.GET.get('page2')
		paged_products2 = paginator2.get_page(page2)

		context={
				'orders':orders,
				'product': paged_products2,

		}
		return render(request,"orders.html",context)
	else:
		return redirect('login_register')

def order_details(request):
	if request.user.is_authenticated:
		id=request.GET["id"]
		
		orders = OrderProduct.objects.filter(user=request.user,id=id)
		print(orders)

		context={
				'orders':orders,	
		}
		return render(request,"order_details.html",context)
	else:
		return redirect('login_register')

def cancle_order(request):
	if request.user.is_authenticated:
		pid=request.GET["pid"]
		orders1 = Order.objects.filter(id=pid)[0]
		orders1.status='Cancelled'
		orders1.save()
		

		
		return redirect("my_orders")
	else:
		return redirect('login_register')