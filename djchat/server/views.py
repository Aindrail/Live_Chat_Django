from django.shortcuts import render
from rest_framework import viewsets
from .models import Server,Category
from .serializer import ServerSerializer,CategorySerializer
from rest_framework.response import Response

class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        if category:
            self.queryset = Server.objects.filter(category_name=category) # this is for accessing the category name
            # self.queryset = Server.objects.filter(category=category)  this is for accessing the category only
        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    def list(self,request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

