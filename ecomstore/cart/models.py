from django.db import models
from catalog.models import Product,Category,User

# Create your models here.
class CartItem(models.Model):
	cart_id = models.CharField(max_length=50)
	date_added = models.DateTimeField(auto_now_add=True)
	quantity = models.IntegerField(default=1)
	product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_item')

	class Meta:
		db_table = 'cart_items'
		ordering = ['date_added']

