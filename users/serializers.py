from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from users.models import NewUser, Client, Employee


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NewUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "role",
        ]

    def validate(self, attrs):
        phone_number = attrs.get("phone_number", "")
        if NewUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": ("Phone number is already in use")}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        return NewUser.objects.create_user(**validated_data)


class EmployeeLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id", "phone_number", "password"]


class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id", "first_name", "phone_number"]

    def create(self, validated_data):
        user = NewUser(**validated_data)
        user.set_unusable_password()
        user.save()

        return user


class ClientLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id", "first_name", "phone_number"]


class ChangePasswordSerializer(WritableNestedModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id", "phone_number", "new_password", "new_password2"]

    def validate(self, attrs):
        new_password = attrs.get("new_password", "")
        new_password2 = attrs.get("new_password2", "")

        if new_password != new_password2:
            raise serializers.ValidationError({"password": ("Пароли не совпадают")})

        return super().validate(attrs)


class AllUsersSerializer(WritableNestedModelSerializer):
    user = PresentablePrimaryKeyRelatedField(
        queryset=NewUser.objects.all(), presentation_serializer=EmployeeRegisterSerializer
    )

    class Meta:
        model = Employee
        fields = "__all__"


class CourierProfileSerializer(serializers.ModelSerializer):
    user = PresentablePrimaryKeyRelatedField(
        queryset=NewUser.objects.all(), presentation_serializer=EmployeeRegisterSerializer
    )

    class Meta:
        model = Employee
        fields = ["id", "user", "salary", "courier_allowance"]


class FloristProfileSerializer(serializers.ModelSerializer):
    user = PresentablePrimaryKeyRelatedField(
        queryset=NewUser.objects.all(), presentation_serializer=EmployeeRegisterSerializer
    )

    class Meta:
        model = Employee
        fields = ["id", "user", "salary", "florist_allowance", "florist_address"]


class ClientProfileSerializer(serializers.ModelSerializer):
    user = PresentablePrimaryKeyRelatedField(
        queryset=NewUser.objects.all(), presentation_serializer=ClientRegisterSerializer
    )

    class Meta:
        model = Client
        fields = "__all__"






