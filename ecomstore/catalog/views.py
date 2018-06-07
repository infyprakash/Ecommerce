from django.shortcuts import render
from catalog.models import Category,Product,CartItem
from django.http import HttpResponseRedirect
from django import template

register = template.Library()

# Create your views here.
def home(request):
	c = Category.objects.all()
	context_dict = {
	'category':c
	}

	return render(request,'home.html',context_dict)

def category_detail(request,id):
	c = Category.objects.get(id=id)
	p = Product.objects.filter(categories__id=c.id)
	context_dict = {
	'product' : p
	}
	return render(request,'category_detail.html',context_dict)


def product_detail(request,id):
	p = Product.objects.get(id=id)
	context_dict = {
	'product':p
	}
	return render(request,'product_detail.html',context_dict)

def add_to_cart(request,id):
	quantity = request.POST['quantity']
	p = Product.objects.get(id=id)
	
	CartItem.objects.create(quantity=quantity,product=p)
	p.quantity = float(p.quantity) - float(quantity)
	p.save()
	return HttpResponseRedirect('/product/{0}/'.format(id))

def show_cart(request):
	cart = CartItem.objects.all()
	context_dict = {
	'cart':cart
	}
	return render(request,'cart.html',context_dict)


	
