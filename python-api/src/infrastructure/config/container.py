from functools import lru_cache
from src.infrastructure.config.settings import get_settings

# Ports
from src.ports.ticket_repository_port import TicketRepositoryPort
from src.ports.ai_service_port import AIServicePort
from src.ports.notification_service_port import NotificationServicePort
from src.ports.websocket_service_port import WebSocketServicePort

# Adapters
from src.adapters.database.in_memory_repository import InMemoryTicketRepository
from src.adapters.database.supabase_repository import SupabaseTicketRepository
from src.adapters.ai.openai_adapter import OpenAIAdapter
from src.adapters.external.notification_adapters import N8nWebhookAdapter, EmailNotificationAdapter
from src.adapters.external.websocket_adapter import websocket_manager

# Use Cases
from src.application.use_cases.process_ticket_use_case import ProcessTicketUseCase
from src.application.use_cases.get_tickets_use_case import GetTicketsUseCase

class Container:
    """
    Dependency Injection Container
    Patrón Dependency Injection manual
    """
    
    def __init__(self):
        self.settings = get_settings()
        self._ticket_repository = None
        self._ai_service = None
        self._notification_service = None
        self._websocket_service = None
        self._process_ticket_use_case = None
        self._get_tickets_use_case = None
    
    @property
    def ticket_repository(self) -> TicketRepositoryPort:
        """Lazy loading del repositorio de tickets"""
        if self._ticket_repository is None:
            if self.settings.use_in_memory_db or not self.settings.has_supabase_config:
                print("Using in-memory database")
                self._ticket_repository = InMemoryTicketRepository()
            else:
                print("Using Supabase database")
                self._ticket_repository = SupabaseTicketRepository(
                    url=self.settings.supabase_url,
                    key=self.settings.supabase_service_key or self.settings.supabase_key
                )
        return self._ticket_repository
    
    @property
    def ai_service(self) -> AIServicePort:
        """Lazy loading del servicio de IA"""
        if self._ai_service is None:
            if not self.settings.has_openai_config:
                raise ValueError("OpenAI API key not configured")
            
            self._ai_service = OpenAIAdapter(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_model
            )
        return self._ai_service
    
    @property
    def notification_service(self) -> NotificationServicePort:
        """Lazy loading del servicio de notificaciones"""
        if self._notification_service is None:
            if self.settings.n8n_webhook_url and self.settings.n8n_webhook_url != "your_n8n_webhook_url_here":
                print("Using n8n webhook notifications")
                self._notification_service = N8nWebhookAdapter(self.settings.n8n_webhook_url)
            else:
                print("Using email notification fallback")
                self._notification_service = EmailNotificationAdapter()
        return self._notification_service
    
    @property
    def websocket_service(self) -> WebSocketServicePort:
        """Servicio WebSocket (singleton)"""
        if self._websocket_service is None:
            self._websocket_service = websocket_manager
        return self._websocket_service
    
    @property
    def process_ticket_use_case(self) -> ProcessTicketUseCase:
        """Caso de uso principal"""
        if self._process_ticket_use_case is None:
            self._process_ticket_use_case = ProcessTicketUseCase(
                ticket_repository=self.ticket_repository,
                ai_service=self.ai_service,
                notification_service=self.notification_service,
                websocket_service=self.websocket_service
            )
        return self._process_ticket_use_case
    
    @property
    def get_tickets_use_case(self) -> GetTicketsUseCase:
        """Caso de uso para obtener tickets"""
        if self._get_tickets_use_case is None:
            self._get_tickets_use_case = GetTicketsUseCase(
                ticket_repository=self.ticket_repository
            )
        return self._get_tickets_use_case

# Global container instance
@lru_cache()
def get_container() -> Container:
    """
    Obtener instancia singleton del container
    """
    return Container()