# Narration Feature Design Document

## Overview

ナレーション機能は、絵コンテの各カットに適切なナレーション（ボイスオーバー）を自動生成する機能です。
段階的な実装アプローチを採用し、Phase 1でテキスト生成、Phase 2で音声生成を実装します。

**作成日**: 2025-11-08
**バージョン**: 1.0
**実装フェーズ**: Phase 1 (Text Generation)

---

## Design Goals

1. **コンテクスト理解**: シーン全体の流れを理解した自然なナレーション
2. **選択的生成**: 必要なカットにのみナレーションを追加
3. **柔軟性**: ナレーションのタイミングと長さを調整可能
4. **コスト効率**: Phase 1は無料で利用可能
5. **拡張性**: Phase 2での音声生成に対応可能な設計

---

## Phase 1: Text Generation (Current Implementation)

### 1.1 Data Structure Extensions

#### CutData Extension

```python
@dataclass
class CutData:
    # Existing fields...
    cut_number: int
    duration: int
    scene_description: str
    action: str
    composition: str
    camera_angle: str
    camera_movement: str
    lighting: str
    mood: str
    image_prompt: str
    video_prompt: str

    # New narration fields
    narration_text: Optional[str] = None          # Narration text content
    narration_needed: bool = False                # Whether narration is required
    narration_duration: Optional[float] = None    # Narration duration in seconds
    narration_timing: Optional[str] = None        # "start", "middle", "end", "throughout"
    narration_style: Optional[str] = None         # "documentary", "dramatic", "casual", etc.

    # Phase 2 fields (not yet implemented)
    generated_narration_path: Optional[str] = None  # Audio file path
    narration_voice: Optional[str] = None          # Voice ID/type for TTS
```

### 1.2 Narration Generator Class

#### Location
`core/narration/narration_generator.py`

#### Class Design

```python
class NarrationGenerator:
    """
    Generate contextual narration text for video storyboard cuts
    Uses Claude API for natural language generation
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize narration generator

        Args:
            api_key: Anthropic API key (defaults to env ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.use_claude = self.api_key is not None

        if self.use_claude:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"

    def analyze_narration_needs(
        self,
        cuts: List[CutData],
        story_context: str,
        style: str = "documentary"
    ) -> List[bool]:
        """
        Analyze which cuts need narration

        Args:
            cuts: List of cut data
            story_context: Overall story description
            style: Narration style

        Returns:
            List of boolean flags indicating narration need
        """
        # Use Claude to determine which cuts benefit from narration
        # Returns list of True/False for each cut
        pass

    def generate_narration_text(
        self,
        cut: CutData,
        story_context: str,
        previous_cuts: List[CutData],
        style: str = "documentary"
    ) -> Optional[str]:
        """
        Generate narration text for a single cut

        Args:
            cut: Cut data
            story_context: Overall story description
            previous_cuts: Previous cuts for context
            style: Narration style

        Returns:
            Generated narration text or None
        """
        # Use Claude to generate contextual narration
        pass

    def calculate_narration_timing(
        self,
        narration_text: str,
        cut_duration: int,
        scene_type: str
    ) -> Dict[str, Any]:
        """
        Calculate optimal timing for narration

        Args:
            narration_text: Narration text
            cut_duration: Cut duration in seconds
            scene_type: Type of scene

        Returns:
            Dictionary with timing, duration, and placement info
        """
        # Estimate narration duration (Japanese: ~300 chars/min)
        # Determine optimal placement within cut
        pass

    def generate_narrations_for_storyboard(
        self,
        storyboard_data: Dict[str, Any],
        style: str = "documentary"
    ) -> Dict[str, Any]:
        """
        Generate narrations for entire storyboard

        Args:
            storyboard_data: Complete storyboard data
            style: Narration style

        Returns:
            Updated storyboard data with narrations
        """
        pass
```

### 1.3 Narration Styles

Support multiple narration styles:

