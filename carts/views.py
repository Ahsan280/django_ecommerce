from django.shortcuts import render,HttpResponse, redirect
from store.models import Product, Variation
from.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    product_variation=[]
    product=Product(id=product_id)
    if request.method=="POST":
        for item in request.POST:
            key=item
            value=request.POST[key]

            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    is_cart_item_exists=CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item=CartItem.objects.filter(product=product, cart=cart)
        # existing variations
        # current variations
        # item id
        ex_var_list=[]
        id=[]
        for item in cart_item:
            existing_variation=item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            index=ex_var_list.index(product_variation)
            item_id=id[index]
            item=CartItem.objects.get(product=product, id=item_id)
            item.quantity+=1
            item.save()
            return redirect("cart")
        else:
            item=CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation)>0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
    else:
        cart_item=CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.variation.clear()
        if len(product_variation)>0:
            cart_item.variation.add(*product_variation)

        cart_item.save()

    return redirect("cart")

def remove_from_cart(request, product_id, cart_item_id):
    product=Product.objects.get(id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart")

def minus(request, product_id, cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=Product.objects.get(id=product_id)
    try:
        cart_items=CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_items.quantity-=1
        cart_items.save()
        if cart_items.quantity==0:
            cart_items.delete()
    except:
        pass
    return redirect("cart")

def cart(request, total=0, quantity=0, cart_item=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+=cart_item.product.price*cart_item.quantity
            quantity+=cart_item.quantity
        tax = total * 0.02
        total_price = total + tax
    except ObjectDoesNotExist:
        pass
    return render(request, "store/cart.html", context={"total":total,
                                                       "quantity":quantity,
                                                       "cart_items":cart_items,
                                                       "tax":tax,
                                                       "total_price":total_price})