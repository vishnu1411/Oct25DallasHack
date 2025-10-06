import asyncio
import logging
from datetime import datetime
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Configuration and utilities
from config.settings import settings
from utils.helpers import setup_logging, validate_config, log_conversation

# Data models
from models.data_models import UserQuery, ConversationContext

# Agents
from agents.intent_detector import IntentDetectorAgent
from agents.inventory_agent import InventoryAgent
from agents.recommendations_agent import RecommendationsAgent
from agents.response_formatter import ResponseFormatterAgent
from agents.alternatives_agent import AlternativesAgent

# Initialize console for rich output
console = Console()

class MultiAgentOrchestrator:
    """Main orchestrator for the multi-agent system with persistent memory"""
    
    def __init__(self):
        self.intent_detector = IntentDetectorAgent()
        self.inventory_agent = InventoryAgent()
        self.recommendations_agent = RecommendationsAgent()
        self.response_formatter = ResponseFormatterAgent()
        self.alternatives_agent = AlternativesAgent()
        
        # Enhanced conversation memory
        self.conversation_history: List[Dict[str, any]] = []
        self.session_context = {
            "products_shown": set(),  # All products shown in this session
            "categories_explored": set(),  # Categories user has seen
            "alternative_requests": [],  # Track alternative requests
            "user_preferences": {},  # Learn user preferences
            "last_query_type": None,  # Track query patterns
            "last_search_query": None,  # Track the last actual search query
            "pending_action": None,  # Track pending actions like "show router options"
            "session_start": datetime.now()
        }
        
    def _is_confirmatory_response(self, user_query: str) -> bool:
        """Check if the user query is a confirmatory response (yes, no, sure, etc.)"""
        confirmatory_words = [
            "yes", "yeah", "yep", "sure", "ok", "okay", "please", "go ahead", 
            "show me", "no", "nope", "not now", "maybe later", "no thanks"
        ]
        
        query_lower = user_query.lower().strip()
        
        # Check if it's a short response that matches confirmatory patterns
        if len(query_lower.split()) <= 3:
            return any(word in query_lower for word in confirmatory_words)
        
        return False
    
    def _handle_confirmatory_response(self, user_query: str) -> str:
        """Handle confirmatory responses based on conversation context"""
        query_lower = user_query.lower().strip()
        
        # Positive confirmations
        positive_responses = ["yes", "yeah", "yep", "sure", "ok", "okay", "please", "go ahead", "show me"]
        is_positive = any(word in query_lower for word in positive_responses)
        
        if is_positive and self.session_context.get("pending_action"):
            # User confirmed they want to see the pending action
            pending_action = self.session_context["pending_action"]
            self.session_context["pending_action"] = None  # Clear the pending action
            return pending_action  # Return the actual query to search for
        
        # Negative responses
        negative_responses = ["no", "nope", "not now", "maybe later", "no thanks"]
        is_negative = any(word in query_lower for word in negative_responses)
        
        if is_negative:
            return "general_browse"  # Show general options
        
        # Default for unclear confirmations
        return user_query
    
    def _update_session_context(self, user_query: str, response: str, query_type: str, products: List = None):
        """Update session context with new information"""
        
        # Track products shown
        if products:
            for product in products:
                if isinstance(product, dict):
                    self.session_context["products_shown"].add(product.get("name", ""))
                else:
                    self.session_context["products_shown"].add(str(product))
        
        # Track categories
        if products:
            for product in products:
                if isinstance(product, dict) and product.get("category"):
                    self.session_context["categories_explored"].add(product["category"])
        
        # Track alternative requests
        if "alternative" in user_query.lower() or "something else" in user_query.lower() or "different" in user_query.lower():
            self.session_context["alternative_requests"].append({
                "query": user_query,
                "timestamp": datetime.now()
            })
        
        # Update last query type and search query
        self.session_context["last_query_type"] = query_type
        if query_type in ["found_products", "alternatives"] and not self._is_confirmatory_response(user_query):
            self.session_context["last_search_query"] = user_query
        
        # Add to conversation history with rich context
        self.conversation_history.append({
            "user": user_query,
            "assistant": response,
            "type": query_type,
            "timestamp": datetime.now(),
            "products_count": len(products) if products else 0,
            "session_turn": len(self.conversation_history) + 1
        })
        
        # Keep only last 10 exchanges to prevent memory bloat
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def _build_context_aware_query(self, user_query: str) -> str:
        """Build context-aware query based on conversation history"""
        
        # Handle confirmatory responses
        if self._is_confirmatory_response(user_query):
            console.print(f"[dim]🤖 Detected confirmatory response: '{user_query}'[/dim]")
            resolved_query = self._handle_confirmatory_response(user_query)
            if resolved_query != user_query:
                console.print(f"[dim]🧠 Resolved to action: '{resolved_query}'[/dim]")
                return resolved_query
        
        # Check for follow-up patterns
        follow_up_keywords = ["something else", "different", "alternative", "other options", "what else"]
        is_follow_up = any(keyword in user_query.lower() for keyword in follow_up_keywords)
        
        if is_follow_up and self.conversation_history:
            last_exchange = self.conversation_history[-1]
            context_query = f"User is asking for alternatives to previous suggestions. Original context: {last_exchange.get('user', '')}. New request: {user_query}. Avoid showing: {list(self.session_context['products_shown'])}"
            console.print(f"[dim]🧠 Context-aware query: Following up on previous suggestions[/dim]")
            return context_query
        
        return user_query
    
    async def process_query(self, user_query: str) -> str:
        """Process a user query with enhanced memory and context awareness"""
        try:
            console.print("🤔 Processing your request...")
            
            # Check if this is a general browse request
            if user_query == "general_browse":
                console.print("[dim]🧠 User declined specific search, showing general options[/dim]")
                # Show some general popular products
                general_response = "No problem! Here are some popular items from our inventory you might be interested in. Would you like to see routers, electronics, or accessories?"
                self._update_session_context(user_query, general_response, "general_browse", [])
                return general_response
            
            # Build context-aware query
            enhanced_query = self._build_context_aware_query(user_query)
            
            # Create conversation context with enhanced memory
            user_query_obj = UserQuery(text=enhanced_query)
            conversation_context = ConversationContext(
                user_query=user_query_obj,
                conversation_history=[
                    f"Turn {h['session_turn']}: {h['user']} -> {h['assistant'][:100]}..."
                    for h in self.conversation_history[-5:]  # Last 5 exchanges
                ]
            )
            
            # Add session context metadata
            if self.session_context["products_shown"]:
                console.print(f"[dim]💭 Session memory: {len(self.session_context['products_shown'])} products shown, {len(self.session_context['categories_explored'])} categories explored[/dim]")
            
            # Pass session context to alternatives agent
            self.alternatives_agent.set_session_context(self.session_context)
            
            # Step 1: Detect intent
            intent_result = await self.intent_detector.process(conversation_context)
            
            # Step 2: Search inventory
            inventory_result = await self.inventory_agent.process(conversation_context)
            search_results = conversation_context.search_results
            
            products_found = len(search_results.products) if search_results else 0
            
            console.print(f"[dim]🔍 Products found in inventory: {products_found}[/dim]")
            
            # FIXED LOGIC: Only go to alternatives if NO products found
            if products_found == 0:
                console.print("[yellow]🔍 No exact matches found, looking for alternatives...[/yellow]")
                alternatives_result = await self.alternatives_agent.process(conversation_context)
                
                if alternatives_result and alternatives_result.metadata.get("alternatives_found", 0) > 0:
                    # Extract products for session tracking
                    alternatives_products = alternatives_result.metadata.get("alternatives", [])
                    
                    # Update session context
                    self._update_session_context(user_query, alternatives_result.response_text, "alternatives", alternatives_products)
                    
                    # Log the conversation
                    log_conversation(user_query, alternatives_result.response_text)
                    
                    return alternatives_result.response_text
                else:
                    # Handle case where no alternatives found - but provide better context
                    if self.session_context["last_search_query"]:
                        fallback_response = f"I don't have specific alternatives for '{enhanced_query}'. However, I've shown you {len(self.session_context['products_shown'])} products in this session. Would you like me to show you something from our main categories: routers, electronics, or hardware?"
                    else:
                        fallback_response = "I couldn't find what you're looking for. Would you like me to show you some popular products from our inventory?"
                    
                    self._update_session_context(user_query, fallback_response, "no_alternatives", [])
                    return fallback_response
            
            else:
                # PRODUCTS FOUND - Show them!
                console.print(f"[green]✅ Found {products_found} products in stock![/green]")
                
                # Step 3: Get recommendations (enhance the found products)
                recommendations_result = await self.recommendations_agent.process(conversation_context)
                
                # Step 4: Format final response
                final_result = await self.response_formatter.process(conversation_context)
                
                # Extract products for session tracking
                found_products = []
                if search_results and search_results.products:
                    found_products = [{"name": p.name, "category": p.category, "price": p.price} for p in search_results.products]
                
                # Update session context
                self._update_session_context(user_query, final_result.response_text, "found_products", found_products)
                
                # Log the conversation
                log_conversation(user_query, final_result.response_text)
                
                return final_result.response_text
            
        except Exception as e:
            error_msg = f"Error processing query: {e}"
            console.print(f"[red]❌ {error_msg}[/red]")
            logging.error(error_msg)
            error_response = "I apologize, but I encountered an error while processing your request. Please try again."
            self._update_session_context(user_query, error_response, "error", [])
            return error_response
    
    def get_conversation_summary(self) -> str:
        """Get detailed conversation summary"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        session_duration = datetime.now() - self.session_context["session_start"]
        unique_products = len(self.session_context["products_shown"])
        categories = len(self.session_context["categories_explored"])
        alternative_requests = len(self.session_context["alternative_requests"])
        
        # Count different types of interactions
        found_product_queries = len([h for h in self.conversation_history if h.get("type") == "found_products"])
        alternative_queries = len([h for h in self.conversation_history if h.get("type") == "alternatives"])
        confirmatory_responses = len([h for h in self.conversation_history if self._is_confirmatory_response(h.get("user", ""))])
        
        summary = f"""
