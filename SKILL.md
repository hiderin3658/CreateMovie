---
name: ai-video-storyboard
description: AI video production assistant for creating storyboards, image prompts, and ItoV prompts for 1-minute videos (6-10 cuts). Generates first-frame images using Gemini API (Imagen 3). Automatically selects optimal compositions and camera work. Use when creating AI-generated videos, storyboards, video production planning, or educational content with visual narratives.
---

# AI Video Storyboard Generator

Automate video storyboard creation with AI-powered image generation, camera work selection, and music prompt generation.

## How to Use This Skill

### As a Claude Skill (Recommended)

This is a **Claude Skill** designed to be used within Claude Code. Simply describe what you want to create:

**Example conversations with Claude:**

```
You: "高校の文化祭準備を題材にした60秒の青春動画の絵コンテを作成して"

Claude will:
1. Analyze your story
2. Create 6-10 cuts with optimal camera work
3. Generate image prompts for Imagen 3
4. Create ItoV prompts for video generation
5. Generate BGM prompts for Suno
```

**With key visual:**
```
You: "このコンセプトアート(image.jpg)のスタイルで魔法学校の動画を作って"

Claude will:
1. Analyze the key visual style
2. Apply consistent style to all cuts
3. Generate cohesive storyboard
```

### As a Python Script (Advanced)

You can also run the Python scripts directly from terminal:

```bash
python scripts/generate_storyboard.py "story description"
```

## Prerequisites

### Required: Gemini API Key

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY='your-api-key-here'
```

Or create a `.env` file:

```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

### Optional Dependencies

Install Python dependencies:

```bash
pip install google-generativeai pillow numpy scikit-learn scipy
```

## Quick Start

### Basic Usage (Fully Automatic)

Generate a complete storyboard with one command:

```bash
python scripts/generate_storyboard.py "高校の文化祭準備を題材にした60秒の青春動画"
```

The AI will automatically:
- ✅ Decide on 6-10 cuts structure
- ✅ Select camera angles and movements
- ✅ Choose compositions (rule of thirds, centered, etc.)
- ✅ Set lighting and mood
- ✅ Generate Imagen 3 images
- ✅ Create ItoV prompts for video generation
- ✅ Generate BGM prompts for Suno

### With Key Visual Reference

Use a reference image to maintain visual consistency:

```bash
python scripts/generate_storyboard.py \
  "魔法学校での一日" \
  --key-visual "path/to/concept_art.jpg"
```

This will:
- Extract art style, colors, and mood from the reference
- Apply consistent style to all cuts
- Maintain visual coherence throughout

### With Video Model Selection

Generate prompts optimized for specific AI video models:

```bash
# For Veo 3.1 (technical, precise)
python scripts/generate_storyboard.py "アクション動画" --model veo3

# For Sora 2 (descriptive, artistic)
python scripts/generate_storyboard.py "感動的な動画" --model sora2

# Auto (both models)
python scripts/generate_storyboard.py "動画" --model auto
```

## Workflow

### 1. Story Input

Provide a story description:

```python
from scripts.generate_storyboard import create_complete_storyboard

storyboard = create_complete_storyboard(
    story="教育コンテンツ：水の循環を説明する60秒動画",
    config={
        "duration": 60,
        "num_cuts": 8,
        "style": "educational"
    }
)
```

### 2. Automatic Scene Breakdown

The AI analyzes your story and creates:
- Cut structure (6-10 cuts)
- Scene descriptions
- Camera angles (ELS, LS, MS, CU, ECU)
- Compositions (rule of thirds, golden ratio, etc.)
- Camera movements (pan, zoom, dolly, tracking)

### 3. Image Generation

First-frame images are generated using Gemini API (Imagen 3):

```python
# Images are automatically generated and saved to output/frames/
# - cut_01.jpg
# - cut_02.jpg
# - ...
```

### 4. ItoV Prompt Generation

Video prompts are created for image-to-video conversion:

```
Example ItoV prompt:
"slow zoom in, bustling student activity, 10 seconds,
establishing mood, maintain first frame composition throughout"
```

### 5. BGM Prompt Generation

Music prompts for Suno are automatically generated:

```python
# Section 1 (Cuts 1-3, 25s)
"[Hopeful intro] Cinematic orchestral, 80bpm, soft,
anticipation building, piano, strings, soft percussion"

# Section 2 (Cuts 4-6, 20s)
"[Energetic main] Uplifting pop-rock, 120bpm, energetic,
excitement, guitar, drums, bass, synth"
```

## Advanced Features

### Iterative Refinement

Review and adjust generated prompts:

```python
# 1. Generate initial storyboard
storyboard = create_complete_storyboard(story)

# 2. Review specific cut
print(storyboard.cuts[2].image_prompt)

# 3. Modify if needed
storyboard.cuts[2].image_prompt = """
extreme wide shot, dramatic clouds forming,
time-lapse effect, volumetric lighting,
epic scale, detailed cumulus clouds
"""

# 4. Regenerate that cut
regenerate_cut(storyboard, cut_number=3)
```

