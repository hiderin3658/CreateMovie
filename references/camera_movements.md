# Camera Movements Reference Guide

Complete guide to camera movements with auto-selection rules and ItoV prompt optimization.

## Auto-Selection by Scene Type

```python
movement_selection = {
    'opening': 'slow_zoom_in' or 'establishing_pan',
    'dialogue': 'static' or 'gentle_push',
    'action': 'tracking' or 'handheld',
    'revelation': 'dolly_in' or 'crane_up',
    'ending': 'slow_pull_back' or 'fade'
}
```

---

## Movement Types

### 1. Static (固定)

**Auto-selected for**: Dialogue, observation, formal scenes

**Description**:
Camera remains completely still. No movement.

**Visual Effect**:
- Stable and grounded
- Allows focus on content
- Professional and controlled

**ItoV Prompt**:

**Basic**:
```
static camera, no movement, stable frame, locked-off shot
```

**With slight life**:
```
static camera with subtle breathing movement, minimal natural drift
```

**Very stable**:
```
tripod-mounted static camera, perfectly still, no shake
```

**Adjustment Examples**:
- "Need some life" → Add `subtle breathing movement`
- "Too rigid" → Add `barely perceptible drift`
- "Documentary feel" → Use `handheld static` (still but human)

**Best for**:
- Interview/dialogue
- Observation
- Formal presentation
- Product showcase
- Establishing context

**Duration**: Any length (most versatile)

---

### 2. Pan (パン)

**Auto-selected for**: Wide space reveal, following action, scanning

**Description**:
Camera rotates horizontally on fixed axis.

**Visual Effect**:
- Reveals space gradually
- Follows moving subjects
- Creates smooth flow

**ItoV Prompt**:

**Basic pan right**:
```
camera pans right slowly, smooth horizontal movement, steady rotation
```

**Basic pan left**:
```
camera pans left, sweeping across scene, horizontal tracking
```

**Fast pan**:
```
quick pan right, fast horizontal sweep, dynamic movement
```

**Slow reveal pan**:
```
slow deliberate pan left, revealing environment gradually, 10 seconds
```

**Following pan**:
```
pan right following subject movement, smooth tracking, keeping subject centered
```

**Adjustment Examples**:
- Speed: `slow pan` vs `fast pan` vs `medium-paced pan`
- Direction: `pan left to right` or `pan right to left`
- Purpose: `revealing pan` vs `following pan` vs `searching pan`

**Best for**:
- Wide landscapes
- Revealing space
- Following walking characters
- Showing relationships between spaces
- Group scenes

**Duration**: 6-12 seconds (slower for wider pans)

---

### 3. Tilt (ティルト)

**Auto-selected for**: Vertical reveals, looking up/down

**Description**:
Camera rotates vertically on fixed axis.

**Visual Effect**:
- Shows height or depth
- Reveals vertical elements
- Creates anticipation

**ItoV Prompt**:

**Tilt up**:
```
camera tilts up slowly, revealing height, vertical movement from ground to sky
```

**Tilt down**:
```
camera tilts down, descending gaze, from sky to ground reveal
```

**Fast tilt**:
```
quick tilt up, rapid vertical movement, dramatic reveal
```

**Character reveal**:
```
slow tilt up from feet to face, character introduction, vertical scan
```

**Adjustment Examples**:
- "Show scale" → `tilt up revealing full height of building`
- "Dramatic reveal" → `quick tilt up to face`
- "Descending" → `tilt down following fall`

**Best for**:
- Tall buildings/trees
- Character introduction (bottom to top)
- Looking down from height
- Vertical action
- Scale demonstration

**Duration**: 4-8 seconds

---

### 4. Zoom (ズーム)

**Auto-selected for**: Focus emphasis, attention direction, surprise

**Description**:
Lens changes focal length, appearing to move toward or away from subject.

**Visual Effect**:
- Draws attention
- Creates tension or release
- Artificial but impactful

**ItoV Prompt**:

**Zoom in (slow)**:
```
slow zoom in, gradually approaching subject, increasing tension, 8 seconds
```

**Zoom in (fast)**:
```
quick zoom in, rapid approach, dramatic emphasis
```

**Zoom out**:
```
zoom out slowly, revealing wider context, pulling back perspective
```

**Crash zoom**:
```
fast dramatic zoom in, intense focus, sudden attention
```