📊 Session Summary:
• Duration: {session_duration.total_seconds()/60:.1f} minutes
• Total queries: {len(self.conversation_history)}
• Found products queries: {found_product_queries}
• Alternative requests: {alternative_queries}
• Confirmatory responses: {confirmatory_responses}
• Unique products shown: {unique_products}
• Categories explored: {categories} ({', '.join(self.session_context['categories_explored']) if self.session_context['categories_explored'] else 'None'})
• Last search query: {self.session_context.get('last_search_query', 'None')}

📝 Recent conversation:
"""
        
        for exchange in self.conversation_history[-3:]:
            query_type = exchange.get('type', 'unknown')
            product_count = exchange.get('products_count', 0)
            summary += f"• [{query_type}] {exchange['user']} → ({product_count} products) {exchange['assistant'][:60]}...\n"
        
        return summary

def display_welcome():
    """Display welcome message and system info"""
    welcome_panel = Panel(
        """[bold blue]🤖 Multi-Agent Router Assistant[/bold blue]

I'm powered by multiple AI agents working together:
• [cyan]Intent Detector[/cyan] - Understands what you're looking for
• [green]Inventory Agent[/green] - Searches our router database  
• [yellow]Alternatives Agent[/yellow] - Finds similar products when items aren't available
• [magenta]Recommendations Agent[/magenta] - Suggests the best options
• [blue]Response Formatter[/blue] - Presents results clearly

