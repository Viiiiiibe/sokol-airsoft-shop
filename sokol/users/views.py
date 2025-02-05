from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView)
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, CustomUserChangeFromUserInterfaceForm
from cart.models import Order


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('index')
    template_name = 'users/signup.html'


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class UserPasswordChange(PasswordChangeView):
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class UserPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "users/password_reset_form.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"


@login_required
def personal_account_main(request):
    return render(request, 'users/personal_account_main.html')


@login_required
def personal_information_edit(request):
    if request.method == "POST":
        form = CustomUserChangeFromUserInterfaceForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user = form.save(commit=False)
            request.user.save()
            return redirect('users:personal_account_main', )
    else:
        form = CustomUserChangeFromUserInterfaceForm(instance=request.user)
    return render(request, 'users/personal_account_main_personal_information.html', {'form': form})


@login_required
def personal_account_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created')
    context = {
        'orders': orders,
    }
    return render(request, 'users/personal_account_orders.html', context)


@login_required
def personal_account_order_detail(request, number):
    order = get_object_or_404(Order, number=number)
    if request.user != order.customer:
        return redirect('users:orders', )
    context = {
        'order': order,
    }
    return render(request, 'users/personal_account_order_detail.html', context)
