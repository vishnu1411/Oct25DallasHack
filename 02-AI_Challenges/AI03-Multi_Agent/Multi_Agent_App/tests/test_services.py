import pytest
from unittest.mock import Mock, patch
from services.azure_search_service import AzureSearchService
from services.openai_service import OpenAIService

class TestAzureSearchService:
    @pytest.mark.asyncio
    async def test_search_initialization(self):
        # Mock the Azure credentials to avoid actual API calls
        with patch('services.azure_search_service.SearchClient'):
            service = AzureSearchService()
            assert service.client is not None

class TestOpenAIService:
    @pytest.mark.asyncio
    async def test_service_initialization(self):
        # Mock the OpenAI client to avoid actual API calls
        with patch('services.openai_service.AsyncAzureOpenAI'):
            service = OpenAIService()
            assert service.client is not None

    @pytest.mark.asyncio
    async def test_detect_intent(self):
        with patch('services.openai_service.AsyncAzureOpenAI'):
            service = OpenAIService()
            
            # Mock the response
            with patch.object(service, 'generate_response') as mock_generate:
                mock_generate.return_value = '{"intent": "product_search", "confidence": 0.8}'
                
                result = await service.detect_intent("I want to buy shoes")
                
                assert result["intent"] == "product_search"
                assert result["confidence"] == 0.8