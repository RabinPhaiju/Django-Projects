
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from core.permissions import BaseAccessPolicy
from core.serializers.signup_serializer import SignupUserSerializer

class UserAccessPolicy(BaseAccessPolicy):
    statements = [
        { "principal": "authenticated", "action": ['signup'], "effect": "allow"},
    ]
    

class UserAPI(CreateModelMixin, GenericViewSet):
    serializer_class = SignupUserSerializer
    http_method_names = ("post",)
    authentication_classes = []
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create(serializer.validated_data)
        # Serialize user data
        data = self.get_serializer(user).data

        return Response(data=data, status=status.HTTP_200_OK)
