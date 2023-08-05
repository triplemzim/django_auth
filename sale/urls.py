from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sale.views import DepotViewSet, CustomerViewSet, ProductViewSet, SubcategoryViewSet

router = DefaultRouter()
router.register(r"depots", DepotViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"products", ProductViewSet)
router.register(r"subcategories", SubcategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]