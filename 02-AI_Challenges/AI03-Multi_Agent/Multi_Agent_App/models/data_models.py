from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class IntentType(str, Enum):
    PRODUCT_SEARCH = "product_search"
    RECOMMENDATION = "recommendation"
    GENERAL_INQUIRY = "general_inquiry"
    UNKNOWN = "unknown"

class UserQuery(BaseModel):
    text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class Intent(BaseModel):
    type: IntentType
    confidence: float
    entities: Dict[str, Any] = {}

class Product(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True
    metadata: Dict[str, Any] = {}

class SearchResult(BaseModel):
    products: List[Product]
    total_count: int
    search_query: str
    search_method: str

class Recommendation(BaseModel):
    product: Product
    reason: str
    confidence: float

class AgentResponse(BaseModel):
    agent_name: str
    intent: Optional[Intent] = None
    search_results: Optional[SearchResult] = None
    recommendations: List[Recommendation] = []
    response_text: str
    confidence: float
    metadata: Dict[str, Any] = {}

class ConversationContext(BaseModel):
    user_query: UserQuery
    intent: Optional[Intent] = None
    search_results: Optional[SearchResult] = None
    recommendations: List[Recommendation] = []
    conversation_history: List[str] = []