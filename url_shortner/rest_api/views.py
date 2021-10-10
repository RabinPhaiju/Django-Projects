from django.shortcuts import render
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentSerializer
from .models import Student
from rest_framework.permissions import IsAuthenticated

class StudentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        data = Student.objects.all()
        serializer = StudentSerializer(data,many=True)
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)