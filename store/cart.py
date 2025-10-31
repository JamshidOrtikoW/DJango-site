from decimal import Decimal
from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)


        item = self.cart.get(product_id)
        if item is None:
            
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        else:
          
            if 'quantity' not in item:
                item['quantity'] = 0
            if 'price' not in item:
                item['price'] = str(product.price)
            
            self.cart[product_id] = item
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
   
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):

        product_ids = list(self.cart.keys())
        if not product_ids:
            return

        products_qs = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products_qs}

        for pid, item in list(self.cart.items()):
            if 'price' not in item:
                item['price'] = '0.00'
            if 'quantity' not in item:
                item['quantity'] = 0

            item_obj = {
                'product': products_map.get(pid),
                'price': Decimal(item['price']),
                'quantity': item['quantity'],
            }
            item_obj['total_price'] = item_obj['price'] * item_obj['quantity']
            yield item_obj

    def __len__(self):
        return sum(item.get('quantity', 0) for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            price = Decimal(item.get('price', '0.00'))
            qty = item.get('quantity', 0)
            total += price * qty
        return total

    def clear(self):
        self.session['cart'] = {}
        self.save()

