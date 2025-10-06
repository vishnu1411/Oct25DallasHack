import logging
import asyncio
from typing import Any, Dict, List
from datetime import datetime
import json

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    try:
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
    except Exception:
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)

def format_price(price: float) -> str:
    """Format price as currency"""
    return f"${price:.2f}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

async def retry_async(func, max_retries: int = 3, delay: float = 1.0):
    """Retry an async function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(delay * (2 ** attempt))

def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate configuration and return list of issues"""
    issues = []
    
    # Check required fields
    required_fields = [
        'AZURE_SEARCH_ENDPOINT',
        'AZURE_SEARCH_KEY', 
        'AZURE_SEARCH_INDEX',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_KEY'
    ]
    
    for field in required_fields:
        if not config.get(field):
            issues.append(f"Missing required configuration: {field}")
    
    return issues

def log_conversation(user_query: str, response: str, metadata: Dict = None):
    """Log conversation for analytics"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "response": response,
            "metadata": metadata or {}
        }
        
        # Simple logging
        logging.info(f"Conversation logged: {user_query[:50]}...")
    except Exception:
        # Fallback logging
        logging.info(f"Conversation: {user_query[:30]}... -> {response[:30]}...")