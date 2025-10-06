from agents.base_agent import BaseAgent
from models.data_models import ConversationContext, AgentResponse, IntentType
from services.azure_search_service import AzureSearchService

class InventoryAgent(BaseAgent):
    """Agent responsible for searching product inventory"""
    
    def __init__(self):
        super().__init__("InventoryAgent")
        self.search_service = AzureSearchService()
    
    async def process(self, context: ConversationContext) -> AgentResponse:
        """Search for products based on user intent"""
        try:
            if not context.intent or context.intent.type != IntentType.PRODUCT_SEARCH:
                return AgentResponse(
                    agent_name=self.name,
                    response_text="No product search needed for this query.",
                    confidence=1.0
                )
            
            search_term = self._extract_search_term(context)
            self.log_info(f"Searching for: {search_term}")
            
            # Perform search
            search_results = await self.search_service.search_products(
                query=search_term,
                max_results=10
            )
            
            # Store results in context
            context.search_results = search_results
            
            if search_results.products:
                response_text = f"Found {len(search_results.products)} products matching '{search_term}'"
                confidence = 0.9
            else:
                response_text = f"No products found for '{search_term}'"
                confidence = 0.3
            
            self.log_info(f"Search completed: {len(search_results.products)} products found")
            
            return AgentResponse(
                agent_name=self.name,
                search_results=search_results,
                response_text=response_text,
                confidence=confidence,
                metadata={"search_method": search_results.search_method}
            )
            
        except Exception as e:
            self.log_error(f"Product search failed: {e}")
            return AgentResponse(
                agent_name=self.name,
                response_text="I'm having trouble searching for products right now.",
                confidence=0.0
            )
    
    def _extract_search_term(self, context: ConversationContext) -> str:
        """Extract search term from context"""
        if context.intent and context.intent.entities:
            return context.intent.entities.get("search_term", context.user_query.text)
        return context.user_query.text
    
    async def close(self):
        """Close search service connection"""
        await self.search_service.close()