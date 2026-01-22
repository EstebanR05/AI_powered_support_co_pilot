import json
import time
from typing import Optional
from openai import AsyncOpenAI
from src.ports.ai_service_port import AIServicePort
from src.domain.value_objects.ai_analysis import AIAnalysisResult

class OpenAIAdapter(AIServicePort):
    """
    Adaptador para OpenAI GPT
    Implementa el puerto de servicio de IA
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self._prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> str:
        """
        Prompt Engineering optimizado para clasificación
        """
        return """
Eres un asistente especializado en análisis de tickets de soporte.
Analiza el siguiente ticket y devuelve un JSON con la categorización exacta.

Categorías disponibles:
- Técnico: Problemas de funcionamiento, errores, bugs
- Facturación: Cobros, pagos, facturas, precios
- Comercial: Ventas, productos, información general
- Soporte: Consultas de uso, guías, tutoriales

Sentimientos disponibles:
- Positivo: Cliente satisfecho, agradecido
- Neutral: Consulta informativa sin emociones
- Negativo: Frustración, enojo, insatisfacción

TICKET: "{description}"

Responde ÚNICAMENTE con un JSON válido en este formato exacto:
{{"category": "categoria", "sentiment": "sentimiento", "confidence": 0.95}}
"""
    
    async def analyze_ticket(self, description: str) -> AIAnalysisResult:
        """
        Analizar ticket usando OpenAI
        """
        try:
            prompt = self._prompt_template.format(description=description)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a ticket analysis expert. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.1  # Baja temperatura para consistencia
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                result = json.loads(content)
                return AIAnalysisResult(
                    category=result["category"],
                    sentiment=result["sentiment"],
                    confidence_score=float(result["confidence"])
                )
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # Fallback en caso de respuesta malformada
                print(f"Failed to parse AI response: {e}. Content: {content}")
                return self._create_fallback_result(description)
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._create_fallback_result(description)
    
    def _create_fallback_result(self, description: str) -> AIAnalysisResult:
        """
        Crear resultado por defecto en caso de error
        """
        # Simple keyword-based fallback
        description_lower = description.lower()
        
        # Determine category
        if any(word in description_lower for word in ["factura", "pago", "cobro", "precio"]):
            category = "Facturación"
        elif any(word in description_lower for word in ["error", "bug", "falla", "problema"]):
            category = "Técnico"
        elif any(word in description_lower for word in ["venta", "compra", "producto"]):
            category = "Comercial"
        else:
            category = "Soporte"
        
        # Determine sentiment
        if any(word in description_lower for word in ["gracias", "excelente", "perfecto", "genial"]):
            sentiment = "Positivo"
        elif any(word in description_lower for word in ["molesto", "terrible", "horrible", "enojado"]):
            sentiment = "Negativo"
        else:
            sentiment = "Neutral"
        
        return AIAnalysisResult(
            category=category,
            sentiment=sentiment,
            confidence_score=0.5  # Baja confianza para fallback
        )
    
    def get_model_info(self) -> dict:
        """
        Información del modelo utilizado
        """
        return {
            "provider": "OpenAI",
            "model": self.model,
            "type": "LLM",
            "version": "1.0"
        }