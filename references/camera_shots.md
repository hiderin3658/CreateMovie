# Camera Shots Reference Guide

Comprehensive guide to camera shots with auto-selection rules and adjustment tips.

## Auto-Selection Rules

The AI automatically selects camera shots based on scene type:

```python
scene_camera_rules = {
    'establishing': 'ELS',      # Location/environment setup
    'character_intro': 'MS',    # Character introduction
    'dialogue': 'MS/MCU',       # Conversation scenes
    'action': 'LS/MS',          # Action sequences
    'emotion': 'CU/ECU',        # Emotional expressions
    'conclusion': 'LS/ELS'      # Closing scenes
}
```

## Shot Types

### 1. Extreme Long Shot (ELS) - 超遠景

**Auto-selected for**: Opening scenes, scene transitions, endings

**Visual Effect**:
- Conveys grandeur and scale
- Shows character in relation to environment
- Creates sense of isolation or vastness

**Prompt Keywords**:
```
extreme wide shot, aerial view, vast landscape, establishing shot,
environmental context, panoramic view
```

**Usage Examples**:
- Opening: "A lone figure walking across vast desert plains"
- Transition: "Cityscape at dawn, skyscrapers reaching into clouds"
- Ending: "The group standing on hilltop overlooking valley below"

**Adjustment Tips**:
- "Want closer view" → Change to LS
- "Want drone perspective" → Add `drone aerial view, bird's eye`
- "Too distant" → Use `high angle wide shot` (between ELS and LS)

---

### 2. Long Shot (LS) - 遠景

**Auto-selected for**: Action sequences, group shots, body language

**Visual Effect**:
- Full body visible with environmental context
- Shows relationships between characters
- Balances subject and surroundings

**Prompt Keywords**:
```
wide shot, full body visible, environmental context,
full figure, establishing distance
```

**Usage Examples**:
- Action: "Two characters fighting, full bodies visible in frame"
- Group: "Five students gathered around table, all visible"
- Movement: "Character walking through corridor, full body"

**Adjustment Tips**:
- "Want to see facial expressions" → Change to MS
- "Too much empty space" → Use `tighter framing`
- "Need more drama" → Add camera movement or diagonal composition

---

### 3. Medium Shot (MS) - 中景

**Auto-selected for**: Dialogue, normal interactions, character focus

**Visual Effect**:
- Shows waist-up or knees-up
- Balances intimacy with context
- Most versatile and common shot

**Prompt Keywords**:
```
medium shot, waist up, conversational distance,
mid-shot, half body, comfortable framing
```

**Usage Examples**:
- Dialogue: "Two characters talking, waist up, facing each other"
- Presentation: "Teacher explaining at whiteboard, upper body visible"
- Interaction: "Character working at desk, hands and face visible"

**Adjustment Tips**:
- "Want more energy" → Add dynamic camera movement
- "Too static" → Use `slight dutch angle` or `over-shoulder`
- "Need intimacy" → Change to MCU or CU

---

### 4. Medium Close-Up (MCU) - 中クローズアップ

**Auto-selected for**: Important dialogue, emotional nuance, character focus

**Visual Effect**:
- Shows chest and head
- Captures facial expressions clearly
- More intimate than MS

**Prompt Keywords**:
```
medium close-up, chest and head, facial detail visible,
upper chest shot, intimate framing
```

**Usage Examples**:
- Dialogue: "Character speaking with emotion, shoulders up"
- Reaction: "Character listening intently, face and chest visible"
- Interview: "Subject answering question, professional framing"

**Adjustment Tips**:
- "Too tight" → Change to MS
- "Want more emotion" → Change to CU
- "Need context" → Pull back to MS with background

---

### 5. Close-Up (CU) - クローズアップ

**Auto-selected for**: Emotional moments, important details, emphasis

**Visual Effect**:
- Shows face and shoulders
- Captures subtle emotions
- Creates intimacy and connection

**Prompt Keywords**:
```
close-up shot, face and shoulders, emotional focus,
tight framing on face, detailed expression
```

**Usage Examples**:
- Emotion: "Character's face showing surprise, eyes wide"
- Emphasis: "Character making important decision, contemplative look"
- Connection: "Two characters' faces close, intimate moment"

**Adjustment Tips**:
- "Want eyes only" → Change to ECU
- "Too intense" → Change to MCU
- "Need more context" → Use MS with shallow depth of field

---

### 6. Extreme Close-Up (ECU) - 超クローズアップ

**Auto-selected for**: Extreme emotion, minute details, dramatic impact

**Visual Effect**:
- Shows eyes, mouth, or specific detail
- Creates intense focus
- Maximum emotional impact

**Prompt Keywords**:
```
extreme close-up, eyes only, intense detail,
macro shot, single feature, dramatic focus
```

**Usage Examples**:
- Drama: "Character's eyes filling with tears, extreme close-up"
- Detail: "Hand reaching for important object, fingers in focus"
- Tension: "Character's trembling lip, extreme close-up"

