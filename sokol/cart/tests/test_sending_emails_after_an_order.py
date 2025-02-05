from django.test import TestCase
from ..models import Order, DeliveryOrder
from django.core import mail
from sokol.settings import EMAIL_HOST_USER, MANAGER_EMAIL


class SendEmails(TestCase):
    def test_send_emails_with_order(self):
        """Тест отправки email после оформления заказа."""
        Order.objects.create(
            price=100000,
            customer_email='name@gmail.com',

        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Заказ оформлен')
        self.assertEqual(mail.outbox[0].body, '')
        self.assertEqual(mail.outbox[0].from_email, f"{EMAIL_HOST_USER}")
        self.assertEqual(mail.outbox[0].to, ['name@gmail.com'])

        self.assertEqual(mail.outbox[1].subject, 'Заявка на заказ из магазина')
        self.assertEqual(mail.outbox[1].body, '')
        self.assertEqual(mail.outbox[1].from_email, f"{EMAIL_HOST_USER}")
        self.assertEqual(mail.outbox[1].to, [f'{MANAGER_EMAIL}'])

    def test_send_emails_with_delivery_order(self):
        """Тест отправки email после оформления заявки на доставку."""
        DeliveryOrder.objects.create(
            customer_email='name@gmail.com',
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Заявка оформлена')
        self.assertEqual(mail.outbox[0].body, '')
        self.assertEqual(mail.outbox[0].from_email, f"{EMAIL_HOST_USER}")
        self.assertEqual(mail.outbox[0].to, ['name@gmail.com'])

        self.assertEqual(mail.outbox[1].subject, 'Заявка на доставку')
        self.assertEqual(mail.outbox[1].body, '')
        self.assertEqual(mail.outbox[1].from_email, f"{EMAIL_HOST_USER}")
        self.assertEqual(mail.outbox[1].to, [f'{MANAGER_EMAIL}'])
