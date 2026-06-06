from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Abstract Base Class (ABC) serving as the definitive structural interface contract 
    for all downstream autonomous sub-agents operating within the multi-tenant research loop.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Enforces a clean naming identifier property across all inherited worker agent classes 
        to ensure transparent tracing and step routing loops inside the orchestrator.
        """
        pass

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        The core asynchronous execution gateway method that each worker agent must implement natively 
        to parse task payloads and gather evidence materials.
        """
        pass
