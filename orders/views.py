from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
# adding custom view to administration
from django.contrib.admin.views.decorators import staff_member_required
# rendering PDF files
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import datetime

from django.contrib.auth.decorators import login_required

from account.models import Address


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('zarinpal:request'))
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})
    else:
        try:
            address = Address.objects.get(user=request.user, fav_address=True)
            if address:
                data_initial = {
                'first_name' : address.first_name,
                'last_name' : address.last_name,
                'phone' : address.phone,
                'address' : address.address,
                'postal_code' : address.postal_code,
                'city' : address.city}
                form = OrderCreateForm(data_initial)
        except:
            form = OrderCreateForm()
        # form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@login_required
def order_repay(request, order_id):
    # launch asynchronous task
    # # TODO: this task should be define in orders.task to send mail for user
    # order_repay.delay(order_id)

    # set the order in the session
    request.session['order_id'] = order_id

    return redirect(reverse('zarinpal:request'))


@login_required
def user_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/order/user_order_detail.html',
                  {'order': order})


@staff_member_required  # it checks both is_active and is_staff field of user request
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    This is the view to generate a PDF invoice for an order. You use the staff_member_
    required decorator to make sure only staff users can access this view.
    """

    order = get_object_or_404(Order, id=order_id)

    html = render_to_string('orders/order/pdf.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
