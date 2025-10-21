# Multi-Agent Retail Assistant

A sophisticated multi-agent system built with Python for retail customer assistance, integrating Azure Cognitive Search and Azure OpenAI services.

## Architecture

The system consists of 4 specialized agents:

1. **IntentDetectorAgent** - Analyzes user queries to determine intent
2. **InventoryAgent** - Searches product inventory using Azure Cognitive Search
3. **RecommendationsAgent** - Generates product recommendations
4. **ResponseFormatterAgent** - Creates natural language responses using Azure OpenAI

## Features

- 🤖 Multi-agent conversational AI
- 🔍 Advanced product search with multiple fallback strategies
- 💡 Intelligent product recommendations
- 🎨 Beautiful console interface with Rich
- ⚡ Async/await for optimal performance
- 🧪 Comprehensive testing framework
- 📝 Detailed logging and conversation tracking

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure Services

Update the `.env` file with your Azure credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_openai_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2023-12-01-preview

# Azure Search Configuration  
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your_search_api_key_here
AZURE_SEARCH_INDEX=retail-index
```

### 3. Run the Application

**Interactive Mode:**
```bash
python main.py
```

**Test Mode:**
```bash
python test_app.py
```

**Run Tests:**
```bash
pytest tests/
```

## Project Structure

```
Multi_Agent_App/
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py
├── models/                 # Data models and schemas
│   ├── __init__.py
│   └── data_models.py
├── services/               # External service integrations
│   ├── __init__.py
│   ├── azure_search_service.py
│   └── openai_service.py
├── agents/                 # Multi-agent system
│   ├── __init__.py
│   ├── base_agent.py
│   ├── intent_detector.py
│   ├── inventory_agent.py
│   ├── recommendations_agent.py
│   └── response_formatter.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── helpers.py
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_services.py
├── main.py                 # Main application
├── test_app.py            # Simple test script
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## Usage Examples

### Basic Product Search
```
User: "I'm looking for running shoes"
Assistant: I found several running shoes in our inventory...
```

### Product Recommendations
```
User: "Can you recommend some good headphones?"
Assistant: Based on your preferences, I recommend these headphones...
```

### General Inquiries
```
User: "What's your return policy?"
Assistant: I can help you with information about our policies...
```

## Agent Pipeline Flow

1. **User Input** → Intent Detection
2. **Intent** → Inventory Search (if product-related)
3. **Search Results** → Recommendation Generation
4. **All Context** → Natural Language Response

## Configuration

The application uses environment variables for configuration. Key settings include:

- **Azure OpenAI**: Endpoint, API key, model deployment
- **Azure Search**: Endpoint, API key, index name
- **Application**: Log level, retry settings, timeouts

## Testing

Run the test suite:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v tests/
```

## Logging

The application logs conversations and system events to:
- Console output (configurable level)
- Log file: `multi_agent_app.log`

## Error Handling

- Graceful fallback for service failures
- Retry mechanisms with exponential backoff
- Comprehensive error logging
- User-friendly error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.