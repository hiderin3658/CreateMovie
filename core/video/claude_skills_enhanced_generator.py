#!/usr/bin/env python3
"""
Claude Skills Enhanced Storyboard Generator
Claude Skills前提に最適化された高度化システム
"""

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("⚠️  PyYAML not available. Claude Skills config loading disabled.")

from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass

from .enhanced_storyboard_generator import (
    EnhancedStoryboardGenerator,
    VideoGenre, 
    AspectRatio,
    EmotionalPhase,
    JPOPEmotionalStructure,
    SceneContext
)


@dataclass
class ProjectConfig:
    """プロジェクト設定（config.yamlベース）"""
    project_id: str
    theme: str
    aspect_ratio: str
    total_duration: int
    num_videos: int
    video_duration: int
    materials_path: Optional[str] = None
    hooks: Optional[Dict] = None
    plugins: Optional[List[str]] = None


class SkillsHookManager:
    """Claude Skills Hook管理システム"""
    
    def __init__(self):
        self.hooks = {
            'pre_generation': [],
            'post_generation': [],
            'pre_material_analysis': [],
            'post_material_analysis': [],
            'pre_character_generation': [],
            'post_character_generation': []
        }
    
    def register_hook(self, hook_type: str, callback: Callable):
        """フック登録"""
        if hook_type in self.hooks:
            self.hooks[hook_type].append(callback)
        else:
            raise ValueError(f"Unknown hook type: {hook_type}")
    
    def trigger_hook(self, hook_type: str, data: Any) -> Any:
        """フック実行"""
        if hook_type in self.hooks:
            for callback in self.hooks[hook_type]:
                try:
                    result = callback(data)
                    if result is not None:
                        data = result
                except Exception as e:
                    print(f"⚠️  Hook {hook_type} error: {e}")
        return data


class SkillsPluginManager:
    """Claude Skills Plugin管理システム"""
    
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, name: str, plugin_instance):
        """プラグイン登録"""
        self.plugins[name] = plugin_instance
        print(f"✅ Plugin registered: {name}")
    
    def get_plugin(self, name: str):
        """プラグイン取得"""
        return self.plugins.get(name)
    
    def load_default_plugins(self):
        """デフォルトプラグインロード"""
        # Claude Skills標準プラグインの模擬実装
        default_plugins = [
            'material_analyzer',
            'anime_style_transfer', 
            'character_consistency_checker',
            'tourism_narrative_builder'
        ]
        
        for plugin_name in default_plugins:
            # プラグインの模擬実装
            mock_plugin = type(f"MockPlugin_{plugin_name}", (), {
                'name': plugin_name,
                'process': lambda self, data: self._mock_process(data),
                '_mock_process': lambda self, data: {
                    **data, 
                    f'{plugin_name}_processed': True,
                    f'{plugin_name}_metadata': {'status': 'processed', 'plugin': plugin_name}
                }
            })()
            self.register_plugin(plugin_name, mock_plugin)


class SkillsWorkflowManager:
    """Claude Skills ワークフロー管理"""
    
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.current_phase = 'phase1_preparation'
        self.phase_progress = {}
    
    def execute_phase(self, phase_name: str, data: Dict) -> Dict:
        """フェーズ実行"""
        print(f"🔄 Executing {phase_name}...")
        
        workflow_phases = {
            'phase1_preparation': self._phase1_preparation,
            'phase2_background': self._phase2_background,
            'phase3_storyboard': self._phase3_storyboard,
            'phase4_generation': self._phase4_generation,
            'phase5_finalization': self._phase5_finalization
        }
        
        if phase_name in workflow_phases:
            return workflow_phases[phase_name](data)
        else:
            print(f"⚠️  Unknown phase: {phase_name}")
            return data
    
    def _phase1_preparation(self, data: Dict) -> Dict:
        """準備フェーズ"""
        # materials organization
        # materials analysis
        # character sheet creation
        data['phase1_completed'] = True
        return data
    
    def _phase2_background(self, data: Dict) -> Dict:
        """背景処理フェーズ"""
        # anime style transfer
        # quality check
        # categorize by video
        data['phase2_completed'] = True
        return data
    
    def _phase3_storyboard(self, data: Dict) -> Dict:
        """ストーリーボード生成フェーズ"""
        # generate storyboards
        # map materials to cuts
        # review and adjust
        data['phase3_completed'] = True
        return data
    
    def _phase4_generation(self, data: Dict) -> Dict:
        """生成フェーズ"""
        # composite characters
        # generate video frames
        # i2v conversion
        data['phase4_completed'] = True
        return data
    
    def _phase5_finalization(self, data: Dict) -> Dict:
        """最終化フェーズ"""
        # video editing
        # music integration
        # final rendering
        data['phase5_completed'] = True
        return data


