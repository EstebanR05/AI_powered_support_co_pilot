import json
import time
import google.generativeai as genai
from typing import Optional
from src.ports.ai_service_port import AIServicePort
from src.domain.value_objects.ai_analysis import AIAnalysisResult
from src.domain.entities.ticket import TicketCategory, TicketSentiment

class GeminiAdapter(AIServicePort):
    """
    Adaptador para Google Gemini
    Implementa el puerto de servicio de IA
    """
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-exp"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
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
        Analizar ticket usando Google Gemini
        """
        try:
            prompt = self._prompt_template.format(description=description)
            
            start_time = time.time()
            response = await self._call_gemini_async(prompt)
            processing_time = time.time() - start_time
            
            # Parse response
            result = self._parse_response(response)
            
            return AIAnalysisResult(
                category=result["category"],
                sentiment=result["sentiment"], 
                confidence=result["confidence"],
                processing_time=processing_time
            )
            
        except Exception as e:
            print(f"Error en análisis Gemini: {str(e)}")
            # Fallback a valores por defecto
            return AIAnalysisResult(
                category=TicketCategory.SUPPORT.value,
                sentiment=TicketSentiment.NEUTRAL.value,
                confidence=0.5,
                processing_time=0.0
            )
    
    async def _call_gemini_async(self, prompt: str) -> str:
        """
        Llamada asíncrona a Gemini
        """
        # Gemini no tiene cliente async nativo, simulamos con run_in_executor
        import asyncio
        loop = asyncio.get_event_loop()
        
        def sync_call():
            response = self.model.generate_content(prompt)
            return response.text
        
        return await loop.run_in_executor(None, sync_call)
    
    def _parse_response(self, response: str) -> dict:
        """
        Parse y validación de respuesta JSON
        """
        try:
            # Limpiar response si viene con markdown
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
            result = json.loads(clean_response.strip())
            
            # Validar campos requeridos
            required_fields = ["category", "sentiment", "confidence"]
            if not all(field in result for field in required_fields):
                raise ValueError("Missing required fields in response")
            
            # Validar categorías
            valid_categories = ["Técnico", "Facturación", "Comercial", "Soporte"]
            if result["category"] not in valid_categories:
                result["category"] = "Soporte"
            
            # Validar sentimientos
            valid_sentiments = ["Positivo", "Neutral", "Negativo"]
            if result["sentiment"] not in valid_sentiments:
                result["sentiment"] = "Neutral"
            
            # Validar confidence
            confidence = float(result["confidence"])
            if not 0.0 <= confidence <= 1.0:
                result["confidence"] = 0.5
            
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error parsing Gemini response: {str(e)}")
            # Fallback response
            return {
                "category": "Soporte",
                "sentiment": "Neutral", 
                "confidence": 0.5
            }
    
    def get_model_info(self) -> dict:
        """
        Información del modelo
        """
        return {
            "provider": "Google",
            "model": self.model.model_name if hasattr(self.model, 'model_name') else "gemini-2.0-flash-exp",
            "version": "2.0"
        }