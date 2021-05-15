"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    path('signup',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('addtocart/<int:id>/',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('checkout/',views.checkout,name='checkout'),
    path('shopdetail/',views.shopdetail,name='shopdetail'),
    path('compare/',views.compare,name='compare'),
    path('plus/<int:id>/',views.plus,name='plus'),
    path('minus/<int:id>/',views.minus,name='minus'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('editprofile/<int:id>/',views.editprofile,name='editprofile'),
    path('myorder/',views.myorder,name='myorder'),
    path('payment_success/',views.payment_success,name='payment_success'),
    path('payment/',views.payment,name='payment'),
    path('search/',views.search,name='search'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
