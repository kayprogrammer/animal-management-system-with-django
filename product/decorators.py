from django.http import HttpResponse
from django.shortcuts import redirect
from animal.models import Employee
import sweetify

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            sweetify.warning(request, title='Warning', text='You must logout first', icon='warning', button='Ok', timer=4000)
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            sweetify.warning(request, title='Warning', text='You must login first', icon='warning', button='Ok', timer=4000)
            return redirect('/login/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'users':
            sweetify.error(request, title='Error', text='You\'re not authorized to view that page', icon='error', button='Ok', timer=4000)
            return redirect('/')

        if group == None: 
            sweetify.error(request, title='Error', text='You\'re not authorized to view that page', icon='error', button='Ok', timer=4000)
            return redirect('/')
            
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function

def non_employees(view_func):
    def wrapper_function(request, *args, **kwargs):
        if Employee.objects.filter(user=request.user).exists():
            sweetify.error(request, title='Error', text='You\'re not authorized to view that page', icon='error', button='Ok', timer=4000)
            return redirect('/animalrecords/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function
