from agents.base_agent import BaseAgent
from models.data_models import ConversationContext, AgentResponse
from services.openai_service import OpenAIService
from typing import List, Dict

class ResponseFormatterAgent(BaseAgent):
    """Agent responsible for formatting final response to user"""
    
    def __init__(self):
        super().__init__("ResponseFormatter")
        self.openai_service = OpenAIService()
    
    async def process(self, context: ConversationContext) -> AgentResponse:
        """Format final response based on conversation context"""
        try:
            # Generate natural language response
            response_text = await self._generate_natural_response(context)
            
            self.log_info("Generated final response")
            
            return AgentResponse(
                agent_name=self.name,
                response_text=response_text,
                confidence=0.9,
                metadata=self._build_response_metadata(context)
            )
            
        except Exception as e:
            self.log_error(f"Response formatting failed: {e}")
            return AgentResponse(
                agent_name=self.name,
                response_text="I apologize, but I'm having trouble formatting my response.",
                confidence=0.0
            )
    
    async def _generate_natural_response(self, context: ConversationContext) -> str:
        """Generate natural language response using OpenAI"""
        # Build context for OpenAI
        system_prompt = """You are a helpful retail assistant. Based on the conversation context, 
        generate a natural, friendly response to the user. Include product information and 
        recommendations when available."""
        
        context_info = self._build_context_summary(context)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User query: {context.user_query.text}"},
            {"role": "assistant", "content": f"Context: {context_info}"}
        ]
        
        return await self.openai_service.generate_response(messages)
    
    def _build_context_summary(self, context: ConversationContext) -> str:
        """Build a summary of the conversation context"""
        summary_parts = []
        
        if context.intent:
            summary_parts.append(f"Intent: {context.intent.type.value}")
        
        if context.search_results and context.search_results.products:
            product_count = len(context.search_results.products)
            summary_parts.append(f"Found {product_count} products")
            
            # Add product details
            for product in context.search_results.products[:3]:  # Top 3
                summary_parts.append(f"- {product.name} (${product.price})")
        
        if context.recommendations:
            rec_count = len(context.recommendations)
            summary_parts.append(f"Generated {rec_count} recommendations")
        
        return ". ".join(summary_parts)
    
    def _build_response_metadata(self, context: ConversationContext) -> Dict:
        """Build metadata for the response"""
        metadata = {
            "has_intent": context.intent is not None,
            "has_search_results": context.search_results is not None,
            "has_recommendations": len(context.recommendations) > 0,
            "product_count": 0,
            "recommendation_count": len(context.recommendations)
        }
        
        if context.search_results:
            metadata["product_count"] = len(context.search_results.products)
            metadata["search_method"] = context.search_results.search_method
        
        return metadata