**Subtle zoom**:
```
gentle imperceptible zoom in, slowly intensifying, very gradual
```

**Adjustment Examples**:
- Intensity: `subtle zoom` vs `dramatic zoom` vs `crash zoom`
- Speed: `slow gradual zoom over 10 seconds` vs `quick 2-second zoom`
- Direction: `zoom in` vs `zoom out`

**Best for**:
- Emphasizing reactions
- Building tension
- Focusing attention
- Surprise moments
- Time transitions

**Duration**: 3-10 seconds (faster for dramatic, slower for subtle)

---

### 5. Dolly / Track (ドリー/トラック)

**Auto-selected for**: Immersion, approach, following action

**Description**:
Camera physically moves toward, away, or alongside subject.

**Visual Effect**:
- Natural movement feel
- Changes perspective and parallax
- More organic than zoom

**ItoV Prompt**:

**Dolly in**:
```
dolly forward toward subject, camera physically moving closer, smooth approach
```

**Dolly out**:
```
dolly back away from subject, pulling back, revealing more space
```

**Tracking shot (following)**:
```
tracking shot following character, camera moving parallel to subject, smooth glide
```

**Dolly + zoom (vertigo effect)**:
```
dolly in while zooming out, vertigo effect, disorienting perspective shift
```

**Slow dolly**:
```
slow gentle dolly forward, subtle approach, building intimacy over 12 seconds
```

**Adjustment Examples**:
- "More intimate" → `dolly in slowly toward face`
- "Reveal world" → `dolly back revealing environment`
- "Follow action" → `tracking dolly following movement`
- "Hitchcock effect" → `dolly zoom (vertigo effect)`

**Best for**:
- Approaching subject
- Following movement
- Creating intimacy
- Revealing environment
- Smooth professional movement

**Duration**: 6-15 seconds (can be longer for subtle moves)

---

### 6. Truck (トラック)

**Auto-selected for**: Lateral movement, passing scenes

**Description**:
Camera moves laterally (sideways) parallel to subject or scene.

**Visual Effect**:
- Smooth lateral flow
- Shows depth layers
- Professional, cinematic feel

**ItoV Prompt**:

**Truck right**:
```
camera trucks right, smooth lateral movement, passing scene from left to right
```

**Truck left**:
```
camera trucks left, sideways motion, gliding past subjects
```

**Trucking with subject**:
```
truck right keeping subject centered, lateral tracking, smooth parallel movement
```

**Adjustment Examples**:
- "Follow walking" → `truck right with character walking`
- "Pass by scene" → `truck left passing stationary subjects`
- "Show depth" → `truck revealing depth layers`

**Best for**:
- Following walking characters from side
- Passing multiple subjects
- Showing depth parallax
- Professional, cinematic shots

**Duration**: 6-12 seconds

---

### 7. Pedestal (ペデスタル)

**Auto-selected for**: Vertical camera movement

**Description**:
Camera moves vertically up or down while keeping level.

**Visual Effect**:
- Adjust framing vertically
- Follow vertical action
- Maintain level horizon

**ItoV Prompt**:

**Pedestal up**:
```
camera pedestal up, rising vertically while keeping level, smooth ascent
```

**Pedestal down**:
```
camera pedestal down, lowering vertically, descending while level
```

**Adjustment Examples**:
- "Rise with subject" → `pedestal up following character standing`
- "Lower view" → `pedestal down for ground perspective`

**Best for**:
- Following standing/sitting actions
- Adjusting vertical framing
- Maintaining level while moving vertically

**Duration**: 3-6 seconds

---

### 8. Crane / Jib (クレーン)

**Auto-selected for**: Grand reveals, aerial perspectives, dramatic moves

**Description**:
Camera moves on boom arm, allowing sweeping vertical and horizontal moves.

**Visual Effect**:
- Epic and cinematic
- God's eye perspective changes
- Grand scale feeling

**ItoV Prompt**:

**Crane up**:
```
crane up shot, camera rising on boom, sweeping upward reveal, majestic movement
```

**Crane down**:
```
crane down from height, descending into scene, dramatic entry
```

**Crane arc**:
```
sweeping crane shot arcing around subject, circular reveal, epic movement
```

