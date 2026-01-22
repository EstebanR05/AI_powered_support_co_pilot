from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class TicketCategory(str, Enum):
    TECHNICAL = "Técnico"
    BILLING = "Facturación" 
    COMMERCIAL = "Comercial"
    SUPPORT = "Soporte"

class TicketSentiment(str, Enum):
    POSITIVE = "Positivo"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negativo"

@dataclass
class Ticket:
    """
    Entidad principal del dominio: Ticket de soporte
    Aplica Domain Driven Design principles
    """
    id: UUID
    description: str
    created_at: datetime
    category: Optional[TicketCategory] = None
    sentiment: Optional[TicketSentiment] = None
    processed: bool = False
    confidence_score: Optional[float] = None
    processing_time: Optional[float] = None
    
    @classmethod
    def create(cls, description: str) -> "Ticket":
        """Factory method para crear un nuevo ticket"""
        return cls(
            id=uuid4(),
            description=description,
            created_at=datetime.utcnow(),
            processed=False
        )
    
    def mark_as_processed(
        self, 
        category: TicketCategory, 
        sentiment: TicketSentiment,
        confidence: float,
        processing_time: float
    ) -> None:
        """Business rule: Marcar ticket como procesado"""
        self.category = category
        self.sentiment = sentiment
        self.confidence_score = confidence
        self.processing_time = processing_time
        self.processed = True
    
    def is_negative_sentiment(self) -> bool:
        """Business rule: Verificar si requiere notificación"""
        return self.sentiment == TicketSentiment.NEGATIVE
    
    def to_dict(self) -> dict:
        """Serialization helper"""
        return {
            "id": str(self.id),
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "category": self.category.value if self.category else None,
            "sentiment": self.sentiment.value if self.sentiment else None,
            "processed": self.processed,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time
        }