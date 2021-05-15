from django.shortcuts import render,redirect
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt

def base(request):
    cat=category.objects.all()
    con={}
    if 'user' in request.session:
        us=request.session['user']
        user=Reg.objects.get(email=us)
        
        c1=Cart.objects.filter(user__id=user.id)
        
        list1=[]
        subtotle=0
        for i in c1:
            list1.append(i.prod.price)
            subtotle+=i.subtotle
        l1=sum(list1)
        x=subtotle*0.3
        con['Cart']=c1
        con['subtotle']=subtotle
        con['x']=int(subtotle*0.3)
        con['adc']=int(subtotle+(subtotle*0.3))
    return render(request,'base.html',con)

def index(request):
    cat=category.objects.all()
    return render(request,'index.html',{'cat':cat})

def shop(request):
    cid=request.GET.get("cid")
    cat=category.objects.all()
    data=product.objects.filter(c_name__id=cid)
    return render(request,'shop.html',{'data':data,'cat':cat})

def shopdetail(request):
    cid=request.GET.get("cid")
    cat=category.objects.all()
    data=product.objects.get(pk=cid)
    return render(request,'single-product.html',{'data':data,'cat':cat})

def compare(request):
    return render(request,'compare.html')

def signup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        address=request.POST['address']
        image=request.FILES['image']
        dob=request.POST['dob']
        error_uname=None
        try:
            user=Reg.objects.get(email=email)
            return render(request,'signup.html',{'error_uname':"Email Id already exists"})
        except:

            user=Reg(fname=fname,lname=lname,username=username,email=email,password=password,phone=phone,address=address,image=image,dob=dob)
            user.save()
            return redirect('login')
    return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        error=None
        try:
            user=Reg.objects.get(email=email)
            if user.password==password:
                request.session['user']=email
                return redirect('/')
            else:
                return render(request,'login.html',{'error':"Invalid Password"})
        except:
            return render(request,'login.html',{'error':"Invallid Email Id or Password"})
    return render(request,'login.html')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    else:
        return redirect('login')
    return redirect('/')

def addtocart(request,id):
    con={}
    print("HHHHHHHHHHHHHHHHHHHHHHhhh")
    if 'user' in request.session:
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        user=request.session['user']
        us=Reg.objects.get(email=user)
        pro=product.objects.get(id=id)
        cartexist=Cart.objects.filter(prod__pname=pro.pname)
        qty=1
        if cartexist:
            return redirect('showcart')
        else:
            Cart(user=us,prod=pro,quantity=qty,subtotle=pro.price).save()
            return redirect('showcart')
        con['Cart']=Cart.objects.filter(user__email=us)
        return render(request,'cart.html',con)
    else:
        return redirect('login')

def showcart(request):
    con={}
    if 'user' in request.session:
        us=request.session['user']
        user=Reg.objects.get(email=us)
        
        c1=Cart.objects.filter(user__id=user.id,status=False)
        
        list1=[]
        subtotle=0
        for i in c1:
            list1.append(i.prod.price)
            subtotle+=i.subtotle
        l1=sum(list1)
        x=subtotle*0.3
        con['Cart']=c1
        con['subtotle']=subtotle
        con['x']=int(subtotle*0.3)
        con['adc']=int(subtotle+(subtotle*0.3))
        return render(request,'cart.html',con)
    else:
        return redirect('login')

def plus(request,id):
    l1=Cart.objects.get(id=id)
    totle=l1.prod.price
    l1.quantity+=1
    l1.subtotle=totle*l1.quantity
    l1.save()
    return redirect('showcart')

def minus(request,id):
    m1=Cart.objects.get(id=id)
    totle=m1.prod.price
    m1.quantity-=1
    m1.subtotle=totle*m1.quantity
    m1.save()
    return redirect('showcart')

def remove(request,id):
    m1=Cart.objects.get(id=id)
    m1.delete()
    return redirect('showcart')

def checkout(request):
    cat=category.objects.all()
    if 'user' in request.session:
        us=request.session['user']
        if request.method=='POST':
            country=request.POST['country']
            state=request.POST['state']
            pincode=request.POST['pincode']
            city=request.POST['city']
            country=request.POST['country']
            date=request.POST['date']
            user_info=Reg.objects.get(email=us)
            cart=Cart.objects.filter(user__id=user_info.id,status=False)
            for c in cart:
                ord=order(user=user_info,cart=c,country=country,state=state,pincode=pincode,city=city,date=date)
                ord.save()
                c.status=True
                c.save()
            return redirect('payment') 
    return render(request,'checkout.html',{'cat':cat})

def payment(request):
    con={}
    if 'user' in request.session:
        us=request.session['user']
        user=Reg.objects.get(email=us)
        
        c1=Cart.objects.filter(user__id=user.id)
        
        list1=[]
        subtotle=0
        for i in c1:
            list1.append(i.prod.price)
            subtotle+=i.subtotle
        l1=sum(list1)
        x=subtotle*0.3
        con['Cart']=c1
        con['subtotle']=subtotle
        con['x']=int(subtotle*0.3)
        con['adc']=int(subtotle+(subtotle*0.3))
        abc=int(subtotle+(subtotle*0.3))
        amount = abc*100 #100 here means 1 dollar,1 rupree if currency INR
        client = razorpay.Client(auth=('rzp_test_wLZHZJcAx14CMc','8dOdy43WOXhOH6SbXE2URedX'))
        con['response'] = client.order.create({'amount':amount,'currency':'USD','payment_capture':1})
        con['cat']=category.objects.all()
        con['amount']=amount
    return render(request,'payment.html',con)


def myaccount(request):
    if 'user' in request.session:
        user=request.session['user']
        user_info=Reg.objects.get(email=user)
    return render(request,'my-account.html',{'user_info':user_info})

def editprofile(request,id):
    if 'user' in request.session:
        data=Reg.objects.get(pk=id)
        if request.method=='POST':
            fname=request.POST['fname']
            lname=request.POST['lname']
            email=request.POST['email']
            phone=request.POST['phone']
            address=request.POST['address']
            image=request.POST['image']
            dob=request.POST['dob']
            
            Reg.objects.filter(pk=id).update(
                fname=fname,lname=lname,email=email,phone=phone,address=address,image=image,dob=dob
            )
        return redirect('myaccount')
    return render(request,'editprofil.html',{'data':data})

@csrf_exempt
def payment_success(request):
    if request.method =="POST":
        print(request.POST)
        return render(request,'payment_success.html')
    return redirect('checkout')

def myorder(request):
    cat=category.objects.all()
    user=request.session['user']
    data=order.objects.filter(user__email=user,cart__status=True)
    return render(request,'myorder.html',{'cat':cat,'data':data})

def search(request):
    if request.method=='GET':
        sch=request.GET['query']
        products=product.objects.filter(pname__icontains=sch)
    return render(request,'search.html',{'products':products,'sch':sch})