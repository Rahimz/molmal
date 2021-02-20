from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from zeep import Client
from orders.models import Order
from .tasks import payment_completed
from tshop.secrets import *


MERCHANT = merchant
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# we use this variable to edit order after the successful payment
paid_order = None


def send_request(request):
    # we get the order detail from session 
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    amount = order.get_total_cost()  # Toman / Required
    #print(amount)
    
    paid_order = order
    
    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
    email = 'email@example.com'  # Optional
    mobile = '09123456789'  # Optional
    CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.


    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            # we change the order status after successful payment
            paid_order.paid = True
            paid_order.save()
            # launch asynchronous task
            payment_completed.delay(paid_order.id)
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
