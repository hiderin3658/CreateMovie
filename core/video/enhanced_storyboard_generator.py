#!/usr/bin/env python3
"""
Enhanced Storyboard Generator
PDFガイドとリファレンス統合による高度化システム
"""
import json
import re
import random
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from .storyboard_generator import CoreStoryboardGenerator, CutData, StoryboardData


class EmotionalPhase(Enum):
    """J-pop構成による感情フェーズ"""
    SABI_HOOK = "sabi_hook"      # サビ（フック）
    A_MELO = "a_melo"            # Aメロ
    B_MELO = "b_melo"            # Bメロ
    SABI_CLIMAX = "sabi_climax"  # サビ（クライマックス）


class AspectRatio(Enum):
    """アスペクト比"""
    HORIZONTAL = "16:9"
    VERTICAL = "9:16"
    SQUARE = "1:1"
    CINEMATIC = "2.35:1"


class VideoGenre(Enum):
    """動画ジャンル"""
    EDUCATIONAL = "educational"
    COMMERCIAL = "commercial"
    NARRATIVE = "narrative"
    DOCUMENTARY = "documentary"
    TOURISM = "tourism"
    MUSIC = "music"


@dataclass
class SceneContext:
    """シーン文脈情報"""
    emotional_phase: EmotionalPhase
    intensity: float  # 0.0-1.0
    pacing: str  # slow, medium, fast
    mood: str
    genre: VideoGenre
    aspect_ratio: AspectRatio
    target_audience: str = "general"


