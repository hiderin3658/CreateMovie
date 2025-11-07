#!/usr/bin/env python3
"""
Image Generator
Handles image generation using Gemini API
"""
import os
import base64
from pathlib import Path
from typing import List, Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ImageGenerator:
    """Image generation using Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize image generator

        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.use_gemini = GEMINI_AVAILABLE and self.api_key

        if self.use_gemini:
            genai.configure(api_key=self.api_key)
            self.image_model = "gemini-2.5-flash-image"

    def generate_images(self, cuts: List, output_dir: str):
        """
        Generate images for cuts

        Args:
            cuts: List of cut data
            output_dir: Output directory
        """
        if not self.use_gemini:
            print("Gemini API not available, skipping image generation")
            return

        frames_dir = Path(output_dir) / 'frames'
        frames_dir.mkdir(parents=True, exist_ok=True)

        for cut in cuts:
            try:
                print(f"  Generating image for Cut {cut.cut_number}...")

                model = genai.GenerativeModel(self.image_model)
                response = model.generate_content(cut.image_prompt)

                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            image_path = frames_dir / f"cut_{cut.cut_number:02d}.jpg"

                            image_data = base64.b64decode(part.inline_data.data)
                            with open(image_path, 'wb') as f:
                                f.write(image_data)

                            cut.generated_image_path = str(image_path)
                            print(f"    ✓ Saved to {image_path}")
                            break

            except Exception as e:
                print(f"    ✗ Error generating image for Cut {cut.cut_number}: {e}")
