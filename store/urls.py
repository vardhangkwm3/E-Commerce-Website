from django.urls import path
from . import views

from .controller import authviews, cart, wishlist, checkout, order

urlpatterns = [
    path('', views.home, name="home"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

    path('product-list', views.productlistAjax),
    path('searchproduct', views.searchproduct, name="searchproduct"),

    path('register/', authviews.register, name="register"),
    path('login/', authviews.loginpage, name="loginpage"),
    path('logout/', authviews.logoutpage, name="logout"),

    path('add-to-cart', cart.addtocart, name="addtcart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),

    path('wishlist', wishlist.index, name="wishlist"),
    path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
    path('delete-wishlist-item', wishlist.DeleteWishlistItem, name="DeleteWishlistItem"),
    
    path('checkout', checkout.index, name="checkout"),
    path('place-order', checkout.placeorder, name="placeorder"),
    path('proceed-to-pay', checkout.razorpaycheck),

    path('my-orders', order.index, name="myorders"),
    path('view-order/<str:t_no>', order.vieworder, name="orderview"),
    path('qty', cart.nocheckout, name="nocheckout"),
]

