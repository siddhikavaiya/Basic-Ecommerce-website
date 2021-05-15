from django.db import models

class category(models.Model):
    c_name=models.CharField(max_length=10)
    def __str__(self):
        return self.c_name

class product(models.Model):
    c_name=models.ForeignKey(category,on_delete=models.CASCADE)
    pname=models.CharField(max_length=20)
    pdis=models.TextField()
    price=models.PositiveIntegerField()
    img1=models.ImageField(upload_to='img1',null=True)
    img2=models.ImageField(upload_to='img2',null=True)
    def __str__(self):
        return self.pname

class Reg(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=10)
    phone=models.PositiveIntegerField(null=True)
    address=models.TextField(null=True)
    dob=models.DateField(null=True)
    image=models.ImageField(upload_to='',null=True)

class Cart(models.Model):
    user=models.ForeignKey(Reg, on_delete=models.CASCADE)
    prod=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    subtotle=models.PositiveIntegerField()
    status=models.BooleanField(default=False)

bar=(('Pending','Pending'),('Accepted','Accepted'),('Out for Delivery','Out for Delivery'),('Delivered','Delivered'))

class order(models.Model):
    user=models.ForeignKey(Reg,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    country=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    pincode=models.PositiveIntegerField()
    date=models.DateField(null=True)
    order_status=models.CharField(choices=bar,max_length=100,default='Pending')
