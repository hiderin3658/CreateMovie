# Troubleshooting Guide

Comprehensive solutions to common problems in AI video storyboard generation.

## Table of Contents

1. [API and Setup Issues](#api-and-setup-issues)
2. [Image Generation Problems](#image-generation-problems)
3. [Video Prompt Issues](#video-prompt-issues)
4. [Composition and Camera Issues](#composition-and-camera-issues)
5. [Style Consistency Problems](#style-consistency-problems)
6. [Music Generation Issues](#music-generation-issues)
7. [Performance and Quality](#performance-and-quality)

---

## API and Setup Issues

### Problem: "GEMINI_API_KEY not found"

**Symptoms**: Error message on startup, no image generation

**Solutions**:

1. **Set environment variable**:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

2. **Create .env file**:
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

3. **Pass directly in code**:
```python
generator = StoryboardGenerator(api_key='your-key')
```

4. **Verify key is set**:
```bash
echo $GEMINI_API_KEY
```

---

### Problem: "Rate limit exceeded"

**Symptoms**: API errors after several requests

**Solutions**:

1. **Add delay between requests**:
```python
config = {"api_delay": 2.0}  # 2 seconds between calls
```

2. **Batch process fewer cuts**:
```python
config = {"num_cuts": 6}  # Reduce from default 8
```

3. **Wait and retry**:
- Gemini free tier: 60 requests/minute
- Wait 60 seconds and retry

4. **Upgrade API plan**:
- Consider paid tier for higher limits

---

### Problem: "API authentication failed"

**Symptoms**: 401 or 403 errors

**Solutions**:

1. **Verify API key is correct**:
- Check for typos
- Ensure no extra spaces
- Copy fresh key from Google AI Studio

2. **Check API key permissions**:
- Ensure Imagen 3 access enabled
- Verify Gemini API access

3. **Regenerate API key**:
- Go to Google AI Studio
- Generate new key
- Update in environment

---

### Problem: "Module not found errors"

**Symptoms**: ImportError for google.genai or other modules

**Solutions**:

1. **Install dependencies**:
```bash
pip install google-generativeai pillow numpy scikit-learn scipy
```

2. **Use requirements file**:
```bash
pip install -r requirements.txt
```

3. **Check Python version**:
```bash
python --version  # Should be 3.8+
```

4. **Use virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## Image Generation Problems

### Problem: "Generated images are too dark"

**Symptoms**: All images appear dim or shadowy

**Solutions**:

1. **Add explicit lighting**:
```python
"bright lighting, well-lit scene, golden hour sunlight"
```

2. **Specify light source**:
```python
"natural daylight from window, soft diffused lighting"
```

3. **Increase brightness**:
```python
"high key lighting, bright atmosphere, overexposed for brightness"
```

4. **Adjust mood descriptor**:
- Change from "moody" to "cheerful"
- Change from "dramatic" to "bright"

**Example Fix**:
```
# Before (too dark)
"classroom scene, students preparing"

# After (brighter)
"brightly lit classroom scene, students preparing,
sunlight streaming through windows, warm daylight,
cheerful atmosphere"
```

---

### Problem: "Not enough characters/people in scene"

**Symptoms**: Expected crowd but only 1-2 people appear

**Solutions**:

1. **Specify number explicitly**:
```python
"15-20 students, crowded classroom, many people"
```

2. **Use crowd descriptors**:
```python
"busy scene, populated, bustling with activity"
```

3. **Describe distribution**:
```python
"students throughout frame, some in foreground, groups in background"
```

4. **Add activity indicators**:
```python
"multiple students working on different tasks, various groups"
```

**Example Fix**:
```
# Before (too few people)
"classroom with students"

# After (more people)
"busy classroom with 15-20 students, crowded scene,
diverse group working together, multiple clusters of activity,
students in foreground and background, bustling atmosphere"
```

---

### Problem: "Characters don't match description"

**Symptoms**: Characters look different than specified

**Solutions**:

1. **Use very specific descriptions**:
```python
"teenage girl, long black hair, school uniform, specific appearance"
```

2. **Reference key visual**:
```python
# Use --key-visual flag
python scripts/generate_storyboard.py "story" --key-visual "character.jpg"
```

3. **Specify in every prompt**:
```python
"same teenage girl as before, long black hair, consistent appearance"
```

4. **Use character sheets**:
- Generate character reference first
- Reference in each subsequent cut

---

### Problem: "Composition is off-center or unbalanced"

**Symptoms**: Important elements cut off or poorly framed

**Solutions**:

1. **Specify composition explicitly**:
```python
"centered composition, subject in center frame"
```

2. **Use specific placement**:
```python
"subject on left third following rule of thirds"
```

3. **Add framing instructions**:
```python
"ensure full body visible in frame, well-framed"
```

4. **Check shot type**:
- ELS might be too wide
- Try MS or LS instead

**Example Fix**:
```
# Before (cut off)
"person in scene"

# After (well-framed)
"person centered in frame, medium shot,
rule of thirds composition, full body visible,
proper headroom, well-balanced framing"
```

---

### Problem: "Generated image doesn't match prompt"

**Symptoms**: AI ignores key prompt elements

**Solutions**:

1. **Simplify prompt**:
- Too complex → AI picks what it understands
- Break into essential elements only

2. **Prioritize elements**:
```python
"[MOST IMPORTANT], [secondary], [nice to have]"
```

3. **Remove conflicting instructions**:
```python
# Bad: "dark mysterious bright cheerful"
# Good: "mysterious atmosphere with soft lighting"
```

4. **Use consistent terminology**:
- Stick to common filmmaking terms
- Avoid jargon or mixed metaphors

5. **Regenerate with variations**:
```python
config = {"variations_per_cut": 3}
# Pick best result
```

---

### Problem: "Style inconsistency between cuts"

**Symptoms**: Each cut looks like different art style

**Solutions**:

1. **Use key visual reference**:
```bash
python scripts/generate_storyboard.py "story" --key-visual "reference.jpg"
```

2. **Add style to every prompt**:
```python
"anime style, cel-shaded, consistent art style"
```

3. **Specify color palette consistently**:
```python
"color palette: #FFE4B5, #87CEEB, #98FB98"
```

4. **Use style guide**:
```python
config = {
    "visual_style": "cinematic",
    "enforce_consistency": True
}
```

---

### Problem: "Safety filter blocked generation"

**Symptoms**: "Content policy violation" error

**Solutions**:

1. **Review prompt for sensitive content**:
- Remove violent terms
- Avoid mature themes
- Use safer alternatives

2. **Rephrase problematic terms**:
```python
# Instead of "fighting"
"sports competition, training scene"

# Instead of "weapons"
"training equipment, props"
```

3. **Context matters**:
- Add "educational" or "artistic context"
- Specify "animated" or "illustrated"

4. **Simplify scene**:
- Remove complex action
- Focus on simpler compositions

---

## Video Prompt Issues

### Problem: "Video doesn't follow ItoV prompt"

**Symptoms**: Generated video movement differs from prompt

**Solutions**:

1. **Simplify movement**:
```python
# Too complex
"dolly in while panning left and tilting up"

# Simpler
"slow zoom in, 8 seconds"
```

2. **Be more specific**:
```python
# Vague
"camera moves"

# Specific
"slow dolly forward, approaching subject, 10 seconds"
```

3. **Add consistency instruction**:
```python
"maintain first frame composition throughout"
```

4. **Match to first frame**:
- Ensure movement makes sense from starting position
- Design first frame with movement in mind

---

### Problem: "Video movement too fast or slow"

**Symptoms**: Pacing feels off

**Solutions**:

1. **Specify exact duration**:
```python
"slow zoom in over exactly 12 seconds"
```

2. **Use speed descriptors**:
```python
# Slower
"very slow, gradual, barely perceptible"

# Faster
"quick, brisk, rapid"
```

3. **Adjust for content**:
- Emotion scenes: longer (10-15s)
- Action scenes: shorter (3-6s)

4. **Test different durations**:
- Try 6s, 8s, 10s versions
- Compare results

---

### Problem: "First frame changes in video"

**Symptoms**: Starting image doesn't match ending video frame

**Solutions**:

1. **Add explicit consistency**:
```python
"maintain first frame composition, preserve starting image elements"
```

2. **Minimize subject movement**:
```python
"subtle movement only, keep character position stable"
```

3. **Use locked camera**:
```python
"static camera, no camera movement, stable frame"
```

4. **Specify what to preserve**:
```python
"keep character appearance consistent, maintain lighting throughout"
```

---

## Composition and Camera Issues

### Problem: "Wrong camera angle for scene"

**Symptoms**: Close-up when should be wide, or vice versa

**Solutions**:

1. **Check auto-selection**:
```python
# Opening should be ELS
# Dialogue should be MS
# Emotion should be CU
```

2. **Override manually**:
```python
cut.camera_angle = 'ELS'  # Force extreme long shot
```

3. **Regenerate with specific angle**:
```python
"extreme wide shot, vast landscape, establishing shot"
```

4. **Review scene type**:
- Might be categorized wrong
- Adjust scene type to match intent

---

### Problem: "Camera movement doesn't match mood"

**Symptoms**: Fast movement in calm scene, static in action scene

**Solutions**:

1. **Check mood-movement matrix**:
- Calm → static or slow dolly
- Action → tracking or handheld
- Emotion → slow push or static

2. **Specify mood clearly**:
```python
"calm atmosphere, gentle slow movement"
```

3. **Override movement**:
```python
cut.camera_movement = 'static'
```

4. **Match movement to emotion**:
```python
# Tense scene
"uncomfortable static shot, building tension"

# Joyful scene
"dynamic handheld, energetic movement"
```

---

### Problem: "Composition looks amateur"

**Symptoms**: Unbalanced, awkward framing

**Solutions**:

1. **Use proven compositions**:
```python
"rule of thirds composition"  # Safe default
"centered composition"  # For portraits
"golden ratio"  # For aesthetics
```

2. **Add professional terms**:
```python
"proper headroom, lead room for gaze direction"
```

3. **Study references**:
- Look at professional storyboards
- Analyze frame composition
- Apply learned principles

4. **Use composition checklist**:
- Focal point clear?
- Balance achieved?
- Negative space purposeful?
- Lines level?

---

## Style Consistency Problems

### Problem: "Colors don't match key visual"

**Symptoms**: Generated images have wrong color palette

**Solutions**:

1. **Verify key visual analysis**:
```python
python scripts/visual_reference_analyzer.py "keyvisual.jpg"
# Check extracted colors
```

2. **Force color palette**:
```python
"color palette: #FFE4B5, #87CEEB, #98FB98"
```

3. **Add color temperature**:
```python
"warm color temperature, golden tones"
```

4. **Specify color mood**:
```python
"vibrant saturated colors" or "desaturated muted colors"
```

---

### Problem: "Art style changes between cuts"

**Symptoms**: Anime in cut 1, realistic in cut 2

**Solutions**:

1. **Add style to every prompt**:
```python
"anime style, cel-shaded, 2D animation look"
```

2. **Use key visual**:
```bash
--key-visual "style_reference.jpg"
```

3. **Be very specific**:
```python
"exactly same art style as previous cuts,
matching cel-shading technique, consistent line art"
```

4. **Reference existing cut**:
```python
"matching Cut 1 visual style, same rendering technique"
```

---

## Music Generation Issues

### Problem: "Music sections don't match video mood"

**Symptoms**: Happy music in sad scene

**Solutions**:

1. **Review emotional arc**:
```python
music_gen.analyze_emotional_arc(storyboard)
# Check detected moods
```

2. **Manually set cut moods**:
```python
cut.mood = 'melancholic'  # Override auto-detected
```

3. **Adjust music generation**:
```python
# Regenerate with corrected moods
music_plan = music_gen.generate_complete_music_plan(storyboard)
```

4. **Edit Suno prompts**:
- Manually adjust genre, tempo, mood
- Fine-tune after generation

---

### Problem: "Too many/few music sections"

**Symptoms**: Music changes too often or not enough

**Solutions**:

1. **Manual section control**:
```python
# Force 3 sections
sections = [
    {'cuts': [1,2,3], 'mood': 'hopeful'},
    {'cuts': [4,5,6], 'mood': 'energetic'},
    {'cuts': [7,8], 'mood': 'triumphant'}
]
```

2. **Adjust transition sensitivity**:
- Lower threshold = fewer sections
- Higher threshold = more sections

3. **Group similar moods**:
- Manually combine adjacent similar moods
- Create longer sections

---

### Problem: "Music doesn't sync with video cuts"

**Symptoms**: Music transitions don't align with cut changes

**Solutions**:

1. **Check timing sheet**:
```python
timing_sheet = music_gen.generate_timing_sheet(suno_prompts, storyboard)
# Review sync points
```

2. **Adjust cut durations**:
- Match music phrase lengths
- Use 4, 8, 12, 16 second patterns

3. **Manual sync points**:
```python
# Specify exact sync points
sync_points = [0, 25, 45, 60]  # seconds
```

4. **Post-process in DAW**:
- Fine-tune in audio editor
- Stretch/compress music sections

---

## Performance and Quality

### Problem: "Generation is very slow"

**Symptoms**: Takes long time to complete

**Solutions**:

1. **Reduce number of cuts**:
```bash
--cuts 6  # Instead of default 8-10
```

2. **Skip image generation initially**:
```bash
--no-images  # Generate storyboard only
```

3. **Batch in stages**:
```python
# Generate storyboard first
# Then generate images separately
```

4. **Use faster model**:
```python
config = {"image_model": "imagen-2.0"}  # If available and faster
```

---

### Problem: "Output quality is inconsistent"

**Symptoms**: Some cuts great, others poor

**Solutions**:

1. **Generate multiple variations**:
```python
config = {"variations_per_cut": 3}
# Select best of each
```

2. **Iterate on poor cuts**:
```python
# Regenerate specific cuts
regenerate_cut(storyboard, cut_number=3)
```

3. **Refine prompts incrementally**:
- Start with auto-generated
- Identify issues
- Adjust specific elements
- Regenerate

4. **Use prompt templates**:
- Start from proven templates
- Customize for your needs

---

### Problem: "Results not meeting expectations"

**Symptoms**: Overall quality lower than hoped

**Solutions**:

1. **Set realistic expectations**:
- AI generation has limitations
- Not photorealistic in all cases
- Iteration is part of process

2. **Iterate and refine**:
- First generation = draft
- Second generation = refined
- Third generation = polished

3. **Learn from results**:
- What works? Do more of that
- What doesn't? Adjust approach
- Build personal prompt library

4. **Use reference images**:
- Key visuals improve results dramatically
- Provide style examples
- Show desired quality level

---

## Quick Diagnostic Checklist

When something goes wrong, check:

- [ ] Is API key set correctly?
- [ ] Are dependencies installed?
- [ ] Is prompt clear and specific?
- [ ] Are there conflicting instructions?
- [ ] Is duration appropriate?
- [ ] Is composition specified?
- [ ] Is style consistent?
- [ ] Is mood clear?
- [ ] Are there too many complex elements?
- [ ] Does first frame support intended movement?

---

## Getting More Help

### Review Documentation
- [Camera Shots Reference](camera_shots.md)
- [Composition Guide](composition_guide.md)
- [Camera Movements](camera_movements.md)
- [ItoV Patterns](itov_patterns.md)

### Test Systematically
1. Identify exact problem
2. Isolate variable
3. Test single change
4. Compare results
5. Iterate

### Build Knowledge
- Save working prompts
- Document what works
- Create personal templates
- Learn from iterations

---

This troubleshooting guide covers most common issues. For specific problems not listed, break down the issue systematically and test individual elements.
