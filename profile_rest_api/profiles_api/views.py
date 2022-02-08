from email import message
from multiprocessing import AuthenticationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from profiles_api import models,permissions,serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.settings import api_settings


# Create your views here.
class HelloApiView(APIView):
    
    serializer_class = serializers.HelloSerializer
    
    def get(self,request,format=None):
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete',
            'Is similar to a traditional Django VIew',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message':'Hello!','an_apiview':an_apiview})

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hell0 {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk=None):
        """Handle updating an object"""
        return Response({'method':'PUT'})

    def patch(self,request,pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})
    
    def delete(self,request,pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})
    
    
class HelloViewSet(viewsets.ViewSet):
    
    serializer_class = serializers.HelloSerializer
    
    def list(self,request):
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]
        return Response({'message':'hello','a_viewset':a_viewset})
    
    def create(self,request):  
        serializer = self.serializer_class(data=request.data)
        
        if(serializer.is_valid()):
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def retrive(self,request,pk = None):
        """Handle getting an object by tis Id"""
        return Response({'method':'Get'})

    def update(self,request, pk=None):
        """Handle updating an object"""
        return Response({'method':'put'})    
    
    def partial_update(self,request, pk=None):
        """Handle updating part of an object"""
        return Response({'method':'patch'})

    def destroy(self,requst,pk=None):
        """Remove the object"""
        return Response({'method':'delete'})
        

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,) # comment
    permission_classes = (permissions.UpdateOwnProfile,) # comment
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email') 

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating, reading and updating profile feed items"""
    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnStatus,
        # IsAuthenticated, # authenticated users can only see their own feed
        IsAuthenticatedOrReadOnly # everyone see their own feed
    )
    queryset = models.ProfileFeedItem.objects.all()
    
    def perform_create(self, serializer):
        '''Sets the user profile to the logged in user'''
        serializer.save(user_profile=self.request.user)