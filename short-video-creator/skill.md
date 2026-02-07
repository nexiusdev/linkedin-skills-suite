---
name: short-video-creator
description: Create short-form videos (15-60s) for multiple platforms using Remotion. Finds trending topics from X, LinkedIn, and Reddit, scores them for video suitability, generates AI images via Gemini, creates animated videos with AI voice over (ElevenLabs) and royalty-free background music (Pixabay), and saves to output folder. Use when user says "create short video", "make a video", "video content", "daily video", or wants to create short-form video content for any platform (Instagram, TikTok, YouTube Shorts, LinkedIn).
---

# Short Video Creator

Create short-form videos (15-60 seconds) with full audio production:
- Find trending topics and score for video suitability
- Generate AI visuals via Gemini
- Produce Remotion-animated videos
- Add AI voice over via ElevenLabs
- Include royalty-free background music from Pixabay
- Export for multi-platform distribution (Instagram, TikTok, YouTube Shorts, LinkedIn)

## Trigger

- "create short video"
- "make a video"
- "video content"
- "daily video"
- "short video about [topic]"
- "create video for [platform]"

## Business Context

All videos align with Nexius Labs positioning:
- **Core Expertise**: Agentic AI systems for SMEs
- **Domain**: Finance, ERP, CRM automation
- **Vision**: AI-native business OS
- **Audience**: SME founders, operations leaders in ASEAN
- **Tone**: Practical implementation over hype, democratizing AI

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  1. FIND TRENDING TOPICS                                    │
│     x-trender + linkedin-trender + reddit-trender           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  2. SCORE FOR VIDEO SUITABILITY                             │
│     Visual potential + Hook strength + Business relevance   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  3. AUTO-SELECT BEST TOPIC                                  │
│     AI picks highest scoring topic                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  4. GENERATE SCRIPT & VISUALS                               │
│     Script + Gemini image generation                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  5. CREATE REMOTION VIDEO (SILENT)                          │
│     Animated video with text overlays                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  6. GENERATE VOICE OVER                                     │
│     ElevenLabs text-to-speech from script                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  7. ADD BACKGROUND MUSIC                                    │
│     Pixabay royalty-free music selection                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  8. RENDER FINAL VIDEO WITH AUDIO                           │
│     Combine video + voice over + music                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  9. SAVE TO OUTPUT FOLDER                                   │
│     Final video + metadata for posting                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Find Trending Topics

### Multi-Source Aggregation

Run trending analysis from all available sources in parallel:

**Source 1: X.com (x-trender)**
- Navigate to x.com/explore
- Look for: Tech/AI discussions, business trends, viral takes
- Filter: Individual thought leaders only, 100+ likes

**Source 2: LinkedIn (linkedin-trender)**
- Analyze LinkedIn feed
- Look for: B2B trends, SME challenges, AI implementation stories
- Filter: 20+ likes, 10+ comments, individuals only

**Source 3: Reddit (reddit-trender)**
- Check r/technology, r/artificial, r/smallbusiness, r/startups
- Look for: Discussions with 100+ upvotes, genuine questions/pain points

### Topic Extraction Template

For each source, extract:

```
TOPIC: [Core subject]
SOURCE: [X / LinkedIn / Reddit]
ENGAGEMENT: [Metrics]
ANGLE: [What made it resonate]
AUTHOR: [Who posted, their authority]
URL: [Link for reference]
```

---

## Step 2: Score Topics for Video Suitability

Not all trending topics work as videos. Score each topic on these criteria:

### Video Suitability Matrix

| Criteria | Weight | Score 1-10 | Description |
|----------|--------|------------|-------------|
| **Visual Potential** | 25% | 1-10 | Can it be represented as an image/animation? |
| **Hook Strength** | 25% | 1-10 | Does it have a strong first 3-second hook? |
| **Business Relevance** | 20% | 1-10 | Aligns with Agentic AI/SME positioning? |
| **Simplicity** | 15% | 1-10 | Can be explained in 30-60 seconds? |
| **Shareability** | 15% | 1-10 | Would viewers share/save this? |

### Scoring Guidelines

**Visual Potential (1-10):**
- 9-10: Inherently visual (diagrams, before/after, demos)
- 7-8: Can be visualized with metaphor (abstract concepts made concrete)
- 5-6: Requires creative visualization
- 1-4: Heavily text/data dependent, poor video fit

