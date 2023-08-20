from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sale.views import *

router = DefaultRouter()
router.register(r"depots", DepotViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"products", ProductViewSet)
router.register(r"subcategories", SubcategoryViewSet)
router.register(r"balance", BalanceViewSet)
router.register(r"stock", StockViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'lineitems', LineItemViewSet)
router.register(r'fullinvoice', FullInvoiceView, basename='invoicewithlineitem')

urlpatterns = [
    # path('create-invoice-lineitems/', CreateInvoiceWithLineItems.as_view(), name='create-invoice-lineitems'),
    path('invoice-detail/<int:invoice_id>/', InvoiceDetailAPIView.as_view(), name='invoice-detail'),
    path("", include(router.urls)),
]