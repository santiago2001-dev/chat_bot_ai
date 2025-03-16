class UseCaseGetAllSales:
    def __init__(self, sales_repo):
        self.sales_repo = sales_repo

    def execute(self):
        return self.sales_repo.get_all()