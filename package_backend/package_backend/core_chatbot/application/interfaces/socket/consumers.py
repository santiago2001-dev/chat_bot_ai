import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core_chatbot.application.infraestructure.Deeep_seek_integration.deep_seek_gateway import DeppSeekIntegration
from core_chatbot.application.infraestructure.Sales.gateway.sales_gateway_data_base import SalesGatewayDataBase
from core_chatbot.application.infraestructure.helpers.build_grafic import SalesMetrics
from core_chatbot.application.infraestructure.product.gateway.products_gateway_dataBase import ProductsGatewayDataBase
from core_chatbot.application.use_cases.product.list_all_product import GetAllProductUseCase
from core_chatbot.application.use_cases.product.recomendation_product_use_case import recomendationUseCase
import re

class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_welcome_message()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        print("Acción recibida:", action)
        print("content", data.get("content"))

        action_handlers = {
            1: self.handle_view_products,
            2: self.handle_consult_stock,
            "get_assistance": self.handle_get_assistance,
            "3": lambda: self.handle_get_assistance_continue(data.get("content")),

        }

        handler = action_handlers.get(action, self.handle_invalid_option)
        await handler()

    async def send_welcome_message(self):
        options = {
            "message": "Bienvenido a Buy n Large Elige una opción 💻💻:",
            "options": [
                {"id": 1, "name": "Ver productos 📦"},
                {"id": 2, "name": "Consultar stock 📈"},
                {"id": 3, "name": "Salir ❌"},
            ],
        }
        await self.send_json(options)

    async def handle_view_products(self):
        products = await self.get_all_products()
        response = {
            "products": [{"id": p.id, "name": p.name, "price": str(p.price)} for p in products],
            "message": "¿Deseas ser asesorado por un agente sobre nuestros productos mas vendidos? 🤖",
            "options": [
                {"id": "get_assistance", "name": "Sí ✅"},
                {"id": "no", "name": "No ❌"},
            ],
        }
        await self.send_json(response)

    async def handle_consult_stock(self):
        chart_base64 = await SalesMetrics().generate_sales_chart()
        response = {"message": "Generated chart", "chart": chart_base64}
        await self.send_json(response)

    async def handle_get_assistance(self):
        recommendation = await self.get_recommendation_assistance()
        response = {"message": recommendation, "options": [{"id": 3, "name": "Escribe mas informacion para hacer la asesoria mas completa 📈"}]}
        await self.send_json(response)

    async def handle_get_assistance_continue(self, prompt):
        try:
            recommendation = await self.get_recommendation_assistance_conitnue(prompt)
            response = {"message": recommendation}

        except Exception as e:
            response = {"error": str(e)}
        await self.send_json(response)

    async def handle_invalid_option(self):
        await self.send_json({"message": "Opción no válida"})

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_all_products(self):
        repository = ProductsGatewayDataBase()
        use_case = GetAllProductUseCase(repository)
        return list(use_case.execute())

    @database_sync_to_async
    def get_recommendation_assistance(self):
        repository = SalesGatewayDataBase()
        deep_seek = DeppSeekIntegration()
        use_case = recomendationUseCase(deep_seek, repository)
        raw_response = use_case.execute()
        return self.clean_response(raw_response)


    @database_sync_to_async
    def get_recommendation_assistance_conitnue(self,prompt):
        repository = SalesGatewayDataBase()
        deep_seek = DeppSeekIntegration()
        use_case = recomendationUseCase(deep_seek, repository)
        message = use_case.interaction_ai(prompt)
        return self.clean_response(message)


    def clean_response(self, text):
        cleaned_text = re.sub(r"[^\w\s.,¿?¡!%#()\-]", "", text)
        return cleaned_text.strip()
