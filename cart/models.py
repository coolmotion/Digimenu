from django.db import models
from main.models import Portion

class Order(models.Model):
	phone = models.CharField(max_length=20, blank=True)
	amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
	date_ordered = models.DateTimeField(auto_now_add=True)	
	# shipped = models.BooleanField(default=False)
	# date_shipped = models.DateTimeField(blank=True, null=True)
	
	def __str__(self):
		return f'Order - {str(self.phone)} id:{str(self.id)}'
	
class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Portion, on_delete=models.CASCADE, null=True)
	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)


	def __str__(self):
		return f'Order Item - {str(self.id)}'
