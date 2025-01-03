from rest_framework import viewsets
from .models import Server,Category
from .serializer import ServerSerializer,CategorySerializer
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.exceptions import ValidationError,AuthenticationFailed

class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_serverid = request.query_params.get('by_serverid')
        with_num_members = request.query_params.get('with_num_members') == 'true'


        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed(detail='You must be logged in to access this resource')  

        if category:
            self.queryset = Server.objects.filter(category_name=category) # this is for accessing the category name
            # self.queryset = Server.objects.filter(category=category)  this is for accessing the category only
        

        if by_user:
            user_id = request.user.id
            self.queryset = Server.objects.filter(members=user_id)

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('members'))
        
        if qty:
            self.queryset = self.queryset[:int(qty)]
        
        if by_serverid:
            try:
                self.queryset= self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f'Server with id {by_serverid} does not exist')
            except ValueError:
                raise ValidationError(detail='Invalid server id')
            
        serializer = ServerSerializer(self.queryset, many=True,context = {"num_members":with_num_members})
        return Response(serializer.data)

class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    def list(self,request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

