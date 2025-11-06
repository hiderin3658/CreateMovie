#!/usr/bin/env python3
"""
Generate images only from existing storyboard JSON
"""
import os
import sys
import json
import base64
from pathlib import Path
import google.generativeai as genai

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_images_only.py <storyboard_json_path> [max_images]")
        sys.exit(1)

    json_path = sys.argv[1]
    max_images = int(sys.argv[2]) if len(sys.argv) > 2 else None

    # Read .env file manually
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)

    # Configure API
    genai.configure(api_key=api_key)

    # Load storyboard
    with open(json_path, 'r', encoding='utf-8') as f:
        storyboard = json.load(f)

    # Create output directory
    output_dir = Path(json_path).parent / 'frames'
    output_dir.mkdir(exist_ok=True)

    print(f"=== Generating Images for {storyboard['title']} ===")
    print(f"Total cuts: {len(storyboard['cuts'])}")
    if max_images:
        print(f"Max images: {max_images}")
    print()

    # Generate images
    model = genai.GenerativeModel('gemini-2.5-flash-image')

    for i, cut in enumerate(storyboard['cuts']):
        if max_images and i >= max_images:
            print(f"\nReached max images limit ({max_images})")
            break

        try:
            print(f"[{i+1}/{len(storyboard['cuts'])}] Generating Cut {cut['cut_number']}...")
            print(f"  Prompt: {cut['image_prompt'][:80]}...")

            response = model.generate_content(cut['image_prompt'])

            # Save image
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        image_path = output_dir / f"cut_{cut['cut_number']:02d}.jpg"

                        image_data = base64.b64decode(part.inline_data.data)
                        with open(image_path, 'wb') as f:
                            f.write(image_data)

                        print(f"  ✓ Saved: {image_path}")
                        break
                else:
                    print(f"  ✗ No image data in response")
            else:
                print(f"  ✗ No candidates in response")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            if "429" in str(e):
                print("\n⚠️  Quota exceeded. Stopping.")
                break

    print(f"\n✅ Done! Images saved to: {output_dir}")

if __name__ == "__main__":
    main()
