from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response

class HelloOrder(generics.GenericAPIView):
    def get(self,request):
        return Response(data={"message":"Hello Order"},status=status.HTTP_200_OK)