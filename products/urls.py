from products.views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'plant-care', PlantCareView)
router.register(r'plants', ProductView)
router.register(r'category', CategoryView)
router.register(r'wishlist', WishlistView)

urlpatterns = [
    path('', include(router.urls)),
]