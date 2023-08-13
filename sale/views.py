from .serializers import *
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from .models import *
from rest_framework.filters import SearchFilter

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .pagination import *

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

class BalanceViewSet(ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    filter_backends = [SearchFilter]
    search_fields = ["customer__name", "transaction_id", "customer__code", "customer__depot__name", "customer__depot__code"]

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [SearchFilter]
    search_fields = ["product__name", "product__code", "depot__name", "depot__code"]

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [SearchFilter]
    search_fields = ["custom_invoice_id", "cutomer_id__name", "payment_status"]

class LineItemViewSet(ModelViewSet):
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ["invoice__custom_invoice_id"]

class FullInvoiceView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceWithLineItemsSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        invoice = instance
        line_items = LineItem.objects.filter(invoice=invoice)
        for line_item in line_items:
            self.replenish_stock(line_item.product, line_item.quantity, invoice.customer.depot)
            line_item.delete()

        invoice.delete()

        return Response({'message': 'Invoice and associated LineItems deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    @transaction.atomic
    def replenish_stock(self, product, quantity, depot):
        stock, created = Stock.objects.get_or_create(product=product, depot=depot)
        stock.quantity += quantity
        stock.save()
    
    

# class CreateInvoiceWithLineItems(APIView):
#     @transaction.atomic
#     def post(self, request, format=None):
#         invoice_data = request.data.get('invoice')
#         line_items_data = request.data.get('line_items')

#         # Create an Invoice instance
#         invoice_serializer = InvoiceSerializer(data=invoice_data)
#         if invoice_serializer.is_valid():
#             invoice_instance = invoice_serializer.save()
#         else:
#             return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Create LineItem instances and associate them with the Invoice
#         line_item_instances = []
#         for line_item_data in line_items_data:
#             line_item_data['invoice'] = invoice_instance.pk
#             line_item_serializer = LineItemSerializer(data=line_item_data)

#             if line_item_serializer.is_valid():
#                 line_item_instances.append(line_item_serializer.save())
#             else:
#                 error_message = {'message': 'Error creating line item', 'errors': line_item_serializer.errors}
#                 return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'message': 'Invoice and LineItems created successfully'}, status=status.HTTP_201_CREATED)

# Optional APIView
class InvoiceDetailAPIView(APIView):

    def get(self, request, invoice_id, format=None):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'message': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        
        line_items = LineItem.objects.filter(invoice=invoice)

        invoice_serializer = InvoiceSerializer(invoice)
        line_items_serializer = LineItemSerializer(line_items, many=True)

        response_data = {
            'invoice': invoice_serializer.data,
            'line_items': line_items_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def put(self, request, invoice_id, format=None):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'message': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        
        invoice_serializer = InvoiceSerializer(instance=invoice, data=request.data.get('invoice'))
        if invoice_serializer.is_valid():
            invoice_instance = invoice_serializer.save()
        else:
            return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        line_items_data = request.data.get('line_items')
        LineItem.objects.filter(invoice=invoice_instance).delete()  # Delete existing line items
        
        line_item_instances = []
        for line_item_data in line_items_data:
            line_item_data['invoice'] = invoice_instance.pk
            line_item_serializer = LineItemSerializer(data=line_item_data)
            if line_item_serializer.is_valid():
                line_item_instances.append(line_item_serializer.save())
            else:
                error_message = {'message': 'Error creating line item', 'errors': line_item_serializer.errors}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Invoice and LineItems updated successfully'}, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def delete(self, request, invoice_id, format=None):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'message': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        line_items = LineItem.objects.filter(invoice=invoice)
        for line_item in line_items:
            self.replenish_stock(line_item.product, line_item.quantity, invoice.customer.depot)
            line_item.delete()

        invoice.delete()

        return Response({'message': 'Invoice and associated LineItems deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    @transaction.atomic
    def replenish_stock(self, product, quantity, depot):
        stock = Stock.objects.get_or_create(product=product, depot=depot)
        stock.quantity += quantity
        stock.save()
                
