import logging
import requests
from agents.base_agent import BaseAgent
from models.data_models import ConversationContext, AgentResponse, Product
from services.azure_search_service import AzureSearchService
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class AlternativesAgent(BaseAgent):
    """Agent responsible for finding alternative products with smart search logic"""
    
    def __init__(self):
        super().__init__("AlternativesAgent")
        self.search_service = AzureSearchService()
        self.alternatives_function_url = "https://recommend-func-cbcsahh8g5a7hnga.swedencentral-01.azurewebsites.net/api/GetRecommendations"
        self.session_context = {}  # Will be set by orchestrator
        
        # Smart product mappings to prevent bad matches
        self.smart_mappings = {
            "Camera": {
                "exact_matches": ["Camera"],
                "related_categories": ["Electronics"],
                "related_products": ["Surface Pro", "Microsoft Mouse", "USB-C Hub"],
                "avoid_terms": ["bag", "card", "drive"]  # Don't match these
            },
            "Memory Card": {
                "exact_matches": ["Memory Card", "SD Card"],
                "related_categories": ["Hardware", "Accessories"],
                "related_products": ["SSD Drive", "USB-C Hub"],
                "avoid_terms": ["graphics", "mouse", "router"]  # Don't match graphics card
            },
            "Lantern": {
                "exact_matches": ["Lantern", "Light", "Lamp"],
                "related_categories": ["Electronics"],
                "related_products": ["Router", "Microsoft Mouse"],  # Tech products only
                "avoid_terms": ["bag", "clothing", "book"]  # Never match bags/clothes
            }
        }
    
    def set_session_context(self, session_context: Dict):
        """Receive session context from orchestrator"""
        self.session_context = session_context
    
    async def process(self, context: ConversationContext) -> AgentResponse:
        """Find smart alternatives with session awareness"""
        try:
            # Only run if there are no search results from inventory
            if context.search_results and context.search_results.products:
                return AgentResponse(
                    agent_name=self.name,
                    response_text="No alternatives needed - products found in inventory.",
                    confidence=1.0,
                    metadata={"alternatives_needed": False}
                )
            
            # Extract product name from user query
            product_name = self._extract_product_name(context.user_query.text)
            self.log_info(f"Looking for smart alternatives to: '{product_name}'")
            
            # Check if this is a follow-up request for different alternatives
            is_follow_up = self._is_follow_up_request(context.user_query.text)
            if is_follow_up:
                self.log_info("Detected follow-up request - will provide different alternatives")
            
            # Get suggestions from Azure Function
            suggestions = await self._call_alternatives_function(product_name)
            self.log_info(f"Azure Function returned: {suggestions}")
            
            # Find smart alternatives with session awareness
            all_alternatives = await self._find_smart_alternatives(suggestions, is_follow_up)
            
            if all_alternatives:
                response_text = self._format_smart_response(product_name, all_alternatives, is_follow_up)
                return AgentResponse(
                    agent_name=self.name,
                    response_text=response_text,
                    confidence=0.9,
                    metadata={
                        "alternatives_found": len(all_alternatives),
                        "search_term": product_name,
                        "alternatives": all_alternatives,
                        "source": "smart_search",
                        "function_suggestions": suggestions,
                        "is_follow_up": is_follow_up
                    }
                )
            else:
                return AgentResponse(
                    agent_name=self.name,
                    response_text=f"I couldn't find suitable alternatives for '{product_name}'. Our inventory focuses on routers, electronics, and tech accessories.",
                    confidence=0.3,
                    metadata={
                        "alternatives_found": 0,
                        "search_term": product_name,
                        "function_suggestions": suggestions
                    }
                )
            
        except Exception as e:
            self.log_error(f"Error finding alternatives: {e}")
            return AgentResponse(
                agent_name=self.name,
                response_text="I encountered an issue while looking for alternatives. Please try again.",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    def _extract_product_name(self, query: str) -> str:
        """Extract and clean product name from query"""
        query_lower = query.lower()
        
        # Handle follow-up requests
        if "something else" in query_lower or "different" in query_lower or "alternative" in query_lower:
            # Try to extract the original product from session context
            if self.session_context.get("alternative_requests"):
                last_request = self.session_context["alternative_requests"][-1]
                return self._extract_product_name(last_request.get("query", query))
        
        # Remove common phrases
        remove_phrases = [
            "do you have", "show me", "find me", "search for", "looking for",
            "in stock", "available", "any", "some", "get me", "i want", "i need",
            "something else", "different", "alternative", "other"
        ]
        
        for phrase in remove_phrases:
            query_lower = query_lower.replace(phrase, "")
        
        # Clean and return
        import re
        clean_query = re.sub(r'[^\w\s]', '', query_lower).strip()
        clean_query = ' '.join(clean_query.split())
        
        return clean_query if clean_query else "general products"
    
    def _is_follow_up_request(self, query: str) -> bool:
        """Check if this is a follow-up request for different alternatives"""
        follow_up_indicators = [
            "something else", "different", "alternative", "other options",
            "what else", "show me more", "anything else", "other products"
        ]
        return any(indicator in query.lower() for indicator in follow_up_indicators)
    
    async def _find_smart_alternatives(self, suggestions: List[str], is_follow_up: bool) -> List[Dict[str, Any]]:
        """Find smart alternatives using enhanced logic"""
        all_alternatives = []
        products_already_shown = self.session_context.get("products_shown", set())
        
        for suggestion in suggestions:
            self.log_info(f"Processing suggestion: '{suggestion}' with smart mapping")
            
            # Get smart mapping for this suggestion
            mapping = self.smart_mappings.get(suggestion, {
                "exact_matches": [suggestion],
                "related_categories": ["Electronics", "Hardware"],
                "related_products": ["Router", "USB-C Hub"],
                "avoid_terms": []
            })
            
            # Try exact matches first
            for exact_term in mapping.get("exact_matches", []):
                results = await self._smart_search_products(exact_term, mapping.get("avoid_terms", []))
                if results:
                    for result in results[:2]:  # Max 2 per exact match
                        if result["name"] not in products_already_shown or is_follow_up:
                            result["match_type"] = f"Exact match for {suggestion}"
                            result["original_suggestion"] = suggestion
                            all_alternatives.append(result)
                            self.log_info(f"Added exact match: {result['name']}")
            
            # If no exact matches or follow-up request, try related products
            if not all_alternatives or is_follow_up:
                for related_product in mapping.get("related_products", []):
                    if len(all_alternatives) >= 5:  # Limit total results
                        break
                    
                    results = await self._smart_search_products(related_product, mapping.get("avoid_terms", []))
                    if results:
                        for result in results[:1]:  # Max 1 per related product
                            if result["name"] not in products_already_shown or is_follow_up:
                                result["match_type"] = f"Related to {suggestion} ({related_product})"
                                result["original_suggestion"] = suggestion
                                all_alternatives.append(result)
                                self.log_info(f"Added related product: {result['name']}")
                                break
        
        # Ensure diversity and filter out already shown products for follow-ups
        if is_follow_up:
            all_alternatives = [alt for alt in all_alternatives if alt["name"] not in products_already_shown]
        
        return self._ensure_smart_diversity(all_alternatives)[:5]
    
    async def _smart_search_products(self, search_term: str, avoid_terms: List[str]) -> List[Dict[str, Any]]:
        """Search with smart filtering to avoid bad matches"""
        try:
            search_results = await self.search_service.search_products(
                query=search_term,
                max_results=10  # Get more to filter
            )
            
            smart_results = []
            if search_results and search_results.products:
                for product in search_results.products:
                    # Check if product name contains avoid terms
                    product_name_lower = product.name.lower()
                    should_avoid = any(avoid_term in product_name_lower for avoid_term in avoid_terms)
                    
                    if not should_avoid:
                        result = {
                            "name": product.name,
                            "category": product.category,
                            "price": product.price,
                            "description": getattr(product, 'description', ''),
                            "reason": f"Smart match for {search_term}"
                        }
                        smart_results.append(result)
                        self.log_info(f"Smart search found: {product.name} (${product.price})")
                    else:
                        self.log_info(f"Avoided bad match: {product.name} (contains avoid terms)")
            
            return smart_results
            
        except Exception as e:
            self.log_error(f"Smart search failed for '{search_term}': {e}")
            return []
    
    def _ensure_smart_diversity(self, alternatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure diverse product types with smart logic"""
        diverse_list = []
        category_count = {}
        base_name_count = {}
        
        for alt in alternatives:
            category = alt.get("category", "Unknown")
            product_name = alt.get("name", "Unknown")
            base_name = product_name.split()[0]  # First word
            
            # Limit per category and base name
            cat_count = category_count.get(category, 0)
            base_count = base_name_count.get(base_name, 0)
            
            if cat_count < 3 and base_count < 2:  # Max 3 per category, 2 per base name
                diverse_list.append(alt)
                category_count[category] = cat_count + 1
                base_name_count[base_name] = base_count + 1
        
        return diverse_list
    
    async def _call_alternatives_function(self, product_name: str) -> List[str]:
        """Call Azure Function - same as before"""
        try:
            clean_product = product_name.title()
            params = {"product": clean_product}
            
            response = requests.get(
                self.alternatives_function_url,
                params=params,
                timeout=15,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and "suggestions" in data:
                        suggestions = data["suggestions"]
                        if isinstance(suggestions, list):
                            return suggestions
                except json.JSONDecodeError as e:
                    self.log_error(f"JSON decode error: {e}")
            
        except Exception as e:
            self.log_error(f"Function call failed: {e}")
        
        return []
    
    def _format_smart_response(self, original_product: str, alternatives: List[Dict[str, Any]], is_follow_up: bool) -> str:
        """Format response with session awareness"""
        if not alternatives:
            return f"I couldn't find suitable alternatives for '{original_product}'."
        
        if is_follow_up:
            intro = f"Here are some different alternatives for '{original_product}' that I haven't shown you yet:"
        else:
            intro = f"I don't have '{original_product}' in stock, but here are some smart alternatives:"
        
        response_parts = [intro]
        
        for i, alt in enumerate(alternatives, 1):
            name = alt.get("name", "Unknown Product")
            price = alt.get("price", 0)
            category = alt.get("category", "")
            match_type = alt.get("match_type", "Related product")
            
            if price > 0:
                response_parts.append(f"\n{i}. {name} - ${price:.2f}")
            else:
                response_parts.append(f"\n{i}. {name}")
            
            response_parts.append(f"   Category: {category}")
            response_parts.append(f"   Why: {match_type}")
        
        session_info = ""
        if self.session_context.get("products_shown"):
            shown_count = len(self.session_context["products_shown"])
            session_info = f"\n\n🧠 In this session, I've shown you {shown_count} different products total."
        
        response_parts.append(session_info)
        return "".join(response_parts)