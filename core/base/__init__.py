"""
Base classes for video generation system
"""
from .generator import BaseVideoGenerator, GeneratorConfig
from .plugin import BasePlugin

__all__ = ['BaseVideoGenerator', 'GeneratorConfig', 'BasePlugin']
