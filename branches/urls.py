from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r"about-us", AboutUsView)
router.register(r"branches", BranchView)

urlpatterns = [
    path("", include(router.urls)),
]
