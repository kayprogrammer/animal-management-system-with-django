from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name = "home"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('signup/', views.signupPage, name = "signup"),
    path('cart/', views.cart, name = "cart"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name = "add_to_cart"),
    path('update_cart/', views.update_cart, name = "update-cart"),
    path('delete_orderitem/<int:item_id>/', views.delete_orderitem, name="delete-item"),
    path('checkout/', views.checkout, name = "checkout"),
    path('process_order/<int:order_id>/', views.process_order, name = "process-order"),
    path('message/', views.message, name = "message"),

]