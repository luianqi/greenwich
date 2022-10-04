from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from orders.models import Order, OrderItem
from products.models import Product, PlantCare
from products.serializers import ProductSerializer, PlantCareSerializer
from users.models import Employee
from users.serializers import CourierProfileSerializer


class OrderSerializer(WritableNestedModelSerializer):
    price_with_discount = serializers.ReadOnlyField()
    courier = PresentablePrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        presentation_serializer=CourierProfileSerializer,
        allow_null=True
    )

    class Meta:
        model = Order
        fields = ["id",
                  "client",
                  "courier",
                  "first_name",
                  "last_name",
                  "phone_number",
                  "address",
                  "comment",
                  "client_status",
                  "courier_status",
                  "total_price",
                  "is_active",
                  "is_cancelled",
                  "price_with_discount",
                  "date_created"]

        read_only_fields = [
            "is_active",
            "is_cancelled",
            "client_status",
            "total_price"]


class OrderItemSerializer(WritableNestedModelSerializer):
    product = PresentablePrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        presentation_serializer=ProductSerializer,
        allow_null=True
    )
    plant_care = PresentablePrimaryKeyRelatedField(
        queryset=PlantCare.objects.all(),
        presentation_serializer=PlantCareSerializer,
        allow_null=True
    )
    order = PresentablePrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        presentation_serializer=OrderSerializer,
        allow_null=True
    )

    class Meta:
        model = OrderItem
        fields = "__all__"

    # def validate(self, attrs):
    #     product = attrs.get("product", "")
    #     plant_care = attrs.get("plant_care", "")
    #
    #     if product is not None and plant_care is not None:
    #         raise serializers.ValidationError(
    #             "Выберите только один вид продукта"
    #         )
    #     return super().validate(attrs)


class ClientHistorySerializer(WritableNestedModelSerializer):
    total_price = serializers.IntegerField(source="order.total_price")
    address = serializers.CharField(source="order.address")
    date_created = serializers.DateTimeField(source="order.date_created")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "address",
            "product",
            "plant_care",
            "total_price",
            "date_created",
        ]


class CourierHistorySerializer(WritableNestedModelSerializer):
    total_price = serializers.IntegerField(source="order.total_price")
    first_name = serializers.CharField(source="order.first_name")
    last_name = serializers.CharField(source="order.last_name")
    address = serializers.CharField(source="order.address")
    date_created = serializers.DateTimeField(source="order.date_created")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "product",
            "plant_care",
            "total_price",
            "date_created",
        ]
