from django.shortcuts import render, get_object_or_404
from orders.models import Order, OrderItem
from .models import DeliveryContainer
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def delivery_selection(request, pk):
    order = get_object_or_404(Order, pk=pk)
    delivery_containers = DeliveryContainer.objects.filter(admin_check=True, order_in_container__lte=4)
    if request.user == order.user:
        return render(request,
                      'delivery/delivery_select.html',
                      {'order': order,
                       'delivery_containers': delivery_containers})
    else:
        # raise Http404
        raise PermissionDenied()
