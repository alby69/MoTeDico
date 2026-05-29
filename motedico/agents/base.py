import logging
from abc import ABC, abstractmethod
from typing import Any
from motedico.config import Settings

class BaseAgent(ABC):
    """
    Base class for all specialized agents in the MoTeDico ecosystem.
    Provides basic logging and event emission capabilities.
    """

    def __init__(self, config: Settings):
        """
        Initialize the agent with configuration and a dedicated logger.
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    @abstractmethod
    async def start(self):
        """
        Initialize and start the agent's background tasks or connections.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def stop(self):
        """
        Gracefully stop the agent and release resources.
        Must be implemented by subclasses.
        """
        pass

    async def emit_event(self, event_type: str, data: Any):
        """
        Log an event emission. In the future, this will broadcast to an internal
        or external (Nostr) event bus.
        """
        self.logger.info(f"Event Emitted: {event_type} - {data}")
