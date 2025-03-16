from core_chatbot.application.domain.models import Venta
from core_chatbot.application.domain.repositorys.sales_repository import SaleRepository


class SalesGatewayDataBase(SaleRepository):
    def get_all(self):
        return Venta.objects.select_related("product").all()
