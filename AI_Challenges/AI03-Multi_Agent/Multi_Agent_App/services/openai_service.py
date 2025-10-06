import asyncio
from typing import Dict, Any, List
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # Fix: Use AZURE_OPENAI_KEY instead of AZURE_OPENAI_API_KEY
        logger.info("OpenAI service initialized (mock mode)")
    
    async def generate_response(self, messages: List[Dict[str, str]], 
                              temperature: float = 0.7) -> str:
        """Mock response generation for testing"""
        try:
            logger.info(f"Generating response for {len(messages)} messages")
            
            # Simple mock response based on the last user message
            if messages:
                last_message = messages[-1].get('content', '')
                if 'router' in last_message.lower():
                    return "I'd be happy to help you find the perfect router! Based on your needs, I can recommend several excellent options from our inventory."
                elif 'price' in last_message.lower():
                    return "I can help you find routers within your budget. What price range are you considering?"
                else:
                    return "Thank you for your inquiry. I'm here to help you find exactly what you're looking for."
            
            return "Thank you for your inquiry. I'm here to help you find exactly what you're looking for."
            
        except Exception as e:
            logger.error(f"Mock response generation failed: {e}")
            return "I apologize, but I'm having trouble generating a response right now."

    async def detect_intent(self, user_query: str) -> Dict[str, Any]:
        """Mock intent detection for testing"""
        try:
            logger.info(f"Detecting intent for: {user_query}")
            
            # Simple keyword-based intent detection
            query_lower = user_query.lower()
            
            if any(word in query_lower for word in ['find', 'search', 'look for', 'show me']):
                return {
                    "intent": "product_search",
                    "confidence": 0.9,
                    "entities": {"product_type": user_query}
                }
            elif any(word in query_lower for word in ['recommend', 'suggest', 'best']):
                return {
                    "intent": "recommendation",
                    "confidence": 0.85,
                    "entities": {"preference": user_query}
                }
            else:
                return {
                    "intent": "general_inquiry",
                    "confidence": 0.7,
                    "entities": {"question": user_query}
                }
                
        except Exception as e:
            logger.error(f"Mock intent detection failed: {e}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": {}
            }

    async def format_response(self, context: Dict[str, Any]) -> str:
        """Mock response formatting for testing"""
        try:
            logger.info("Formatting response with context")
            return "I've processed your request and here's what I found for you."
            
        except Exception as e:
            logger.error(f"Mock response formatting failed: {e}")
            return "I apologize, but I'm having trouble formatting the response right now."