**Adjustment Examples**:
- "Grand opening" → `crane up from ground level to aerial view`
- "Dramatic entry" → `crane down from above into close-up`
- "Reveal scale" → `crane back and up, revealing vast environment`

**Best for**:
- Opening/closing shots
- Dramatic reveals
- Showing scale
- Epic moments
- Transitional shots

**Duration**: 10-20 seconds (longer moves are impactful)

---

### 9. Handheld (ハンドヘルド)

**Auto-selected for**: Documentary feel, tension, realism, action

**Description**:
Camera held by operator, natural shake and movement.

**Visual Effect**:
- Realistic and immersive
- Adds energy and tension
- Documentary authenticity

**ItoV Prompt**:

**Basic handheld**:
```
handheld camera, natural shake, documentary style, organic movement
```

**Active handheld**:
```
dynamic handheld, following action, energetic shake, tense atmosphere
```

**Subtle handheld**:
```
gentle handheld, slight natural movement, barely perceptible shake
```

**Chaotic handheld**:
```
intense handheld, rapid movements, shaky, high tension, action scene
```

**Adjustment Examples**:
- "More stable" → `steadicam handheld, smooth but organic`
- "More intense" → `chaotic handheld, rapid movements`
- "Documentary" → `observational handheld, natural operator movement`

**Best for**:
- Action sequences
- Documentary style
- POV shots
- Tension/urgency
- Realistic moments

**Duration**: Any length, but intensity affects viewer comfort

---

### 10. Steadicam / Gimbal (ステディカム)

**Auto-selected for**: Smooth complex movements

**Description**:
Stabilized camera allowing smooth movement through space.

**Visual Effect**:
- Impossibly smooth
- Floating sensation
- Professional and polished

**ItoV Prompt**:

**Floating movement**:
```
steadicam shot, smooth gliding movement, floating through space, seamless flow
```

**Following smoothly**:
```
gimbal-stabilized tracking, smoothly following subject, effortless movement
```

**Complex move**:
```
steadicam moving through environment, weaving smoothly, continuous single shot
```

**Adjustment Examples**:
- "Through doorways" → `steadicam gliding through doors and corridors`
- "Around subject" → `circular steadicam move around subject`
- "Impossible smooth" → `gimbal-stabilized perfect smoothness`

**Best for**:
- Long takes
- Following through spaces
- Complex choreography
- Professional, polished feel
- Immersive POV

**Duration**: 10-60 seconds (can be very long)

---

## Combining Movements

### Common Combinations

**Dolly + Pan**:
```
dolly forward while panning left, complex approach, revealing subject
```

**Crane + Pan**:
```
crane up while panning across scene, sweeping majestic reveal
```

**Truck + Tilt**:
```
truck right while tilting up, dynamic compound movement
```

**Zoom + Track (Vertigo Effect)**:
```
dolly in while zooming out, vertigo effect, psychological disorientation
```

---

## Movement by Emotion

| Emotion | Primary Movement | Secondary | Avoid |
|---------|-----------------|-----------|-------|
| **Calm** | Static, Slow dolly | Gentle pan | Handheld, Fast |
| **Tense** | Handheld, Slow zoom in | Static (uncomfortable) | Smooth crane |
| **Exciting** | Tracking, Handheld | Fast pan | Static |
| **Intimate** | Slow dolly in, Static | Subtle zoom | Crane, Fast |
| **Epic** | Crane, Sweeping | Slow dolly | Static, Handheld |
| **Mysterious** | Slow dolly, Creeping | Gentle pan | Fast, Jerky |
| **Chaotic** | Intense handheld, Fast | Quick pan/tilt | Static, Smooth |

---

## Movement Speed Guide

| Speed | Duration (for full move) | Use Case |
|-------|-------------------------|----------|
| **Very Slow** | 15-20 seconds | Subtle, imperceptible |
| **Slow** | 10-15 seconds | Deliberate, controlled |
| **Medium** | 6-10 seconds | Standard, natural |
| **Fast** | 3-5 seconds | Dramatic, attention-grabbing |
| **Very Fast** | 1-2 seconds | Shock, surprise, whip |

---

## Troubleshooting

### "Movement feels too fast"
**Solutions**:
- Increase duration: `over 12 seconds`
- Add `slow`, `gentle`, `gradual`
- Reduce movement amount

