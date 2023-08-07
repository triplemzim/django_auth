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

class BalanceSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields['customer'] = CustomerSerializer(read_only=True)
        return super().to_representation(instance)
    

    class Meta:
        model = Balance
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        self.fields['depot'] = DepotSerializer(read_only=True)
        return super().to_representation(instance)

    class Meta:
        model = Stock
        fields = '__all__'