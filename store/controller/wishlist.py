from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from store.models import WishList, Product

@login_required(login_url='loginpage')
def index(request):
    wishitems = WishList.objects.filter(user=request.user)
    cntxt = {'wishitems': wishitems}
    return render(request, 'store/wishlist.html', cntxt)

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(WishList.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "Product already in Wishlist"})
                else:
                    WishList.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product added to WishList"})
            else:
                return JsonResponse({'status': "No Such Product Found"})
        else:
            return JsonResponse({'status': "Login To Continue"})
    return redirect('/')

def DeleteWishlistItem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(WishList.objects.filter(user=request.user, product_id=prod_id)):
                WishListitem = WishList.objects.get(product_id=prod_id)
                WishListitem.delete()
                return JsonResponse({'status': "Product removed from wishlist"})
            else:
                return JsonResponse({'status': "Product not found in wishlist"})
        else:
            return JsonResponse({'status': "Login To Continue"})
        
    return redirect('/')