| Style | Description | Use Case |
|-------|-------------|----------|
| `documentary` | Informative, objective | Educational, tourism videos |
| `dramatic` | Emotional, storytelling | Drama, narrative content |
| `casual` | Conversational, friendly | Vlogs, lifestyle content |
| `epic` | Grand, cinematic | Trailers, promotional videos |
| `minimal` | Sparse, artistic | Art films, abstract content |

### 1.4 Narration Decision Logic

Narration is typically needed for:

1. **Establishing shots**: Setting context, location, time
2. **Emotional moments**: Internal monologue, character thoughts
3. **Explanatory scenes**: Complex actions, technical details
4. **Transitions**: Connecting scenes, time jumps
5. **Opening/Closing**: Introduction, conclusion

Narration is typically NOT needed for:

1. **Dialogue scenes**: Action/dialogue is self-explanatory
2. **Pure action**: Fast-paced movement speaks for itself
3. **Music-driven moments**: Music carries the emotion
4. **Very short cuts**: < 3 seconds

### 1.5 Configuration Extension

```python
@dataclass
class GeneratorConfig:
    # Existing fields...

    # New narration fields
    generate_narrations: bool = False
    narration_style: str = "documentary"
    narration_language: str = "ja"  # "ja", "en", etc.
```

### 1.6 CLI Arguments

```bash
python scripts/generate_storyboard_v2.py "story" \
    --narration                          # Enable narration generation
    --narration-style documentary        # Set narration style
    --narration-language ja              # Set language
```

### 1.7 Markdown Report Format

```markdown
### Cut 1 (6s)

> 📸 **Image not generated** (API key not available)
> Use the Image Prompt below to generate this frame.

**Scene**: 夜明けの街並み。桜の花びらが風に舞う中、遠くに学校のシルエット
**Action**: カメラが街並みをゆっくりパン。桜吹雪が画面を横切る
**Camera**: ELS | rule_of_thirds
**Movement**: slow_pan_right
**Mood**: hopeful, peaceful | morning golden hour, soft pink tones

**Narration** (Start - 3.5s):
```
朝日が街を照らす中、新しい一日が始まろうとしていた。
桜の花びらが風に舞い、春の訪れを告げている。
```
> 💡 Style: documentary | Timing: Start of cut | Duration: ~3.5s

**Image Prompt**:
```
extreme wide shot, dawn cityscape with cherry blossoms...
```
```

---

## Phase 2: Audio Generation (Future Implementation)

### 2.1 Audio Generation Options

#### Option A: Gemini 2.5 Flash TTS (Recommended)

**Pros:**
- Free tier: 15 req/min, 1M req/day
- Low latency, low cost
- 24 languages support
- Style control via natural language
- Native integration with existing Gemini usage

**Cons:**
- Newer API, less mature
- Limited voice customization

**Implementation:**
```python
def generate_audio_gemini(self, text: str, output_path: str, style: str = "calm"):
    """Generate audio using Gemini 2.5 Flash TTS"""
    model = genai.GenerativeModel("gemini-2.5-flash-tts")

    prompt = f"""
    Read this narration in a {style} voice:
    {text}
    """

    response = model.generate_content(prompt)
    # Extract and save audio data
```

#### Option B: Google Cloud Text-to-Speech

**Pros:**
- Mature API with extensive documentation
- Free tier: 1M chars/month (WaveNet), 4M chars/month (Standard)
- Wide voice selection
- Fine-grained control (SSML)

**Cons:**
- Requires separate billing setup
- More complex configuration

**Implementation:**
```python
def generate_audio_gcp_tts(self, text: str, output_path: str, voice_name: str):
    """Generate audio using Google Cloud TTS"""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_path, 'wb') as out:
        out.write(response.audio_content)
```

### 2.2 Audio File Management

```
outputs/
  └── storyboard_name_timestamp/
      ├── storyboard.json
      ├── storyboard_report.md
      ├── frames/              # Images
      │   └── cut_01.jpg
      └── narrations/          # Audio files
          ├── cut_01.mp3
          ├── cut_03.mp3
          └── cut_05.mp3
```

### 2.3 Phase 2 CLI Arguments

