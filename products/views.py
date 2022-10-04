from django.db.models import Count
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from products.models import PlantCare, Category, Product, Wishlist
from products.serializers import (
    PlantCareSerializer,
    CategorySerializer,
    ProductSerializer,
    WishlistSerializer,
)
from users.models import Employee
from users.permissions import IsFloristOrReadOnly, IsAdminOrReadOnly, IsSuperuser


class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsFloristOrReadOnly | IsAdminOrReadOnly | IsSuperuser, )
    filter_fields = ["category", "is_sold"]
    search_fields = ["name", "category__name"]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    def perform_create(self, serializer):
        florist = Employee.objects.get(user=self.request.user)
        serializer.save(florist=florist)


class PlantCareView(ModelViewSet):
    serializer_class = PlantCareSerializer
    queryset = PlantCare.objects.all()
    permission_classes = (IsAdminOrReadOnly | IsSuperuser, )
    filter_fields = ["choice"]
    filter_backends = [DjangoFilterBackend]


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsFloristOrReadOnly | IsSuperuser, )
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)


class WishlistView(ModelViewSet):
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()


class PopularProducts(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        popular = Product.objects.all().order_by("-total_sales")[:3]
        serializer = self.serializer_class(popular, many=True)
        return Response(serializer.data)


class EasyToCareProducts(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.filter(is_easy=True)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)


class MonthlyProductsTotal(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        florist = Employee.objects.get(user=request.user)
        data = (
            Product.objects.filter(is_sold=True, florist=florist)
            .annotate(month=TruncMonth("date_created"))
            .values("month")
            .annotate(total_sold=Count("id"))
        )
        return Response(data)


class FloristPlantHistory(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        florist = Employee.objects.get(user=request.user)
        products = Product.objects.filter(florist=florist)

        serializer = self.serializer_class(products, many=True)

        return Response(serializer.data)
