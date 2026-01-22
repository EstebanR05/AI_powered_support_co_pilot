import pytest
from unittest.mock import AsyncMock
from src.domain.entities.ticket import Ticket, TicketCategory, TicketSentiment
from src.domain.value_objects.ai_analysis import TicketProcessingRequest, AIAnalysisResult
from src.application.use_cases.process_ticket_use_case import ProcessTicketUseCase

@pytest.mark.asyncio
async def test_process_ticket_use_case():
    """
    Test del caso de uso principal
    """
    # Arrange
    mock_repo = AsyncMock()
    mock_ai_service = AsyncMock()
    mock_notification = AsyncMock()
    mock_websocket = AsyncMock()
    
    # Setup mocks
    test_ticket = Ticket.create("Test ticket description")
    
    # Configure repository mock to return None for find_by_id (new ticket)
    mock_repo.find_by_id.return_value = None
    mock_repo.save.return_value = test_ticket
    mock_repo.update.return_value = test_ticket
    
    mock_ai_service.analyze_ticket.return_value = AIAnalysisResult(
        category="Técnico",
        sentiment="Negativo", 
        confidence_score=0.9
    )
    
    mock_notification.send_notification.return_value = True
    
    use_case = ProcessTicketUseCase(
        ticket_repository=mock_repo,
        ai_service=mock_ai_service,
        notification_service=mock_notification,
        websocket_service=mock_websocket
    )
    
    # Act
    request = TicketProcessingRequest(
        ticket_id="new-ticket-id",  # Use string that's not a valid UUID
        description="Test ticket description"
    )
    
    result = await use_case.execute(request)
    
    # Assert
    assert result.category == "Técnico"
    assert result.sentiment == "Negativo"
    assert result.confidence == 0.9
    assert result.processed is True
    assert result.notification_sent is True
    
    # Verify calls
    mock_ai_service.analyze_ticket.assert_called_once_with("Test ticket description")
    mock_notification.send_notification.assert_called_once()
    mock_websocket.broadcast_ticket_update.assert_called_once()

def test_ticket_entity():
    """
    Test de la entidad Ticket
    """
    # Test creation
    ticket = Ticket.create("Test description")
    
    assert ticket.description == "Test description"
    assert ticket.processed is False
    assert ticket.category is None
    assert ticket.sentiment is None
    
    # Test processing
    ticket.mark_as_processed(
        TicketCategory.TECHNICAL,
        TicketSentiment.NEGATIVE,
        0.95,
        1.5
    )
    
    assert ticket.processed is True
    assert ticket.category == TicketCategory.TECHNICAL
    assert ticket.sentiment == TicketSentiment.NEGATIVE
    assert ticket.confidence_score == 0.95
    assert ticket.processing_time == 1.5
    assert ticket.is_negative_sentiment() is True

def test_ai_analysis_value_object():
    """
    Test del value object AIAnalysisResult
    """
    # Valid analysis
    analysis = AIAnalysisResult(
        category="Técnico",
        sentiment="Positivo",
        confidence_score=0.85
    )
    
    assert analysis.category == "Técnico"
    assert analysis.sentiment == "Positivo"
    assert analysis.confidence_score == 0.85
    assert analysis.is_high_confidence() is True
    
    # Invalid confidence score
    with pytest.raises(ValueError):
        AIAnalysisResult(
            category="Técnico",
            sentiment="Positivo", 
            confidence_score=1.5
        )