class ProductAdapter:
    @staticmethod
    def adapt_product_data(data):
        return {
            "name": data.get("name"),
            "description": data.get("description"),
            "price": data.get("price"),
        }
