import asyncio
from typing import Dict, List, Optional
from uuid import UUID
from src.ports.ticket_repository_port import TicketRepositoryPort
from src.domain.entities.ticket import Ticket

class InMemoryTicketRepository(TicketRepositoryPort):
    """
    Implementación en memoria para desarrollo y testing
    En producción se reemplazaría por SupabaseTicketRepository
    """
    
    def __init__(self):
        self._tickets: Dict[UUID, Ticket] = {}
        self._lock = asyncio.Lock()
    
    async def save(self, ticket: Ticket) -> Ticket:
        """Guardar nuevo ticket"""
        async with self._lock:
            self._tickets[ticket.id] = ticket
            return ticket
    
    async def find_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        """Buscar ticket por ID"""
        return self._tickets.get(ticket_id)
    
    async def find_unprocessed(self) -> List[Ticket]:
        """Buscar tickets no procesados"""
        return [ticket for ticket in self._tickets.values() if not ticket.processed]
    
    async def find_all(self) -> List[Ticket]:
        """Obtener todos los tickets"""
        return list(self._tickets.values())
    
    async def update(self, ticket: Ticket) -> Ticket:
        """Actualizar ticket existente"""
        async with self._lock:
            if ticket.id not in self._tickets:
                raise ValueError(f"Ticket with ID {ticket.id} not found")
            self._tickets[ticket.id] = ticket
            return ticket
    
    async def delete(self, ticket_id: UUID) -> bool:
        """Eliminar ticket"""
        async with self._lock:
            if ticket_id in self._tickets:
                del self._tickets[ticket_id]
                return True
            return False
    
    async def count(self) -> int:
        """Contar tickets"""
        return len(self._tickets)
    
    async def clear_all(self) -> None:
        """Limpiar todos los tickets (para testing)"""
        async with self._lock:
            self._tickets.clear()