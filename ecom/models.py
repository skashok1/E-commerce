from django.db import models

class Product(models.Model):
	product_id =models.AutoField(primary_key =True)
	product_name =models.CharField(max_length =50)
	category =models.CharField(max_length =50 ,default ="")
	sub_category =models.CharField(max_length =50, default ="")
	brand_name =models.CharField(max_length =20)
	price =models.IntegerField(default =0)
	descript =models.CharField(max_length =300)
	pub_date =models.DateField()
	image =models.ImageField(upload_to ="ecom/images", default ="")
	brand_name =models.CharField(max_length =50, default ="")

	def __str__(self):
		return self.product_name

class Contact(models.Model):
	msg_id =models.AutoField(primary_key =True)
	name =models.CharField(max_length =50)
	email =models.CharField(max_length =70, default ="")
	phone =models.CharField(max_length =70, default ="")
	message =models.CharField(max_length =2000, default ="")

	def __str__(self):
		return self.name

class Orders(models.Model):
	"""docstring for Orders"""
	order_id =models.AutoField(primary_key =True)
	items_json =models.CharField(max_length =5000)
	amount =models.IntegerField(default =0)
	name =models.CharField(max_length =50)
	email =models.CharField(max_length =60)
	address =models.CharField(max_length =1000)
	city =models.CharField(max_length =50)
	state =models.CharField(max_length =50)
	zip_code =models.CharField(max_length =50)
	phone =models.CharField(max_length =50, default ="")


class UpdateOrder(models.Model):
	"""docstring for UpdateOrder"""
	update_id =models.AutoField(primary_key =True)
	order_id =models.IntegerField(default ="")
	update_desc =models.CharField(max_length =5000)
	timestamp =models.DateField(auto_now_add =True)

	def __str__(self):
		return self.update_desc[0:8] + "..."
		


