# AI Video Storyboard Generator

Claude Skill for automated video storyboard creation with AI-powered image generation, camera work selection, and music prompt generation.

## 🎬 Features

- **Automated Storyboard Generation**: Create 6-10 cut storyboards from story descriptions
- **AI Image Generation**: Generate first-frame images using Gemini API (Imagen 3)
- **Smart Camera Work**: Automatic selection of camera angles, compositions, and movements
- **ItoV Prompt Generation**: Optimized prompts for image-to-video conversion
- **Visual Consistency**: Key visual reference support for unified art style
- **BGM Generation**: Automatic Suno-optimized music prompts
- **Model Optimization**: Support for both Veo 3.1 and Sora 2

## 📋 Prerequisites

### Required

**Gemini API Key**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

```bash
export GEMINI_API_KEY='your-api-key-here'
```

### Python Dependencies

```bash
pip install google-generativeai pillow numpy scikit-learn scipy
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Usage

Generate a complete storyboard:

```bash
python scripts/generate_storyboard.py "高校の文化祭準備を題材にした60秒の青春動画"
```

### With Key Visual Reference

Maintain visual consistency across all cuts:

```bash
python scripts/generate_storyboard.py \
  "魔法学校での一日" \
  --key-visual "path/to/concept_art.jpg"
```

### Custom Configuration

```bash
python scripts/generate_storyboard.py \
  "教育動画：宇宙の仕組み" \
  --duration 60 \
  --cuts 8 \
  --output my_output \
  --style "educational" \
  --title "Space Education Video"
```

## 📖 Documentation

- **[SKILL.md](SKILL.md)** - Complete usage guide and examples
- **[Camera Shots Reference](references/camera_shots.md)** - Shot types and selection guide
- **[Composition Guide](references/composition_guide.md)** - Visual composition techniques
- **[Camera Movements](references/camera_movements.md)** - Movement types and patterns
- **[ItoV Patterns](references/itov_patterns.md)** - Video prompt optimization
- **[Troubleshooting](references/troubleshooting.md)** - Common issues and solutions

## 🏗️ Project Structure

```
ai-video-storyboard/
├── SKILL.md                           # Main skill documentation
├── README.md                          # This file
├── scripts/                           # Executable scripts
│   ├── generate_storyboard.py        # Main storyboard generator
│   ├── visual_reference_analyzer.py  # Key visual analysis
│   └── music_generator_suno.py       # BGM prompt generation
├── references/                        # Reference documentation
│   ├── camera_shots.md
│   ├── composition_guide.md
│   ├── camera_movements.md
│   ├── itov_patterns.md
│   └── troubleshooting.md
└── assets/                           # Templates and examples
    ├── templates/
    │   ├── storyboard_template.json
    │   └── character_sheet.json
    └── examples/
        └── educational_video.json
```

## 💡 Usage Examples

### Educational Content

```python
from scripts.generate_storyboard import create_complete_storyboard

storyboard = create_complete_storyboard(
    "教育動画：光合成の仕組みを説明する60秒",
    config={
        "visual_style": "educational illustration",
        "duration": 60,
        "num_cuts": 8
    }
)
```

### Marketing Video

```python
storyboard = create_complete_storyboard(
    "新製品スマートフォンの魅力を伝える60秒CM",
    config={
        "visual_style": "dynamic and engaging",
        "pacing": "fast",
        "generate_images": True
    }
)
```

### With Key Visual

```python
storyboard = create_complete_storyboard(
    "ファンタジー世界での冒険",
    key_visual_path="fantasy_concept.jpg",
    config={
        "enforce_visual_consistency": True
    }
```

## 🎨 Output Files

After generation:

```
output/
├── storyboard.json           # Complete storyboard data (JSON)
├── storyboard_report.md      # Visual report with images (Markdown)
├── music_plan.json           # BGM section data (optional)
└── frames/                   # Generated images
    ├── cut_01.jpg
    ├── cut_02.jpg
    └── ...
```

## 🔧 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--duration` | Video duration in seconds | 60 |
| `--cuts` | Number of cuts | auto (6-10) |
| `--key-visual` | Reference image path | None |
| `--output` | Output directory | output |
| `--title` | Storyboard title | AI Generated Storyboard |
| `--style` | Visual style | cinematic |
| `--no-images` | Skip image generation | False |
| `--no-music` | Skip music generation | False |
| `--model` | Video model (veo3/sora2/auto) | auto |

## 📊 API Costs

Using Gemini API (Imagen 3):

- **Image generation**: ~$0.03 per image
- **8-cut video**: ~$0.24 total
- **10-cut video**: ~$0.30 total
- **Vision analysis**: ~$0.001 per image

## 🤝 Contributing

This is a Claude Skill for the Claude Code system. For improvements:

1. Test changes thoroughly
2. Update documentation
3. Follow existing code style
4. Add examples for new features

## 📝 License

MIT License - See LICENSE file for details

## 🆘 Support

- **Documentation**: See [SKILL.md](SKILL.md)
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md)
- **Examples**: Check `assets/examples/` for sample storyboards

## 🔄 Version History

### v1.0.0 (2025-01-02)

- Initial release
- Core storyboard generation
- Imagen 3 image generation
- Automatic camera work selection
- ItoV prompt generation
- Key visual reference support
- BGM prompt generation for Suno
- Model optimization (Veo 3.1 / Sora 2)

## 🎯 Roadmap

- [ ] Video model integration (direct ItoV generation)
- [ ] Advanced character consistency
- [ ] Multi-language support
- [ ] Web UI interface
- [ ] Batch processing
- [ ] Template library expansion

---

**Made for Claude Code** - AI-powered video production assistant
