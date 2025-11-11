#!/usr/bin/env python3
"""
Image Generator
Handles image generation using Gemini API
"""
import os
import base64
from pathlib import Path
from typing import List, Optional
from PIL import Image

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
        self.generation_errors = []  # Track generation errors
        self.images_generated_count = 0
        self.images_failed_count = 0

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
            error_msg = "Gemini API not available (library not installed or API key not set)"
            print(error_msg)
            self.generation_errors.append({
                'type': 'api_unavailable',
                'message': error_msg,
                'cuts_affected': 'all'
            })
            return

        frames_dir = Path(output_dir) / 'frames'
        frames_dir.mkdir(parents=True, exist_ok=True)

        for cut in cuts:
            try:
                print(f"  Generating image for Cut {cut.cut_number}...")

                model = genai.GenerativeModel(self.image_model)

                # 参照画像がある場合は画像とプロンプトを組み合わせる
                content_parts = []
                if hasattr(cut, 'reference_images') and cut.reference_images:
                    # 参照画像を読み込み（最大3枚）
                    reference_count = 0
                    for ref_img_path in cut.reference_images[:3]:  # Gemini 2.5 Flash Image limit
                        ref_path = Path(ref_img_path)
                        if ref_path.exists():
                            try:
                                # PIL.Imageで画像を読み込み
                                img = Image.open(ref_path)
                                content_parts.append(img)
                                reference_count += 1
                                print(f"    + Reference image {reference_count}: {ref_path.name}")
                            except Exception as img_error:
                                print(f"    ⚠️  Failed to load reference image {ref_path.name}: {img_error}")
                        else:
                            print(f"    ⚠️  Reference image not found: {ref_path}")

                    if reference_count > 0:
                        print(f"    → Using {reference_count} reference image(s)")

                # プロンプトを追加
                content_parts.append(cut.image_prompt)

                # 画像生成リクエスト
                response = model.generate_content(content_parts)

                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            image_path = frames_dir / f"cut_{cut.cut_number:02d}.jpg"

                            image_data = base64.b64decode(part.inline_data.data)
                            with open(image_path, 'wb') as f:
                                f.write(image_data)

                            cut.generated_image_path = str(image_path)
                            self.images_generated_count += 1
                            print(f"    ✓ Saved to {image_path}")
                            break
                    else:
                        # No inline_data found
                        error_msg = "No image data in response"
                        print(f"    ✗ {error_msg}")
                        self.images_failed_count += 1
                        self.generation_errors.append({
                            'cut_number': cut.cut_number,
                            'type': 'no_image_data',
                            'message': error_msg
                        })
                else:
                    # No candidates
                    error_msg = "No candidates in response"
                    print(f"    ✗ {error_msg}")
                    self.images_failed_count += 1
                    self.generation_errors.append({
                        'cut_number': cut.cut_number,
                        'type': 'no_candidates',
                        'message': error_msg
                    })

            except Exception as e:
                error_type = self._classify_error(e)
                error_msg = str(e)
                print(f"    ✗ Error generating image for Cut {cut.cut_number}: {error_msg}")

                self.images_failed_count += 1
                self.generation_errors.append({
                    'cut_number': cut.cut_number,
                    'type': error_type,
                    'message': error_msg,
                    'exception_type': type(e).__name__
                })

    def _classify_error(self, exception: Exception) -> str:
        """Classify error type for better reporting"""
        error_str = str(exception).lower()
        exception_name = type(exception).__name__

        if 'quota' in error_str or 'resourceexhausted' in exception_name.lower():
            return 'quota_exceeded'
        elif 'permission' in error_str or 'unauthorized' in error_str:
            return 'permission_denied'
        elif 'not found' in error_str or '404' in error_str:
            return 'model_not_found'
        elif 'timeout' in error_str:
            return 'timeout'
        elif 'network' in error_str or 'connection' in error_str:
            return 'network_error'
        else:
            return 'unknown_error'

    def get_error_summary(self) -> dict:
        """Get summary of generation errors"""
        return {
            'total_generated': self.images_generated_count,
            'total_failed': self.images_failed_count,
            'errors': self.generation_errors,
            'has_errors': len(self.generation_errors) > 0
        }
