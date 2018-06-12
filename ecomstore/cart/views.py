from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from catalog.models import Product
from django.http import HttpResponseRedirect,HttpResponse



# Create your views here.
@login_required(login_url='/login/')
# def add_to_cart(request,id):
# 	if (request.session.get('cart_id')==None):
# 		request.session['cart_id'] = request.user.id

# 	print('--',request.session['cart_id'])

# 	quantity = request.POST['quantity']
# 	p = Product.objects.get(id=id)
# 	try:
# 		cart_item = CartItem.objects.get(cart_id=request.user.id,product__id=p.id)
# 	except CartItem.DoesNotExist:
# 		p = Product.objects.get(id=id)
# 		CartItem.objects.create(cart_id=request.user.id,quantity=quantity,product=p)
# 	else:
# 		cart_item.quantity = cart_item.quantity + int(quantity)
# 		cart_item.save()

# 	return HttpResponseRedirect('/product/{0}/'.format(id))

# @login_required(login_url='/login/')
# def add_to_cart(request,id):
# 	quantity = request.POST['quantity']
# 	try:
# 		cart_item = CartItem.objects.get(cart_id=request.user.id)
# 	except CartItem.DoesNotExist:
# 		request.session['cartid'] = request.user.id
# 		p = Product.objects.get(id=id)
# 		CartItem.objects.create(cart_id=request.user.id,quantity=quantity,product=p)
# 	else:
# 		try:
# 			p = Product.objects.get(id=id)
# 			c_item = CartItem.objects.filter(product__id=p.id)
# 		except CartItem.DoesNotExist:
# 			CartItem.objects.create(cart_id=request.user.id,quantity=quantity,product=p)
# 		else:
# 			for c in c_item:
# 				c.quantity = c.quantity + int(quantity)
# 				c.save()
# 	return HttpResponseRedirect('/product/{0}/'.format(id))

@login_required(login_url='/login/')
def add_to_cart(request,id):
	if (request.session.get('cartid',' ')):
		request.session['cartid'] = request.user.id
	print (request.session.get('cartid'))
	quantity = request.POST['quantity']
	p = Product.objects.get(id=id)
	cart = CartItem.objects.filter(cart_id=request.user.id,product__id=p.id)
	if not cart:
		CartItem.objects.create(cart_id=request.user.id,quantity=quantity,product=p)
	else:
		for c in cart:
			c.quantity = c.quantity + int(quantity)
			c.save()
	return HttpResponseRedirect('/product/{0}/'.format(id))










@login_required(login_url='/login/')
def show_cart(request):
	print (request.session.get('cartid'))
	cart = CartItem.objects.filter(cart_id=int(request.session.get('cartid')))
	    
	context_dict = {
	'cart':cart
	}
	return render(request,'mycart.html',context_dict)


from xhtml2pdf import pisa 
# import cStringIO as StringIO 
from django.template.loader import get_template 
from django.template import Context 
outputFilename = 'invoice.pdf'

from django.conf import settings
from django.core.mail import EmailMessage

def checkout(request):
	user = request.user
	if not user.address:
		return HttpResponseRedirect('/get/address/')
	else:
		cart = CartItem.objects.filter(cart_id=request.user.id)
		item = []
		total = 0
		for c in cart:
			itemid = c.product.id
			product = Product.objects.get(id=itemid)
			total = total + float(c.quantity)*float(product.price)
			item.append({'name':product.name,'quantity':c.quantity,'price':product.price,'total':float(c.quantity)*float(product.price)})
		print(item)
		context_dict = {
			'item':item,
			'total':total
			}

		html = get_template('invoice.html').render(context_dict)
		res =open(outputFilename, "w+b")
		pdf = pisa.CreatePDF(html, dest=res)
		res.seek(0)
		pdf = res.read()
		res.close()
		return HttpResponse(pdf, 'application/pdf') 

	# response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="' + outputFilename + '"'

	

	# email = EmailMessage('Invoice', 'Invoice of purchased items', settings.EMAIL_HOST_USER, [request.user.email])
	# f = open(outputFilename, 'rb')
	# email.attach_file(outputFilename,'application/pdf')
	# email.send()

	





# def set_session(request):
# 	request.session['my_session'] = request.user.id
# 	return HttpResponse('session set')

# def get_session(request):
# 	print(request.session.get('my_session'))
# 	return HttpResponse('session:{0}'.format(request.session.get('my_session'))) 

