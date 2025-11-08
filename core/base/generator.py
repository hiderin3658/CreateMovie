#!/usr/bin/env python3
"""
Base Video Generator Class
Provides the foundation for all video generation functionality
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable, TYPE_CHECKING
from dataclasses import dataclass
import json

if TYPE_CHECKING:
    from .plugin import BasePlugin


@dataclass
class GeneratorConfig:
    """Configuration for video generator"""
    duration: int = 60
    num_cuts: Optional[int] = None
    visual_style: str = "cinematic"
    generate_images: bool = True
    generate_music: bool = True
    output_dir: str = "output"
    title: str = "AI Generated Storyboard"
    auto_naming: bool = True
    overwrite: bool = False

    def to_dict(self) -> Dict:
        return {
            'duration': self.duration,
            'num_cuts': self.num_cuts,
            'visual_style': self.visual_style,
            'generate_images': self.generate_images,
            'generate_music': self.generate_music,
            'output_dir': self.output_dir,
            'title': self.title,
            'auto_naming': self.auto_naming,
            'overwrite': self.overwrite
        }


class BaseVideoGenerator(ABC):
    """Base class for all video generators"""

    def __init__(self, config: Optional[GeneratorConfig] = None):
        """
        Initialize base generator

        Args:
            config: Generator configuration
        """
        self.config = config or GeneratorConfig()
        self.hooks: Dict[str, List[Callable]] = {}
        self.plugins: List[Any] = []

    @abstractmethod
    def generate_storyboard(self, input_data: Dict) -> Dict:
        """
        Generate storyboard (must be implemented by subclasses)

        Args:
            input_data: Input data for generation

        Returns:
            Generated storyboard data
        """
        pass

    def register_hook(self, event: str, handler: Callable):
        """
        Register a hook for extending functionality

        Args:
            event: Event name (e.g., 'pre_generation', 'post_generation')
            handler: Callback function to execute
        """
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(handler)

    def trigger_hook(self, event: str, data: Any) -> Any:
        """
        Trigger hooks for an event

        Args:
            event: Event name
            data: Data to pass to hooks

        Returns:
            Modified data after all hooks
        """
        if event in self.hooks:
            for handler in self.hooks[event]:
                data = handler(data)
        return data

    def add_plugin(self, plugin: 'BasePlugin'):
        """
        Add a plugin to extend functionality

        Args:
            plugin: Plugin instance
        """
        plugin.setup(self)
        self.plugins.append(plugin)

    def process_plugins(self, data: Dict, stage: str) -> Dict:
        """
        Process data through plugins for a specific stage

        Args:
            data: Data to process
            stage: Processing stage (e.g., 'analysis', 'generation')

        Returns:
            Processed data
        """
        for plugin in self.plugins:
            if plugin.supports_stage(stage):
                data = plugin.process(data, stage)
        return data

    def load_config_from_file(self, config_path: str) -> Dict:
        """
        Load configuration from JSON file

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self, config_path: str):
        """
        Save current configuration to file

        Args:
            config_path: Path to save config
        """
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config.to_dict(), f, indent=2)
