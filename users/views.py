from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import NewUser, Client, Employee
from users.permissions import IsSuperuser, IsAdminOrReadOnly, IsFloristOrReadOnly, IsCourierOrReadOnly, \
    IsClientOrReadOnly
from users.serializers import (
    EmployeeLoginSerializer,
    EmployeeRegisterSerializer,
    ClientLoginSerializer,
    ClientRegisterSerializer,
    ClientProfileSerializer,
    CourierProfileSerializer,
    FloristProfileSerializer,
    AllUsersSerializer, ChangePasswordSerializer,
)


class EmployeeRegisterView(generics.GenericAPIView):
    serializer_class = EmployeeRegisterSerializer
    permission_classes = (IsSuperuser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(APIView):
    serializer_class = EmployeeLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]

        user = NewUser.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        refresh = RefreshToken.for_user(user)
        is_superuser = user.is_superuser

        return Response(
            {
                "role": user.role,
                "id": user.pk,
                "is_superuser": is_superuser,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class ClientRegisterView(generics.GenericAPIView):
    serializer_class = ClientRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientLoginView(APIView):
    serializer_class = ClientLoginSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        client = NewUser.objects.filter(role="Клиент")
        serializer = self.serializer_class(client, many=True)
        return Response(serializer.data)

    def post(self, request):
        first_name = request.data["first_name"]
        phone_number = request.data["phone_number"]

        user = NewUser.objects.filter(
            phone_number=phone_number, first_name=first_name
        ).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": user.role,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class PasswordChange(APIView):
    serializer_class = ChangePasswordSerializer
    queryset = NewUser.objects.all()
    permission_classes = (IsSuperuser, )

    def post(self, request):
        phone_number = request.data["phone_number"]
        new_password = request.data["new_password"]

        user = NewUser.objects.filter(phone_number=phone_number).first()
        user.set_password(new_password)
        user.save()

        return Response({"статус": ("Пароль успешно изменён")})


class AllUsersView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = AllUsersSerializer
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )
    filter_fields = ["user__role"]
    filter_backends = [DjangoFilterBackend]


class AllUsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = AllUsersSerializer
    permission_classes = (IsSuperuser, )


class CourierWageHistory(APIView):
    serializer_class = CourierProfileSerializer
    queryset = Employee.objects.all()
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        data = (
            self.queryset.filter(user=request.user)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(wage_for_month=Sum("courier_allowance"))
        )
        return Response(data)


class FloristWageHistory(APIView):
    serializer_class = FloristProfileSerializer
    queryset = Employee.objects.all()
    permission_classes = (IsSuperuser | IsAdminOrReadOnly, )

    def get(self, request):
        data = (
            self.queryset.filter(user=request.user)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(wage_for_month=Sum("florist_allowance"))
        )
        return Response(data)


class CourierProfileView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = CourierProfileSerializer
    permission_classes = (IsCourierOrReadOnly, )

    def get_queryset(self):
        return self.queryset.filter(user__role="Курьер")


class CourierProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.filter(user__role="Курьер")
    serializer_class = CourierProfileSerializer
    permission_classes = (IsSuperuser, )


class FloristProfileView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = FloristProfileSerializer
    permission_classes = (IsFloristOrReadOnly, )

    def get_queryset(self):
        return self.queryset.filter(user__role="Флорист")


class FloristProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.filter(user__role="Флорист")
    serializer_class = FloristProfileSerializer
    permission_classes = (IsSuperuser, )


class ClientProfileView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = (IsClientOrReadOnly, )


class ClientProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = (IsClientOrReadOnly, )

