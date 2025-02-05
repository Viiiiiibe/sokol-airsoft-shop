from sokol.celery import app
from smtplib import SMTPDataError
from .models import Order, DeliveryOrder
from sokol.settings import EMAIL_HOST_USER, MANAGER_EMAIL
from django.core.mail import send_mail
from django.template.loader import get_template
import logging

logger = logging.getLogger('django')


@app.task
def send_email_to_manager_with_order(order_pk):
    order = Order.objects.get(pk=order_pk)
    context = {
        'order': order
    }
    if not order.manager_has_been_notified:
        try:
            send_mail(
                "Заявка на заказ из магазина",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{MANAGER_EMAIL}"],
                fail_silently=False,
                html_message=get_template('email/order_confirm_to_manager.html').render(context)
            )
            Order.objects.filter(pk=order_pk).update(manager_has_been_notified=True)
        except SMTPDataError:
            logger.info(f"SMTPDataError, email to manager with order {order.number} not sent")


@app.task
def send_email_to_customer_with_order(order_pk):
    order = Order.objects.get(pk=order_pk)
    context = {
        'order': order
    }
    if not order.manager_has_been_notified:
        try:
            send_mail(
                "Заказ оформлен",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{order.customer_email}"],
                fail_silently=False,
                html_message=get_template('email/order_confirm_to_customer.html').render(context)
            )
        except SMTPDataError:
            logger.info(f"SMTPDataError, email to customer with order {order.number} confirmation not sent")


@app.task
def send_email_to_manager_with_delivery_order(delivery_order_pk):
    delivery_order = DeliveryOrder.objects.get(pk=delivery_order_pk)
    context = {
        'order': delivery_order
    }
    if not delivery_order.manager_has_been_notified:
        try:
            send_mail(
                "Заявка на доставку",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{MANAGER_EMAIL}"],
                fail_silently=False,
                html_message=get_template('email/delivery_order_confirm_to_manager.html').render(context)
            )
            DeliveryOrder.objects.filter(pk=delivery_order_pk).update(manager_has_been_notified=True)
        except SMTPDataError:
            logger.info(f"SMTPDataError, email to manager with delivery order {delivery_order.number} not sent")


@app.task
def send_email_to_customer_with_delivery_order(delivery_order_pk):
    delivery_order = DeliveryOrder.objects.get(pk=delivery_order_pk)
    context = {
        'order': delivery_order
    }
    if not delivery_order.manager_has_been_notified:
        try:
            send_mail(
                "Заявка оформлена",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{delivery_order.customer_email}"],
                fail_silently=False,
                html_message=get_template('email/delivery_order_confirm_to_customer.html').render(context)
            )
        except SMTPDataError:
            logger.info(
                f"SMTPDataError, email to customer with delivery order "
                f"{delivery_order.number} confirmation not sent"
            )
