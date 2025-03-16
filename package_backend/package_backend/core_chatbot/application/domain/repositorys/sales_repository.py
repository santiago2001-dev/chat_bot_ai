from abc import ABC, abstractmethod

class SaleRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass