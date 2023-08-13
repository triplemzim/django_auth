from rest_framework import serializers, viewsets
from .models import *
from django.db import transaction

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


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceWithLineItemsSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, source='lineitem')
    
    class Meta:
        model = Invoice
        fields = '__all__'

    # def get(self, instance):
    #     data = super().to_representation(instance)
    #     line_items = LineItem.objects.filter(invoice=instance)
    #     line_item_data = LineItemSerializer(line_items, many=True).data
    #     data['line_items'] = line_item_data
    #     return data

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user


    @transaction.atomic
    def create(self, validated_data):
        print('Working on invoice create')
        line_items_data = validated_data.pop('lineitem')
        invoice = Invoice.objects.create(**validated_data)

        Balance.objects.create(invoice=invoice, customer=invoice.customer, 
                                category='Debit', transaction_id=uuid.uuid4(),
                                entry_user=self._user(), amount=invoice.payment_amount)

        Balance.objects.create(invoice=invoice, customer=invoice.customer, 
                                category='Credit', transaction_id=uuid.uuid4(),
                                entry_user=self._user(), 
                                amount=invoice.total_amount - invoice.payment_amount)

        for line_item_data in line_items_data:
            line_item = LineItem.objects.create(invoice=invoice, **line_item_data)
            self.update_stock(line_item.product, 0, line_item.quantity, line_item.invoice.customer.depot)

        return invoice

    @transaction.atomic
    def update(self, instance, validated_data):
        print('Working on invoice update')
        line_items_data = validated_data.pop('lineitem')
        instance = super().update(instance, validated_data)

        debit_balance = Balance.objects.filter(invoice=instance, category='Debit').first()
        credit_balance = Balance.objects.filter(invoice=instance, category='Credit').first()

        debit_balance.amount = instance.payment_amount
        debit_balance.save()
        credit_balance.amount = instance.total_amount - instance.payment_amount
        credit_balance.save()

        old_line_items = LineItem.objects.filter(invoice=instance)
        for line_item in old_line_items:
            self.update_stock(line_item.product, line_item.quantity, 0, instance.customer.depot)
            line_item.delete()

        for line_item in line_items_data:
            line_item = LineItem.objects.create(invoice=instance, **line_item)
            self.update_stock(line_item.product, 0, line_item.quantity, line_item.invoice.customer.depot)

        return instance

    @transaction.atomic
    def update_stock(self, product, old_quantity, new_quantity, depot):
        try:
            stock, created = Stock.objects.get_or_create(product=product, depot=depot)
            stock.quantity += old_quantity
            stock.quantity -= new_quantity
            
            if stock.quantity < 0:
                raise serializers.ValidationError(f"Not enough stock available for product {product} in depot {depot}")

            stock.save()
        except Stock.DoesNotExist:
            raise serializers.ValidationError(f"No stock available for product {product} in depot {depot}")