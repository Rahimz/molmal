from celery import shared_task 
from django.core.mail import send_mail
from .models import Order
from shop.recommender import Recommender


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail motification when an order is
    successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfullu placed an order.' \
              f'Your order ID is {order.id}'
    mail_sent = send_mail(subject,
                          message,
                          'admin@tshop.com',
                          [order.email])
    # This part call the recommender and add bought product to redis db
    # when an order create
    order_items = order.items.all()
    products = []
    for oi in order_items:
        products.append(oi.product)

    recommender = Recommender()
    recommender.products_bought(products)
    return mail_sent