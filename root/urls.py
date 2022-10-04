"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from orders.views import *
from users.views import *
from products.views import *
from root.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", api_root),
    path("reset-password", PasswordChange.as_view(), name="reset-password"),
    path("rest-login/", include("rest_framework.urls")),
    path("branches/", include('branches.urls')),
    path("products/", include('products.urls')),
    path("orders/", include('orders.urls')),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name='token-verify'),
    path("employee-register", EmployeeRegisterView.as_view(), name='employee-register'),
    path("employee-login", EmployeeLoginView.as_view(), name='employee-login'),
    path("client-register", ClientRegisterView.as_view(), name='client-register'),
    path("client-login", ClientLoginView.as_view(), name='client-login'),
    path("all-users", AllUsersView.as_view(), name='all-users'),
    path("all-users/<int:pk>/", AllUsersDetailView.as_view(), name='all-users-detail'),
    path("client-profile/", ClientProfileView.as_view(), name='client-profile'),
    path("client-profile/<int:pk>/", ClientProfileDetailView.as_view(), name='client-detail'),
    path("florist-profile/", FloristProfileView.as_view(), name='florist-profile'),
    path("florist-profile/<int:pk>/", FloristProfileDetailView.as_view(), name='florist-detail'),
    path("courier-profile/", CourierProfileView.as_view(), name='courier-profile'),
    path("courier-profile/<int:pk>/", CourierProfileDetailView.as_view(), name='courier-detail'),
    path("popular-products", PopularProducts.as_view(), name='popular-products'),
    path("easy-products", EasyToCareProducts.as_view(), name='easy-products'),
    path("total-orders", MonthlyOrdersTotal.as_view(), name='total-orders'),
    path("total-products", MonthlyProductsTotal.as_view(), name='total-products'),
    path("income", MonthlyIncome.as_view(), name='income'),
    path("client-history", ClientOrderHistory.as_view(), name='client-history'),
    path("courier-order-history", CourierOrderHistory.as_view(), name='courier-history'),
    path("florist-plant-history", FloristPlantHistory.as_view(), name='florist-history'),
    path("courier-wage", CourierWageHistory.as_view(), name='courier-wage'),
    path("florist-wage", FloristWageHistory.as_view(), name='florist-wage'),

    # path("total/", TotalOrders.as_view()),

]
