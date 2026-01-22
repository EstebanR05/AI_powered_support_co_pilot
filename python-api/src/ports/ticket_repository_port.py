from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.entities.ticket import Ticket

class TicketRepositoryPort(ABC):
    """
    Puerto para persistencia de tickets
    Define el contrato sin implementación
    """
    
    @abstractmethod
    async def save(self, ticket: Ticket) -> Ticket:
        """Guardar un ticket"""
        pass
    
    @abstractmethod
    async def find_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        """Buscar ticket por ID"""
        pass
    
    @abstractmethod
    async def find_unprocessed(self) -> List[Ticket]:
        """Buscar tickets no procesados"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Ticket]:
        """Obtener todos los tickets"""
        pass
    
    @abstractmethod
    async def update(self, ticket: Ticket) -> Ticket:
        """Actualizar un ticket"""
        pass