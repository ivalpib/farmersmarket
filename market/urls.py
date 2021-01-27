from django.contrib import admin
from django.urls import path
from .import views


urlpatterns =[
	path('',views.index,name='home'),
	path('register/',views.register, name='register'),
	path('login/',views.login, name='login'),
	path('product/',views.product, name='product'),
	path('about/',views.about, name='about'),
	path('contact/',views.contact, name='contact'),
	path('dashboard/',views.dashboard, name='dashboard'),
	path('logout/',views.logout, name='logout'),
	path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
	# path('abc/',views.abc,name='abc'),
	# path('finalorder/',views.finalorder,name='finalorder'),
	path('vendorproducts/',views.vendorproducts, name='vendorproducts'),
	path('productcategory/',views.productcategory, name='productcategory'),
	path('placeorder/',views.placeorder, name='placeorder'),
	path('sales/',views.sales, name='sales'),

]