from django.shortcuts import redirect
from . models import Employee
import sweetify

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if Employee.objects.filter(user=request.user).exists():
            if request.user.employee.designation == 'Administrator':
                return view_func(request, *args, **kwargs)
            else:
                sweetify.error(request, title='Error', text='You\'re not authorized to view that page', icon='error', button='Ok', timer=4000)
                return redirect('/')
        else:
            sweetify.error(request, title='Error', text='You\'re not authorized to view that page', icon='error', button='Ok', timer=4000)
            return redirect('/')
    return wrapper_function

def employees_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if not Employee.objects.filter(user=request.user).exists():
            sweetify.error(request, title='Error', text='You\'re not authorized to view that page', icon='error', button='Ok', timer=4000)
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function