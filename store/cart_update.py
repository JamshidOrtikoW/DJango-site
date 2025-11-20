from django.shortcuts import redirect
from .cart import Cart 

def cart_update(request, product_id):
    cart = Cart(request)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.update(product_id=product_id, quantity=quantity)
    return redirect('store:cart_detail')