**Hook Strength (1-10):**
- 9-10: Pattern interrupt, controversy, surprising stat
- 7-8: Strong curiosity gap, relatable pain point
- 5-6: Standard educational hook
- 1-4: Weak or unclear hook potential

**Business Relevance (1-10):**
- 9-10: Core expertise (Agentic AI, SME automation)
- 7-8: Adjacent (general AI, business efficiency)
- 5-6: Loosely related (tech trends, business tips)
- 1-4: Off-topic (entertainment, unrelated news)

**Simplicity (1-10):**
- 9-10: One clear insight, easy to grasp
- 7-8: 2-3 connected points
- 5-6: Requires explanation but doable
- 1-4: Too complex for short video

**Shareability (1-10):**
- 9-10: "I need to show this to my team"
- 7-8: Bookmark-worthy insight
- 5-6: Interesting but not urgent
- 1-4: Low save/share potential

### Video Suitability Score Calculation

```
Score = (Visual × 0.25) + (Hook × 0.25) + (Relevance × 0.20) + (Simplicity × 0.15) + (Shareability × 0.15)
```

**Priority Tiers:**
- **EXCELLENT** (8.0-10): Create video immediately
- **GOOD** (6.5-7.9): Strong candidate
- **FAIR** (5.0-6.4): Consider with modifications
- **SKIP** (<5.0): Not suitable for video format

---

## Step 3: Auto-Select Best Topic

After scoring all topics, **automatically select the highest-scoring topic**.

### Selection Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIDEO TOPIC ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sources checked: X.com, LinkedIn, Reddit
Topics found: [X]
Topics scored: [Y]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP 3 VIDEO-SUITABLE TOPICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1 [TOPIC NAME]
   Source: [X/LinkedIn/Reddit]
   Score: [X.X] - [EXCELLENT/GOOD/FAIR]

   Visual: [X]/10 | Hook: [X]/10 | Relevance: [X]/10
   Simple: [X]/10 | Share: [X]/10

   Why it works: [1-2 sentence explanation]

#2 [TOPIC NAME]
   Source: [Source]
   Score: [X.X] - [Rating]
   [Same format]

#3 [TOPIC NAME]
   Source: [Source]
   Score: [X.X] - [Rating]
   [Same format]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SELECTED: #1 - [TOPIC NAME]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Selection rationale: [Why this topic is best for video]

Proceeding with video creation...
```

User can override: "use topic #2 instead" or "suggest a different angle"

---

## Step 4: Generate Script & Visuals

### Video Script Structure

**Template (30-second video):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIDEO SCRIPT: [TOPIC]
Duration: [30/45/60] seconds
Platform: [Target platform or "Multi-platform"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCENE 1: HOOK (0-3 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Text on screen: "[Pattern interrupt / Question / Stat]"
Visual: [Background description]
Audio cue: [If any]

SCENE 2: CONTEXT (3-8 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Text on screen: "[The problem / The situation]"
Visual: [Visual metaphor or illustration]

SCENE 3: INSIGHT (8-20 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Text on screen: "[Key insight - 2-3 points]"
Visual: [Diagram / Animation / Demo]

SCENE 4: TAKEAWAY (20-27 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Text on screen: "[Actionable takeaway]"
Visual: [Supporting visual]

SCENE 5: CTA (27-30 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Text on screen: "[Follow for more / Save this / Comment]"
Visual: [Brand or profile callout]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Image Generation via Gemini

Using Claude for Chrome, generate background image:

**Gemini Prompt Template:**

```
Create a professional, eye-catching image for a short video about [TOPIC].

Requirements:
- Style: Modern, bold, social media-ready
- Dimensions: 1080x1920 (9:16 vertical)
- Composition: Leave center area relatively simple for text overlay
- Colors: High contrast, vibrant, works on mobile
- Theme: [SPECIFIC VISUAL METAPHOR from script]
- Mood: [Professional / Inspiring / Urgent / Educational]

Do NOT include:
- Text or words in the image
- Watermarks
- Busy patterns that compete with overlays
- Stock photo aesthetic
- Faces (unless specifically requested)

