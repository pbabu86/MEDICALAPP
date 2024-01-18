from django.contrib import admin
from django.urls import path
from medicareapp import views
from medicareapp.views import SimpleView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('About',views.About),
    path('prasad',views.prasad),
    path('Contact',views.Contact),
    path('home',views.home),
    path('edit/<rid>',views.edit),
    path('delete/<rid>',views.delete),
    path('myview',SimpleView.as_view()),
    path('hello',views.hello),
    path('pdetails/<pid>',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
  
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
  