### Key Visual Analysis

Extract style from reference images:

```python
from scripts.visual_reference_analyzer import VisualReferenceAnalyzer

analyzer = VisualReferenceAnalyzer()
analysis = analyzer.analyze_key_visual("concept_art.jpg")

print(f"Style: {analysis.style}")
print(f"Colors: {analysis.colors}")
print(f"Mood: {analysis.mood}")
```

### Music Emotional Arc

Analyze and generate music sections:

```python
from scripts.music_generator_suno import MusicPromptGenerator

music_gen = MusicPromptGenerator()
music_plan = music_gen.generate_complete_music_plan(storyboard)

print(f"Sections: {len(music_plan['sections'])}")
print(f"Emotional Arc: {music_plan['emotional_arc']['overall_journey']}")
```

## Output Files

After generation, you'll find:

```
output/
├── storyboard.json              # Complete storyboard data
├── storyboard_report.md         # Visual report with images
├── music_plan.json              # BGM section data
├── suno_prompts.md              # Ready-to-use Suno prompts
└── frames/                      # Generated images
    ├── cut_01.jpg
    ├── cut_02.jpg
    └── ...
```

## Camera Work Reference

### Automatic Shot Selection

The AI automatically selects appropriate shots based on scene type:

- **Establishing scenes** → ELS (Extreme Long Shot)
- **Character introduction** → MS (Medium Shot)
- **Dialogue** → MS/MCU (Medium Close-Up)
- **Action sequences** → LS/MS (Long Shot/Medium Shot)
- **Emotional moments** → CU/ECU (Close-Up/Extreme Close-Up)
- **Conclusion** → LS/ELS

### Camera Movements

Automatically selected based on mood and action:

- **Static**: Dialogue, observation
- **Pan**: Wide space introduction
- **Zoom**: Drawing attention, surprise
- **Dolly**: Immersion, approach
- **Tracking**: Following action

See [references/camera_shots.md](references/camera_shots.md) for detailed explanations.

## Composition Guide

### Auto-Selected Compositions

- **Rule of Thirds**: General scenes, landscapes
- **Golden Ratio**: Artistic scenes, beauty emphasis
- **Centered**: Character introduction, formal scenes
- **Diagonal**: Action, dynamic scenes

See [references/composition_guide.md](references/composition_guide.md) for details.

## Troubleshooting

### API Errors

**Error: API key not found**
```bash
# Set API key
export GEMINI_API_KEY='your-key'
```

**Error: Rate limit exceeded**
```python
# Add delay between requests
config = {"api_delay": 2.0}  # 2 seconds between calls
```

### Image Generation Issues

**Problem: Images too dark**
```python
# Add lighting modifiers
"bright lighting, well-lit, golden hour"
```

**Problem: Not enough characters**
```python
# Specify number
"crowded scene, 15-20 people, busy atmosphere"
```

**Problem: Composition off-center**
```python
# Specify composition explicitly
"centered composition, symmetrical layout"
```

### Prompt Optimization

For better results:

1. **Be specific**: "soft morning sunlight from left window" > "good lighting"
2. **Add context**: "students in school uniforms preparing festival decorations"
3. **Include mood**: "cheerful atmosphere, warm colors, optimistic mood"
4. **Specify style**: "anime style, cel-shaded, vibrant colors"

See [references/troubleshooting.md](references/troubleshooting.md) for more solutions.

## Examples

### Educational Video

```python
storyboard = create_complete_storyboard(
    "宇宙の仕組みを説明する60秒の教育動画",
    config={
        "style": "educational",
        "pacing": "steady",
        "visual_style": "clear and informative"
    }
)
```

### Marketing Video

```python
storyboard = create_complete_storyboard(
    "新製品スマートフォンの魅力を伝える60秒CM",
    config={
        "style": "marketing",
        "pacing": "fast",
        "visual_style": "dynamic and engaging"
    }
)
```

### Narrative Video

```python
storyboard = create_complete_storyboard(
    "友情をテーマにした感動的な60秒ショートフィルム",
    config={
        "style": "narrative",
        "pacing": "varies with story",
        "visual_style": "cinematic"
    }
)
```

## API Costs

Using Gemini API (Imagen 3):

- **Image generation**: ~$0.03 per image
- **8-cut video**: ~$0.24 total
- **10-cut video**: ~$0.30 total

Vision analysis (for key visual):
- **Per image**: ~$0.001

## Tips for Best Results

1. **Start simple**: Let AI handle the basics first
2. **Iterate gradually**: Adjust one element at a time
3. **Use references**: Key visuals improve consistency
4. **Check compositions**: Review auto-selected camera work
5. **Test music sync**: Ensure BGM matches emotional flow
6. **Save iterations**: Keep version history for comparison

## Support

For detailed documentation:
- [Camera Shots Reference](references/camera_shots.md)
- [Composition Guide](references/composition_guide.md)
- [Camera Movements](references/camera_movements.md)
- [ItoV Patterns](references/itov_patterns.md)
- [Video Model Optimization](references/video_model_patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)

## License

MIT License