### "Movement feels too slow"
**Solutions**:
- Decrease duration
- Add `dynamic`, `energetic`
- Increase movement extent

### "Movement feels mechanical"
**Solutions**:
- Add `slight ease in/out`
- Use `natural acceleration`
- Try handheld or gimbal for organic feel

### "Movement distracts from subject"
**Solutions**:
- Reduce speed
- Use static or subtle movement
- Match movement to action

### "Need more energy"
**Solutions**:
- Use handheld or tracking
- Increase speed
- Add dynamic compound movements

---

## Pro Tips

### 1. Match Movement to Story Beat
- **Beginning**: Slow, exploratory (slow dolly, pan)
- **Building**: Increasing pace (medium tracking)
- **Climax**: Fast, intense (handheld, fast movements)
- **Resolution**: Calming (slow pull back, static)

### 2. Motivate Camera Movement
Always have a reason:
- **Following action**: Track with character
- **Revealing information**: Pan to new element
- **Character POV**: Mimic how they'd look
- **Emotional shift**: Zoom during realization

### 3. Ease In and Out
Movements should accelerate and decelerate naturally:
```
slow dolly in, ease in at start, ease out at end, natural acceleration
```

### 4. Use Movement Sparingly
Not every shot needs movement:
- Static shots have power
- Movement should serve purpose
- Too much movement = dizzy viewers

### 5. Match Music Rhythm
Sync camera moves to music beats:
- Start movement on beat
- Hit key point on accent
- Match pace to tempo

---

## ItoV Prompt Formula

For optimal image-to-video results, use this structure:

```
[Movement Type] + [Speed/Quality] + [Subject Action] + [Duration] + [Mood] + [Consistency Note]
```

**Example**:
```
Slow dolly forward, smooth approach, character turning to camera,
8 seconds, building tension, maintain composition balance throughout
```

---

## Movement Checklist

Before finalizing camera movement:

- [ ] Does movement serve the story?
- [ ] Is speed appropriate for mood?
- [ ] Will it be comfortable to watch?
- [ ] Does it reveal information appropriately?
- [ ] Is duration suitable for movement extent?
- [ ] Will it work with intended music/pacing?
- [ ] Does it match the visual style (documentary vs cinematic)?
- [ ] Is the first frame well-composed for the movement?

---

## Common Mistakes

### 1. Too Much Movement
**Problem**: Every shot moves, viewer gets dizzy
**Fix**: Use static shots to ground viewer

### 2. Aimless Movement
**Problem**: Camera moves without purpose
**Fix**: Always motivate movement with story reason

### 3. Wrong Speed
**Problem**: Movement too fast or too slow for context
**Fix**: Match speed to emotion and pacing

### 4. Fighting the Action
**Problem**: Camera moves opposite to subject
**Fix**: Move with or complement subject movement

### 5. Ignoring First Frame
**Problem**: Movement doesn't work with starting composition
**Fix**: Design first frame knowing where movement goes

---

## Quick Reference Table

| Movement | Difficulty | Impact | Best For | Avoid For |
|----------|-----------|--------|----------|-----------|
| **Static** | Easy | Low-Med | Dialogue, formal | Dynamic action |
| **Pan** | Easy | Medium | Reveal, follow | Close emotion |
| **Tilt** | Easy | Medium | Vertical reveal | Horizontal |
| **Zoom** | Easy | High | Emphasis, tension | Natural realism |
| **Dolly** | Medium | High | Approach, immersion | Fast action |
| **Track** | Medium | High | Following | Static subjects |
| **Crane** | Hard | Very High | Epic, grand | Intimate |
| **Handheld** | Easy | Medium | Realism, tension | Formal, calm |
| **Steadicam** | Hard | High | Complex smooth | Simple shots |

---

## Movement Intensity Ladder

From most calm to most energetic:

1. **Static** - No movement
2. **Subtle dolly** - Barely perceptible approach
3. **Slow pan** - Gentle reveal
4. **Medium dolly** - Clear but smooth
5. **Tracking** - Active following
6. **Fast pan/tilt** - Quick revelation
7. **Dynamic crane** - Sweeping movement
8. **Handheld** - Energetic shake
9. **Intense handheld** - Chaotic, urgent

Choose position on ladder based on scene energy needs.

---

This guide helps you understand and adjust AI-selected camera movements for dynamic storytelling.
