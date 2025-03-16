from core_chatbot.application.infraestructure.Deeep_seek_integration.deep_seek_gateway import DeppSeekIntegration


class recomendationUseCase:
    def __init__(self, depepse_integration: DeppSeekIntegration,sales_repo):
        self.depepse_integration = depepse_integration
        self.sales_repo = sales_repo

    def execute(self):
        sales = self.sales_repo.get_all()[:6]
        sales_list = list(
            map(lambda sale: f"{sale.product.name} - {sale.quantity} unidades - ${sale.total_price}", sales))

        prompt = (
                "Basado en esta lista de ventas de productos, ¿cuáles recomendarías por características de hardware "
                "a un cliente actuando como un asesor comercial?\n" + "\n".join(sales_list)
        )

        return self.interaction_ai(prompt)

    def interaction_ai(self,prompt):
        return self.depepse_integration.StartChat(prompt)

