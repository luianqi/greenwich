from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'order', OrderView)
router.register(r'order-item', OrderItemView)

urlpatterns = [
    path('', include(router.urls)),
]