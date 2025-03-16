from rest_framework.routers import DefaultRouter
from django.urls import path, include
from core_chatbot.application.interfaces.rest.product_view import ProductViewSet
from core_chatbot.application.interfaces.rest.sale_view import SaleViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"sales",SaleViewSet, basename="sales")
urlpatterns = [
    path('', include(router.urls)),
]