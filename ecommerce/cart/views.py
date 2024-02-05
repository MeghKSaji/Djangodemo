from django.shortcuts import render
from shop.models import Product
from cart.models import Cart
from cart.models import Order,Account
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
@login_required
def cartview(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total+=i.quantity*i.product.price

    return render(request,'cartview.html',{'c':cart,'total':total})

@login_required
def addtocart(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if (p.stock > 0):
          cart.quantity+=1
          cart.save()
          p.stock-=1
          p.save()
    except:
        if(p.stock >0):
           cart=Cart.objects.create(product=p,user=u,quantity=1)
           cart.save()
           p.stock-=1
           p.save()

    return cartview(request)
# Create your views here
@login_required
def decrease_quantity(request, n):
    p = Product.objects.get(name=n)
    u = request.user

    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            # If quantity becomes 0, remove the item from the cart
            cart.delete()
            p.stock += 1
            p.save()
    except Cart.DoesNotExist:
        pass  # Handle the case when the product is not in the cart

    return cartview(request)
@login_required
def deleteqty(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    cart = Cart.objects.get(user=u, product=p)
    cart.delete()
    p.stock += cart.quantity
    p.save()
    return cartview(request)
@login_required
def orderform(request):
    if (request.method == "POST"):
        a = request.POST['a']
        ph = request.POST['ph']
        an = request.POST['an']

        u=request.user
        cart=Cart.objects.filter(user=u)

        total=0
        for i in cart:
            total += i.quantity * i.product.price


        try:
            num=int(an)
            ac=Account.objects.get(acctnum=num)
            if(ac.amount>=total):
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=ph,no_of_items=i.quantity,order_status="paid")
                    o.save()
                cart.delete()
                msg="Your Order placed successfully"
                return render(request,'orderdetail.html',{'msg':msg})
            else:
                msg = "Insufficient Amount. You can't Place Order"
                return render(request, 'orderdetail.html', {'msg': msg})
        except:
            pass


    return render(request, 'orderform.html')



@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,"orderview.html",{'o':o,'u':u.username})