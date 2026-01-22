import time
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from src.infrastructure.config.container import get_container, Container
from src.application.dto.ticket_dto import (
    ProcessTicketRequest, 
    ProcessTicketResponse, 
    TicketResponse,
    HealthCheckResponse
)
from src.domain.value_objects.ai_analysis import TicketProcessingRequest

router = APIRouter()

# Dependency injection
def get_process_ticket_use_case(container: Container = Depends(get_container)):
    return container.process_ticket_use_case

def get_get_tickets_use_case(container: Container = Depends(get_container)):
    return container.get_tickets_use_case

def get_websocket_service(container: Container = Depends(get_container)):
    return container.websocket_service

@router.post("/process-ticket", response_model=ProcessTicketResponse)
async def process_ticket(
    request: ProcessTicketRequest,
    use_case = Depends(get_process_ticket_use_case)
):
    """
    Endpoint principal: Procesar ticket con IA
    """
    try:
        # Convert DTO to domain value object
        domain_request = TicketProcessingRequest(
            ticket_id=request.ticket_id,
            description=request.description
        )
        
        result = await use_case.execute(domain_request)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/tickets", response_model=List[TicketResponse])
async def get_tickets(
    use_case = Depends(get_get_tickets_use_case)
):
    """
    Obtener todos los tickets
    """
    try:
        tickets = await use_case.execute()
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tickets: {str(e)}")

@router.get("/health", response_model=HealthCheckResponse)
async def health_check(container: Container = Depends(get_container)):
    """
    Health check endpoint con información de servicios
    """
    start_time = time.time()
    
    # Check services
    services = {
        "database": "healthy",
        "ai_service": "healthy",
        "websocket": "healthy"
    }
    
    try:
        # Check AI service
        if container.settings.has_gemini_config:
            ai_info = container.ai_service.get_model_info()
            services["ai_service"] = f"healthy - {ai_info['model']}"
        else:
            services["ai_service"] = "not configured"
        
        # Check notification service
        notification_healthy = await container.notification_service.health_check()
        services["notification"] = "healthy" if notification_healthy else "unavailable"
        
        # Check WebSocket connections
        ws_count = await container.websocket_service.get_connected_clients_count()
        services["websocket"] = f"healthy - {ws_count} connections"
        
    except Exception as e:
        services["error"] = str(e)
    
    uptime = time.time() - start_time
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        services=services,
        uptime=uptime
    )

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    container: Container = Depends(get_container)
):
    """
    WebSocket endpoint para comunicación en tiempo real
    """
    websocket_service = container.websocket_service
    
    await websocket_service.connect(websocket)
    
    try:
        while True:
            # Recibir mensajes del cliente
            data = await websocket.receive_text()
            
            # Procesar mensaje
            await websocket_service.handle_client_message(websocket, data)
            
    except WebSocketDisconnect:
        websocket_service.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        websocket_service.disconnect(websocket)