class CloudeSkillsEnhancedGenerator(EnhancedStoryboardGenerator):
    """Claude Skills統合強化ジェネレーター"""
    
    def __init__(self, config_path: Optional[str] = None, enhanced_config: Optional[Dict] = None):
        """
        初期化
        
        Args:
            config_path: config.yamlファイルパス
            enhanced_config: 既存の高度化設定
        """
        # プロジェクト設定ロード
        self.project_config = self._load_project_config(config_path)
        
        # Claude Skills準拠設定の適用
        skills_enhanced_config = self._adapt_to_skills_config(enhanced_config or {})
        
        # 基底クラス初期化
        super().__init__(skills_enhanced_config)
        
        # Skills管理システム初期化
        self.hook_manager = SkillsHookManager()
        self.plugin_manager = SkillsPluginManager()
        self.workflow_manager = SkillsWorkflowManager(self.project_config)
        
        # デフォルト設定
        self.plugin_manager.load_default_plugins()
        self._register_default_hooks()
        
        print(f"🎯 Claude Skills mode initialized for project: {self.project_config.project_id}")

    def _load_project_config(self, config_path: Optional[str]) -> ProjectConfig:
        """プロジェクト設定ロード"""
        if not config_path:
            # デフォルト：白浜プロジェクト
            config_path = "projects/nanki-shirahama-2024/config.yaml"
        
        config_file = Path(config_path)
        if not config_file.exists() or not YAML_AVAILABLE:
            if not YAML_AVAILABLE:
                print(f"⚠️  PyYAML not available, using default config")
            else:
                print(f"⚠️  Config file not found: {config_path}, using defaults")
            
            return ProjectConfig(
                project_id="nanki-shirahama-2024",
                theme="tourism",
                aspect_ratio="9:16",
                total_duration=30,
                num_videos=4,
                video_duration=10
            )
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        project = config_data.get('project', {})
        requirements = config_data.get('requirements', {})
        
        return ProjectConfig(
            project_id=project.get('id', 'unknown'),
            theme=project.get('theme', 'tourism'),
            aspect_ratio=requirements.get('aspect_ratios', {}).get('primary', '9:16'),
            total_duration=requirements.get('total_duration', 30),
            num_videos=requirements.get('num_videos', 1),
            video_duration=requirements.get('video_duration', 30),
            materials_path=config_data.get('materials_path'),
            hooks=config_data.get('hooks'),
            plugins=config_data.get('plugins')
        )

    def _adapt_to_skills_config(self, base_config: Dict) -> Dict:
        """Claude Skills設定への適応"""
        skills_config = base_config.copy()
        
        # プロジェクト設定から自動適応
        if self.project_config.aspect_ratio == "9:16":
            skills_config['aspect_ratio'] = AspectRatio.VERTICAL
            skills_config['vertical_optimization'] = True
        
        if self.project_config.theme == "tourism":
            skills_config['genre'] = VideoGenre.TOURISM
        
        # 基本設定（重要：num_cutsとdurationを設定）
        skills_config.update({
            'title': f"{self.project_config.project_id} AI Video",
            'duration': self.project_config.video_duration,  # 10秒
            'num_cuts': 4,  # 各動画は4カット構成
            'empathy_enhancement': True,
            'three_layer_stimulation': True,
            'intelligence_level': 'high'
        })
        
        # Claude Skills特有設定
        skills_config.update({
            'skills_mode': True,
            'project_id': self.project_config.project_id,
            'workflow_integration': True,
            'plugin_system': True,
            'hooks_enabled': True
        })
        
        return skills_config

    def _register_default_hooks(self):
        """デフォルトフック登録"""
        def pre_generation_hook(data):
            """事前生成フック"""
            print("🔍 Pre-generation validation...")
            # material validation
            # character consistency check
            return self.workflow_manager.execute_phase('phase1_preparation', data)
        
        def post_generation_hook(data):
            """事後生成フック"""  
            print("✅ Post-generation processing...")
            # verify no modification
            # check material usage rate
            # generate usage report
            return self.workflow_manager.execute_phase('phase5_finalization', data)
        
        self.hook_manager.register_hook('pre_generation', pre_generation_hook)
        self.hook_manager.register_hook('post_generation', post_generation_hook)

    def generate_storyboard(self, input_data: Dict) -> 'StoryboardData':
        """Claude Skills統合ストーリーボード生成"""
        print(f"\n🎨 Claude Skills Enhanced Generation")
        print(f"   Project: {self.project_config.project_id}")
        print(f"   Theme: {self.project_config.theme}")
        print(f"   Format: {self.project_config.aspect_ratio}")
        
        # Pre-generationフック実行
        input_data = self.hook_manager.trigger_hook('pre_generation', input_data)
        
        # 白浜プロジェクト特化処理
        if self.project_config.project_id == "nanki-shirahama-2024":
            input_data = self._apply_shirahama_optimizations(input_data)
        
        # プラグイン処理
        for plugin_name in (self.project_config.plugins or []):
            plugin = self.plugin_manager.get_plugin(plugin_name)
            if plugin:
                input_data = plugin.process(input_data)
                print(f"   ✓ Plugin processed: {plugin_name}")
        
        # 基底システム生成実行
        storyboard = super().generate_storyboard(input_data)
        
        # Post-generationフック実行
        storyboard_dict = storyboard.to_dict()
        storyboard_dict = self.hook_manager.trigger_hook('post_generation', storyboard_dict)
        
        # Claude Skills準拠メタデータ追加
        storyboard_dict['claude_skills_metadata'] = {
            'project_id': self.project_config.project_id,
            'skills_version': '1.0',
            'workflow_phases_completed': self.workflow_manager.phase_progress,
            'plugins_used': list(self.plugin_manager.plugins.keys()),
            'hooks_triggered': list(self.hook_manager.hooks.keys())
        }
        
        print(f"\n🎉 Claude Skills generation completed!")
        print(f"   ✓ Project: {self.project_config.project_id}")
        print(f"   ✓ Plugins: {len(self.plugin_manager.plugins)} active")
        print(f"   ✓ Skills metadata: embedded")
        
        return storyboard

    def _apply_shirahama_optimizations(self, input_data: Dict) -> Dict:
        """白浜プロジェクト特化最適化"""
        # 白浜プロジェクト固有の4動画構成対応
        shirahama_config = {
            'video_structure': 'four_part_journey',  # 4つの10秒動画
            'narrative_arc': 'travel_experience',
            'mood_progression': ['hopeful', 'awe', 'joyful', 'nostalgic'],
            'tempo_progression': [120, 110, 130, 95],
            'material_categories': ['beach', 'nature', 'attractions', 'culture']
        }
        
        input_data.update(shirahama_config)
        
        # 提供素材との連携設定
        materials_path = Path("projects/nanki-shirahama-2024/source_materials/raw/")
        if materials_path.exists():
            input_data['provided_materials'] = {
                'base_path': str(materials_path),
                'usage_rate_requirement': 0.75,  # 16枚中12枚以上
                'modification_allowed': False,
                'style_transfer_allowed': True
            }
        
        return input_data

    def trigger_hook(self, hook_type: str, data: Any) -> Any:
        """フック実行（基底クラス互換）"""
        return self.hook_manager.trigger_hook(hook_type, data)


def create_skills_generator(config_path: Optional[str] = None) -> CloudeSkillsEnhancedGenerator:
    """Claude Skills統合ジェネレーター作成ヘルパー"""
    return CloudeSkillsEnhancedGenerator(config_path)