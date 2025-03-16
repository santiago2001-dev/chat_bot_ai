class ListByIdUseCaseProduct:
    def __init__(self, repository):
        self.repository = repository

    def execute(self,product_id):
        return self.repository.get_by_id(product_id)