```bash
# Phase 2: Generate audio files
python scripts/generate_storyboard_v2.py "story" \
    --narration                    # Generate narration text
    --generate-audio               # Generate audio files
    --tts-engine gemini            # "gemini" or "gcp"
    --voice calm                   # Voice style/name
```

---

## API Cost Analysis

### Phase 1: Text Generation (Claude)

**Claude 3.5 Sonnet:**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Typical Usage per Storyboard:**
- 10 cuts × 5 narrations = 5 narrations
- ~500 tokens input per narration = 2,500 tokens
- ~100 tokens output per narration = 500 tokens
- **Cost per storyboard: ~$0.01**

### Phase 2: Audio Generation (Gemini TTS)

**Gemini 2.5 Flash TTS:**
- Free tier: 15 requests/min, 1M requests/day
- Cost: $0 for most use cases

**Typical Usage:**
- 5 narrations per storyboard
- **Cost per storyboard: $0 (within free tier)**

### Total Cost Estimate

- **Development/Testing**: Essentially free with API free tiers
- **Production (1000 storyboards)**: ~$10 for Claude, $0 for TTS
- **Very economical for the value provided**

---

## Technical Implementation Notes

### Japanese Text Processing

**Character Count → Duration Estimation:**
- Japanese speech rate: ~300 characters/minute
- Formula: `duration_seconds = (char_count / 300) * 60`
- Example: 30 chars ≈ 6 seconds

**Punctuation Handling:**
- Pause after `。`: 0.5s
- Pause after `、`: 0.3s
- Adjust timing based on punctuation

### Context Management

**Pass to Claude:**
1. Overall story description
2. Previous 2-3 cuts for context
3. Current cut details
4. Desired narration style
5. Duration constraints

**Claude Prompt Template:**
```
You are creating narration for a video storyboard.

Story Context:
{story_description}

Previous Cuts:
{previous_cuts_summary}

Current Cut (Cut {cut_number}, {duration}s):
- Scene: {scene_description}
- Action: {action}
- Mood: {mood}
- Camera: {camera_info}

Generate a {style} narration that:
1. Fits within {max_duration}s (approx {max_chars} Japanese characters)
2. Complements the visual without being redundant
3. Maintains narrative flow from previous cuts
4. Matches the {mood} mood

Narration:
```

### Error Handling

1. **API Key Missing**: Skip narration, log warning
2. **API Rate Limit**: Retry with exponential backoff
3. **Generation Failure**: Log error, continue with other cuts
4. **Text Too Long**: Truncate or regenerate with shorter constraint

---

## Testing Strategy

### Unit Tests

1. `test_narration_need_analysis`: Verify correct cuts identified
2. `test_narration_generation`: Test text generation quality
3. `test_timing_calculation`: Validate duration estimates
4. `test_style_variations`: Ensure style differences work

### Integration Tests

1. **Full Storyboard**: Generate complete storyboard with narrations
2. **Different Styles**: Test all narration styles
3. **Edge Cases**: Very short/long cuts, no context, etc.

### Manual Review Criteria

1. **Natural Flow**: Narration sounds natural in context
2. **Timing**: Fits within cut duration
3. **Relevance**: Adds value, not redundant
4. **Style**: Matches requested style
5. **Language**: Grammatically correct, appropriate level

---

## Future Enhancements (Post-Phase 2)

1. **Multi-language Support**: Generate narrations in multiple languages
2. **Voice Customization**: User-selectable voices and accents
3. **Emotion Control**: Fine-tune emotional expression in audio
4. **Background Music Integration**: Mix narration with BGM
5. **Subtitle Generation**: Auto-generate subtitle files (SRT/VTT)
6. **Voice Cloning**: Use custom voice samples
7. **Batch Processing**: Generate audio for multiple storyboards efficiently

---

## References

- [Gemini API Audio Generation](https://ai.google.dev/gemini-api/docs/speech-generation)
- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs)
- [Claude API Documentation](https://docs.anthropic.com/)
- [Japanese Speech Rate Research](https://www.jstage.jst.go.jp/)

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-08 | Initial design document |

---

## Approval

- [ ] Design reviewed
- [ ] Phase 1 implementation approved
- [ ] Ready for implementation
