from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Branch, AboutUs


class BranchSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = Branch
        fields = "__all__"


class AboutUsSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = AboutUs
        fields = "__all__"
