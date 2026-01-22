from typing import List
from src.ports.ticket_repository_port import TicketRepositoryPort
from src.application.dto.ticket_dto import TicketResponse

class GetTicketsUseCase:
    """
    Caso de uso: Obtener lista de tickets
    """
    
    def __init__(self, ticket_repository: TicketRepositoryPort):
        self.ticket_repository = ticket_repository
    
    async def execute(self) -> List[TicketResponse]:
        """
        Obtener todos los tickets
        """
        tickets = await self.ticket_repository.find_all()
        return [
            TicketResponse(
                id=str(ticket.id),
                description=ticket.description,
                created_at=ticket.created_at.isoformat(),
                category=ticket.category.value if ticket.category else None,
                sentiment=ticket.sentiment.value if ticket.sentiment else None,
                processed=ticket.processed,
                confidence_score=ticket.confidence_score,
                processing_time=f"{ticket.processing_time:.2f}s" if ticket.processing_time else None
            )
            for ticket in tickets
        ]