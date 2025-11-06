# Composition Guide

Complete guide to visual composition with auto-selection matrix and adjustment techniques.

## Auto-Selection Matrix

The AI automatically selects composition based on scene type:

```python
composition_matrix = {
    'opening': 'rule_of_thirds',      # Balanced introduction
    'character': 'centered',           # Character focus
    'dialogue': 'over_shoulder',       # Natural conversation
    'action': 'diagonal',              # Dynamic movement
    'emotion': 'centered_tight',       # Emotional focus
    'landscape': 'golden_ratio'        # Aesthetic beauty
}
```

---

## Composition Types

### 1. Rule of Thirds (三分割法)

**Auto-applied for**: General scenes, landscapes, everyday moments

**Description**:
Divide frame into 3×3 grid. Place important elements at intersections or along lines.

**Visual Effect**:
- Balanced and natural
- Professional look
- Visually pleasing without being forced

**Prompt Modifiers**:

**Basic**:
```
rule of thirds composition, balanced framing
```

**Left placement**:
```
subject on left third, looking right, negative space on right
```

**Right placement**:
```
subject on right third, looking left, balanced composition
```

**Top placement**:
```
subject on upper third, sky/background in lower two-thirds
```

**Bottom placement**:
```
ground/foreground in lower third, sky in upper two-thirds
```

**Adjustment Tips**:
- "Too rigid" → Add `slightly off-center for dynamic balance`
- "Need more tension" → Move to intersection points
- "Too much empty space" → Use `tighter rule of thirds`

**Best for**:
- Landscapes with horizon
- Character with background interest
- Establishing shots
- Static scenes

---

### 2. Golden Ratio (黄金比)

**Auto-applied for**: Artistic scenes, beauty emphasis, aesthetic focus

**Description**:
Based on Fibonacci sequence (1:1.618). More refined than rule of thirds.

**Visual Effect**:
- Mathematically beautiful
- Sophisticated and elegant
- Natural flow to the eye

**Prompt Modifiers**:

**Basic**:
```
golden ratio composition, divine proportion layout
```

**With spiral**:
```
fibonacci spiral composition, natural flow leading to focal point
```

**Balanced**:
```
golden ratio framing, harmonious proportions
```

**Adjustment Tips**:
- "Too subtle" → Use more obvious placement
- "Want impact" → Combine with strong color contrast
- "Mathematical precision" → Add `precise golden ratio positioning`

**Best for**:
- Portrait photography
- Architectural scenes
- Nature photography
- Artistic compositions

---

### 3. Centered Composition (中心構図)

**Auto-applied for**: Character introduction, symmetry, formal scenes

**Description**:
Place main subject in the center of frame.

**Visual Effect**:
- Powerful and direct
- Formal and stable
- Immediate focus

**Prompt Modifiers**:

**Perfect center**:
```
centered composition, symmetrical, subject dead center
```

**Slightly off-center**:
```
near-centered composition, subtle off-center for tension
```

**With symmetry**:
```
perfectly centered, symmetrical composition, mirrored balance
```

**Tight centered**:
```
centered tight framing, minimal negative space, focused
```

**Adjustment Tips**:
- "Too static" → Add `slightly off-center for subtle dynamism`
- "Need energy" → Add diagonal elements within frame
- "Too formal" → Shift slightly off-center

**Best for**:
- Portraits
- Product photography
- Formal presentations
- Symmetrical architecture
- Character introduction

---

### 4. Diagonal Composition (対角線構図)

**Auto-applied for**: Action, dynamic scenes, movement

**Description**:
Key elements arranged along diagonal lines (usually corner to corner).

**Visual Effect**:
- Dynamic and energetic
- Sense of movement
- Visual tension

**Prompt Modifiers**:

**Strong diagonal**:
```
diagonal composition, dynamic angles, 45-degree orientation
```

**Subtle diagonal**:
```
subtle diagonal lines, gentle dynamic movement
```

**Multiple diagonals**:
```
intersecting diagonal lines, complex dynamic composition
```

**Leading diagonal**:
```
diagonal leading line from corner, drawing eye through frame
```

**Adjustment Tips**:
- "Too chaotic" → Use `gentle diagonal` or single diagonal line
- "Need more energy" → Use `strong diagonal lines, sharp angles`
- "Looks tilted" → Ensure horizon is level, diagonals are content

**Best for**:
- Action sequences
- Sports
- Dynamic movement
- Creating tension
- Breaking monotony

---

### 5. Leading Lines (誘導線構図)

**Auto-applied for**: Guiding viewer's eye, depth, perspective

**Description**:
Use natural or man-made lines to lead eye toward subject.

**Visual Effect**:
- Creates depth
- Guides attention
- Strong sense of perspective