class IntelligentSelectionEngine:
    """インテリジェント選択エンジン"""
    
    # ムード別カメラアングル（リファレンス活用）
    MOOD_CAMERA_MATRIX = {
        'peaceful': {'primary': ['MS', 'LS'], 'secondary': ['ELS'], 'avoid': ['ECU']},
        'energetic': {'primary': ['MS', 'CU'], 'secondary': ['LS'], 'avoid': ['ELS']},
        'tense': {'primary': ['CU', 'ECU'], 'secondary': ['MS'], 'avoid': ['ELS', 'LS']},
        'intimate': {'primary': ['CU', 'MCU'], 'secondary': ['MS'], 'avoid': ['ELS']},
        'epic': {'primary': ['ELS', 'LS'], 'secondary': ['MS'], 'avoid': ['ECU']},
        'mysterious': {'primary': ['MS', 'CU'], 'secondary': ['LS'], 'avoid': ['ELS']},
        'dramatic': {'primary': ['CU', 'ECU'], 'secondary': ['MCU'], 'avoid': ['ELS']},
        'joyful': {'primary': ['MS', 'LS'], 'secondary': ['MCU'], 'avoid': ['ECU']}
    }
    
    # ムード別構図（リファレンスから）
    MOOD_COMPOSITION_MATRIX = {
        'peaceful': {'primary': ['rule_of_thirds', 'symmetry'], 'secondary': ['negative_space'], 'avoid': ['diagonal']},
        'energetic': {'primary': ['diagonal', 'dynamic_angles'], 'secondary': ['rule_of_thirds'], 'avoid': ['centered']},
        'formal': {'primary': ['centered', 'symmetry'], 'secondary': ['rule_of_thirds'], 'avoid': ['diagonal']},
        'intimate': {'primary': ['centered_tight', 'close_framing'], 'secondary': ['golden_ratio'], 'avoid': ['negative_space']},
        'lonely': {'primary': ['negative_space', 'small_centered'], 'secondary': ['rule_of_thirds'], 'avoid': ['symmetry']},
        'dramatic': {'primary': ['diagonal', 'low_angle'], 'secondary': ['frame_within_frame'], 'avoid': ['symmetry']},
        'serene': {'primary': ['golden_ratio', 'symmetry'], 'secondary': ['horizontal_lines'], 'avoid': ['diagonal']}
    }
    
    # ムード別カメラムーブメント（リファレンスから）
    MOOD_MOVEMENT_MATRIX = {
        'calm': {'primary': ['static', 'slow_dolly'], 'secondary': ['gentle_pan'], 'avoid': ['handheld', 'fast']},
        'tense': {'primary': ['handheld', 'slow_zoom_in'], 'secondary': ['static'], 'avoid': ['smooth_crane']},
        'exciting': {'primary': ['tracking', 'handheld'], 'secondary': ['fast_pan'], 'avoid': ['static']},
        'intimate': {'primary': ['slow_dolly_in', 'static'], 'secondary': ['subtle_zoom'], 'avoid': ['crane', 'fast']},
        'epic': {'primary': ['crane', 'sweeping'], 'secondary': ['slow_dolly'], 'avoid': ['static', 'handheld']},
        'mysterious': {'primary': ['slow_dolly', 'creeping'], 'secondary': ['gentle_pan'], 'avoid': ['fast', 'jerky']},
        'chaotic': {'primary': ['intense_handheld', 'fast'], 'secondary': ['quick_pan'], 'avoid': ['static', 'smooth']}
    }
    
    # ジャンル別優先構図
    GENRE_COMPOSITION_PREFERENCES = {
        VideoGenre.EDUCATIONAL: ['rule_of_thirds', 'centered'],
        VideoGenre.COMMERCIAL: ['golden_ratio', 'centered', 'negative_space'],
        VideoGenre.NARRATIVE: 'all_types',  # ストーリーに応じて変動
        VideoGenre.DOCUMENTARY: ['rule_of_thirds'],  # 自然
        VideoGenre.TOURISM: ['rule_of_thirds', 'golden_ratio', 'leading_lines'],
        VideoGenre.MUSIC: ['diagonal', 'dynamic_angles', 'symmetry']
    }
    
    # アスペクト比別最適化
    ASPECT_RATIO_OPTIMIZATIONS = {
        AspectRatio.VERTICAL: {
            'preferred_compositions': ['centered', 'rule_of_thirds_vertical', 'negative_space_vertical'],
            'avoid_compositions': ['wide_diagonal'],
            'camera_considerations': 'vertical_flow_priority'
        },
        AspectRatio.HORIZONTAL: {
            'preferred_compositions': ['rule_of_thirds', 'golden_ratio', 'leading_lines'],
            'avoid_compositions': [],
            'camera_considerations': 'horizontal_flow_priority'
        }
    }

    def select_camera_angle(self, context: SceneContext, scene_type: str) -> str:
        """文脈に基づいたインテリジェントなカメラアングル選択"""
        mood = context.mood.lower()
        intensity = context.intensity
        
        # ムード優先選択
        if mood in self.MOOD_CAMERA_MATRIX:
            mood_prefs = self.MOOD_CAMERA_MATRIX[mood]
            candidates = mood_prefs['primary'].copy()
            
            # 強度に基づく調整
            if intensity > 0.7:  # 高強度
                if 'CU' in candidates or 'ECU' in candidates:
                    candidates = [c for c in candidates if c in ['CU', 'ECU']]
                else:
                    candidates.append('CU')
            elif intensity < 0.3:  # 低強度
                candidates = [c for c in candidates if c in ['ELS', 'LS', 'MS']]
        else:
            # フォールバック：従来の基本ルール
            basic_rules = {
                'establishing': 'ELS', 'character_intro': 'MS', 'dialogue': 'MS',
                'action': 'LS', 'emotion': 'CU', 'conclusion': 'LS'
            }
            return basic_rules.get(scene_type, 'MS')
        
        # ランダム選択（重み付きできる）
        return random.choice(candidates) if candidates else 'MS'

    def select_composition(self, context: SceneContext, scene_type: str) -> str:
        """文脈に基づいたインテリジェントな構図選択"""
        mood = context.mood.lower()
        genre = context.genre
        aspect_ratio = context.aspect_ratio
        
        candidates = []
        
        # ムード優先
        if mood in self.MOOD_COMPOSITION_MATRIX:
            mood_prefs = self.MOOD_COMPOSITION_MATRIX[mood]
            candidates.extend(mood_prefs['primary'])
        
        # ジャンル調整
        if genre in self.GENRE_COMPOSITION_PREFERENCES:
            genre_prefs = self.GENRE_COMPOSITION_PREFERENCES[genre]
            if genre_prefs != 'all_types':
                candidates = [c for c in candidates if c in genre_prefs]
        
        # アスペクト比最適化
        if aspect_ratio in self.ASPECT_RATIO_OPTIMIZATIONS:
            ratio_prefs = self.ASPECT_RATIO_OPTIMIZATIONS[aspect_ratio]
            preferred = ratio_prefs['preferred_compositions']
            candidates = [c for c in candidates if c in preferred] or candidates
        
        return random.choice(candidates) if candidates else 'rule_of_thirds'

    def select_camera_movement(self, context: SceneContext, scene_type: str) -> str:
        """文脈に基づいたインテリジェントなカメラムーブメント選択"""
        mood = context.mood.lower()
        pacing = context.pacing
        intensity = context.intensity
        
        candidates = []
        
        # ムード優先選択
        if mood in self.MOOD_MOVEMENT_MATRIX:
            mood_prefs = self.MOOD_MOVEMENT_MATRIX[mood]
            candidates.extend(mood_prefs['primary'])
        
        # ペーシング調整
        if pacing == 'fast':
            fast_movements = ['tracking', 'handheld', 'quick_pan', 'fast_zoom']
            candidates = [c for c in candidates if c in fast_movements] or fast_movements[:2]
        elif pacing == 'slow':
            slow_movements = ['static', 'slow_dolly', 'slow_zoom_in', 'gentle_pan']
            candidates = [c for c in candidates if c in slow_movements] or slow_movements[:2]
        
        # 強度調整
        if intensity > 0.8:
            intense_movements = ['handheld', 'fast_zoom', 'dynamic_tracking']
            candidates.extend(intense_movements)
        
        return random.choice(candidates) if candidates else 'static'


