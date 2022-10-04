from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'token-verify': reverse('token-verify', request=request, format=format),
        'token-refresh': reverse('token_refresh', request=request, format=format),
        'reset-password': reverse('reset-password', request=request, format=format),
        'employee-register': reverse('employee-register', request=request, format=format),
        'employee-login': reverse('employee-login', request=request, format=format),
        'client-register': reverse('client-register', request=request, format=format),
        'client-login': reverse('client-login', request=request, format=format),
        'all-users': reverse('all-users', request=request, format=format),
        'client-profile': reverse('client-profile', request=request, format=format),
        'florist-profile': reverse('florist-profile', request=request, format=format),
        'courier-profile': reverse('courier-profile', request=request, format=format),
        'popular-products': reverse('popular-products', request=request, format=format),
        'easy-products': reverse('easy-products', request=request, format=format),
        'total-orders': reverse('total-orders', request=request, format=format),
        'total-products': reverse('total-products', request=request, format=format),
        'income': reverse('income', request=request, format=format),
        'client-history': reverse('client-history', request=request, format=format),
        'courier-order-history': reverse('courier-history', request=request, format=format),
        'florist-plant-history': reverse('florist-history', request=request, format=format),
        'courier-wage': reverse('courier-wage', request=request, format=format),
        'florist-wage': reverse('florist-wage', request=request, format=format)
    })