**Prompt Modifiers**:

**Road/path**:
```
leading lines composition, road leading to subject, perspective depth
```

**Architecture**:
```
converging lines, architectural perspective leading to focal point
```

**Natural lines**:
```
natural leading lines, organic flow toward subject
```

**Multiple lines**:
```
multiple leading lines converging at subject
```

**Adjustment Tips**:
- "Lines too obvious" → Use `subtle leading lines`
- "Need stronger guidance" → Use `converging perspective lines`
- "Lines distract" → Soften with depth of field

**Best for**:
- Roads and paths
- Hallways and corridors
- Railways
- Rivers and shorelines
- Architecture

---

### 6. Frame Within Frame (額縁構図)

**Auto-applied for**: Focus emphasis, depth creation, isolation

**Description**:
Use elements in scene to create natural frame around subject.

**Visual Effect**:
- Draws eye to subject
- Creates depth layers
- Adds context and isolation simultaneously

**Prompt Modifiers**:

**Window frame**:
```
frame within frame, subject framed by window, layered composition
```

**Door frame**:
```
doorway framing subject, natural frame, depth layers
```

**Natural frame**:
```
tree branches framing subject, organic frame within frame
```

**Architecture frame**:
```
architectural elements framing subject, geometric frame
```

**Adjustment Tips**:
- "Frame too dark" → Add `bright frame, well-lit edges`
- "Subject lost" → Use `clear frame, strong subject contrast`
- "Too busy" → Use `simple frame, clean edges`

**Best for**:
- Windows and doors
- Archways
- Tree branches
- Mirrors
- Creating focus

---

### 7. Negative Space (ネガティブスペース)

**Auto-applied for**: Minimalism, isolation, emphasis

**Description**:
Use empty space around subject to create emphasis.

**Visual Effect**:
- Clean and minimal
- Subject stands out
- Creates mood (loneliness, peace, etc.)

**Prompt Modifiers**:

**Minimal**:
```
negative space composition, minimalist, subject with empty space
```

**Lots of space**:
```
vast negative space, small subject, emphasis through isolation
```

**Directional space**:
```
subject on left, negative space on right, directional gaze space
```

**Adjustment Tips**:
- "Too empty" → Add `subtle background interest`
- "Subject too small" → Reduce negative space amount
- "Need mood" → Specify space character: `peaceful white space`

**Best for**:
- Minimalist style
- Product photography
- Emotional isolation
- Clean aesthetics
- Modern design

---

### 8. Symmetry (シンメトリー)

**Auto-applied for**: Formal scenes, balance, architectural subjects

**Description**:
Perfect or near-perfect mirror balance across vertical or horizontal axis.

**Visual Effect**:
- Formal and stable
- Visually satisfying
- Strong and confident

**Prompt Modifiers**:

**Perfect symmetry**:
```
perfect symmetry, mirrored composition, bilateral balance
```

**Vertical symmetry**:
```
vertical symmetry, left-right mirror balance
```

**Horizontal symmetry**:
```
horizontal symmetry, top-bottom balance
```

**Radial symmetry**:
```
radial symmetry, centered circular balance
```

**Adjustment Tips**:
- "Too rigid" → Use `near-symmetry with subtle variation`
- "Need interest" → Add `asymmetric element for tension`
- "More impact" → Use `perfect bilateral symmetry`

**Best for**:
- Architecture
- Formal portraits
- Nature patterns
- Reflections
- Religious or ceremonial scenes

---

## Combining Compositions

### Common Combinations

**Rule of Thirds + Leading Lines**:
```
subject at rule of thirds intersection, leading lines guiding to subject
```

**Golden Ratio + Negative Space**:
```
golden ratio placement with generous negative space, minimalist elegance
```

**Centered + Symmetry**:
```
perfectly centered symmetrical composition, formal balance
```

**Diagonal + Leading Lines**:
```
diagonal leading lines creating dynamic flow, energetic movement
```

---

## Composition by Mood

| Mood | Primary Composition | Secondary | Avoid |
|------|-------------------|-----------|-------|
| **Peaceful** | Symmetry, Rule of thirds | Negative space | Diagonal |
| **Energetic** | Diagonal, Dynamic angles | Rule of thirds | Centered |
| **Formal** | Centered, Symmetry | Rule of thirds | Diagonal |
| **Intimate** | Centered tight, Close framing | Golden ratio | Negative space |
| **Lonely** | Negative space, Centered small | Rule of thirds | Symmetry |
| **Dramatic** | Diagonal, Low angle | Frame within frame | Symmetry |
| **Peaceful** | Golden ratio, Symmetry | Horizontal lines | Diagonal |

---

## Composition by Genre

