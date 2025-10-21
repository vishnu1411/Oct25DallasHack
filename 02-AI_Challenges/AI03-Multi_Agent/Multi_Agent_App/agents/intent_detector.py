from agents.base_agent import BaseAgent
from models.data_models import ConversationContext, AgentResponse, Intent, IntentType
from services.openai_service import OpenAIService
import re

class IntentDetectorAgent(BaseAgent):
    """Agent responsible for detecting user intent"""
    
    def __init__(self):
        super().__init__("IntentDetector")
        self.openai_service = OpenAIService()
    
    async def process(self, context: ConversationContext) -> AgentResponse:
        """Detect intent from user query"""
        try:
            self.log_info(f"Analyzing query: {context.user_query.text}")
            
            # Simple rule-based intent detection for demo
            intent = self._detect_intent_rules(context.user_query.text)
            
            # Store intent in context
            context.intent = intent
            
            self.log_info(f"Detected intent: {intent.type} (confidence: {intent.confidence})")
            
            return AgentResponse(
                agent_name=self.name,
                intent=intent,
                response_text=f"I understand you're looking for {intent.type.value}.",
                confidence=intent.confidence,
                metadata={"entities": intent.entities}
            )
            
        except Exception as e:
            self.log_error(f"Intent detection failed: {e}")
            return AgentResponse(
                agent_name=self.name,
                intent=Intent(type=IntentType.UNKNOWN, confidence=0.0),
                response_text="I'm having trouble understanding your request.",
                confidence=0.0
            )
    
    def _detect_intent_rules(self, query: str) -> Intent:
        """Simple rule-based intent detection"""
        query_lower = query.lower()
        
        # Product search keywords
        search_keywords = ['find', 'search', 'look for', 'show me', 'do you have']
        if any(keyword in query_lower for keyword in search_keywords):
            return Intent(
                type=IntentType.PRODUCT_SEARCH,
                confidence=0.9,
                entities={"search_term": query}
            )
        
        # Recommendation keywords
        rec_keywords = ['recommend', 'suggest', 'what should', 'best', 'popular']
        if any(keyword in query_lower for keyword in rec_keywords):
            return Intent(
                type=IntentType.RECOMMENDATION,
                confidence=0.85,
                entities={"preference": query}
            )
        
        # General inquiry keywords
        general_keywords = ['how', 'what', 'when', 'where', 'why', 'help', 'info']
        if any(keyword in query_lower for keyword in general_keywords):
            return Intent(
                type=IntentType.GENERAL_INQUIRY,
                confidence=0.7,
                entities={"question": query}
            )
        
        # Default to product search if unsure
        return Intent(
            type=IntentType.PRODUCT_SEARCH,
            confidence=0.5,
            entities={"search_term": query}
        )