from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework import serializers

from products.models import Category, Product, PlantCare, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = PresentablePrimaryKeyRelatedField(
        queryset=Category.objects.all(), presentation_serializer=CategorySerializer
    )
    # picture = Base64ImageField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["is_sold", "total_sales", "florist"]


class PlantCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantCare
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
