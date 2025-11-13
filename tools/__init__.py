"""
Project management tools and generic material system
"""
from .project_manager import ProjectManager
from .material_system import MaterialSystem, MaterialConfig, Material
from .material_analyzer import MaterialAnalyzer
from .material_matcher import MaterialMatcher
from .usage_tracker import UsageTracker
from .matching_strategies import (
    MaterialMatchingStrategy,
    TourismMatchingStrategy,
    EducationMatchingStrategy,
    MarketingMatchingStrategy,
    CompetitionMatchingStrategy,
    DefaultMatchingStrategy
)
from .research_loader import ResearchDatabase, Location, StoryFramework
from .research_aware_strategy import ResearchAwareStrategy

__all__ = [
    'ProjectManager',
    'MaterialSystem',
    'MaterialConfig',
    'Material',
    'MaterialAnalyzer',
    'MaterialMatcher',
    'UsageTracker',
    'MaterialMatchingStrategy',
    'TourismMatchingStrategy',
    'EducationMatchingStrategy',
    'MarketingMatchingStrategy',
    'CompetitionMatchingStrategy',
    'DefaultMatchingStrategy',
    'ResearchDatabase',
    'Location',
    'StoryFramework',
    'ResearchAwareStrategy',
]
