from django.contrib import admin
from .models import Order, DeliveryOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'created', 'price', 'customer_email', 'manager_has_been_notified',
                    'status')
    search_fields = ('pk', 'number', 'customer_email',)
    list_filter = ('manager_has_been_notified', 'status')
    list_editable = ('status',)


class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'created', 'customer_email', 'manager_has_been_notified', 'status')
    search_fields = ('pk', 'number', 'customer_email',)
    list_filter = ('manager_has_been_notified', 'status')
    list_editable = ('status',)


admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryOrder, DeliveryOrderAdmin)
