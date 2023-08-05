from rest_framework import serializers, viewsets
from .models import *

class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory 
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    depot = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='depot-detail'
    )
    class Meta:
        model = Customer
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = "__all__"