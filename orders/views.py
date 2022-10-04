from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from orders.models import Order, OrderItem
from orders.serializers import (
    OrderSerializer,
    OrderItemSerializer,
    ClientHistorySerializer)
from users.models import Employee, Client
from users.permissions import IsOrder, IsAdminOrReadOnly, IsSuperuser, IsCourierOrReadOnly


class OrderView(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsOrder | IsSuperuser, )
    filter_fields = ["is_active", "courier_status"]
    search_fields = ["client__user__first_name", "client__user__phone_number"]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return self.queryset.filter(id=-1)
        elif user.role == "Клиент":
            client = Client.objects.get(user=user)
            return self.queryset.filter(client=client, is_cancelled=False)

        return self.queryset.filter(is_cancelled=False)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.instance.calculate_total_price()
        return Response(serializer.data)

    def perform_create(self, serializer):
        courier = Employee.objects.get(user=self.request.user)
        serializer.save(courier=courier)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", True)
        serializer = self.serializer_class(
            instance, data=request.data, partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            if instance.courier_status != "Cancel":
                instance.save()
                return Response(serializer.data)
            return Response(serializer.errors)


class OrderItemView(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data["product"]
            plant_care = serializer.validated_data["plant_care"]
            quantity = serializer.validated_data["quantity"]

            if product:
                if product.quantity < quantity:
                    return Response(
                        {"В наличии нет столько растений"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    product.quantity -= quantity
                    product.total_sales += quantity
                    product.save()
            if plant_care:
                if plant_care.quantity < quantity:
                    return Response(
                        {"В наличии нет столько товаров"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    plant_care.quantity -= quantity
                    plant_care.save()

            if plant_care is not None and product is not None:
                return Response(
                    {"Выберите только один вид продукта"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
        return Response(serializer.data)


class MonthlyOrdersTotal(APIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        courier = Employee.objects.get(user=request.user)
        data = (
            self.queryset.filter(courier_status="Delivered", courier=courier)
            .annotate(month=TruncMonth("date_created"))
            .values("month")
            .annotate(total_orders=Count("id"))
        )
        return Response(data)


class MonthlyIncome(APIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        data = (
            self.queryset.filter(courier_status="Delivered")
            .annotate(month=TruncMonth("date_created"))
            .annotate(week=TruncWeek("date_created"))
            .values("month", "week")
            .annotate(income=Sum("total_price"), total_sold=Count("id"))
            .order_by()
        )

        return Response(data)


class ClientOrderHistory(APIView):

    def get(self, request):
        client = Client.objects.get(user=request.user)
        items = OrderItem.objects.filter(
            order__client=client, order__courier_status="Delivered"
        )
        serializer = ClientHistorySerializer(items, many=True)

        return Response(serializer.data)


class CourierOrderHistory(APIView):
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        courier = Employee.objects.get(user=request.user)
        orders = Order.objects.filter(courier=courier)

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)
