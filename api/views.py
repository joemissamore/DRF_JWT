from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import *
# from .models import UserSerialializer, User, MyTokenObtainPairSerializer
from .serializers import *
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework import permissions

# Create your views here.


class UserView(generics.ListAPIView):
    serializer_class = UserSerialializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class MyTokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(MyTokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer
