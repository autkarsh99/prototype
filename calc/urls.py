from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('add',views.add,name='add'),
    path('ranger',views.ranger),
    path('signup',views.signup,name='signup'),
    path('search',views.search,name='search'),
    path('sendBotMessage',views.sendBotMessage)
]