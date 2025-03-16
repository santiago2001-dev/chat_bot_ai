from rest_framework import serializers

from core_chatbot.application.domain.models import Product, Stock, Venta


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Serializa el objeto completo

    class Meta:
        model = Venta
        fields = '__all__'
