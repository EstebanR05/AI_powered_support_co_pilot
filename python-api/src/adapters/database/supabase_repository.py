from typing import Dict, List, Optional
from uuid import UUID
from supabase import create_client, Client
from src.ports.ticket_repository_port import TicketRepositoryPort
from src.domain.entities.ticket import Ticket, TicketCategory, TicketSentiment
from datetime import datetime

class SupabaseTicketRepository(TicketRepositoryPort):
    """
    Implementación de repositorio usando Supabase
    Para producción
    """
    
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)
        self.table_name = "tickets"
    
    async def save(self, ticket: Ticket) -> Ticket:
        """Guardar nuevo ticket en Supabase"""
        try:
            data = {
                "id": str(ticket.id),
                "description": ticket.description,
                "created_at": ticket.created_at.isoformat(),
                "category": ticket.category.value if ticket.category else None,
                "sentiment": ticket.sentiment.value if ticket.sentiment else None,
                "processed": ticket.processed,
                "confidence_score": ticket.confidence_score,
                "processing_time": ticket.processing_time
            }
            
            result = self.client.table(self.table_name).insert(data).execute()
            return ticket
            
        except Exception as e:
            print(f"Error saving ticket to Supabase: {e}")
            raise
    
    async def find_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        """Buscar ticket por ID en Supabase"""
        try:
            result = self.client.table(self.table_name).select("*").eq("id", str(ticket_id)).execute()
            
            if result.data:
                return self._map_to_ticket(result.data[0])
            return None
            
        except Exception as e:
            print(f"Error finding ticket by ID: {e}")
            return None
    
    async def find_unprocessed(self) -> List[Ticket]:
        """Buscar tickets no procesados"""
        try:
            result = self.client.table(self.table_name).select("*").eq("processed", False).execute()
            return [self._map_to_ticket(data) for data in result.data]
            
        except Exception as e:
            print(f"Error finding unprocessed tickets: {e}")
            return []
    
    async def find_all(self) -> List[Ticket]:
        """Obtener todos los tickets"""
        try:
            result = self.client.table(self.table_name).select("*").order("created_at", desc=True).execute()
            return [self._map_to_ticket(data) for data in result.data]
            
        except Exception as e:
            print(f"Error finding all tickets: {e}")
            return []
    
    async def update(self, ticket: Ticket) -> Ticket:
        """Actualizar ticket en Supabase"""
        try:
            data = {
                "description": ticket.description,
                "category": ticket.category.value if ticket.category else None,
                "sentiment": ticket.sentiment.value if ticket.sentiment else None,
                "processed": ticket.processed,
                "confidence_score": ticket.confidence_score,
                "processing_time": ticket.processing_time
            }
            
            result = self.client.table(self.table_name).update(data).eq("id", str(ticket.id)).execute()
            return ticket
            
        except Exception as e:
            print(f"Error updating ticket: {e}")
            raise
    
    def _map_to_ticket(self, data: dict) -> Ticket:
        """Mapear datos de Supabase a entidad Ticket"""
        category = None
        if data.get("category"):
            category = TicketCategory(data["category"])
        
        sentiment = None
        if data.get("sentiment"):
            sentiment = TicketSentiment(data["sentiment"])
        
        return Ticket(
            id=UUID(data["id"]),
            description=data["description"],
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            category=category,
            sentiment=sentiment,
            processed=data.get("processed", False),
            confidence_score=data.get("confidence_score"),
            processing_time=data.get("processing_time")
        )