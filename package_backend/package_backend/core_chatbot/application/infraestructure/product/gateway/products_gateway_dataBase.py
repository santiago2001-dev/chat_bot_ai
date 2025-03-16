from core_chatbot.application.domain.models import Product
from core_chatbot.application.domain.repositorys.prodcuts_repository import ProductRepository


class ProductsGatewayDataBase(ProductRepository):
    def get_by_id(self, product_id):
        product = Product.objects.get(id=product_id)
        products = [product]
        return products

    def get_by_name(self, name):
        product =  Product.objects.get(name=name)
        products = [product]
        return products

    def get_all(self):
        return Product.objects.all()
