#!/usr/bin/env python3
"""
Project Manager
Manages video generation projects
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class ProjectManager:
    """Project management system"""

    def __init__(self, workspace: Path):
        """
        Initialize project manager

        Args:
            workspace: Workspace directory
        """
        self.workspace = Path(workspace)
        self.projects_dir = self.workspace / "projects"
        self.active_projects = {}

    def create_project(
        self,
        name: str,
        project_type: str,
        requirements: Dict,
        materials: Optional[Path] = None
    ) -> str:
        """
        Create new project

        Args:
            name: Project name
            project_type: Type (competition, client, personal)
            requirements: Project requirements
            materials: Optional materials directory

        Returns:
            Project ID
        """
        project_id = self.generate_project_id(name)

        project_path = self.projects_dir / "active" / project_id
        self.create_project_structure(project_path)

        config = self.create_project_config(
            project_id, name, project_type, requirements
        )
        self.save_config(project_path / "config.yaml", config)

        if materials:
            self.import_materials(materials, project_path / "source_materials")

        self.active_projects[project_id] = project_path

        return project_id

    def generate_project_id(self, name: str) -> str:
        """Generate project ID from name"""
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name.lower())
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{clean_name}_{timestamp}"

    def create_project_structure(self, project_path: Path):
        """Create project directory structure"""
        directories = [
            "source_materials/required",
            "source_materials/optional",
            "generated/storyboards",
            "generated/images",
            "review/drafts",
            "submission/final",
            "workspace/temp"
        ]

        for dir_path in directories:
            (project_path / dir_path).mkdir(parents=True, exist_ok=True)

    def create_project_config(
        self,
        project_id: str,
        name: str,
        project_type: str,
        requirements: Dict
    ) -> Dict:
        """Create project configuration"""
        return {
            'project': {
                'id': project_id,
                'name': name,
                'type': project_type,
                'created': datetime.now().isoformat()
            },
            'requirements': requirements,
            'status': {
                'current': 'planning',
                'progress': 0
            }
        }

    def save_config(self, config_path: Path, config: Dict):
        """Save configuration to YAML file"""
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    def import_materials(self, source: Path, dest: Path):
        """Import materials to project"""
        import shutil
        if source.is_dir():
            shutil.copytree(source, dest / source.name, dirs_exist_ok=True)
        else:
            shutil.copy2(source, dest / source.name)
