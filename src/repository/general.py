from abc import ABC, abstractmethod
from typing import Dict, Any

from pydantic import BaseModel


class Repository(ABC):
    @abstractmethod
    def create(self, payload: Any):
        pass

    @abstractmethod
    def read_all(self):
        pass
    
    @abstractmethod
    def read_one(self, id: int):
        pass

    @abstractmethod
    def update(self, id: int, payload: Any):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

