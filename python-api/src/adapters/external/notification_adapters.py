import httpx
from src.ports.notification_service_port import NotificationServicePort
from src.domain.value_objects.ai_analysis import NotificationPayload

class N8nWebhookAdapter(NotificationServicePort):
    """
    Adaptador para notificaciones via n8n webhook
    """
    
    def __init__(self, webhook_url: str, timeout: int = 10):
        self.webhook_url = webhook_url
        self.timeout = timeout
    
    async def send_notification(self, payload: NotificationPayload) -> bool:
        """
        Enviar notificación via webhook a n8n
        """
        if not self.webhook_url or self.webhook_url == "your_n8n_webhook_url_here":
            print("n8n webhook URL not configured, skipping notification")
            return False
            
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload.to_dict(),
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code in [200, 201, 202]:
                    print(f"Notification sent successfully to n8n: {payload.ticket_id}")
                    return True
                else:
                    print(f"Failed to send notification. Status: {response.status_code}")
                    return False
                    
        except httpx.TimeoutException:
            print("Timeout sending notification to n8n")
            return False
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    async def health_check(self) -> bool:
        """
        Verificar si n8n está disponible
        """
        if not self.webhook_url or self.webhook_url == "your_n8n_webhook_url_here":
            return False
            
        try:
            # Enviar ping simple
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(self.webhook_url.replace('/webhook/', '/health'))
                return response.status_code == 200
        except:
            return False


class EmailNotificationAdapter(NotificationServicePort):
    """
    Adaptador para notificaciones por email (simulado)
    """
    
    def __init__(self, smtp_config: dict = None):
        self.smtp_config = smtp_config or {}
    
    async def send_notification(self, payload: NotificationPayload) -> bool:
        """
        Simular envío de email
        """
        print(f"📧 EMAIL SENT - Ticket: {payload.ticket_id}, Message: {payload.message}")
        return True
    
    async def health_check(self) -> bool:
        """
        Verificar servicio de email
        """
        return True