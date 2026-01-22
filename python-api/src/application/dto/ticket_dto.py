from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CreateTicketRequest(BaseModel):
    description: str = Field(..., min_length=1, max_length=5000)

class ProcessTicketRequest(BaseModel):
    ticket_id: str = Field(..., description="UUID of the ticket to process")
    description: str = Field(..., min_length=1, max_length=5000)

class TicketResponse(BaseModel):
    id: str
    description: str
    created_at: str
    category: Optional[str] = None
    sentiment: Optional[str] = None
    processed: bool
    confidence_score: Optional[float] = None
    processing_time: Optional[str] = None

class ProcessTicketResponse(BaseModel):
    ticket_id: str
    category: str
    sentiment: str
    confidence: float
    processed: bool
    processing_time: str
    notification_sent: bool = False

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    services: dict
    uptime: float