class ListByNameUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self,name):
        return self.repository.get_by_name(name)
