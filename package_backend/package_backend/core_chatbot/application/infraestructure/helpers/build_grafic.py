import matplotlib
matplotlib.use('Agg')  # Establecer backend antes de importar pyplot
import matplotlib.pyplot as plt
import io
import base64

from channels.db import database_sync_to_async
from django.db.models import QuerySet
from core_chatbot.application.domain.models import Venta


class SalesMetrics:
    @database_sync_to_async
    def generate_sales_chart(self):
        sales: QuerySet[Venta] = Venta.objects.all()

        if not sales.exists():
            return ""  # Return an empty string if no data exists

        products = [sale.product.name for sale in sales]
        quantities = [sale.quantity for sale in sales]

        plt.figure(figsize=(8, 5))
        plt.bar(products, quantities, color=['blue', 'green', 'red', 'purple'])
        plt.xlabel("Productos")
        plt.ylabel("Unidades vendidas")
        plt.title(" Ventas destacadas de nuestros productos")
        plt.xticks(rotation=45)

        # Save the image to an in-memory buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches="tight")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()

        # Encode the image as Base64
        return base64.b64encode(image_png).decode('utf-8')
