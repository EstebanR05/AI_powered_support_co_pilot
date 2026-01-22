import json
from typing import List, Set
from fastapi import WebSocket, WebSocketDisconnect
from src.ports.websocket_service_port import WebSocketServicePort
from src.domain.entities.ticket import Ticket

class WebSocketManager(WebSocketServicePort):
    """
    Manager para conexiones WebSocket
    Patrón Observer para notificaciones en tiempo real
    """
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Aceptar nueva conexión"""
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Desconectar cliente"""
        self.active_connections.discard(websocket)
        print(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast_ticket_update(self, ticket: Ticket) -> None:
        """
        Enviar actualización de ticket a todos los clientes
        """
        if not self.active_connections:
            return
            
        message = {
            "type": "ticket_update",
            "data": ticket.to_dict()
        }
        
        # Crear lista de conexiones para evitar modificación durante iteración
        connections_copy = list(self.active_connections)
        
        for connection in connections_copy:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error sending message to client: {e}")
                self.disconnect(connection)
    
    async def broadcast_message(self, message: dict):
        """
        Enviar mensaje personalizado a todos los clientes
        """
        if not self.active_connections:
            return
            
        connections_copy = list(self.active_connections)
        
        for connection in connections_copy:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                self.disconnect(connection)
    
    async def get_connected_clients_count(self) -> int:
        """
        Obtener número de clientes conectados
        """
        return len(self.active_connections)
    
    async def handle_client_message(self, websocket: WebSocket, data: str):
        """
        Procesar mensaje del cliente
        """
        try:
            message = json.loads(data)
            message_type = message.get("type")
            
            if message_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong", "timestamp": message.get("timestamp")}))
            elif message_type == "subscribe":
                # Cliente solicita suscribirse a actualizaciones
                await websocket.send_text(json.dumps({"type": "subscribed", "status": "success"}))
            else:
                print(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {data}")
        except Exception as e:
            print(f"Error handling client message: {e}")


# Singleton instance
websocket_manager = WebSocketManager()