Should feel: Premium, scroll-stopping, shareable
```

**Browser Automation:**
1. Navigate to `gemini.google.com/app`
2. Enter image prompt
3. Wait for generation
4. Click to expand image
5. Take screenshot (save `imageId`)

---

## Step 5: Create Remotion Video

### Project Setup

Save files to: `short-video-creator/projects/[date]-[topic-slug]/`

```
[date]-[topic-slug]/
├── public/
│   └── background.png (Gemini image)
├── src/
│   ├── Root.tsx
│   └── ShortVideo.tsx
├── package.json
├── remotion.config.ts
└── metadata.json
```

### Remotion Composition

```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { ShortVideo } from "./ShortVideo";

export const RemotionRoot = () => {
  return (
    <Composition
      id="ShortVideo"
      component={ShortVideo}
      durationInFrames={900}  // 30 seconds at 30fps
      fps={30}
      width={1080}
      height={1920}  // 9:16 vertical
      defaultProps={{
        hook: "Your hook text here",
        context: "The context line",
        insights: ["Insight 1", "Insight 2", "Insight 3"],
        takeaway: "Your actionable takeaway",
        cta: "Follow for more!",
        brandName: "Nexius Labs",
      }}
    />
  );
};
```

### Animation Component

```tsx
// src/ShortVideo.tsx
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
  spring,
} from "remotion";

type Props = {
  hook: string;
  context: string;
  insights: string[];
  takeaway: string;
  cta: string;
  brandName: string;
};

export const ShortVideo: React.FC<Props> = ({
  hook,
  context,
  insights,
  takeaway,
  cta,
  brandName,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Ken Burns zoom effect on background
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.15], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      {/* Background Image with Ken Burns */}
      <Img
        src={staticFile("background.png")}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />

      {/* Dark gradient overlay */}
      <AbsoluteFill
        style={{
          background: "linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%)",
        }}
      />

      {/* Scene 1: Hook (0-3 seconds) */}
      <Sequence from={0} durationInFrames={3 * fps}>
        <AnimatedText text={hook} style="hook" />
      </Sequence>

      {/* Scene 2: Context (3-8 seconds) */}
      <Sequence from={3 * fps} durationInFrames={5 * fps}>
        <AnimatedText text={context} style="context" />
      </Sequence>

      {/* Scene 3: Insights (8-20 seconds) */}
      <Sequence from={8 * fps} durationInFrames={12 * fps}>
        <InsightsList insights={insights} />
      </Sequence>

      {/* Scene 4: Takeaway (20-27 seconds) */}
      <Sequence from={20 * fps} durationInFrames={7 * fps}>
        <AnimatedText text={takeaway} style="takeaway" />
      </Sequence>

      {/* Scene 5: CTA (27-30 seconds) */}
      <Sequence from={27 * fps} durationInFrames={3 * fps}>
        <CTASection cta={cta} brandName={brandName} />
      </Sequence>
    </AbsoluteFill>
  );
};

