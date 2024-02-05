from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from shop.models import Category
from shop.models import Product
from django.http import HttpResponse

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


def allcategories(request):
    k = Category.objects.all()

    return render(request,'category.html', {'c':k})

@login_required
def prod(request, p):
        c = Category.objects.get(name=p)
        j=Product.objects.filter(category=c)
        return render(request, 'products.html', {'c': c,'j':j})




def detail(request,p):

    j = Product.objects.get(name=p)
    return render(request, 'detail.html', {'j': j})

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcategories')
        else:
            return HttpResponse('Not Registered user')
    return render(request,'login.html')

def register(request):
    if (request.method == "POST"):
        e = request.POST['e']
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        fname = request.POST['f']
        lname = request.POST['l']




        if (p == cp):
              user = User.objects.create_user(email=e, username=u, password=p, first_name=fname, last_name=lname)

              user.save()
              return redirect('shop:allcategories')
        else:

          return HttpResponse('passwords are not same')
    return render(request,'register.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')
