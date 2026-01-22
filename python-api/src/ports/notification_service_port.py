from abc import ABC, abstractmethod
from src.domain.value_objects.ai_analysis import NotificationPayload

class NotificationServicePort(ABC):
    """
    Puerto para servicios de notificación
    Permite intercambiar implementaciones (email, webhook, etc.)
    """
    
    @abstractmethod
    async def send_notification(self, payload: NotificationPayload) -> bool:
        """
        Enviar notificación
        Retorna True si fue exitoso
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verificar si el servicio está disponible
        """
        pass