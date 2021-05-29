from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import PizzaModel,OrderModel,usercart
from django.contrib.auth.models import User

# Create your views here.
def adminloginview(request):
    return render(request,'pizzaapp/adminlogin.html')

def authenticateadmin(request):
    username=request.POST['username']
    password=request.POST['password']

    user= authenticate(username=username,password=password)

    #if user exists
    if user is not None and user.username=="vivek":
        login(request,user)
        return redirect('adminhomepage')
    
    #if user does not exists
    if user is None:
        messages.add_message(request,messages.ERROR,"invalid credentials")
        return redirect('adminloginpage')

def adminhomepageview(request):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    context={'pizzas':PizzaModel.objects.all()}
    return render (request,"pizzaapp/adminhomepage.html",context)

def logoutadmin(request):
    logout(request)
    return redirect('adminloginpage')

def addpizza(request):
    #code to add the pizza into the database
    name=request.POST['pizza']
    price=request.POST['price']
    image_fetch=request.FILES['image']
    u=PizzaModel(name=name,price=price,image=image_fetch)
    u.save()
    messages.add_message(request,messages.SUCCESS,'Pizza Added to the database successfully')
    return redirect('adminhomepage')

def deletepizza(request,pizzapk):
    #code to delete the pizza
    PizzaModel.objects.filter(id=pizzapk).delete()
    return redirect('adminhomepage')

def homepageview(request):
    #code to redirect user to homepage
    if not request.user.is_authenticated:
        return render (request,"pizzaapp/homepage.html")
    else:
        return redirect('customerpage')

def signup(request):
    #code to add user signup information in the user database
    firstname=request.POST['firstname']
    lastname=request.POST['lastname']
    username= request.POST['username']
    password=request.POST['password']
    email=request.POST['email']
    #if user already exists
    if User.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"User already exists")
        return redirect('homepage')
    #if user does not exist
    User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email).save()
    messages.add_message(request,messages.ERROR,"User created")
    return redirect ('homepage')

def userloginview(request):
    return render(request,"pizzaapp/userlogin.html")

def userauthenticate(request):
    username=request.POST['username']
    password=request.POST['password']

    user= authenticate(username=username,password=password)

    #if user exists
    if user is not None:
        login(request,user)
        return redirect('customerpage')
    
    #if user does not exists
    if user is None:
        messages.add_message(request,messages.ERROR,"invalid credentials")
        return redirect('userlogin')

def customerwelcomeview(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    username=request.user.username
    context={'username':username,'pizzas':PizzaModel.objects.all()}
    return render(request,"pizzaapp/customerwelcome.html",context)

def logoutuser(request):
    logout(request)
    return redirect('userlogin')

def userorders(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    elif OrderModel.objects.filter(username= request.user.username,status="PENDING").exists():
        orders= OrderModel.objects.filter(username= request.user.username,status="PENDING")
        firstname= request.user.first_name
        lastname= request.user.last_name
        context= {'orders': orders,'firstname':firstname,'lastname':lastname}
        return render (request,"pizzaapp/myorders.html",context)
    elif OrderModel.objects.filter(username= request.user.username,status="ACCEPTED").exists():
        orders= OrderModel.objects.filter(username= request.user.username,status="ACCEPTED")
        firstname= request.user.first_name
        lastname= request.user.last_name
        context= {'orders': orders,'firstname':firstname,'lastname':lastname}
        return render (request,"pizzaapp/myorders.html",context)
    else:
        messages.add_message(request,messages.INFO,"You have no Pending orders!")
        return redirect('customerpage')

def adminorders(request):
    if not request.user.is_authenticated and request.user.username=="vivek":
        return redirect('adminloginpage')
    elif OrderModel.objects.filter(status="PENDING").exists():
        orders=OrderModel.objects.filter(status="PENDING")
        context= {'orders': orders}
        return render (request,"pizzaapp/adminorders.html",context)
    else:
        messages.add_message(request,messages.INFO,"No Received orders at the moment")
        return redirect ('adminhomepage')

def acceptorder(request,orderpk):
    order=OrderModel.objects.filter(id=orderpk)[0]
    order.status="ACCEPTED"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def declineorder(request,orderpk):
    order=OrderModel.objects.filter(id=orderpk)[0]
    order.status="DECLINED"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def addtocart(request,cartpk):
    pizza=PizzaModel.objects.get(id=cartpk)
    qty=request.POST['qty']
    username= request.user.username 
    intqty=int(qty)
    amount=int(pizza.price)*(intqty)
    u=usercart(username=username,item_name=pizza.name,item_price=pizza.price,item_image=pizza.image.url,quantity=qty,amount=amount)
    u.save()
    messages.add_message(request,messages.SUCCESS,"Pizza added to Cart!")
    return redirect ('customerpage')

def cartview(request):
    username=request.user.username
    if usercart.objects.filter(username=username).exists():
        useritems=usercart.objects.filter(username=username)
        totalamount=0
        for useritem in useritems:
            totalamount+=int(useritem.amount)
        context={'useritems':useritems,'totalamount':totalamount}
        return render(request,'pizzaapp/cartpage.html',context)
    else:
        messages.add_message(request,messages.INFO,"Your Cart seems to be empty!")
        return redirect('customerpage')

def deletefromcart(request,cartdelpk):
    u=usercart.objects.filter(id=cartdelpk)
    u.delete()
    messages.add_message(request,messages.SUCCESS,"Item Deleted from Cart Successfully")
    return redirect('cart')

def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    username= request.user.username 
    firstname= request.user.first_name
    lastname= request.user.last_name
    address= request.POST['address']
    phoneno=request.POST['phoneno']
    status="PENDING"
    cartitems=usercart.objects.filter(username=username)
    totalamount=0
    ordereditems=""
    for item in cartitems:
        ordereditems+=str(item.item_name) + " " +"x"+str(item.quantity)+" "
        totalamount+=int(item.amount)     
    OrderModel(username=username,phone=phoneno,address=address,status=status,ordereditems=ordereditems,totalamount=totalamount).save()
    messages.add_message(request,messages.SUCCESS,"Order Successfully Placed")
    return redirect('orders')

def adminacceptedorders(request):
    if not request.user.is_authenticated and request.user.username=="vivek":
        return redirect('adminloginpage')
    elif OrderModel.objects.filter(status="ACCEPTED").exists():
        orders=OrderModel.objects.filter(status="ACCEPTED")
        context= {'orders': orders}
        return render (request,'pizzaapp/acceptedorders.html',context)
    else:
        messages.add_message(request,messages.INFO,"No Accepted orders at the moment")
        return redirect ('adminhomepage')

def adminmarkasdelivered(request,orderpk):
    order=OrderModel.objects.filter(id=orderpk)[0]
    order.status="DELIVERED"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def admindeliveredorders(request):
    if not request.user.is_authenticated and request.user.username=="vivek":
        return redirect('adminloginpage')
    orders=OrderModel.objects.filter(status="DELIVERED")
    context= {'orders': orders}
    return render (request,'pizzaapp/deliveredorders.html',context)