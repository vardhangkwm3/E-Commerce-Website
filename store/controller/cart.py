from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import JsonResponse
from store.models import Product, Cart
from django.contrib.auth.decorators import login_required

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            # if(product_check):
            if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                return JsonResponse({'status': "Product already in cart"})
            else:
                prod_qty = int(request.POST.get('product_qty'))
                if product_check.qty >= prod_qty:
                    Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                    return JsonResponse({'status': "Product added Successfully"})
                else:
                    return JsonResponse({'status': "Only "+ str(product_check.qty)+ " quantity Avilable"})
            # else:
            #     return JsonResponse({'status': "No Such Product Found"})
        else:
            return JsonResponse({'status': "Login To Continue"})
    return redirect('/')

@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    cntxt = {'cart': cart}
    return render(request, 'store/cart.html', cntxt)

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
    return redirect('/')

def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            crtitem = Cart.objects.get(product_id=prod_id, user=request.user)
            crtitem.delete()
        return JsonResponse({'status': "Product Removed From Cart"})
    return redirect('/')
    
def nocheckout(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            prod_qty = int(request.POST.get('product_qty'))
            product = Product.objects.get(id=prod_id)
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            if cart.product_qty > product.qty:
                return JsonResponse({'status': "Only "+ str(prod_qty)+ " quantity Avilable"})
            cart.save()
    return redirect('/')