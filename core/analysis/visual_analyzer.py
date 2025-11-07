#!/usr/bin/env python3
"""
Visual Analyzer
Core visual analysis functionality extracted from visual_reference_analyzer.py
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


@dataclass
class VisualAnalysis:
    """Visual analysis results from key visual image"""
    style: str
    colors: List[str]
    mood: str
    composition: str
    lighting: str
    elements: List[str]
    texture: str
    camera_angle: str
    depth: str
    contrast: str
    saturation: str

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'style': self.style,
            'colors': self.colors,
            'mood': self.mood,
            'composition': self.composition,
            'lighting': self.lighting,
            'elements': self.elements,
            'texture': self.texture,
            'camera_angle': self.camera_angle,
            'depth': self.depth,
            'contrast': self.contrast,
            'saturation': self.saturation
        }


class VisualAnalyzer:
    """Analyze key visual images to extract style elements"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize analyzer

        Args:
            api_key: Gemini API key for advanced analysis
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.use_gemini = GEMINI_AVAILABLE and self.api_key

        if self.use_gemini:
            genai.configure(api_key=self.api_key)
            self.vision_model = "gemini-2.0-flash-exp"

    def analyze_key_visual(self, image_path: str) -> VisualAnalysis:
        """
        Analyze key visual image

        Args:
            image_path: Path to the reference image

        Returns:
            VisualAnalysis object
        """
        if not PIL_AVAILABLE:
            # Return default analysis if PIL not available
            return VisualAnalysis(
                style="digital illustration",
                colors=['#FFE4B5', '#87CEEB', '#FF6B6B'],
                mood="neutral",
                composition="rule_of_thirds",
                lighting="natural lighting",
                elements=["characters", "background"],
                texture="medium detail",
                camera_angle="eye level",
                depth="moderate depth",
                contrast="medium contrast",
                saturation="medium saturation"
            )

        image = Image.open(image_path)

        style = self._detect_art_style(image, image_path)
        colors = self._extract_color_palette(image)
        mood = self._analyze_mood(image)
        composition = self._analyze_composition(image)
        lighting = self._detect_lighting(image)
        elements = self._identify_elements(image)
        texture = self._analyze_texture(image)
        camera_angle = self._detect_camera_angle(image)
        depth = self._analyze_depth(image)
        contrast = self._analyze_contrast(image)
        saturation = self._analyze_saturation(image)

        return VisualAnalysis(
            style=style,
            colors=colors,
            mood=mood,
            composition=composition,
            lighting=lighting,
            elements=elements,
            texture=texture,
            camera_angle=camera_angle,
            depth=depth,
            contrast=contrast,
            saturation=saturation
        )

    def _detect_art_style(self, image, image_path: str) -> str:
        """Detect art style"""
        return self._fallback_style_detection(image)

    def _fallback_style_detection(self, image) -> str:
        """Fallback style detection"""
        return "digital illustration"

    def _extract_color_palette(self, image) -> List[str]:
        """Extract dominant colors"""
        if not PIL_AVAILABLE or not NUMPY_AVAILABLE:
            return ['#FFE4B5', '#87CEEB', '#FF6B6B', '#4ECDC4', '#95E1D3']

        img_small = image.resize((150, 150))

        if img_small.mode != 'RGB':
            img_small = img_small.convert('RGB')

        pixels = list(img_small.getdata())

        try:
            from sklearn.cluster import KMeans

            pixel_array = np.array(pixels)
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixel_array)

            colors = kmeans.cluster_centers_.astype(int)

            hex_colors = []
            for color in colors:
                hex_color = '#{:02x}{:02x}{:02x}'.format(
                    int(color[0]), int(color[1]), int(color[2])
                )
                hex_colors.append(hex_color)

            return hex_colors
        except ImportError:
            return ['#FFE4B5', '#87CEEB', '#FF6B6B', '#4ECDC4', '#95E1D3']

    def _analyze_mood(self, image) -> str:
        """Analyze mood"""
        return "neutral"

    def _analyze_composition(self, image) -> str:
        """Analyze composition"""
        return "rule_of_thirds"

    def _detect_lighting(self, image) -> str:
        """Detect lighting"""
        return "natural lighting"

    def _identify_elements(self, image) -> List[str]:
        """Identify visual elements"""
        return ["characters", "background", "objects"]

    def _analyze_texture(self, image) -> str:
        """Analyze texture"""
        return "medium detail"

    def _detect_camera_angle(self, image) -> str:
        """Detect camera angle"""
        return "eye level"

    def _analyze_depth(self, image) -> str:
        """Analyze depth"""
        return "moderate depth"

    def _analyze_contrast(self, image) -> str:
        """Analyze contrast"""
        return "medium contrast"

    def _analyze_saturation(self, image) -> str:
        """Analyze saturation"""
        return "medium saturation"