[bold green]💭 ENHANCED: Smart Conversation Flow + Memory![/bold green]
✅ Understands confirmatory responses (yes, no, sure, okay)
✅ Remembers conversation context and pending actions
✅ Shows products when in stock, alternatives when out of stock
✅ Avoids repeating suggestions within the same session

Ask me about routers and I'll help you find the perfect one!

[bold]Examples:[/bold]
• "show me wireless routers" → I'll show available routers
• "do you have drones?" → I'll suggest alternatives
• "yes" (after I offer to show you something) → I'll understand the context

Type 'quit' to exit or 'summary' to see conversation history.""",
        title="🚀 Welcome",
        border_style="blue"
    )
    console.print(welcome_panel)

def display_config_status():
    """Display configuration status"""
    console.print("\n" + "="*70)
    console.print("[bold cyan]System Configuration[/bold cyan]")
    
    # Create status table
    table = Table()
    table.add_column("Service", style="bold")
    table.add_column("Status", style="bold")
    
    table.add_row("Multi-Agent System", "✅ Active")
    table.add_row("Router Database", "✅ Connected (Real Azure Search)")
    table.add_row("Intent Detection", "✅ Ready")
    table.add_row("Inventory Search", "✅ Ready") 
    table.add_row("Alternatives Finder", "✅ Ready")
    table.add_row("Recommendations", "✅ Ready")
    table.add_row("Response Formatting", "✅ Ready")
    table.add_row("Conversation Flow", "✅ Enhanced")
    table.add_row("Context Awareness", "✅ Enabled")
    table.add_row("Memory System", "✅ Active")
    
    console.print(table)
    
    # Validate configuration
    config_dict = {
        'AZURE_SEARCH_ENDPOINT': settings.AZURE_SEARCH_ENDPOINT,
        'AZURE_SEARCH_KEY': settings.AZURE_SEARCH_KEY,
        'AZURE_SEARCH_INDEX': settings.AZURE_SEARCH_INDEX,
        'AZURE_OPENAI_ENDPOINT': settings.AZURE_OPENAI_ENDPOINT,
        'AZURE_OPENAI_KEY': settings.AZURE_OPENAI_KEY
    }
    
    config_issues = validate_config(config_dict)
    if config_issues:
        console.print(Panel(
            "\n".join([f"• {issue}" for issue in config_issues]),
            title="⚠️ Configuration Issues",
            border_style="yellow"
        ))
        
        console.print("\n[red]Please update your .env file with the required Azure credentials.[/red]")
        return False
    
    return True

async def main():
    """Main application entry point"""
    # Setup logging
    setup_logging(settings.LOG_LEVEL)
    
    console.print("[bold green]DEBUG: Initializing ENHANCED MultiAgentOrchestrator[/bold green]")
    
    # Display welcome and configuration
    display_welcome()
    
    if not display_config_status():
        return
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    console.print("[bold green]DEBUG: Enhanced conversation flow with confirmatory response handling[/bold green]")
    
    console.print("\n" + "─" * 70)
    
    try:
        while True:
            # Get user input
            user_input = console.input("\n[bold cyan]Your question: [/bold cyan]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("\n[bold blue]👋 Thank you for using the Multi-Agent Router Assistant![/bold blue]")
                console.print(orchestrator.get_conversation_summary())
                break
            
            if user_input.lower() in ['summary', 'history']:
                console.print("\n" + orchestrator.get_conversation_summary())
                continue
            
            if not user_input.strip():
                continue
            
            # Process the query
            response = await orchestrator.process_query(user_input)
            
            # Display the response
            console.print(f"\n[bold green]🤖 Assistant:[/bold green] {response}")
            console.print("\n" + "─" * 70)
            
    except KeyboardInterrupt:
        console.print("\n\n[bold blue]👋 Goodbye![/bold blue]")
        console.print(orchestrator.get_conversation_summary())
    except Exception as e:
        console.print(f"\n[bold red]❌ Application Error: {e}[/bold red]")
        logging.error(f"Application error: {e}")

if __name__ == "__main__":
    asyncio.run(main())