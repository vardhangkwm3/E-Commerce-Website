from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Order, OrderItem
from django.contrib.auth.decorators import login_required

def index(request):
    orders = Order.objects.filter(user=request.user)
    cntxt = {'orders': orders}
    return render(request, "store/orders/index.html", cntxt)

def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    cntxt = {'order': order, 'orderitems': orderitems}
    return render(request, 'store/orders/view.html', cntxt)