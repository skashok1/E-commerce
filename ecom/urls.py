from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name ='Shophome'),
    path("about/", views.about, name ='About Us'),
    path("contact/", views.contact, name ='Contact Us'),
    path("tracker/", views.tracker, name ='Tracking Status'),
    path("search/", views.search, name ='Search'),
    path("productview/<int:myid>", views.productview, name ='Product view'),
    path("checkout/", views.checkout, name ='Checkout'),
    path("handlerequest/", views.handlerequest, name ='handleRequest'),
]
