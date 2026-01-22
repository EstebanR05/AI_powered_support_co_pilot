from abc import ABC, abstractmethod
from src.domain.value_objects.ai_analysis import AIAnalysisResult

class AIServicePort(ABC):
    """
    Puerto para servicios de IA
    Abstrae la implementación específica del LLM
    """
    
    @abstractmethod
    async def analyze_ticket(self, description: str) -> AIAnalysisResult:
        """
        Analizar un ticket y retornar categoría y sentimiento
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Obtener información del modelo utilizado
        """
        pass