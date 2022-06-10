import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from product.decorators import authenticated_user, unauthenticated_user
from product.forms import RegisterForm, ShippingForm

from product.models import FoodProduct, Message, Order, OrderItem
import sweetify
# Create your views here.

@unauthenticated_user
def signupPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)

    context = {'form':form}
    return render(request, 'product/signup.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            sweetify.success(request, title='Success', text='You\'re now logged in', icon='success', button='Ok', timer=3000)
            return redirect('/')
        else:
            sweetify.error(request, title='Error', text='Your username OR password is incorrect', icon='error', button='Ok', timer=3000)
    return render(request, 'product/login.html')

@authenticated_user
def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        food_products = FoodProduct.objects.all()
        orderitems = OrderItem.objects.filter(user=request.user, order=None)
        products = [o.product.name for o in orderitems]

    context = {'food_products':food_products, 'orderitems':orderitems, 'products':products}
    return render(request, 'product/home.html', context)

@authenticated_user
def cart(request):
    orderitems = OrderItem.objects.filter(user = request.user, order = None)
    total = sum([item.get_total for item in orderitems])
    context = {'orderitems':orderitems, 'total':total}
    return render(request, 'product/cart.html', context)

@authenticated_user
def add_to_cart(request, product_id):
    product = FoodProduct.objects.get(id=product_id)
    quantity = request.POST.get('qty-2')
    orderitem, created = OrderItem.objects.get_or_create(user=request.user, product=product, order = None)
    orderitem.quantity = quantity
    orderitem.save()
    return redirect('/cart/')

@authenticated_user
def update_cart(request):
    if 'update' in request.POST:
        quantities = request.POST.getlist('quantity') 
        orderitems = OrderItem.objects.filter(user=request.user, order = None)
        for o, q in zip(orderitems, quantities):
            o.quantity = q
            o.save(update_fields=['quantity'])
    elif 'delete' in request.POST:
        OrderItem.objects.filter(user=request.user, order = None).delete()

    return redirect('/cart/')

@authenticated_user
def delete_orderitem(request, item_id):
    OrderItem.objects.get(user=request.user, id = item_id).delete()
    return redirect('/cart/')

@authenticated_user
def checkout(request):

    orderitems = OrderItem.objects.filter(user = request.user, order = None)
    subtotal = sum([item.get_total for item in orderitems])
    total = subtotal + 2000
    form = ShippingForm()
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping_address = form.save()
            order = Order.objects.create(shipping_address = shipping_address, user = request.user)
            orderitems.update(order=order)
            return redirect(f'/process_order/{order.id}/')
        else:
            print(form.errors)

    context = {'orderitems':orderitems, 'total':total, 'form':form, 'subtotal':subtotal}
    return render(request, 'product/checkout.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@authenticated_user
def process_order(request, order_id):
    order = Order.objects.get(id = order_id, user = request.user, verified=False)
    orderitems = order.orderitems.all()
    subtotal = sum([item.get_total for item in orderitems])
    total = sum([item.get_total for item in orderitems]) + 2000
    # data = json.loads(request.body)
    # ord_id = data.get('order_id')
    if is_ajax(request=request):
        order.verified = True
        order.save()
        return JsonResponse('worked', safe=False)
    context = {'order':order, 'orderitems':orderitems, 'total':total, 'subtotal':subtotal}
    return render(request, 'product/order.html', context)

@authenticated_user
def message(request):

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    message = request.POST.get('message')

    Message.objects.create(name = name, phone = phone, email = email, message = message)
    sweetify.success(request, title='Success', text='We\'ve received your message and will get back to you shortly', icon='success', button='Ok', timer=3000)

    return redirect('/')