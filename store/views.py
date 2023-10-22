from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.controller import authviews

from .models import *

# Create your views here.
def home(request):
    trending_products = Product.objects.filter(trending=1)
    cntxt = {'trending_products': trending_products}
    return render(request, "store/index.html", cntxt)

def collections(request):
    category = Category.objects.filter(status=0)
    cntxt = {'category': category}
    return render(request, "store/collections.html", cntxt)

def collectionsview(request, slug):
    if Category.objects.filter(slug=slug, status=0):
        products = Product.objects.filter(category__slug=slug)  
        cate = Category.objects.filter(slug=slug).first()
        cntxt = {'products': products, 'category': cate}
        return render(request, 'store/products/index.html', cntxt)
    else:
        authviews.logoutpage(request)
        return redirect('collections')

def productview(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=0):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            cntxt = {'products': products}
        else:
            authviews.logoutpage(request)
            return redirect('collections')
    else:
        messages.error(request, "No such category found23")
        return redirect('collections')
    return render(request, 'store/products/view.html', cntxt)

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productList = list(products)

    return JsonResponse(productList, safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()

            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request, "No product Matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))