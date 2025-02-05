from django.shortcuts import render


def our_team(request):
    return render(request, 'about/our_team.html')


def contacts(request):
    return render(request, 'about/contacts.html')


def payment_and_delivery(request):
    return render(request, 'about/payment_and_delivery.html')
