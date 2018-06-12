from django.shortcuts import render
from catalog.models import Category,Product,Address,User
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django import template
from catalog.forms import LoginForm,UserForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required,permission_required


register = template.Library()

# Create your views here.
from django.template import RequestContext
def home(request):
	c = Category.objects.all()

	context_dict = {
	'category':c,
	'user':request.user
	}

	return render(request,'home.html',context_dict)

def category_detail(request,id):
	c = Category.objects.get(id=id)
	p = Product.objects.filter(categories__id=c.id)
	context_dict = {
	'product' : p
	}
	return render(request,'category_detail.html',context_dict)

def show_address(request):
	if request.method=='POST':
		district = request.POST.get('district')
		city = request.POST.get('city')
		ward = request.POST.get('ward')
		a = Address.objects.create(district=district,city=city,ward_no=ward)
		u = User.objects.get(id=request.user.id)
		u.address = a
		u.save()
		return HttpResponseRedirect('/checkout/')
	else:
		return render(request,'address.html')


def product_detail(request,id):
	p = Product.objects.get(id=id)
	context_dict = {
	'product':p
	}
	return render(request,'product_detail.html',context_dict)

# @login_required
# @permission_required('catalog.add_cartitem', raise_exception=True)
# def add_to_cart(request,id):
# 	quantity = request.POST['quantity']
# 	p = Product.objects.get(id=id)
	
# 	CartItem.objects.create(quantity=quantity,product=p)
# 	p.quantity = float(p.quantity) - float(quantity)
# 	p.save()
# 	return HttpResponseRedirect('/product/{0}/'.format(id))

# def show_cart(request):
# 	cart = CartItem.objects.all()
# 	context_dict = {
# 	'cart':cart
# 	}
# 	return render(request,'cart.html',context_dict)


def create_user(request):

	if request.method == 'POST':
		form = UserForm(request.POST)
		
		if form.is_valid():
			# email = form.cleaned_data['email']
			# subject = 'FirstPick account created'
			# message = 'Welcome to FirstPick, go shopping online now!!!!'
			# sender = 'infymee@gmail.com'
			# send_mail(subject, message,sender,[email])
			form.save()
			return HttpResponseRedirect('/')

	else:
		form = UserForm()
	return render(request,'create_user.html',{'forms':form})

def login_page(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			# username=request.POST['username']
			# user = authenticate(username=username,email=email, password=password)
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponseNotFound('<h1>INVALID LOGIN</h1>')
	else:
		form = LoginForm()
		return render(request,'login_page.html',{'forms':form})

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def check(request):
	session = request.session
	print (session)
	return HttpResponse(session)


	
