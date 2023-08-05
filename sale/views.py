from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework import generics
from rest_framework.filters import SearchFilter

class DepotViewSet(ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "code"]

class SubcategoryViewSet(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer 
    filter_backends = [SearchFilter]
    search_fields = ["name"]

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    filter_backends = [SearchFilter]
    search_fields = ["name", "category_name", "code", "category_id"]

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer 
    filter_backends = [SearchFilter]
    search_fields = ["name", "depot", "code"]