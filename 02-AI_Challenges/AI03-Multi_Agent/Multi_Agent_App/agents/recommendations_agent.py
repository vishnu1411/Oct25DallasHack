from agents.base_agent import BaseAgent
from models.data_models import ConversationContext, AgentResponse, Recommendation, IntentType
from typing import List
import random

class RecommendationsAgent(BaseAgent):
    """Agent responsible for generating product recommendations"""
    
    def __init__(self):
        super().__init__("RecommendationsAgent")
    
    async def process(self, context: ConversationContext) -> AgentResponse:
        """Generate product recommendations"""
        try:
            recommendations = []
            
            if context.intent and context.intent.type == IntentType.RECOMMENDATION:
                recommendations = self._generate_recommendations_by_intent(context)
            elif context.search_results and context.search_results.products:
                recommendations = self._generate_recommendations_by_search(context)
            
            # Store recommendations in context
            context.recommendations = recommendations
            
            if recommendations:
                response_text = f"I have {len(recommendations)} recommendations for you."
                confidence = 0.85
            else:
                response_text = "I don't have specific recommendations at the moment."
                confidence = 0.3
            
            self.log_info(f"Generated {len(recommendations)} recommendations")
            
            return AgentResponse(
                agent_name=self.name,
                recommendations=recommendations,
                response_text=response_text,
                confidence=confidence
            )
            
        except Exception as e:
            self.log_error(f"Recommendation generation failed: {e}")
            return AgentResponse(
                agent_name=self.name,
                response_text="I'm having trouble generating recommendations right now.",
                confidence=0.0
            )
    
    def _generate_recommendations_by_intent(self, context: ConversationContext) -> List[Recommendation]:
        """Generate recommendations based on user intent"""
        recommendations = []
        
        if context.search_results and context.search_results.products:
            # Take top 3 products as recommendations
            for product in context.search_results.products[:3]:
                recommendations.append(
                    Recommendation(
                        product=product,
                        reason="Based on your search preferences",
                        confidence=0.8
                    )
                )
        
        return recommendations
    
    def _generate_recommendations_by_search(self, context: ConversationContext) -> List[Recommendation]:
        """Generate recommendations based on search results"""
        recommendations = []
        
        if context.search_results and context.search_results.products:
            # Select top products and add recommendation reasoning
            for i, product in enumerate(context.search_results.products[:3]):
                reasons = [
                    "Highly rated product",
                    "Popular choice",
                    "Great value for money",
                    "Best seller in category"
                ]
                
                recommendations.append(
                    Recommendation(
                        product=product,
                        reason=random.choice(reasons),
                        confidence=max(0.6, 0.9 - i * 0.1)  # Decreasing confidence
                    )
                )
        
        return recommendations