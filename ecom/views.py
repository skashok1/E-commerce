from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, UpdateOrder
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = 'yO3x5b!yarCJYcVe';

def index(request):
	#products =Product.objects.all()
	#print(products)
	#n =len(products)
	
	#params ={'no_of_slide':nSlide, 'product':products,'range':range(nSlide)} 
	allProds =[]
	catprods =Product.objects.values('category', 'product_id')
	cats =[item['category'] for item in catprods]
	for cat in cats:
		prod =Product.objects.filter(category =cat)

		n =len(prod)
		nSlide =n//4+ceil((n/4)-(n//4)) 
		allProds.append([prod, range(1, nSlide), nSlide])
	#all_prods =[[products, range(1, nSlide), nSlide],
	         #  [products, range(1, nSlide), nSlide]]

	params ={'allProds':allProds}

	return render(request, 'ecom/index.html', params)

def searchMatch(query, item):
	'''return true only if query matches the item'''
	if query in item.descript.lower() or query in item.product_name.lower() or query in item.category.lower():
		return True
	else:
		return False

def search(request):
	query =request.GET.get('search')
	allProds =[]
	catprods =Product.objects.values('category', 'product_id')
	cats =[item['category'] for item in catprods]
	for cat in cats:
		prodtemp = Product.objects.filter(category=cat)
		prod = [item for item in prodtemp if searchMatch(query, item)]

		n =len(prod)
		nSlide =n//4+ceil((n/4)-(n//4)) 
		if len(prod) !=0:

			allProds.append([prod, range(1, nSlide), nSlide])
	#all_prods =[[products, range(1, nSlide), nSlide],
	         #  [products, range(1, nSlide), nSlide]]

	params ={'allProds':allProds}

	return render(request, 'ecom/index.html', params)


def about(request):
	return render(request, 'ecom/about.html')

def contact(request):
	if request.method =="POST":
		name =request.POST.get('name','')
		email =request.POST.get('email','')
		phone =request.POST.get('phone','')
		message =request.POST.get('message','')
		contact =Contact(name =name, email =email, phone =phone, message =message)
		contact.save()

	return render(request, 'ecom/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = UpdateOrder.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'ecom/tracker.html')


def productview(request, myid):
	#Fetch the product by the id//
	product =Product.objects.filter(product_id =myid)
	print(product)
	return render(request, 'ecom/prodView.html',{'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = UpdateOrder(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'ecom/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'aWcZfn29349698783490',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT':str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/ecom/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'ecom/paytm.html', {'param_dict': param_dict})

    return render(request, 'ecom/checkout.html')

@csrf_exempt

def handlerequest(request):
	#paytm send post request here...
	form =request.POST
	response_dict ={}
	for i in form.keys():
		response_dict[i] =form[i]

		if i =='CHECKSUMHASH':
			checksum =form[i]

	verify  =Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
	if verify:
		if response_dict['RESPCODE'] =='01':
			print('order successful')

		else:
			print('order was not successful because' + response_dict['RESPMSG'])

	return render(request, 'ecom/paymentstatus.html', {'response':response_dict})
	return render(request, 'ecom/checkout.html', {'thank':thank, 'id': id})


