import time
import asyncio
from typing import Optional
from uuid import UUID
from datetime import datetime

from src.ports.ticket_repository_port import TicketRepositoryPort
from src.ports.ai_service_port import AIServicePort
from src.ports.notification_service_port import NotificationServicePort
from src.ports.websocket_service_port import WebSocketServicePort

from src.domain.entities.ticket import Ticket, TicketCategory, TicketSentiment
from src.domain.value_objects.ai_analysis import TicketProcessingRequest, NotificationPayload
from src.application.dto.ticket_dto import ProcessTicketResponse

class ProcessTicketUseCase:
    """
    Caso de uso principal: Procesar ticket con IA
    Orquesta todas las operaciones necesarias
    """
    
    def __init__(
        self,
        ticket_repository: TicketRepositoryPort,
        ai_service: AIServicePort,
        notification_service: NotificationServicePort,
        websocket_service: WebSocketServicePort
    ):
        self.ticket_repository = ticket_repository
        self.ai_service = ai_service
        self.notification_service = notification_service
        self.websocket_service = websocket_service
    
    async def execute(self, request: TicketProcessingRequest) -> ProcessTicketResponse:
        """
        Ejecutar el procesamiento completo del ticket
        """
        start_time = time.time()
        
        try:
            # 1. Buscar o crear el ticket
            ticket = await self._get_or_create_ticket(request)
            
            # 2. Analizar con IA
            ai_result = await self.ai_service.analyze_ticket(request.description)
            
            # 3. Mapear resultados a enums del dominio
            category = self._map_category(ai_result.category)
            sentiment = self._map_sentiment(ai_result.sentiment)
            
            # 4. Actualizar ticket
            processing_time = time.time() - start_time
            ticket.mark_as_processed(category, sentiment, ai_result.confidence_score, processing_time)
            
            # 5. Persistir cambios
            updated_ticket = await self.ticket_repository.update(ticket)
            
            # 6. Enviar notificación si es negativo
            notification_sent = False
            if ticket.is_negative_sentiment():
                notification_sent = await self._send_notification(ticket)
            
            # 7. Actualizar WebSocket
            await self.websocket_service.broadcast_ticket_update(updated_ticket)
            
            # 8. Retornar respuesta
            return ProcessTicketResponse(
                ticket_id=str(ticket.id),
                category=category.value,
                sentiment=sentiment.value,
                confidence=ai_result.confidence_score,
                processed=True,
                processing_time=f"{processing_time:.2f}s",
                notification_sent=notification_sent
            )
            
        except Exception as e:
            # Log error and re-raise
            print(f"Error processing ticket: {e}")
            raise
    
    async def _get_or_create_ticket(self, request: TicketProcessingRequest) -> Ticket:
        """Buscar ticket existente o crear uno nuevo"""
        try:
            ticket_uuid = UUID(request.ticket_id)
            existing_ticket = await self.ticket_repository.find_by_id(ticket_uuid)
            if existing_ticket:
                return existing_ticket
        except ValueError:
            pass  # Invalid UUID format, create new ticket
        
        # Crear nuevo ticket
        new_ticket = Ticket.create(request.description)
        return await self.ticket_repository.save(new_ticket)
    
    def _map_category(self, ai_category: str) -> TicketCategory:
        """Mapear categoría de IA a enum del dominio"""
        mapping = {
            "Técnico": TicketCategory.TECHNICAL,
            "Facturación": TicketCategory.BILLING,
            "Comercial": TicketCategory.COMMERCIAL,
            "Soporte": TicketCategory.SUPPORT
        }
        return mapping.get(ai_category, TicketCategory.SUPPORT)
    
    def _map_sentiment(self, ai_sentiment: str) -> TicketSentiment:
        """Mapear sentimiento de IA a enum del dominio"""
        mapping = {
            "Positivo": TicketSentiment.POSITIVE,
            "Neutral": TicketSentiment.NEUTRAL,
            "Negativo": TicketSentiment.NEGATIVE
        }
        return mapping.get(ai_sentiment, TicketSentiment.NEUTRAL)
    
    async def _send_notification(self, ticket: Ticket) -> bool:
        """Enviar notificación para sentimientos negativos"""
        try:
            payload = NotificationPayload(
                ticket_id=str(ticket.id),
                message=f"Ticket {ticket.id} requires immediate attention - Negative sentiment detected",
                severity="high"
            )
            return await self.notification_service.send_notification(payload)
        except Exception as e:
            print(f"Failed to send notification: {e}")
            return False