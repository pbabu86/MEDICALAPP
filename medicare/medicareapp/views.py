from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from medicareapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay

# Create your views here.
def About(request):
    
    return HttpResponse("This is About Page")

def prasad(request):
    
    return render(request,"prasad.html")

def Contact(request):
    

    return HttpResponse('Hello from contact Page')

def home(request):
    return render(request, '/home')
   
    #userid=request.user.id
    #print("Id of logged in user:",userid)
    #print("Result:",request.user.is_authenticated)
    #context={}
    #p=Product.objects.filter(is_active=True)
    #print(p)
   # context['products']=p
    #return render(request,'index.html',context)

      
def edit(request,rid):
    print("ID to be edited:",rid)

    return HttpResponse("ID to be edited:"+rid)

def delete(request,rid):
    print("ID to be deleted:",rid)

    return HttpResponse("ID to be deleted:"+rid)

class SimpleView (View):

    def get(self,request):
        return HttpResponse("Hello from Simple View")
    
def hello(request):
    context={}
    context['name']="Prashanth"
    context['x']=20
    context['y']=100
    context['list']=[10,20,30,40,50,60]
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':20000},
        {'id':2,'name':'jeans','cat':'cloths','price':500},
        {'id':3,'name':'adidas shoes','cat':'Shoes','price':2200},
        {'id':4,'name':'vivo','cat':'mobile','price':15000},

    ]
    return render(request,'hello.html',context)


def home(request):
   
    #userid=request.user.id
    #print("Id of logged in user:",userid)
    #print("Result:",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    #print(p)
    context['products']=p
    return render(request,'index.html',context)

    '''
    return HttpResponse('Welcome to Home Page')
    '''
def product_details(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)

def register(request):
    context={}
    if request .method=="POST":#GET==POST F|POST==POST T
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']

        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Field cannot be Empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Password and Confirm Password Didn't Match"
            return render(request, 'register.html',context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully, Please Login"
                return render(request, 'register.html',context)
            except Exception:

                context['errmsg']="User with same Username already Exist!"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    
def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']

        if uname=='' or upass=='':
            context['errmsg']="Fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)#start session and store id of logged in user in session
                return redirect('/home')
            else:
                context['errmsg']="Invalid username and Password!!"
                return render(request,'login.html',context)     
    else:
        return render (request,'login.html')
    
def user_logout(request):
        logout(request)
        return redirect('/home')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    #print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    #print(type(sv))
    if sv=='0':
        col='price'  #Ascending  ==> low to high
    else:
        col='-price'  #Descending  ==> high tom low
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):

    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)

    p=Product.objects.filter(q1 & q2 &q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    #print(min)
    #print(max)
    #return HttpResponse("Value fetched!!!")

def addtocart(request,pid):
    
    if request.user.is_authenticated:
        userid=request.user.id 
        #print(pid)
        #print(userid)
        q1=Q(uid=userid)
        q2=Q(pid=pid)
        pcount=Cart.objects.filter(q1 & q2)
        l=len(pcount)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=Product.objects.filter(id=pid)
        #print(p[0])
        context={}
        context['products']=p

        if l==0:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            #c.save()
            context['success']="Product Added in the Cart!!"

        else:
            context['error']="Product already Exists in the cart!!"
            
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    s=0
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800

    #print(c)
    #print(c[0].uid)
    #print(c[0].uid.is_staff)
    #print(c[0].pid.name)
    context={}
    context['n']=np
    context['products']=c
    context['total']=s
    return render(request,'cart.html',context)

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("order Id:",oid)
    for x in c:
        
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['n']=np
        #print(x)
        #print(x.pid)
        #print(x.uid)
       # print(x.qty)
    return render(request,'placeorder.html',context)
    
def updateqty(request,qv,cid):
    #print(type(qv))
    c=Cart.objects.filter(id=cid)
    #print(c)
    #print(c[0])
    #print(c[0].qty)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
        #pass
    #return HttpResponse("In update qty")
    return redirect('/viewcart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id

    #return HttpResponse("In make payment section")
    client = razorpay.Client(auth=("rzp_test_CWTHqJ7YpK5WM4", "M7lV7cbwrc90J2NG3Zu1LeK9"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    #$return HttpResponse("success")
    context={}
    context['data']=payment
   
    return render(request,'pay.html',context)