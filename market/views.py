from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Product, Order, Vendor, Category, OrderItem
from cart.cart import Cart
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from .forms import orderForm

# Create your views here.
# def abc(request):

	#send quantity, product_id,
	# abc = 8  # call the quantity of product added by vendor/logged user
	# abe = 5  
	# print(abc)
	# bcd = abc - abe
	# abc = FinalOrder.objects.order_by('-quantity')
	
	# for n in abc:
	# 	id = n.product_id
	# 	oqunatity = n.quantity
	# 	print(id)
	# 	quantity = Product.objects.filter(id=id)
	# 	print(quantity.name)
		# abc = Product.objects.filter(id=id).update(quantity=quantity-oqunatity)

		
		# print(abc)
		# aqw = Product.objects.get(id = id) 
		# print(aqw.name)
	# print(aqw)	
	# return render(request,'abc.html',{'aqw':aqw})
def index(request):
	latest = Product.objects.order_by('-post_date')[:8]
	popular = Product.objects.order_by('-sales')[:8]	
	return render(request,'home.html',{'latest':latest,'popular':popular})

def register(request):
	if request.user.is_authenticated:
		# print(request.user.id)
		return render(request,'home.html')
	else:
		if request.method == 'POST':
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			username = request.POST['username']
			password1 = request.POST['password1']
			password2 = request.POST['password2']
			email = request.POST['email']
			name = request.POST['name']

			if password1==password2:
				if User.objects.filter(username=username).exists():
					messages.info(request,'Username Taken')
					return render(request,'register.html')
				elif User.objects.filter(email=email).exists():
					messages.info(request,'Email Taken')
					return render(request,'register.html')
				else:
					user = User.objects.create_user(username=username,password=password1, email=email, first_name=first_name,last_name=last_name)
					user.save()

					# abc = request.POST['username']

					# To register vendor details
					# id = user.id
					bcd = request.POST['email']
					# print(id)
					if len(name)!= 0:
						if len(bcd)!=0:
							if Vendor.objects.filter(name=name).exists():
								user.delete()
								messages.info(request,'Name Taken')
								return render(request,'register.html')
							else:
								vendor = Vendor.objects.create(name=name,user = user)
								vendor.save()
								messages.success(request,'Please wait for 24 hours to be validate as Vendor but you can enjoy product sa Customer till then' )
								user = auth.authenticate(username=username,password=password1)
								auth.login(request,user)
								# print('user_created')
								latest = Product.objects.order_by('-post_date')
								popular = Product.objects.order_by('post_date')	
								return render(request,'home.html',{'latest':latest,'popular':popular})

					user = auth.authenticate(username=username,password=password1)
					auth.login(request,user)
					# print('user_created')
					latest = Product.objects.order_by('-post_date')
					popular = Product.objects.order_by('post_date')	
					return render(request,'home.html',{'latest':latest,'popular':popular})
					
			else:
				messages.info(request,'Password are not matching..')
				return render(request,'register.html')

		else: 
			return render(request,'register.html')

def login(request):
	if request.user.is_authenticated:
		return render(request,'home.html')
	else:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']

			user = auth.authenticate(username=username,password=password)

			if user is not None:
				auth.login(request,user)
				if user.is_staff!=0:
					vendor = Vendor.objects.get(user_id=user.id)
					print(vendor.id)
					# products = Product.objects.filter(user_id=)
					return render(request,'dashboard.html',{'vendor':vendor})
				messages.success(request,' You are now logged in Successfully. ')
				latest = Product.objects.order_by('-post_date')
				popular = Product.objects.order_by('post_date')	
				return render(request,'home.html',{'latest':latest,'popular':popular})
				
			else:
				messages.info(request,'Login Credentials not matched.')
				return redirect('login')

		else:
			return render(request,'login.html')

def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		messages.success(request,'You are now logged out')
		return redirect('/')

def dashboard(request):
	if request.user.is_authenticated:
		return render(request,'dashboard.html')
	else:
		return redirect('login')

def product(request):
	product_list = Product.objects.all()
	paginator = Paginator(product_list, 8) 
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	content = {'page_obj':page_obj}
	return render(request, 'product.html',content)

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

# @login_required(login_url="/login")
def cart_add(request, id):
	if request.user.is_authenticated:
		cart = Cart(request)
		product = Product.objects.get(id=id)
		cart.add(product=product)
		return JsonResponse({"messages":len(request.session['cart'])})
	else:
		# print('abc')
		return redirect('login')



@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    try:
    	cart.decrement(product=product)

    finally:
    	return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
	form = orderForm
	content = {'form':form}
	return render(request,'cart/cart_detail.html',content)

def vendorproducts(request):
	vproduct = Product.objects.order_by('vendor_id')
	vuser = Vendor.objects.order_by('id')
	# print(vproduct)
	return render(request,'vendor.html',{'vproducts':vproduct,'vuser':vuser})

def productcategory(request):
	cproduct = Product.objects.order_by('category_id')
	cats = Category.objects.order_by('id')
	# print(vproduct)
	return render(request,'category.html',{'cproducts':cproduct,'cats':cats})

def placeorder(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
			order_by = request.user.id
			# print(order_by)
			phone = request.POST['phone']
			location = request.POST['location']

		order = Order.objects.create(order_by_id=order_by,phone=phone,location=location)
		order.save()

		# try:
		# 	form.save()
		# except Exception as e:
		# 	print(e)
			
	ses = request.session['cart']
	for key, value in ses.items():
		product_id = (value['product_id'])
		product_qty = (value['quantity'])
		product_price = (value['price'])
		total_amount = float(product_price) * float(product_qty)
		data = OrderItem.objects.create(order_id = order.id, product_id=product_id,quantity=product_qty,total=total_amount)
		data.save()
	return render(request,'home.html')

def sales(request):
	orders = Order.objects.order_by('id')
	for order in orders:
		orderitems = OrderItem.objects.filter(order = order.id)
		for orderitem in orderitems:
			product = Product.objects.get(id=orderitem.product_id)
			product.sales = product.sales + int(orderitem.quantity)
			Product.objects.filter(id=orderitem.product_id).update(sales=product.sales)
			OrderItem.objects.filter(id=orderitem.id).update(quantity=0)

		Order.objects.get(id=order.id).delete()
	
		# print(abbb.sales)
		# abbb.sales = abbb.sales + int(ab.quantity) 
	return render(request,'home.html')
# def add_product(request):
# 	if 
# def finalorder(request):
# 	for key,value in request.session.cart.items:
# 		qty = value.quantity
# 		productid = value.product_id
# 		abc = Product.objects.get(id=productid)
# 		abc.sale = abc.sale+qty  #popular product lagi
# 		abc.quantity = abc.quantity-qty #stock ko lagi

# 		print(qty+'quantity')
# 		print(abc.quantity)
# 		print(abc.sale)




		#quantity product bata ghatauney pani yei baata garney
		#harek choti cart ko quantity aaucha jun sales ma plus hunchha



	
