from rest_framework.viewsets import ModelViewSet

from branches.models import Branch, AboutUs
from branches.serializers import BranchSerializer, AboutUsSerializer


class BranchView(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class AboutUsView(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

