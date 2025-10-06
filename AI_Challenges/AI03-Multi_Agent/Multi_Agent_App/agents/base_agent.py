from abc import ABC, abstractmethod
from typing import Any, Dict
from models.data_models import ConversationContext, AgentResponse
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    async def process(self, context: ConversationContext) -> AgentResponse:
        """Process the conversation context and return agent response"""
        pass
    
    def log_info(self, message: str):
        """Log info message with agent name"""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_error(self, message: str):
        """Log error message with agent name"""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_debug(self, message: str):
        """Log debug message with agent name"""
        self.logger.debug(f"[{self.name}] {message}")