**Adjustment Tips**:
- **Use sparingly** - Loses impact if overused
- "Too intense" → Change to CU
- "Need more face" → Use CU showing full face
- Best for: Climactic moments, revelations, key decisions

---

## Combining Shots

### Typical Sequence Patterns

**Opening Sequence**:
1. ELS - Establish location
2. LS - Show character in environment
3. MS - Character doing action
4. CU - Character's expression

**Dialogue Sequence**:
1. MS - Two-shot of both characters
2. MCU - Speaker A
3. CU - Listener B reaction
4. MCU - Speaker B responds

**Action Sequence**:
1. LS - Wide view of action starting
2. MS - Character performing action
3. CU - Character's determined face
4. LS - Action result/impact

**Emotional Climax**:
1. MS - Character approaching moment
2. MCU - Building emotion
3. CU - Emotion peaks
4. ECU - Tears/eyes (climax)
5. MS - Resolution/aftermath

---

## Shot Duration Guidelines

| Shot Type | Typical Duration | Reason |
|-----------|------------------|---------|
| ELS | 8-12 seconds | Need time to absorb environment |
| LS | 6-10 seconds | Establish context and action |
| MS | 5-8 seconds | Standard pace, comfortable viewing |
| MCU | 4-6 seconds | Focused attention, quicker read |
| CU | 3-5 seconds | Intense emotion, brief impact |
| ECU | 2-4 seconds | Maximum intensity, very brief |

**Note**: Adjust based on:
- **Fast-paced action**: Shorter durations
- **Contemplative scenes**: Longer durations
- **Dialogue**: Match to speaking pace
- **Music sync**: Align with musical beats

---

## Common Mistakes to Avoid

### 1. Too Many Close-Ups
**Problem**: Loses sense of space and context
**Solution**: Intersperse with wider shots (LS, MS)

### 2. Static Shot Selection
**Problem**: All same shot type becomes monotonous
**Solution**: Vary shots - use shot progression patterns

### 3. Wrong Shot for Scene
**Problem**: CU in action scene, ELS for intimate moment
**Solution**: Follow auto-selection rules or adjust purposefully

### 4. Rapid Shot Changes
**Problem**: Cuts too fast between different shot sizes
**Solution**: Use gradual progression (LS → MS → CU)

### 5. Neglecting Transitions
**Problem**: Jarring jumps between shots
**Solution**: Use similar shot sizes or natural breaks

---

## Pro Tips

### 1. Match Shot to Emotion
- **Distant emotions** (loneliness, isolation) → ELS, LS
- **Moderate emotions** (conversation, interaction) → MS, MCU
- **Intense emotions** (love, anger, fear) → CU, ECU

### 2. Consider Aspect Ratio
- **16:9 (Standard)**: All shots work well
- **2.35:1 (Cinematic)**: Favors wider shots (ELS, LS)
- **9:16 (Vertical)**: Favors tighter shots (MS, CU)

### 3. Use Depth of Field
- **Wide shots**: Keep everything in focus (deep DOF)
- **Close shots**: Blur background (shallow DOF)

### 4. Frame for Next Shot
- If cutting from LS to CU, frame subject in lower third of LS
- Prepares viewer's eye for the transition

### 5. Break Rules Intentionally
- ECU at opening for mystery/intrigue
- ELS for emotional moment to show loneliness
- MS throughout for documentary-style realism

---

## Quick Reference Table

| Shot | Distance | Use Case | Duration | DOF |
|------|----------|----------|----------|-----|
| ELS | Very Far | Establish, scale | 8-12s | Deep |
| LS | Far | Action, groups | 6-10s | Deep |
| MS | Medium | Dialogue, default | 5-8s | Medium |
| MCU | Close | Emotion, focus | 4-6s | Medium |
| CU | Very Close | Intensity, detail | 3-5s | Shallow |
| ECU | Extreme | Climax, emphasis | 2-4s | Very Shallow |

---

## Troubleshooting

### "My shots feel disconnected"
→ Use shot progression: Don't jump from ELS to ECU
→ Add transitional MS or MCU shots

### "My video feels slow"
→ Use more MS and MCU, fewer long holds on ELS
→ Increase pace of cuts in action scenes

### "My video feels rushed"
→ Let wider shots (ELS, LS) breathe longer
→ Don't cut away from CU too quickly

### "Can't decide between two shot types"
→ Consider the emotion: Closer = more intimate
→ Consider the context: Wider = more information
→ Generate both and compare

---

## Examples by Genre

### Educational Video
- Primary: MS (explain), CU (detail)
- Secondary: LS (demonstrate), MCU (engage)
- Rare: ELS, ECU

### Marketing/Commercial
- Primary: MS (product), MCU (person), CU (feature)
- Secondary: LS (lifestyle), ECU (detail)
- Pattern: Fast-paced variety

### Narrative Drama
- Full range: ELS to ECU
- Follow emotional arc
- More CU/ECU at climax

### Documentary
- Primary: MS (interview), LS (context)
- Secondary: CU (emotion), ELS (scope)
- Natural, less stylized

---

This guide helps you understand and adjust the AI's automatic shot selection for optimal storytelling.
