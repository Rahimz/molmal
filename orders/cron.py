from .models import Order, OrderItem


def OrderCleaner():
    """
    This function clean every order that
    does not pay after 24 hours.
    """
    orders = Order.objects.all().filter(paid=False)
    for order in orders:
        if order.created.day > 1 :
            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                product = order_item.product
                product.stock += order_item.quantity
                product.save()
            order.active = False
            order.save()
