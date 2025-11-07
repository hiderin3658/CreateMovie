#!/usr/bin/env python3
"""
Base Plugin Class
Provides the foundation for all plugin extensions
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .generator import BaseVideoGenerator


class BasePlugin(ABC):
    """Base class for all plugins"""

    def __init__(self, name: str):
        """
        Initialize plugin

        Args:
            name: Plugin name
        """
        self.name = name
        self.generator: Optional['BaseVideoGenerator'] = None

    @abstractmethod
    def setup(self, generator: 'BaseVideoGenerator'):
        """
        Setup plugin with generator instance

        Args:
            generator: Video generator instance
        """
        self.generator = generator

    @abstractmethod
    def supports_stage(self, stage: str) -> bool:
        """
        Check if plugin supports a specific stage

        Args:
            stage: Processing stage name

        Returns:
            True if stage is supported
        """
        pass

    @abstractmethod
    def process(self, data: Dict, stage: str) -> Dict:
        """
        Process data at a specific stage

        Args:
            data: Data to process
            stage: Processing stage

        Returns:
            Processed data
        """
        pass

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value from generator

        Args:
            key: Config key
            default: Default value if not found

        Returns:
            Configuration value
        """
        if self.generator and hasattr(self.generator.config, key):
            return getattr(self.generator.config, key)
        return default
