from django import template
register = template.Library()
from product.models import OrderItem

# @register.inclusion_tag('shop/nav-items.html', takes_context=True)
# def navItems(context):
#     request = context['request']
#     about = About.objects.get()
#     orderitems = OrderItem.objects.filter(session_key = request.COOKIES.get('sess_key'), ordered=False)
#     orderitems_total = orderitems.count()
#     categories = Category.objects.all()
#     return {'about': about, 'orderitems_total': orderitems_total, 'categories':categories}

# @register.inclusion_tag('shop/footer.html', takes_context=True)
# def footer(context):
#     request = context['request']
#     about = About.objects.get()
#     return {'about': about}

# @register.inclusion_tag('admin-templates/nav-items.html', takes_context=True)
# def adminNav_items(context):
#     request = context['request']
#     about = About.objects.get()
#     user = request.user
#     return {'user':user, 'about': about, 'path':request.path}

@register.filter
def in_session(orderitems, session_key):
    return orderitems.filter(session_key=session_key, ordered=False)
