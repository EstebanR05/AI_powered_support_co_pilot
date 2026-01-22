from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.ticket import Ticket

class WebSocketServicePort(ABC):
    """
    Puerto para comunicación en tiempo real
    """
    
    @abstractmethod
    async def broadcast_ticket_update(self, ticket: Ticket) -> None:
        """
        Enviar actualización de ticket a todos los clientes conectados
        """
        pass
    
    @abstractmethod
    async def get_connected_clients_count(self) -> int:
        """
        Obtener número de clientes conectados
        """
        pass