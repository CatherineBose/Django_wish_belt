from django.conf.urls import url 
from . import views              
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^dashboard$',views.dashboard),
    url(r'^AddItem$', views.addItem),
    url(r'^wish_items/create$',views.createItem),
    url(r'^wish_items/?P<id>\d+',views.itemAddedByUsers)
   
]