// Animated text component with spring animation
const AnimatedText: React.FC<{ text: string; style: string }> = ({ text, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 0.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  const translateY = spring({
    frame,
    fps,
    config: { damping: 200 },
  }) * -30 + 30;

  const styles: Record<string, React.CSSProperties> = {
    hook: {
      fontSize: 72,
      fontWeight: 800,
      textTransform: "uppercase",
      letterSpacing: 2,
    },
    context: {
      fontSize: 48,
      fontWeight: 500,
    },
    takeaway: {
      fontSize: 56,
      fontWeight: 700,
      background: "rgba(255,215,0,0.9)",
      color: "#000",
      padding: "20px 40px",
      borderRadius: 12,
    },
  };

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <div
        style={{
          color: "white",
          textAlign: "center",
          textShadow: "2px 2px 8px rgba(0,0,0,0.8)",
          padding: "0 60px",
          maxWidth: "90%",
          ...styles[style],
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// Insights list with staggered animation
const InsightsList: React.FC<{ insights: string[] }> = ({ insights }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "flex-start",
        padding: "0 60px",
      }}
    >
      {insights.map((insight, index) => {
        const delay = index * fps; // 1 second delay between each
        const localFrame = Math.max(0, frame - delay);

        const opacity = interpolate(localFrame, [0, 0.3 * fps], [0, 1], {
          extrapolateRight: "clamp",
        });

        const translateX = interpolate(localFrame, [0, 0.3 * fps], [-50, 0], {
          extrapolateRight: "clamp",
        });

        return (
          <div
            key={index}
            style={{
              opacity,
              transform: `translateX(${translateX}px)`,
              fontSize: 44,
              fontWeight: 600,
              color: "white",
              textShadow: "2px 2px 6px rgba(0,0,0,0.7)",
              marginBottom: 30,
              display: "flex",
              alignItems: "center",
              gap: 20,
            }}
          >
            <span style={{
              background: "#FFD700",
              color: "#000",
              width: 50,
              height: 50,
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontWeight: 800,
              fontSize: 28,
            }}>
              {index + 1}
            </span>
            {insight}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// CTA section with pulse animation
const CTASection: React.FC<{ cta: string; brandName: string }> = ({ cta, brandName }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 0.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  const scale = interpolate(
    frame % (fps / 2),
    [0, fps / 4, fps / 2],
    [1, 1.05, 1],
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 200,
        opacity,
      }}
    >
      <div
        style={{
          fontSize: 52,
          fontWeight: 700,
          color: "#FFD700",
          textShadow: "2px 2px 6px rgba(0,0,0,0.7)",
          textAlign: "center",
          transform: `scale(${scale})`,
        }}
      >
        {cta}
      </div>
      <div
        style={{
          fontSize: 32,
          fontWeight: 500,
          color: "white",
          marginTop: 20,
          opacity: 0.8,
        }}
      >
        @{brandName}
      </div>
    </AbsoluteFill>
  );
};
```

### Initial Render Command (Silent Video)

```bash
cd short-video-creator/output/[project-folder]/remotion
npm install
npx remotion render ShortVideo video.mp4
```

This creates the silent video with animations. Audio is added in the next steps.

---

## Step 6: Generate Voice Over

### ElevenLabs Text-to-Speech

Generate professional AI voice over from the video script.

**Browser Automation Steps:**

1. Navigate to `elevenlabs.io/app/speech-synthesis/text-to-speech`
2. Enter the full script as one continuous text:

```
[HOOK]. [CONTEXT]. [INSIGHT 1]. [INSIGHT 2]. [INSIGHT 3]. [TAKEAWAY]. [CTA].
```

**Example script for voice over:**
```
App releases just surged 60%. After 3 years of flat growth, AI coding tools changed everything. Non-coders are building real apps. Tools like Claude and Cursor lead the way. The barrier to building just disappeared. You don't need to code anymore. You need to create. Follow for more AI insights.
```

3. **Voice Selection:**
   - **Rachel** - Clear, professional female narrator (recommended)
   - **Adam** - Confident male narrator
   - **Clyde** - Warm, engaging male voice

4. **Model:** Eleven Multilingual v2

5. Click "Generate speech"

6. Download the MP3 file when ready (file downloads to `C:\Users\melve\Downloads\`)

7. Check Downloads folder and copy to project:
```bash
# Check Downloads folder for the voice over file
powershell "Get-ChildItem 'C:\Users\melve\Downloads' -Filter 'ElevenLabs_*.mp3' | Sort-Object LastWriteTime -Descending | Select-Object -First 1"

# Copy voice over to project folder
powershell "Copy-Item 'C:\Users\melve\Downloads\ElevenLabs_*.mp3' '[project-folder]\voiceover.mp3'"

# Copy to Remotion public folder for rendering
powershell "Copy-Item '[project-folder]\voiceover.mp3' '[project-folder]\remotion\public\voiceover.mp3'"
```

### Voice Over Guidelines

| Aspect | Recommendation |
|--------|----------------|
| Pace | Natural, slightly faster than conversational |
| Duration | Should be ~20-25 seconds for 30-second video |
| Style | Informative, engaging, not robotic |
| Voice | Match to content tone (professional for business, energetic for trends) |

---

## Step 7: Add Background Music

### Pixabay Royalty-Free Music

Find suitable background music from Pixabay's free library.

**Browser Automation Steps:**

1. Navigate to `pixabay.com/music/search/`

2. **Search terms by video type:**
   - Tech/AI content: "corporate upbeat", "technology inspiring", "modern electronic"
   - Business/SME: "corporate motivational", "business background"
   - Educational: "inspiring background", "documentary"
   - Trending/News: "news background", "dynamic corporate"

3. **Filter criteria:**
   - Duration: Match video length (30-60 seconds ideally)
   - Mood: Upbeat, inspiring, professional
   - No lyrics (instrumental only)

4. Preview tracks and select one that:
   - Doesn't overpower voice over
   - Matches video energy
   - Has consistent tempo

5. Download MP3 file (file downloads to `C:\Users\melve\Downloads\`)

6. Check Downloads folder and copy to project:
```bash
# Check Downloads folder for recent music files
powershell "Get-ChildItem 'C:\Users\melve\Downloads' -Filter '*.mp3' | Sort-Object LastWriteTime -Descending | Select-Object -First 3"

# Copy music to project folder (use actual filename from Downloads)
powershell "Copy-Item 'C:\Users\melve\Downloads\[music-file].mp3' '[project-folder]\music.mp3'"

# Copy to Remotion public folder for rendering
powershell "Copy-Item '[project-folder]\music.mp3' '[project-folder]\remotion\public\music.mp3'"
```

### Recommended Music Sources

| Source | URL | License |
|--------|-----|---------|
| Pixabay Music | pixabay.com/music | Free for commercial use |
| Mixkit | mixkit.co/free-stock-music | Free for commercial use |

### Music Selection Tips

- **Volume**: Background music at 10-20% of voice over volume
- **Style**: Match energy without being distracting
- **Loop-friendly**: Choose tracks that work if video is extended
- **Avoid**: Tracks with sudden changes, heavy bass drops, or competing melodies

---

## Step 8: Render Final Video with Audio

### Update Remotion Component

Add Audio components to `ShortVideo.tsx`:

```tsx
import {
  AbsoluteFill,
  Audio,  // Add this import
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
  spring,
} from "remotion";

// Inside the ShortVideo component, add before closing </AbsoluteFill>:

      {/* Voice Over */}
      <Audio src={staticFile("voiceover.mp3")} volume={1} />

      {/* Background Music (lower volume) */}
      <Audio src={staticFile("music.mp3")} volume={0.15} />
    </AbsoluteFill>
```

### Volume Guidelines

| Audio Track | Volume Level | Notes |
|-------------|--------------|-------|
| Voice Over | 1.0 (100%) | Primary audio, full volume |
| Background Music | 0.10-0.20 (10-20%) | Subtle, doesn't compete with voice |

### Final Render Command

```bash
cd short-video-creator/output/[project-folder]/remotion
npx remotion render ShortVideo video_with_audio.mp4
```

### Copy Final Video to Output

```bash
# Copy final video to main output folder
powershell "Copy-Item '[project-folder]\remotion\video_with_audio.mp4' '[project-folder]\video_with_audio.mp4'"
```

---

## Step 9: Save to Output Folder

### Output Structure

All videos saved to: `short-video-creator/output/`

```
short-video-creator/output/
├── 2026-01-24_ai-vibe-coding/
│   ├── remotion/                    # Remotion project folder
│   │   ├── public/
│   │   │   ├── background.png       # Gemini-generated image
│   │   │   ├── voiceover.mp3        # ElevenLabs voice over
│   │   │   └── music.mp3            # Pixabay background music
│   │   ├── src/
│   │   │   ├── Root.tsx
│   │   │   ├── ShortVideo.tsx
│   │   │   └── index.ts
│   │   ├── package.json
│   │   ├── remotion.config.ts
│   │   ├── tsconfig.json
│   │   └── video_with_audio.mp4     # Rendered video
│   ├── video.mp4                    # Silent video (backup)
│   ├── video_with_audio.mp4         # Final video with audio
│   ├── voiceover.mp3                # Voice over file
│   ├── music.mp3                    # Background music
│   ├── background.png               # Background image
│   ├── metadata.json                # Video metadata
│   ├── script.md                    # Full script
│   └── captions.txt                 # Timed captions
├── 2026-01-25_sme-automation-myth/
│   └── ...
```

### Metadata File

```json
{
  "id": "2026-01-24_ai-vibe-coding",
  "created": "2026-01-24T10:30:00+08:00",
  "topic": "AI Vibe Coding: iOS App Releases Surge 60%",
  "source": "X.com",
  "sourceUrl": "https://x.com/...",
  "videoSuitabilityScore": 9.35,
  "duration": 30,
  "dimensions": "1080x1920",
  "platforms": ["Instagram Reels", "TikTok", "YouTube Shorts", "LinkedIn"],
  "script": {
    "hook": "App releases just surged 60%.",
    "context": "After 3 years of flat growth, AI coding tools changed everything.",
    "insights": [
      "Non-coders are building real apps",
      "Tools like Claude & Cursor lead the way",
      "The barrier to building just disappeared"
    ],
    "takeaway": "You don't need to code anymore. You need to create.",
    "cta": "Follow for more AI insights"
  },
  "audio": {
    "voiceOver": {
      "file": "voiceover.mp3",
      "service": "ElevenLabs",
      "voice": "Rachel",
      "model": "Eleven Multilingual v2",
      "duration": "21s"
    },
    "backgroundMusic": {
      "file": "music.mp3",
      "source": "Pixabay",
      "title": "The Upbeat Inspiring Corporate",
      "artist": "The_Mountain",
      "license": "Royalty-free",
      "volume": 0.15
    }
  },
  "files": {
    "silentVideo": "video.mp4",
    "finalVideo": "video_with_audio.mp4",
    "voiceOver": "voiceover.mp3",
    "music": "music.mp3",
    "background": "background.png"
  },
  "status": "complete",
  "posted": {
    "instagram": "2026-01-24",
    "tiktok": null,
    "youtube": null,
    "linkedin": null
  },
  "tags": ["ai", "vibe-coding", "no-code", "app-development", "tech-trends"]
}
```

### Captions File

```
[00:00] The LLM isn't the bottleneck.
[00:03] In Agentic AI systems, most failures happen elsewhere.
[00:08] 1. Tool integration is 60% of the work
[00:12] 2. State management is often overlooked
[00:16] 3. The real cost is in orchestration
[00:20] Focus on the plumbing, not just the brain.
[00:27] Follow for more Agentic AI insights
```

---

## Activity Log

**Log location:** `shared/logs/video-activity.md`

### On Each Run:

1. **Read log first** to check:
   - Topics already covered this week (avoid duplicates)
   - Videos created but not yet posted
   - Performance data from previous videos

2. **After creation**, update log:
   - Add new video to "Videos Created" table
   - Update posting status when published

### What to Log:

```
| Date | Topic | Score | Duration | Status | Platforms Posted |
```

---

## Platform-Specific Exports

### Export Variations

After creating the base video, can export for different platforms:

| Platform | Dimensions | Duration | Notes |
|----------|------------|----------|-------|
| Instagram Reels | 1080x1920 (9:16) | 15-90s | Vertical, captions optional |
| TikTok | 1080x1920 (9:16) | 15-60s | Vertical, trending sounds |
| YouTube Shorts | 1080x1920 (9:16) | 15-60s | Vertical, 60s max |
| LinkedIn | 1080x1920 or 1920x1080 | 30-90s | Both orientations work |

### Quick Export Commands

```bash
# Instagram/TikTok/YouTube Shorts (9:16 vertical, 30s)
npx remotion render ShortVideo out/reel-30s.mp4

# LinkedIn (same but 45s version)
npx remotion render ShortVideo out/linkedin-45s.mp4 --props='{"duration":45}'
```

---

## Quick Start Commands

**Full workflow (autonomous):**
```
create short video
```

**Specific topic:**
```
create short video about [topic]
```

**From specific source:**
```
create video from LinkedIn trends
```

**Check pending videos:**
```
what videos are ready to post?
```

---

## Quality Checklist

Before saving video:
- [ ] Topic score >= 6.5 (GOOD or EXCELLENT)
- [ ] Hook captures attention in first 3 seconds
- [ ] Video is 15-60 seconds (platform appropriate)
- [ ] Text is readable on mobile
- [ ] Visual aligns with topic
- [ ] CTA is clear
- [ ] Metadata file is complete
- [ ] Captions file is generated

---

## Edge Cases

**No suitable trending topics found:**
```
No topics scored above 6.5 for video suitability.

Options:
1. Lower threshold to 5.0 (FAIR rating)?
2. Use evergreen topic from content pillars?
3. Check specific platform for trends?
```

**Gemini image generation fails:**
```
Simplify prompt and retry:
- Use more generic visual concept
- Remove specific requirements
- Try different visual metaphor
```

**User wants specific platform:**
```
Creating for [Platform]:
- Adjusting dimensions to [X]
- Optimizing duration to [Y]
- Platform-specific CTA: [Z]
```

---

## Integration Points

| Skill/Service | Purpose |
|---------------|---------|
| x-trender | Get trending topics from X.com |
| linkedin-trender | Get trending topics from LinkedIn |
| reddit-trender | Get trending topics from Reddit |
| linkedin-image-generator | Shared Gemini workflow pattern |
| remotion-best-practices | Animation rules and patterns |
| instagram-reel-creator | Can post to Instagram after creation |

### External Services

| Service | URL | Purpose |
|---------|-----|---------|
| Gemini | gemini.google.com/app | AI image generation for backgrounds |
| ElevenLabs | elevenlabs.io/app | AI voice over generation |
| Pixabay Music | pixabay.com/music | Royalty-free background music |
| Mixkit | mixkit.co/free-stock-music | Alternative royalty-free music |

---

## Downloads Folder

**IMPORTANT:** All files downloaded via browser automation go to the user's Downloads folder:

```
C:\Users\melve\Downloads\
```

### Files Downloaded to Downloads Folder

| File Type | Source | Typical Filename Pattern |
|-----------|--------|--------------------------|
| Background images | Gemini | `Gemini_Generated_Image_*.png` or screenshot image ID |
| Voice overs | ElevenLabs | `ElevenLabs_*_Rachel_*.mp3` |
| Background music | Pixabay | `[track-name].mp3` |
| Final rendered videos | Remotion | `video_with_audio.mp4` (when downloaded for posting) |

### Workflow Pattern

**After downloading any file:**
```bash
# Check Downloads folder for recent files
powershell "Get-ChildItem 'C:\Users\melve\Downloads' -Filter '*.mp3' | Sort-Object LastWriteTime -Descending | Select-Object -First 3"

# Copy voice over from Downloads to project
powershell "Copy-Item 'C:\Users\melve\Downloads\ElevenLabs_*.mp3' '[project-folder]\voiceover.mp3'"

# Copy music from Downloads to project
powershell "Copy-Item 'C:\Users\melve\Downloads\[music-filename].mp3' '[project-folder]\music.mp3'"
```

### When Uploading to Platforms (Instagram, TikTok, etc.)

**CRITICAL:** When a native file dialog opens for upload, the file to select is in:
```
C:\Users\melve\Downloads\
```

For final video uploads:
1. Copy the rendered video to Downloads folder with a clear name:
   ```bash
   powershell "Copy-Item '[project-folder]\video_with_audio.mp4' 'C:\Users\melve\Downloads\[topic-slug]-reel.mp4'"
   ```

2. When the platform's file picker opens, navigate to Downloads and select the file

3. Inform user which file to select:
   ```
   Please select the file: [topic-slug]-reel.mp4 from your Downloads folder
   ```

---

## Quick Reference: Full Video Creation Checklist

```
□ 1. Find trending topics (x-trender, linkedin-trender, reddit-trender)
□ 2. Score topics for video suitability (>= 6.5 required)
□ 3. Auto-select best topic
□ 4. Generate script (hook, context, insights, takeaway, CTA)
□ 5. Generate background image via Gemini
□ 6. Create Remotion project and render silent video
□ 7. Generate voice over via ElevenLabs (Rachel voice recommended)
□ 8. Download royalty-free music from Pixabay
□ 9. Add Audio components to ShortVideo.tsx
□ 10. Copy audio files to remotion/public folder
□ 11. Re-render video with audio
□ 12. Save final video to output folder
□ 13. Update activity log
□ 14. Post to platforms (Instagram, TikTok, YouTube, LinkedIn)
```

---

## Troubleshooting

### Voice Over Issues

**ElevenLabs not loading:**
- Try navigating directly to `elevenlabs.io/app/speech-synthesis/text-to-speech`
- Check if logged in (requires free account)

**Voice sounds robotic:**
- Use Eleven Multilingual v2 model
- Choose natural voices (Rachel, Adam)
- Adjust speed slider if available

### Music Issues

**Can't find suitable music:**
- Try broader search terms ("corporate", "inspiring", "background")
- Check Mixkit as alternative source
- Ensure instrumental only (no vocals)

### Audio Sync Issues

**Voice over too long for video:**
- Trim voice over or extend video duration
- Adjust speaking pace in ElevenLabs settings

**Music too loud:**
- Reduce volume to 0.10-0.15 in Remotion Audio component
- Re-render video

### Render Issues

**Audio not playing in rendered video:**
- Ensure audio files are in `remotion/public/` folder
- Check file names match exactly in ShortVideo.tsx
- Verify Audio component import from "remotion"
