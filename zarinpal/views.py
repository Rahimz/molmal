from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from zeep import Client
from orders.models import Order
from .tasks import payment_completed
from tshop.secrets import *
import requests
import json
import datetime


MERCHANT = merchant
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# we use this variable to edit order after the successful payment
paid_order = None


def send_request(request):
    # we get the order detail from session
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    amount = int(order.get_total_cost())  # Toman / Required
    #print(amount)

    paid_order = order

    # set the order in the session
    request.session['order_id'] = order.id
    request.session['order_paid'] = None

    description = "سفارش شماره {}".format(order.id)  # Required
    email = 'email@example.com'  # Optional
    mobile = '09123456789'  # Optional

    # send request to payment system
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST,
                        data=json.dumps(req_data),
                        headers=req_header)
    authority = req.json()['data']['authority']

    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

    # result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    # if result.Status == 100:
    #     return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    # else:
    #     return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                request.session['order_paid'] = True
                order = Orders.objects.get(order_id=request.session['order_id'])
                order.paid = True
                order.updated = datetime.now()
                order.save()
                return render(request, 'zarinpal/success.html',
                              {'message': 'Transaction success.\nRefID: ' +
                                           str(req.json()['data']['ref_id']),
                               'order': orders})
                # return HttpResponse('Transaction success.\nRefID: ' + str(
                #     req.json()['data']['ref_id']))
            elif t_status == 101:
                return render(request, 'zarinpal/success.html',
                              {'message': 'Transaction submitted : ' +
                                          str(req.json()['data']['message'])})
                # return HttpResponse('Transaction submitted : ' + str(
                #     req.json()['data']['message']))
            else:
                return render(request,
                              'zarinpal/fail.html',
                              {'message': str (req.json()['data']['message'])})
                # return HttpResponse('Transaction failed.\nStatus: ' +
                #                     str(req.json()['data']['message']))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request,
                          'zarinpal/fail.html',
                          {'message': f"Error code: {e_code}, Error Message: {e_message}"})
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        # req_header = {"accept": "application/json",
        #               "content-type": "application/json'"}
        # req_data = {
        #     "merchant_id": MERCHANT,
        #     "amount": amount,
        #     "authority": t_authority
        # }
        # req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        # return render(request,
        #               'zarinpal/fail.html',
        #               {'message': ''})
        # return HttpResponse()
        return render(request, 'zarinpal/fail.html',
                      {'message': 'Transaction failed or canceled by user'})
