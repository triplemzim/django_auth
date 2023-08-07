from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sale.views import DepotViewSet, CustomerViewSet, ProductViewSet, SubcategoryViewSet, BalanceViewSet, StockViewSet

router = DefaultRouter()
router.register(r"depots", DepotViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"products", ProductViewSet)
router.register(r"subcategories", SubcategoryViewSet)
router.register(r"balance", BalanceViewSet)
router.register(r"stock", StockViewSet)

urlpatterns = [
    path("", include(router.urls)),
]