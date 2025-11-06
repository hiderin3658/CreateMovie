#!/usr/bin/env python3
"""
Visual Reference Analyzer
Analyzes key visual images to extract style, colors, and mood for consistent video generation
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from PIL import Image
import numpy as np
from collections import Counter
import colorsys

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    pass  # python-dotenv not installed, skip

# Google Gemini imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("Warning: google-generativeai not installed. Using fallback methods.")
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


class VisualReferenceAnalyzer:
    """Analyze key visual images to extract world-building elements"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize analyzer with optional Gemini API key
        
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
        Analyze key visual image to extract style elements
        
        Args:
            image_path: Path to the reference image
            
        Returns:
            VisualAnalysis object with extracted information
        """
        # Load image
        image = Image.open(image_path)
        
        # Perform different types of analysis
        style = self._detect_art_style(image, image_path)
        colors = self._extract_color_palette(image)
        mood = self._analyze_mood(image, image_path)
        composition = self._analyze_composition(image, image_path)
        lighting = self._detect_lighting(image, image_path)
        elements = self._identify_elements(image, image_path)
        texture = self._analyze_texture(image, image_path)
        camera_angle = self._detect_camera_angle(image, image_path)
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
    
    def _detect_art_style(self, image: Image.Image, image_path: str) -> str:
        """Detect the art style of the image"""
        
        if self.use_gemini:
            prompt = """
            Analyze the art style of this image. Identify:
            1. Overall style (anime, realistic, cartoon, painterly, etc.)
            2. Rendering technique (2D, 3D, digital painting, watercolor, etc.)
            3. Visual characteristics (line art, cel-shaded, photorealistic, etc.)
            
            Return a concise style description in 3-5 words.
            Example: "watercolor anime style" or "photorealistic 3D render"
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            return response if response else self._fallback_style_detection(image)
        
        return self._fallback_style_detection(image)
    
    def _fallback_style_detection(self, image: Image.Image) -> str:
        """Fallback method to detect style without API"""
        # Analyze image properties
        img_array = np.array(image)
        
        # Check for hard edges (indicates illustration/anime)
        edges = self._detect_edges(img_array)
        edge_ratio = np.sum(edges) / edges.size
        
        # Check color distribution
        unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[-1]), axis=0))
        
        # Determine style based on characteristics
        if edge_ratio > 0.1:
            if unique_colors < 1000:
                return "anime cel-shaded"
            else:
                return "digital illustration"
        elif unique_colors < 500:
            return "minimalist design"
        elif unique_colors > 50000:
            return "photorealistic"
        else:
            return "digital painting"
    
    def _extract_color_palette(self, image: Image.Image) -> List[str]:
        """Extract dominant colors from image"""
        
        # Resize for faster processing
        img_small = image.resize((150, 150))
        
        # Convert to RGB if necessary
        if img_small.mode != 'RGB':
            img_small = img_small.convert('RGB')
        
        # Get all pixels
        pixels = list(img_small.getdata())
        
        # Use k-means clustering or simple frequency
        # For simplicity, using most common colors with clustering
        from sklearn.cluster import KMeans
        
        try:
            # Reshape pixels for clustering
            pixel_array = np.array(pixels)
            
            # Perform k-means clustering
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixel_array)
            
            # Get cluster centers (dominant colors)
            colors = kmeans.cluster_centers_.astype(int)
            
            # Convert to hex
            hex_colors = []
            for color in colors:
                hex_color = '#{:02x}{:02x}{:02x}'.format(
                    int(color[0]), int(color[1]), int(color[2])
                )
                hex_colors.append(hex_color.upper())
            
            return hex_colors
            
        except ImportError:
            # Fallback if sklearn not available
            return self._simple_color_extraction(img_small)
    
    def _simple_color_extraction(self, image: Image.Image) -> List[str]:
        """Simple color extraction without sklearn"""
        # Quantize image to reduce colors
        img_quant = image.quantize(colors=5)
        
        # Get palette
        palette = img_quant.getpalette()
        
        if palette:
            # Extract 5 colors from palette
            colors = []
            for i in range(5):
                r = palette[i*3]
                g = palette[i*3 + 1]
                b = palette[i*3 + 2]
                hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
                colors.append(hex_color.upper())
            return colors
        
        # Fallback colors
        return ["#FFE4B5", "#87CEEB", "#98FB98", "#FFB6C1", "#F0E68C"]
    
    def _analyze_mood(self, image: Image.Image, image_path: str) -> str:
        """Analyze the mood/atmosphere of the image"""
        
        if self.use_gemini:
            prompt = """
            Analyze the mood and atmosphere of this image.
            Consider: lighting, colors, composition, subject matter.
            
            Return a mood description in 2-3 words.
            Example: "peaceful morning" or "dramatic tension" or "playful energy"
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            return response if response else self._fallback_mood_analysis(image)
        
        return self._fallback_mood_analysis(image)
    
    def _fallback_mood_analysis(self, image: Image.Image) -> str:
        """Analyze mood based on color and brightness"""
        img_array = np.array(image.convert('RGB'))
        
        # Calculate average brightness
        brightness = np.mean(img_array)
        
        # Calculate color warmth
        r_mean = np.mean(img_array[:, :, 0])
        b_mean = np.mean(img_array[:, :, 2])
        warmth = r_mean - b_mean
        
        # Determine mood
        if brightness > 180:
            if warmth > 20:
                return "bright cheerful"
            else:
                return "light airy"
        elif brightness < 80:
            if warmth < -20:
                return "dark mysterious"
            else:
                return "moody dramatic"
        else:
            if abs(warmth) < 20:
                return "balanced neutral"
            elif warmth > 0:
                return "warm inviting"
            else:
                return "cool calm"
    
    def _analyze_composition(self, image: Image.Image, image_path: str) -> str:
        """Analyze image composition"""
        
        if self.use_gemini:
            prompt = """
            Analyze the composition of this image.
            Identify: rule of thirds, golden ratio, symmetry, diagonal, centered, etc.
            
            Return the primary composition technique in 2-3 words.
            Example: "rule of thirds" or "centered symmetrical"
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            return response if response else "balanced composition"
        
        return "balanced composition"
    
    def _detect_lighting(self, image: Image.Image, image_path: str) -> str:
        """Detect lighting characteristics"""
        
        if self.use_gemini:
            prompt = """
            Analyze the lighting in this image.
            Consider: direction, quality (hard/soft), color temperature.
            
            Return lighting description in 2-4 words.
            Example: "soft natural daylight" or "dramatic side lighting"
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            return response if response else self._fallback_lighting_analysis(image)
        
        return self._fallback_lighting_analysis(image)
    
    def _fallback_lighting_analysis(self, image: Image.Image) -> str:
        """Simple lighting analysis"""
        img_array = np.array(image.convert('RGB'))
        
        # Analyze brightness distribution
        brightness = np.mean(img_array, axis=2)
        
        # Check for directional lighting
        left_bright = np.mean(brightness[:, :brightness.shape[1]//2])
        right_bright = np.mean(brightness[:, brightness.shape[1]//2:])
        top_bright = np.mean(brightness[:brightness.shape[0]//2, :])
        bottom_bright = np.mean(brightness[brightness.shape[0]//2:, :])
        
        # Determine lighting
        if abs(left_bright - right_bright) > 20:
            return "side lighting"
        elif top_bright > bottom_bright + 20:
            return "top lighting"
        elif np.std(brightness) < 30:
            return "soft even lighting"
        else:
            return "natural lighting"
    
    def _identify_elements(self, image: Image.Image, image_path: str) -> List[str]:
        """Identify key visual elements"""
        
        if self.use_gemini:
            prompt = """
            List the main visual elements in this image.
            Focus on: characters, objects, environment, special effects.
            
            Return a list of 3-5 key elements, separated by commas.
            Example: "girl with umbrella, rain, city street, neon lights"
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            if response:
                return [elem.strip() for elem in response.split(',')]
        
        return ["subject", "background", "foreground elements"]
    
    def _analyze_texture(self, image: Image.Image, image_path: str) -> str:
        """Analyze texture and surface quality"""
        
        if self.use_gemini:
            prompt = """
            Analyze the texture and surface quality.
            Consider: smooth, rough, soft, detailed, painterly, etc.
            
            Return texture description in 2-3 words.
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            return response if response else "medium detail"
        
        return "medium detail"
    
    def _detect_camera_angle(self, image: Image.Image, image_path: str) -> str:
        """Detect camera angle"""
        
        if self.use_gemini:
            prompt = """
            Identify the camera angle: eye level, high angle, low angle, bird's eye, etc.
            
            Return angle in 2-3 words.
            """
            
            response = self._query_gemini_vision(image_path, prompt)
            return response if response else "eye level"
        
        return "eye level"
    
    def _analyze_depth(self, image: Image.Image) -> str:
        """Analyze depth of field"""
        # Simple edge detection to estimate depth
        img_array = np.array(image.convert('L'))
        edges = self._detect_edges(img_array)
        
        edge_density = np.sum(edges) / edges.size
        
        if edge_density < 0.05:
            return "shallow depth"
        elif edge_density > 0.15:
            return "deep depth"
        else:
            return "moderate depth"
    
    def _analyze_contrast(self, image: Image.Image) -> str:
        """Analyze image contrast"""
        img_array = np.array(image.convert('L'))
        
        std_dev = np.std(img_array)
        
        if std_dev < 30:
            return "low contrast"
        elif std_dev > 60:
            return "high contrast"
        else:
            return "medium contrast"
    
    def _analyze_saturation(self, image: Image.Image) -> str:
        """Analyze color saturation"""
        img_array = np.array(image.convert('RGB'))
        
        # Convert to HSV
        hsv_array = np.array([colorsys.rgb_to_hsv(r/255, g/255, b/255) 
                              for r, g, b in img_array.reshape(-1, 3)])
        
        # Get average saturation
        avg_saturation = np.mean(hsv_array[:, 1])
        
        if avg_saturation < 0.3:
            return "low saturation"
        elif avg_saturation > 0.7:
            return "high saturation"
        else:
            return "medium saturation"
    
    def _detect_edges(self, img_array: np.ndarray) -> np.ndarray:
        """Simple edge detection"""
        from scipy import ndimage
        
        try:
            # Sobel edge detection
            sx = ndimage.sobel(img_array, axis=0, mode='constant')
            sy = ndimage.sobel(img_array, axis=1, mode='constant')
            edges = np.hypot(sx, sy)
            return edges > np.mean(edges)
        except ImportError:
            # Fallback simple difference
            return np.zeros_like(img_array, dtype=bool)
    
    def _query_gemini_vision(self, image_path: str, prompt: str) -> Optional[str]:
        """Query Gemini Vision API"""
        if not self.use_gemini:
            return None
        
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # Create model and generate content
            model = genai.GenerativeModel(self.vision_model)
            response = model.generate_content([
                prompt,
                {
                    'mime_type': 'image/jpeg',
                    'data': base64.b64encode(image_data).decode()
                }
            ])

            return response.text.strip() if response else None
            
        except Exception as e:
            print(f"Gemini Vision API error: {e}")
            return None
    
    def apply_to_prompts(
        self,
        prompts: List[Dict],
        visual_analysis: VisualAnalysis
    ) -> List[Dict]:
        """
        Apply visual analysis to all prompts
        
        Args:
            prompts: List of prompt dictionaries
            visual_analysis: Analysis results from key visual
            
        Returns:
            Updated prompts with visual style applied
        """
        style_tokens = self.generate_style_tokens(visual_analysis)
        
        for prompt in prompts:
            if 'image_prompt' in prompt:
                # Add style tokens
                prompt['image_prompt'] = self._inject_style_tokens(
                    prompt['image_prompt'],
                    style_tokens
                )
            
            if 'video_prompt' in prompt:
                # Add consistency instruction
                prompt['video_prompt'] += f"\nmaintain {visual_analysis.style} visual style"
        
        return prompts
    
    def generate_style_tokens(self, visual_analysis: VisualAnalysis) -> Dict[str, str]:
        """
        Generate style tokens from analysis
        
        Args:
            visual_analysis: Visual analysis results
            
        Returns:
            Dictionary of style tokens to inject into prompts
        """
        tokens = {
            'style': visual_analysis.style,
            'color_palette': f"color palette: {', '.join(visual_analysis.colors[:3])}",
            'mood': f"{visual_analysis.mood} atmosphere",
            'lighting': visual_analysis.lighting,
            'composition_hint': visual_analysis.composition,
            'texture': f"{visual_analysis.texture} texture",
            'contrast': visual_analysis.contrast,
            'saturation': visual_analysis.saturation
        }
        
        # Create a combined style string
        tokens['combined'] = f"""
        {visual_analysis.style}, 
        {tokens['color_palette']},
        {tokens['mood']},
        {visual_analysis.lighting},
        {visual_analysis.texture} texture
        """.strip()
        
        return tokens
    
    def _inject_style_tokens(self, prompt: str, style_tokens: Dict[str, str]) -> str:
        """Inject style tokens into prompt"""
        
        # Find where to insert style (before aspect ratio or at end)
        if "16:9" in prompt:
            parts = prompt.split("16:9")
            return f"{parts[0]}{style_tokens['combined']}, 16:9{parts[1] if len(parts) > 1 else ''}"
        else:
            return f"{prompt}, {style_tokens['combined']}"
    
    def generate_consistency_guide(self, visual_analysis: VisualAnalysis) -> Dict:
        """
        Generate visual consistency guidelines
        
        Args:
            visual_analysis: Analysis results
            
        Returns:
            Consistency guidelines dictionary
        """
        return {
            'must_include': {
                'style': visual_analysis.style,
                'primary_colors': visual_analysis.colors[:3],
                'mood': visual_analysis.mood
            },
            'should_maintain': {
                'lighting_direction': visual_analysis.lighting,
                'composition_style': visual_analysis.composition,
                'texture_quality': visual_analysis.texture
            },
            'can_vary': {
                'camera_angle': "Can change for dramatic effect",
                'secondary_colors': "Can add complementary colors",
                'depth_of_field': "Can adjust for focus"
            }
        }
    
    def save_analysis(self, analysis: VisualAnalysis, output_path: str):
        """Save analysis results to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis.to_dict(), f, ensure_ascii=False, indent=2)
    
    def load_analysis(self, input_path: str) -> VisualAnalysis:
        """Load analysis results from JSON"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return VisualAnalysis(**data)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python visual_reference_analyzer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Initialize analyzer
    analyzer = VisualReferenceAnalyzer()
    
    print(f"Analyzing key visual: {image_path}")
    
    # Analyze image
    analysis = analyzer.analyze_key_visual(image_path)
    
    # Print results
    print("\n=== Visual Analysis Results ===")
    print(f"Style: {analysis.style}")
    print(f"Colors: {', '.join(analysis.colors)}")
    print(f"Mood: {analysis.mood}")
    print(f"Composition: {analysis.composition}")
    print(f"Lighting: {analysis.lighting}")
    print(f"Elements: {', '.join(analysis.elements)}")
    print(f"Texture: {analysis.texture}")
    print(f"Camera Angle: {analysis.camera_angle}")
    print(f"Depth: {analysis.depth}")
    print(f"Contrast: {analysis.contrast}")
    print(f"Saturation: {analysis.saturation}")
    
    # Generate style tokens
    tokens = analyzer.generate_style_tokens(analysis)
    print(f"\n=== Style Tokens for Prompts ===")
    print(tokens['combined'])
    
    # Save analysis
    output_path = "visual_analysis.json"
    analyzer.save_analysis(analysis, output_path)
    print(f"\n✅ Analysis saved to {output_path}")
