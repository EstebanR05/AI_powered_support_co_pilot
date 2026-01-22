# 🧪 Testing Guide

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=src tests/
```

### Run Specific Test File
```bash
pytest tests/test_ticket_processing.py -v
```

## Test Structure

### Unit Tests
- **Domain Tests**: Test business logic in entities and value objects
- **Use Case Tests**: Test application layer orchestration
- **Adapter Tests**: Test external service integrations

### Integration Tests
- **API Tests**: Test HTTP endpoints
- **Database Tests**: Test repository implementations
- **End-to-End Tests**: Test complete workflows

## Test Data

### Example Ticket Descriptions for Testing

**Technical Category**:
- "The application crashes when I click the save button"
- "Getting 500 error when uploading files"
- "Database connection timeout errors"

**Billing Category**:
- "I was charged twice for my subscription"
- "Cannot update my payment method"
- "Need invoice for last month"

**Commercial Category**:
- "What are your enterprise pricing plans?"
- "Need information about bulk licenses"
- "Interested in custom features"

**Support Category**:
- "How do I reset my password?"
- "Need help setting up my account"
- "Where can I find the user manual?"

### Sentiment Examples

**Positive**:
- "Thank you for the excellent support!"
- "Great product, just need help with setup"
- "Appreciate your quick response"

**Neutral**:
- "I need to update my billing address"
- "How do I export my data?"
- "What are your business hours?"

**Negative**:
- "This is completely broken and unusable"
- "Very frustrated with the constant errors"
- "Worst customer service ever"

## Mock Configuration

### Environment Variables for Testing
```env
ENVIRONMENT=testing
OPENAI_API_KEY=test_key_for_mocking
SUPABASE_URL=test_url
SUPABASE_KEY=test_key
N8N_WEBHOOK_URL=http://test-webhook.com
```

### Running Tests Without External Dependencies
```bash
# Tests will automatically use in-memory database and mocked services
pytest tests/ -v
```