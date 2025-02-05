from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, DeliveryOrder
from cart.tasks import send_email_to_manager_with_order, send_email_to_customer_with_order, \
    send_email_to_manager_with_delivery_order, send_email_to_customer_with_delivery_order


@receiver(post_save, sender=Order)
def create_order(instance, **kwargs):
    send_email_to_customer_with_order.delay(instance.pk)
    send_email_to_manager_with_order.delay(instance.pk)


@receiver(post_save, sender=DeliveryOrder)
def create_delivery_order(instance, **kwargs):
    send_email_to_customer_with_delivery_order.delay(instance.pk)
    send_email_to_manager_with_delivery_order.delay(instance.pk)