### Educational Video
**Primary**: Rule of thirds (clear, balanced)
**Secondary**: Centered (direct focus)
**Technique**: Keep it simple and clear

### Marketing/Commercial
**Primary**: Golden ratio (aesthetic appeal)
**Secondary**: Centered (product focus), Negative space (clean)
**Technique**: Eye-catching and clean

### Narrative/Drama
**Primary**: All types (varies with story)
**Secondary**: Match to emotion
**Technique**: Serve the narrative

### Documentary
**Primary**: Rule of thirds (natural)
**Secondary**: As available in real situations
**Technique**: Adapt to reality

---

## Quick Adjustment Guide

### Problem: "Composition feels unbalanced"
**Solutions**:
- Check weight distribution (visual weight should balance)
- Add element to empty side
- Use negative space intentionally
- Try rule of thirds

### Problem: "Composition feels boring"
**Solutions**:
- Add diagonal elements
- Try off-center placement
- Use leading lines
- Add foreground interest

### Problem: "Composition feels chaotic"
**Solutions**:
- Simplify elements
- Use centered or symmetrical composition
- Increase negative space
- Use frame within frame to isolate

### Problem: "Subject gets lost"
**Solutions**:
- Use frame within frame
- Increase contrast with background
- Simplify background
- Center subject
- Use negative space

---

## Technical Considerations

### Aspect Ratios

**16:9 (Standard)**:
- All compositions work well
- Horizontal emphasis
- Good for landscapes and groups

**9:16 (Vertical/Phone)**:
- Vertical compositions excel
- Centered works well
- Avoid wide diagonal compositions

**1:1 (Square)**:
- Perfect for symmetry
- Centered compositions shine
- Golden ratio spiral works beautifully

**2.35:1 (Cinematic)**:
- Emphasizes horizontal elements
- Leading lines work excellently
- Requires wider compositions

---

## Pro Tips

### 1. Layer Your Compositions
Combine foreground, midground, background with composition rules:
```
rule of thirds with layered depth, foreground framing, subject in midground
```

### 2. Consider Movement Direction
If subject moves, leave space in direction of movement:
```
subject on left third, moving right, space ahead
```

### 3. Eye Line Direction
For portraits, leave space in direction subject is looking:
```
subject on right third, looking left, gaze space
```

### 4. Use Odd Numbers
Groups of 3 or 5 are more visually interesting than 2 or 4:
```
three subjects in rule of thirds composition, triangular arrangement
```

### 5. Break Rules Intentionally
- Center a character to show isolation despite action around them
- Use diagonal in calm scene to foreshadow coming conflict
- Symmetry in action scene for "calm before storm" effect

---

## Composition Checklist

Before finalizing a shot, check:

- [ ] Does composition support the story/emotion?
- [ ] Is the focal point clear?
- [ ] Is there visual balance (intentional imbalance okay if purposeful)?
- [ ] Does negative space serve a purpose?
- [ ] Are lines (horizon, architecture) level unless intentionally tilted?
- [ ] Does composition guide viewer's eye where you want?
- [ ] Is there adequate depth (foreground/background interest)?
- [ ] Does it work at the intended viewing size?

---

## Common Mistakes

### 1. Always Using Same Composition
**Problem**: Monotonous viewing experience
**Fix**: Vary compositions throughout storyboard

### 2. Fighting the Composition
**Problem**: Subject placement conflicts with natural lines
**Fix**: Work with environmental elements, not against

### 3. Ignoring the Rule of Thirds Grid
**Problem**: Important elements fall on dead spaces
**Fix**: Align key elements to grid intersections

### 4. Centered Everything
**Problem**: Static and boring
**Fix**: Use centered only when appropriate (formal, symmetry)

### 5. Too Complex
**Problem**: Multiple competing composition techniques
**Fix**: Choose one primary technique, others as subtle support

---

## Quick Reference Table

| Composition | Strength | Use For | Avoid For |
|-------------|----------|---------|-----------|
| **Rule of Thirds** | Versatile, natural | Most scenes | Formal moments |
| **Golden Ratio** | Aesthetic, elegant | Beauty, art | Fast action |
| **Centered** | Strong, direct | Portraits, formal | Dynamic action |
| **Diagonal** | Dynamic, energy | Action, tension | Calm, peaceful |
| **Leading Lines** | Depth, guidance | Perspective | Close-ups |
| **Frame within Frame** | Focus, depth | Isolation, emphasis | Wide establishing |
| **Negative Space** | Minimal, clean | Isolation, modern | Busy action |
| **Symmetry** | Formal, balanced | Architecture | Natural, casual |

---

This guide helps you understand and adjust AI-selected compositions for powerful visual storytelling.
