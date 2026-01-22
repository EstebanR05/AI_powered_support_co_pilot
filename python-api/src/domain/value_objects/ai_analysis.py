from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AIAnalysisResult:
    """
    Value Object para el resultado del análisis de IA
    Inmutable y sin identidad propia
    """
    category: str
    sentiment: str
    confidence_score: float
    
    def __post_init__(self):
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
    
    def is_high_confidence(self) -> bool:
        """Business rule: Determinar si el análisis es confiable"""
        return self.confidence_score >= 0.8

@dataclass(frozen=True) 
class TicketProcessingRequest:
    """
    Value Object para la solicitud de procesamiento
    """
    ticket_id: str
    description: str
    
    def __post_init__(self):
        if not self.description.strip():
            raise ValueError("Description cannot be empty")
        if len(self.description) > 5000:
            raise ValueError("Description is too long")

@dataclass(frozen=True)
class NotificationPayload:
    """
    Value Object para notificaciones
    """
    ticket_id: str
    message: str
    severity: str = "high"
    
    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "message": self.message,
            "severity": self.severity
        }