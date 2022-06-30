from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import status

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *
from .renderers import *


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class UserLogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        default_error_messages = {
            'bad_token': 'Token is expired or invalid'
        }
        if serializer.is_valid(raise_exception=True):
            token = request.data.get('tokens').get('refresh')
            try:
                token = RefreshToken(token)
                token.blacklist()
            except TokenError:
                return Response(default_error_messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemDetail(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ItemListView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Item.objects.none()
        if q is not None:
            results = qs.search(q)
        return results


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.data.get('user_id')
        obj = Order.objects.filter(created_by=user_id)
        serializer = OrderSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
