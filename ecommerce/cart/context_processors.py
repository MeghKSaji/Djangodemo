from cart.models import Cart
def total(request):
    item_count=0
    if request.user:
     u=request.user
     try:
        cart=Cart.objects.filter(user=u)

        for i in cart:
            item_count+=i.quantity
     except:
        item_count=0
    return {'count':item_count}
