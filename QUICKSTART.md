# Quick Start Guide

Get started with AI Video Storyboard Generator in 5 minutes!

## Step 1: Install Dependencies

```bash
cd ai-video-storyboard
pip install -r requirements.txt
```

## Step 2: Set API Key

Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

```bash
export GEMINI_API_KEY='your-api-key-here'
```

Or create a `.env` file:

```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

## Step 3: Generate Your First Storyboard

### Basic Example

```bash
python scripts/generate_storyboard.py "高校の文化祭準備を題材にした60秒の青春動画"
```

This will:
- ✅ Analyze your story
- ✅ Create 8 cuts with camera angles
- ✅ Generate first-frame images (Imagen 3)
- ✅ Create ItoV prompts for video generation
- ✅ Generate BGM prompts for Suno

### With Key Visual

Maintain visual consistency:

```bash
python scripts/generate_storyboard.py \
  "魔法学校での一日" \
  --key-visual "path/to/concept_art.jpg"
```

### Custom Settings

```bash
python scripts/generate_storyboard.py \
  "教育動画：宇宙の仕組み" \
  --duration 60 \
  --cuts 8 \
  --output my_output \
  --title "Space Video"
```

## Step 4: Check Output

After generation, find your files in:

```
output/
├── storyboard.json          # Complete data
├── storyboard_report.md     # Visual report
└── frames/                  # Generated images
    ├── cut_01.jpg
    ├── cut_02.jpg
    └── ...
```

## Common Options

| Flag | Description | Example |
|------|-------------|---------|
| `--duration` | Video length in seconds | `--duration 60` |
| `--cuts` | Number of cuts | `--cuts 8` |
| `--key-visual` | Reference image | `--key-visual ref.jpg` |
| `--output` | Output directory | `--output my_video` |
| `--style` | Visual style | `--style anime` |
| `--no-images` | Skip image generation | `--no-images` |
| `--no-music` | Skip music prompts | `--no-music` |

## Examples by Use Case

### Educational Video

```bash
python scripts/generate_storyboard.py \
  "教育コンテンツ：光合成の仕組み" \
  --style "educational illustration" \
  --duration 60
```

### Marketing Video

```bash
python scripts/generate_storyboard.py \
  "新製品スマートフォンの紹介" \
  --style "dynamic cinematic" \
  --duration 30 \
  --cuts 6
```

### Narrative Short

```bash
python scripts/generate_storyboard.py \
  "友情をテーマにした感動ストーリー" \
  --key-visual "character_design.jpg" \
  --duration 60
```

## Next Steps

1. **Review Output**: Check `output/storyboard_report.md`
2. **Adjust if Needed**: Modify prompts and regenerate specific cuts
3. **Generate Video**: Use ItoV prompts with video generation tools
4. **Add Music**: Use Suno prompts to generate BGM

## Troubleshooting

### "API key not found"
```bash
export GEMINI_API_KEY='your-key'
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Images too dark"
Adjust prompts in output, regenerate with:
```
"bright lighting, well-lit, golden hour sunlight"
```

## Learn More

- **[SKILL.md](SKILL.md)** - Complete documentation
- **[Camera Shots Guide](references/camera_shots.md)** - Shot selection
- **[Troubleshooting](references/troubleshooting.md)** - Common issues

## Support

Need help? Check:
1. [Troubleshooting Guide](references/troubleshooting.md)
2. [SKILL.md](SKILL.md) for detailed usage
3. [Examples](assets/examples/) for sample storyboards

Happy creating! 🎬
