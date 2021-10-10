from rest_api.models import Breed, Cat
from rest_framework import viewsets
from rest_api.serializers import BreedSerializer, CatSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class BreedViewSet(viewsets.ModelViewSet):
    class Meta:
        model = Breed
        fields = ('name',)
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = BreedSerializer

    queryset = Breed.objects.all()

class CatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cats to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = CatSerializer

    queryset = Cat.objects.all()