class JPOPEmotionalStructure:
    """J-pop構成による感情設計システム"""
    
    @staticmethod
    def analyze_story_for_jpop_structure(story: str, duration: int, num_cuts: int) -> List[Dict]:
        """ストーリーをJ-pop構成に分析"""
        # 基本4構成: サビ→Aメロ→Bメロ→サビ
        base_structure = [
            EmotionalPhase.SABI_HOOK,     # 冒頭フック（7-10秒）
            EmotionalPhase.A_MELO,        # 展開・説明（7-10秒）
            EmotionalPhase.B_MELO,        # 深化・多様性（7-10秒）
            EmotionalPhase.SABI_CLIMAX    # クライマックス（6-8秒）
        ]
        
        # J-pop理想時間配分（PDFガイドライン準拠）
        ideal_durations = JPOPEmotionalStructure._calculate_ideal_phase_durations(duration)
        
        # カット数分配（時間比率に基づく）
        phase_cuts = []
        total_assigned_cuts = 0
        
        for i, (phase, phase_duration) in enumerate(zip(base_structure, ideal_durations)):
            # 時間比率でカット数を計算
            time_ratio = phase_duration / duration
            phase_cut_count = max(1, round(num_cuts * time_ratio))
            
            # 最後のフェーズで調整
            if i == len(base_structure) - 1:
                phase_cut_count = num_cuts - total_assigned_cuts
            
            cut_duration = max(3, phase_duration // phase_cut_count)
            
            for j in range(phase_cut_count):
                cut_data = JPOPEmotionalStructure._create_phase_cut(
                    phase, j, cut_duration, story
                )
                phase_cuts.append(cut_data)
            
            total_assigned_cuts += phase_cut_count
        
        return phase_cuts

    @staticmethod
    def _calculate_ideal_phase_durations(total_duration: int) -> List[int]:
        """J-pop理想構成に基づく時間配分計算"""
        if total_duration <= 30:
            # 短時間動画：均等4分割
            base_duration = total_duration // 4
            return [base_duration, base_duration, base_duration, total_duration - (base_duration * 3)]
        
        elif total_duration <= 45:
            # 中時間動画：理想比率を維持
            # サビ1: 9秒, Aメロ: 11秒, Bメロ: 13秒, サビ2: 12秒
            ratio = total_duration / 45
            return [
                max(6, round(9 * ratio)),   # サビ1（フック）
                max(8, round(11 * ratio)),  # Aメロ
                max(8, round(13 * ratio)),  # Bメロ  
                max(6, round(12 * ratio))   # サビ2（クライマックス）
            ]
        
        elif total_duration <= 90:
            # 長時間動画：拡張構成
            # サビ1: 10秒, Aメロ: 20秒, Bメロ: 35秒, サビ2: 25秒
            remaining = total_duration
            sabi1 = min(12, max(8, total_duration // 8))      # フック: 8-12秒
            sabi2 = min(15, max(10, total_duration // 6))     # クライマックス: 10-15秒
            remaining -= (sabi1 + sabi2)
            
            # 残りをAメロ:Bメロ = 2:3で配分
            amelo = remaining * 2 // 5
            bmelo = remaining - amelo
            
            return [sabi1, amelo, bmelo, sabi2]
        
        else:
            # 超長時間動画（90秒超）：拡張構成 + 複数サイクル検討
            # 基本的には90秒ケースを拡張
            base_90 = JPOPEmotionalStructure._calculate_ideal_phase_durations(90)
            scale_factor = total_duration / 90
            return [max(8, round(d * scale_factor)) for d in base_90]

    @staticmethod
    def _create_phase_cut(phase: EmotionalPhase, cut_index: int, duration: int, story: str) -> Dict:
        """フェーズ別カット作成"""
        phase_characteristics = {
            EmotionalPhase.SABI_HOOK: {
                'intensity': 0.8,
                'pacing': 'fast',
                'mood': 'energetic',
                'scene_types': ['opening', 'hook', 'attention_grab'],
                'emotion_target': 'immediate_impact'
            },
            EmotionalPhase.A_MELO: {
                'intensity': 0.4,
                'pacing': 'medium',
                'mood': 'explanatory',
                'scene_types': ['character', 'context', 'development'],
                'emotion_target': 'understanding'
            },
            EmotionalPhase.B_MELO: {
                'intensity': 0.6,
                'pacing': 'medium',
                'mood': 'deepening',
                'scene_types': ['complexity', 'variation', 'buildup'],
                'emotion_target': 'engagement'
            },
            EmotionalPhase.SABI_CLIMAX: {
                'intensity': 1.0,
                'pacing': 'fast',
                'mood': 'climactic',
                'scene_types': ['climax', 'resolution', 'impact'],
                'emotion_target': 'maximum_impact'
            }
        }
        
        char = phase_characteristics[phase]
        scene_type = char['scene_types'][cut_index % len(char['scene_types'])]
        
        return {
            'duration': duration,
            'scene_description': f"{phase.value.replace('_', ' ').title()} scene {cut_index + 1}",
            'action': f"Action for {phase.value} phase",
            'scene_type': scene_type,
            'mood': char['mood'],
            'emotional_phase': phase,
            'intensity': char['intensity'],
            'pacing': char['pacing'],
            'emotion_target': char['emotion_target']
        }


class VerticalOptimizer:
    """縦型9:16最適化システム"""
    
    @staticmethod
    def optimize_for_vertical(base_prompt: str, composition: str, context: SceneContext) -> str:
        """縦型向けプロンプト最適化"""
        vertical_optimizations = {
            'aspect_ratio': '9:16 vertical aspect ratio',
            'flow_direction': 'vertical visual flow from top to bottom',
            'framing': 'tight framing suitable for mobile viewing',
            'focal_point': 'subject in upper two-thirds for natural eye flow',
            'text_space': 'space at bottom for text/UI elements',
            'background': 'simplified background to focus attention'
        }
        
        # 基本的な縦型指定
        optimized_prompt = base_prompt.replace('16:9', '9:16')
        
        # 縦型特有の要素を追加
        additions = [
            vertical_optimizations['aspect_ratio'],
            vertical_optimizations['flow_direction']
        ]
        
        # 構図に応じた調整
        if composition in ['rule_of_thirds', 'golden_ratio']:
            additions.append(vertical_optimizations['focal_point'])
        
        if composition == 'centered':
            additions.append('vertically centered composition for mobile impact')
        
        # クローズアップの強化（縦型で効果的）
        if any(keyword in base_prompt.lower() for keyword in ['close-up', 'face', 'portrait']):
            additions.append('enhanced close-up framing for vertical viewing')
        
        return base_prompt + ', ' + ', '.join(additions)


class EmotionalEngagementEnhancer:
    """感情移入促進機能"""
    
    # 共感起点パターン
    EMPATHY_HOOKS = {
        'daily_life': ['morning routine everyone knows', 'familiar workplace scenario'],
        'universal_emotion': ['feeling lost in a new place', 'excitement before adventure'],
        'relatable_challenge': ['trying to decide what to do', 'looking for something special'],
        'sensory_connection': ['warm sunlight on skin', 'cool ocean breeze']
    }
    
    # 1-2秒1アクションのテンポ設計
    ACTION_PACING = {
        'fast': {'actions_per_second': 1.0, 'cut_style': 'quick_cuts'},
        'medium': {'actions_per_second': 0.7, 'cut_style': 'natural_flow'},
        'slow': {'actions_per_second': 0.5, 'cut_style': 'contemplative'}
    }
    
    @staticmethod
    def enhance_emotional_connection(cut_data: Dict, context: SceneContext) -> Dict:
        """感情的接続の強化"""
        phase = cut_data.get('emotional_phase', EmotionalPhase.A_MELO)
        
        if phase == EmotionalPhase.SABI_HOOK:
            # 冒頭で共感起点を設定
            empathy_type = random.choice(list(EmotionalEngagementEnhancer.EMPATHY_HOOKS.keys()))
            hook = random.choice(EmotionalEngagementEnhancer.EMPATHY_HOOKS[empathy_type])
            cut_data['empathy_hook'] = hook
            cut_data['scene_description'] = f"Opening with relatable moment: {hook}"
        
        # アクションテンポの調整
        pacing = cut_data.get('pacing', 'medium')
        tempo_info = EmotionalEngagementEnhancer.ACTION_PACING.get(pacing, 
                     EmotionalEngagementEnhancer.ACTION_PACING['medium'])
        
        cut_data['action_tempo'] = tempo_info
        cut_data['recommended_cuts_per_beat'] = tempo_info['actions_per_second']
        
        return cut_data

    @staticmethod
    def generate_three_layer_stimulation(cut_data: Dict) -> Dict:
        """3層刺激（視覚・聴覚・感情）の生成"""
        stimulation_layers = {
            'visual': EmotionalEngagementEnhancer._generate_visual_stimulation(cut_data),
            'auditory': EmotionalEngagementEnhancer._generate_auditory_cues(cut_data),
            'emotional': EmotionalEngagementEnhancer._generate_emotional_triggers(cut_data)
        }
        
        cut_data['three_layer_stimulation'] = stimulation_layers
        return cut_data
    
    @staticmethod
    def _generate_visual_stimulation(cut_data: Dict) -> Dict:
        """視覚刺激の生成"""
        intensity = cut_data.get('intensity', 0.5)
        
        if intensity > 0.7:
            return {
                'movement': 'dynamic motion and color changes',
                'color': 'high contrast and vibrant colors',
                'effects': 'motion blur and dynamic lighting'
            }
        elif intensity > 0.4:
            return {
                'movement': 'gentle movement and smooth transitions',
                'color': 'warm and inviting color palette',
                'effects': 'soft lighting and natural flow'
            }
        else:
            return {
                'movement': 'minimal movement for focus',
                'color': 'calm and soothing colors',
                'effects': 'stable lighting and clear focus'
            }
    
    @staticmethod
    def _generate_auditory_cues(cut_data: Dict) -> Dict:
        """聴覚手がかりの生成"""
        mood = cut_data.get('mood', 'neutral')
        phase = cut_data.get('emotional_phase', EmotionalPhase.A_MELO)
        
        audio_suggestions = {
            'bgm_style': EmotionalEngagementEnhancer._suggest_bgm_style(mood, phase),
            'sfx_needs': EmotionalEngagementEnhancer._suggest_sound_effects(cut_data),
            'rhythm_sync': 'sync visual cuts with musical beats'
        }
        
        return audio_suggestions
    
    @staticmethod
    def _generate_emotional_triggers(cut_data: Dict) -> Dict:
        """感情的トリガーの生成"""
        return {
            'surprise_element': 'unexpected reveal or transition',
            'connection_point': 'moment for viewer identification',
            'satisfaction_hook': 'visual or narrative payoff'
        }
    
    @staticmethod
    def _suggest_bgm_style(mood: str, phase: EmotionalPhase) -> str:
        """BGMスタイルの提案"""
        style_matrix = {
            'energetic': 'upbeat and driving rhythm',
            'peaceful': 'gentle and flowing melody',
            'mysterious': 'ambient and atmospheric',
            'dramatic': 'building orchestral tension',
            'joyful': 'bright and uplifting'
        }
        
        base_style = style_matrix.get(mood, 'balanced instrumental')
        
        # フェーズによる調整
        if phase == EmotionalPhase.SABI_HOOK:
            return f"{base_style} with strong opening hook"
        elif phase == EmotionalPhase.SABI_CLIMAX:
            return f"{base_style} building to emotional peak"
        
        return base_style
    
    @staticmethod
    def _suggest_sound_effects(cut_data: Dict) -> List[str]:
        """効果音の提案"""
        scene_type = cut_data.get('scene_type', 'dialogue')
        
        sfx_library = {
            'opening': ['ambient atmosphere', 'subtle music swell'],
            'action': ['movement sounds', 'impact effects'],
            'character': ['footsteps', 'clothing rustle'],
            'climax': ['dramatic sting', 'emotional crescendo']
        }
        
        return sfx_library.get(scene_type, ['natural ambient sound'])


class EnhancedStoryboardGenerator(CoreStoryboardGenerator):
    """高度化されたストーリーボードジェネレーター"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        高度化ジェネレーターの初期化
        
        Args:
            config: 設定辞書（従来のGeneratorConfigに加えて新機能設定）
        """
        # デフォルト設定の拡張
        default_enhanced_config = {
            'aspect_ratio': AspectRatio.VERTICAL,  # デフォルトで縦型
            'genre': VideoGenre.TOURISM,
            'emotional_structure': 'jpop',
            'intelligence_level': 'high',  # low, medium, high
            'empathy_enhancement': True,
            'three_layer_stimulation': True,
            'vertical_optimization': True
        }
        
        if config:
            default_enhanced_config.update(config)
        
        super().__init__()
        self.enhanced_config = default_enhanced_config
        self.selection_engine = IntelligentSelectionEngine()
        
    def generate_storyboard(self, input_data: Dict) -> StoryboardData:
        """高度化されたストーリーボード生成"""
        story_description = input_data.get('story_description', '')
        visual_analysis = input_data.get('visual_analysis')
        
        # 入力データの拡張解析
        context = self._analyze_enhanced_context(input_data)
        
        print("\n🧠 Enhanced analysis...")
        print(f"  📊 Genre: {context.genre.value}")
        print(f"  📱 Aspect Ratio: {context.aspect_ratio.value}")
        print(f"  💡 Intelligence Level: {self.enhanced_config['intelligence_level']}")
        
        # フックの事前生成
        input_data = self.trigger_hook('pre_generation', input_data)
        
        # J-pop構成による感情設計
        print("\n🎵 Applying J-pop emotional structure...")
        cuts_data = JPOPEmotionalStructure.analyze_story_for_jpop_structure(
            story_description, 
            self.config.duration, 
            self.config.num_cuts
        )
        
        # インテリジェント選択による高度化
        print(f"\n🎯 Creating {len(cuts_data)} cuts with intelligent selection...")
        cuts = []
        for i, cut_info in enumerate(cuts_data):
            # シーンコンテキストの作成
            scene_context = SceneContext(
                emotional_phase=cut_info.get('emotional_phase', EmotionalPhase.A_MELO),
                intensity=cut_info.get('intensity', 0.5),
                pacing=cut_info.get('pacing', 'medium'),
                mood=cut_info.get('mood', 'neutral'),
                genre=context.genre,
                aspect_ratio=context.aspect_ratio
            )
            
            # インテリジェント選択
            cut = self._create_enhanced_cut(
                i + 1,
                cut_info,
                scene_context,
                visual_analysis
            )
            
            # 感情移入促進機能
            if self.enhanced_config.get('empathy_enhancement', True):
                cut_dict = cut.to_dict()
                cut_dict = EmotionalEngagementEnhancer.enhance_emotional_connection(
                    cut_dict, scene_context
                )
                
                if self.enhanced_config.get('three_layer_stimulation', True):
                    cut_dict = EmotionalEngagementEnhancer.generate_three_layer_stimulation(cut_dict)
                
                # CutDataオブジェクトの更新
                for key, value in cut_dict.items():
                    if hasattr(cut, key):
                        setattr(cut, key, value)
            
            cuts.append(cut)
            phase_name = cut_info.get('emotional_phase', EmotionalPhase.A_MELO).value.replace('_', ' ').title()
            print(f"  ✓ Cut {i + 1} ({phase_name}): {cut.scene_description[:50]}...")
        
        # 高度化されたストーリーボード作成
        storyboard = StoryboardData(
            title=self.config.title,
            duration=self.config.duration,
            num_cuts=len(cuts),
            cuts=cuts,
            style_guide=self._create_enhanced_style_guide(visual_analysis, context),
            key_visual_analysis=visual_analysis,
            created_at=datetime.now().isoformat()
        )
        
        # ポスト生成フック
        storyboard_dict = storyboard.to_dict()
        storyboard_dict = self.trigger_hook('post_generation', storyboard_dict)
        
        print(f"\n✅ Enhanced storyboard generation complete!")
        print(f"   📱 Optimized for {context.aspect_ratio.value}")
        print(f"   🎭 {context.genre.value.title()} genre")
        print(f"   🎵 J-pop emotional structure applied")
        
        return storyboard

    def _analyze_enhanced_context(self, input_data: Dict) -> SceneContext:
        """拡張コンテキスト解析"""
        # 基本値の抽出
        genre = VideoGenre(self.enhanced_config.get('genre', 'tourism'))
        aspect_ratio = AspectRatio(self.enhanced_config.get('aspect_ratio', '9:16'))
        
        # ストーリーからの自動推論
        story = input_data.get('story_description', '').lower()
        
        # ジャンル自動推論
        if 'education' in story or 'learn' in story or 'teach' in story:
            genre = VideoGenre.EDUCATIONAL
        elif 'product' in story or 'buy' in story or 'brand' in story:
            genre = VideoGenre.COMMERCIAL
        elif 'music' in story or 'song' in story or 'concert' in story:
            genre = VideoGenre.MUSIC
        elif 'travel' in story or 'visit' in story or 'destination' in story:
            genre = VideoGenre.TOURISM
        
        return SceneContext(
            emotional_phase=EmotionalPhase.A_MELO,  # 初期値
            intensity=0.5,
            pacing='medium',
            mood='neutral',
            genre=genre,
            aspect_ratio=aspect_ratio,
            target_audience=input_data.get('target_audience', 'general')
        )

    def _create_enhanced_cut(
        self, 
        cut_number: int, 
        cut_info: Dict, 
        context: SceneContext, 
        visual_analysis: Optional[Dict]
    ) -> CutData:
        """高度化されたカット作成"""
        scene_type = cut_info.get('scene_type', 'dialogue')
        
        # インテリジェント選択
        camera_angle = self.selection_engine.select_camera_angle(context, scene_type)
        composition = self.selection_engine.select_composition(context, scene_type)
        camera_movement = self.selection_engine.select_camera_movement(context, scene_type)
        
        # 高度化画像プロンプト生成
        image_prompt = self._generate_enhanced_image_prompt(
            cut_info, camera_angle, composition, visual_analysis, context
        )
        
        # 縦型最適化
        if context.aspect_ratio == AspectRatio.VERTICAL and self.enhanced_config.get('vertical_optimization', True):
            image_prompt = VerticalOptimizer.optimize_for_vertical(
                image_prompt, composition, context
            )
        
        # 高度化ビデオプロンプト生成
        veo3_prompt = self._generate_enhanced_veo3_prompt(cut_info, camera_movement, context)
        sora2_prompt = self._generate_enhanced_sora2_prompt(cut_info, camera_movement, context)
        
        # モデル推奨の高度化
        recommended_model = self._select_optimal_model(context, cut_info)
        
        return CutData(
            cut_number=cut_number,
            duration=cut_info.get('duration', 8),
            scene_description=cut_info.get('scene_description', ''),
            action=cut_info.get('action', ''),
            composition=composition,
            camera_angle=camera_angle,
            camera_movement=camera_movement,
            lighting=self._determine_enhanced_lighting(cut_info.get('mood', 'neutral'), context),
            mood=cut_info.get('mood', 'neutral'),
            image_prompt=image_prompt,
            veo3_prompt=veo3_prompt,
            sora2_prompt=sora2_prompt,
            recommended_model=recommended_model
        )

    def _generate_enhanced_image_prompt(
        self, 
        cut_info: Dict, 
        camera_angle: str, 
        composition: str, 
        visual_analysis: Optional[Dict],
        context: SceneContext
    ) -> str:
        """高度化画像プロンプト生成"""
        # 基本プロンプト生成
        base_prompt = super()._generate_image_prompt(cut_info, camera_angle, composition, visual_analysis)
        
        # 縦型指定に変更
        if context.aspect_ratio == AspectRatio.VERTICAL:
            base_prompt = base_prompt.replace('16:9', '9:16')
        
        # ジャンル特化の追加
        genre_enhancements = {
            VideoGenre.TOURISM: 'travel photography style, destination appeal, inviting atmosphere',
            VideoGenre.EDUCATIONAL: 'clear and instructional, professional presentation',
            VideoGenre.COMMERCIAL: 'high production value, premium quality, market appeal',
            VideoGenre.DOCUMENTARY: 'authentic and realistic, natural lighting',
            VideoGenre.MUSIC: 'dynamic and rhythmic, artistic composition',
            VideoGenre.NARRATIVE: 'cinematic storytelling, emotional depth'
        }
        
        enhancement = genre_enhancements.get(context.genre, '')
        if enhancement:
            base_prompt += f", {enhancement}"
        
        # 強度ベース調整
        intensity_enhancements = {
            0.8: "high impact, dramatic emphasis, strong visual presence",
            0.6: "moderate intensity, engaging composition, clear focus",
            0.3: "subtle and gentle, soft approach, understated elegance"
        }
        
        # 最も近い強度を選択
        intensity_key = min(intensity_enhancements.keys(), 
                           key=lambda x: abs(x - context.intensity))
        base_prompt += f", {intensity_enhancements[intensity_key]}"
        
        return base_prompt

    def _generate_enhanced_veo3_prompt(
        self, 
        cut_info: Dict, 
        camera_movement: str, 
        context: SceneContext
    ) -> str:
        """高度化Veo3プロンプト生成"""
        duration = cut_info.get('duration', 8)
        
        # リファレンスベースのムーブメント記述
        movement_descriptions = {
            'static': f"Camera: Static shot with natural breathing movement, {duration} seconds",
            'slow_zoom_in': f"Camera: Gradual zoom in over {duration} seconds, building intimacy",
            'slow_pull_back': f"Camera: Slow pull back revealing context, {duration} seconds",
            'tracking': f"Camera: Smooth tracking shot following subject, {duration} seconds",
            'handheld': f"Camera: Natural handheld movement with {context.pacing} energy, {duration} seconds",
            'gentle_pan': f"Camera: Smooth pan across scene over {duration} seconds",
            'crane': f"Camera: Majestic crane movement revealing scale, {duration} seconds"
        }
        
        movement_desc = movement_descriptions.get(camera_movement, 
                       f"Camera: {camera_movement} movement, {duration} seconds")
        
        # 感情フェーズ対応
        phase_enhancements = {
            EmotionalPhase.SABI_HOOK: "with strong opening impact, immediate viewer engagement",
            EmotionalPhase.A_MELO: "with steady development, clear narrative progression", 
            EmotionalPhase.B_MELO: "with building complexity, layered visual interest",
            EmotionalPhase.SABI_CLIMAX: "with maximum impact, emotional crescendo"
        }
        
        phase = cut_info.get('emotional_phase', EmotionalPhase.A_MELO)
        phase_enhancement = phase_enhancements.get(phase, '')
        
        # 3層刺激対応
        stimulation = cut_info.get('three_layer_stimulation', {})
        if stimulation:
            visual_stim = stimulation.get('visual', {})
            movement_enhancement = visual_stim.get('movement', 'natural movement')
        else:
            movement_enhancement = 'natural cinematic movement'
        
        prompt_parts = [
            movement_desc,
            f"Action: {cut_info.get('action', 'scene development')}",
            f"Visual enhancement: {movement_enhancement}",
            f"Mood: {context.mood} atmosphere",
            phase_enhancement,
            "Maintain composition and reference image consistency"
        ]
        
        return '. '.join(filter(None, prompt_parts)) + '.'

    def _generate_enhanced_sora2_prompt(
        self, 
        cut_info: Dict, 
        camera_movement: str, 
        context: SceneContext
    ) -> str:
        """高度化Sora2プロンプト生成"""
        duration = cut_info.get('duration', 8)
        
        # より自然言語的な記述（Sora2向け）
        movement_descriptions = {
            'static': f"The camera remains perfectly still for {duration} seconds, allowing the scene to breathe naturally",
            'slow_zoom_in': f"The camera slowly zooms in over {duration} seconds, gradually drawing the viewer closer to the subject",
            'tracking': f"The camera smoothly follows the movement through {duration} seconds, maintaining perfect framing",
            'handheld': f"The camera captures {duration} seconds with organic handheld movement, adding authentic human perspective",
            'crane': f"The camera sweeps majestically for {duration} seconds, revealing the grand scope of the scene"
        }
        
        movement_desc = movement_descriptions.get(camera_movement,
                       f"The camera moves with {camera_movement} for {duration} seconds")
        
        # ストーリー要素の統合
        scene_desc = cut_info.get('scene_description', '')
        action = cut_info.get('action', 'natural scene progression')
        
        # 感情的文脈の追加
        emotional_context = {
            EmotionalPhase.SABI_HOOK: f"This opening {duration}-second sequence immediately captures attention",
            EmotionalPhase.A_MELO: f"This {duration}-second development builds understanding", 
            EmotionalPhase.B_MELO: f"This {duration}-second sequence adds depth and complexity",
            EmotionalPhase.SABI_CLIMAX: f"This {duration}-second climax delivers maximum emotional impact"
        }
        
        phase = cut_info.get('emotional_phase', EmotionalPhase.A_MELO)
        emotional_intro = emotional_context.get(phase, f"This {duration}-second sequence")
        
        # 縦型配慮
        aspect_consideration = ""
        if context.aspect_ratio == AspectRatio.VERTICAL:
            aspect_consideration = "The vertical composition guides the viewer's eye naturally from top to bottom. "
        
        prompt = f"""{emotional_intro} featuring {scene_desc}. {action}. {movement_desc}. {aspect_consideration}The scene maintains {context.mood} atmosphere with {context.pacing} pacing, ensuring visual consistency with the reference image throughout the sequence.""".strip()
        
        return prompt

    def _select_optimal_model(self, context: SceneContext, cut_info: Dict) -> str:
        """最適モデル選択"""
        # 文脈に基づくモデル推奨
        if context.genre == VideoGenre.COMMERCIAL:
            return 'Veo 3'  # 高品質重視
        elif context.intensity > 0.7:
            return 'Sora 2'  # ドラマティック表現
        elif context.pacing == 'slow':
            return 'Veo 3'  # 微細な動き
        else:
            return 'Veo 3'  # デフォルト

    def _determine_enhanced_lighting(self, mood: str, context: SceneContext) -> str:
        """高度化照明決定"""
        # 基本的な照明マッピング
        base_lighting = super()._determine_lighting(mood)
        
        # ジャンル補正
        genre_lighting = {
            VideoGenre.COMMERCIAL: 'premium studio lighting',
            VideoGenre.DOCUMENTARY: 'natural authentic lighting', 
            VideoGenre.TOURISM: 'golden hour travel lighting',
            VideoGenre.EDUCATIONAL: 'clear instructional lighting'
        }
        
        enhancement = genre_lighting.get(context.genre, '')
        if enhancement:
            return f"{base_lighting}, {enhancement}"
        
        return base_lighting

    def _create_enhanced_style_guide(
        self, 
        visual_analysis: Optional[Dict], 
        context: SceneContext
    ) -> Dict:
        """高度化スタイルガイド作成"""
        base_guide = super()._create_style_guide(visual_analysis)
        
        # 高度化要素の追加
        enhanced_elements = {
            'aspect_ratio': context.aspect_ratio.value,
            'genre_optimization': context.genre.value,
            'emotional_structure': 'j-pop_four_phase',
            'intelligence_features': {
                'mood_based_selection': True,
                'context_aware_composition': True,
                'vertical_optimization': self.enhanced_config.get('vertical_optimization', True),
                'three_layer_stimulation': self.enhanced_config.get('three_layer_stimulation', True)
            },
            'targeting': {
                'audience': context.target_audience,
                'platform': 'mobile_first' if context.aspect_ratio == AspectRatio.VERTICAL else 'multi_platform',
                'engagement_strategy': 'j_pop_emotional_flow'
            }
        }
        
        base_guide.update(enhanced_elements)
        return base_guide