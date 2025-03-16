from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class GetAllProductUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()