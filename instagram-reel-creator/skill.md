---
name: instagram-reel-creator
description: Create and post Instagram Reels with AI-generated images and Remotion animations. Use when user says "daily instagram content", "create instagram reel", "instagram video post", or wants to create short-form video content for Instagram. Integrates x-trender for trending topics, Nano Banana MCP for image generation, and Remotion for video animation. Fully autonomous daily workflow.
---

# Instagram Reel Creator

Create 15-30 second Instagram Reels by combining trending topics, AI-generated images from Nano Banana MCP, and Remotion animations.

## Trigger

- "daily instagram content"
- "create instagram reel"
- "instagram video post"
- "make instagram video"

## Workflow Overview

```
x-trender (trending topic) --> Nano Banana MCP (image) --> Remotion (animation) --> Instagram (post)
```

**Key Principle:** Every Reel gets a unique, topic-specific image generated from Nano Banana MCP. Do NOT reuse images or default to gradient backgrounds unless generation fails.

## Step 1: Get Trending Topic

Use x-trender skill to find today's trending topic:

1. Invoke x-trender to analyze X.com/explore
2. Select topic with HIGH cross-platform potential
3. Extract:
   - **Core topic** for image concept
   - **Key angle** for text overlay
   - **Hook line** (first 3 seconds)

**Topic Selection Criteria for Instagram:**
- Visual-friendly (can be represented as image)
- Relatable to broad audience
- Not overly technical
- Emotional hook potential

## Step 2: Generate Image via Nano Banana MCP

**CRITICAL: Always generate images that match the video script and trending topic.**

Use Nano Banana MCP tools (with optional nano-banana-prompts skill for recommendations) to generate a contextually relevant background image.

### Pre-Generation Analysis

Before writing the image prompt, analyze:
1. **Core topic:** What is the main subject? (e.g., "Claude AI Excel Add-in", "AI job displacement")
2. **Emotional tone:** Is it exciting, concerning, surprising, revolutionary?
3. **Key visual elements:** What physical objects, people, or scenes represent this?
4. **Color scheme:** What colors match the emotion and topic? (tech = blue/purple, warning = red/orange, finance = green/gold)
5. **Composition:** How can we show contrast, comparison, or transformation?

### Dynamic Image Prompt Creation

**For each video, craft a unique prompt based on:**
1. **Trending topic** from Step 1
2. **Video script** content (hook + main text)
3. **Visual metaphor** that represents the core message
4. **Specific visual elements** (not abstract concepts)

### Image Prompt Template

```
Create a professional, eye-catching image for an Instagram Reel about [SPECIFIC TOPIC FROM TRENDING DATA].

Visual Concept: [DESCRIBE SPECIFIC SCENE/METAPHOR BASED ON SCRIPT]

Requirements:
- Style: Modern, bold, Instagram-worthy aesthetic
- Aspect Ratio: 9:16 vertical for Instagram Reels
- Composition: Leave space for text overlay (center area clear or simple)
- Colors: Vibrant, high contrast for mobile viewing
- Scene: [SPECIFIC VISUAL ELEMENTS THAT MATCH THE TOPIC]

Example Topics & Visual Concepts:
- "Claude AI Excel Add-in" → Split-screen: stressed analyst with Excel spreadsheet (left) vs AI automation with glowing interface (right)
- "AI replacing jobs" → Office worker surrounded by AI robots, dramatic lighting
- "New AI breakthrough" → Futuristic laboratory with glowing AI technology
- "Tech company announcement" → Professional tech keynote stage with product reveal

Do NOT include:
- Text or words in the image
- Watermarks
- Busy patterns that compete with text overlay
- Generic stock photo scenes

Should feel: Premium, scroll-stopping, native to Instagram, SPECIFIC to the topic
```

### Example Prompt Construction

**Example 1: "DeepSeek AI challenges ChatGPT"**

Pre-Generation Analysis:
- Core topic: AI competition between China and Silicon Valley
- Emotional tone: Dramatic, surprising, competitive
- Key visual elements: Tech offices, screens with code, contrast between East/West
- Color scheme: Cool blue (China) vs warm orange (Silicon Valley)
- Composition: Split-screen showing rivalry

Generated image prompt:
```
Create a professional, eye-catching image for an Instagram Reel about DeepSeek AI challenging ChatGPT dominance.

Visual Concept: Dramatic tech confrontation scene - futuristic Chinese tech office with glowing screens showing AI algorithms on left side, Silicon Valley tech headquarters on right side, electric energy between them suggesting competition. Modern, cinematic lighting with blue and purple tech glow.

Requirements:
- Style: Modern, bold, Instagram-worthy aesthetic
- Aspect Ratio: 9:16 vertical for Instagram Reels
- Composition: Leave space for text overlay in center
- Colors: Vibrant high contrast - cool blue (China side) vs warm orange (Silicon Valley side)
- Scene: Two opposing tech environments with dramatic tension

Do NOT include text, watermarks, or busy patterns.
Should feel: Premium, scroll-stopping, tech rivalry drama
```

**Example 2: "New AI can predict diseases before symptoms"**

Pre-Generation Analysis:
- Core topic: Medical AI breakthrough
- Emotional tone: Hopeful, scientific, life-saving
- Key visual elements: Doctor, medical scans, AI interface, patient care
- Color scheme: Medical white/blue, tech purple glow
- Composition: Doctor using AI system with holographic medical data

Generated image prompt:
```
Create a professional, eye-catching image for an Instagram Reel about AI predicting diseases before symptoms appear.

Visual Concept: Modern hospital setting with doctor examining futuristic AI interface displaying holographic medical scans and predictive analytics. Warm, hopeful lighting from left side, cool tech glow from AI screens on right. Patient silhouette in background showing care context.

Requirements:
- Style: Modern, hopeful medical aesthetic
- Aspect Ratio: 9:16 vertical for Instagram Reels
- Composition: Doctor in foreground with glowing AI interface, medical data visualization
- Colors: Medical white and blue tones with purple AI glow accents
- Scene: Professional medical environment with advanced technology

Do NOT include text, watermarks, or busy patterns.
Should feel: Cutting-edge medical innovation, hopeful future
```

**Example 3: "Mass tech layoffs hit 50,000 workers"**

Pre-Generation Analysis:
- Core topic: Job losses in tech industry
- Emotional tone: Concerning, sobering, uncertain
- Key visual elements: Empty office, tech workers, economic downturn visuals
- Color scheme: Desaturated blues and grays, some warm human tones
- Composition: Empty modern tech office showing scale of impact

Generated image prompt:
```
Create a professional, eye-catching image for an Instagram Reel about mass tech layoffs.

Visual Concept: Modern tech office space, partially empty with some desks vacant and boxes packed, soft natural light streaming through large windows creating dramatic shadows. Remaining workers in background appear contemplative. Sleek but somber atmosphere showing the human impact of layoffs.

Requirements:
- Style: Photojournalistic, cinematic, Instagram-worthy
- Aspect Ratio: 9:16 vertical for Instagram Reels
- Composition: Wide shot showing scale of empty office, text overlay space in upper third
- Colors: Desaturated blues and grays with warm human skin tones for emotional contrast
- Scene: Contemporary tech office with realistic details, not dystopian

Do NOT include text, watermarks, or busy patterns.
Should feel: Sobering, human, real-world impact of tech industry changes
```

**Example 4: "Startup raises $100M for AI agents"**

Pre-Generation Analysis:
- Core topic: Startup funding, AI innovation success
- Emotional tone: Exciting, optimistic, ambitious
- Key visual elements: Startup team, investment celebration, futuristic tech
- Color scheme: Vibrant blues, purples, gold accents for success
- Composition: Dynamic upward movement, celebrating achievement

Generated image prompt:
```
Create a professional, eye-catching image for an Instagram Reel about a startup raising $100M for AI agents.

Visual Concept: Young diverse startup team in modern co-working space celebrating with futuristic AI holographic displays floating around them showing agent workflows and funding metrics. Dynamic upward composition suggesting growth and success. Vibrant lighting with tech glow and celebratory atmosphere.

Requirements:
- Style: Modern, energetic, startup culture aesthetic
- Aspect Ratio: 9:16 vertical for Instagram Reels
- Composition: Upward diagonal composition, team in lower third, tech elements rising above
- Colors: Vibrant blues and purples with gold/yellow success accents
- Scene: Contemporary startup environment with futuristic AI visualization

Do NOT include text, watermarks, or busy patterns.
Should feel: Exciting innovation, startup success, future-forward optimism
```

### MCP Generation Workflow

**ALWAYS ATTEMPT IMAGE GENERATION FIRST - DO NOT SKIP TO GRADIENT FALLBACK**

1. **Optional: Get prompt recommendation from nano-banana-prompts skill**
   ```
   Skill: nano-banana-prompts
   Args: "Instagram Reel background about [topic] - modern, bold, 9:16 vertical"
   → Use recommended prompt or craft custom prompt
   ```

2. **Generate image via Nano Banana MCP:**
   ```
   mcp__nanobanana__generate_image(
     prompt="[Dynamically generated prompt specific to topic]",
     model="gemini-2.5-flash-image",
     image_size="2K",
     aspect_ratio="9:16",  # Instagram Reel vertical format
     output_path="./instagram-reel-creator/assets/background-[date].png",
     response_format="markdown"
   )
   ```

3. **Tool automatically:**
   - Sends request to Gemini API
   - Waits for generation (10-30 seconds)
   - Downloads and saves image to specified path
   - Returns confirmation with image path

### Image to Remotion Integration

After image is generated (automatically saved by MCP tool):

1. Copy image from assets to the Remotion project's `public/` folder:
   ```
   Copy: instagram-reel-creator/assets/background-[date].png
   To: instagram-reel-[date]/public/background.png
   ```

2. Update `InstagramReel.tsx` to use the image:
   ```tsx
   // Replace gradient background with image
   <Img
     src={staticFile("background.png")}
     style={{
       width: "100%",
       height: "100%",
       objectFit: "cover",
     }}
   />
   ```

3. Verify the image loads correctly before rendering
4. If image is missing, check file path and retry generation

**IMPORTANT: Only use gradient fallback if MCP generation fails after 2-3 attempts with different prompts.**

## Step 3: Create Remotion Video Project

### Project Structure

```
instagram-reel/
├── public/
│   └── background.png (Gentube image placed here)
├── src/
│   ├── Root.tsx
│   └── InstagramReel.tsx
├── package.json
└── remotion.config.ts
```

### Composition Settings

```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { InstagramReel } from "./InstagramReel";

export const RemotionRoot = () => {
  return (
    <Composition
      id="InstagramReel"
      component={InstagramReel}
      durationInFrames={900}  // 30 seconds at 30fps
      fps={30}
      width={1080}
      height={1920}  // 9:16 vertical
      defaultProps={{
        hookLine: "Did you know...",
        mainText: "Your key insight here",
        ctaText: "Follow for more!",
      }}
    />
  );
};
```

### Animation Component

**Default: With Generated Image from Gentube**

```tsx
// src/InstagramReel.tsx
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, Sequence } from "remotion";

type Props = {
  hookLine: string;
  mainText: string;
  ctaText: string;
};

export const InstagramReel: React.FC<Props> = ({ hookLine, mainText, ctaText }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Background zoom animation (Ken Burns effect)
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      {/* Background Image from Gentube */}
      <Img
        src={staticFile("background.png")}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />

      {/* Dark overlay for text readability */}
      <AbsoluteFill
        style={{
          backgroundColor: "rgba(0, 0, 0, 0.4)",
        }}
      />

      {/* Hook Line (0-3 seconds) */}
      <Sequence from={0} durationInFrames={3 * fps}>
        <HookText text={hookLine} />
      </Sequence>

      {/* Main Content (3-25 seconds) */}
      <Sequence from={3 * fps} durationInFrames={22 * fps}>
        <MainContent text={mainText} />
      </Sequence>

      {/* CTA (25-30 seconds) */}
      <Sequence from={25 * fps} durationInFrames={5 * fps}>
        <CTAText text={ctaText} />
      </Sequence>
    </AbsoluteFill>
  );
};

// FALLBACK: Gradient Background (Only if Gentube fails)
// Uncomment and use this version only when image generation completely fails
/*
export const InstagramReel: React.FC<Props> = ({ hookLine, mainText, ctaText }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Animated gradient - customize colors based on topic
  const gradientProgress = interpolate(frame, [0, durationInFrames], [0, 100], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      {/* Animated Gradient - CUSTOMIZE COLORS FOR EACH TOPIC */}
      <div
        style={{
          width: "100%",
          height: "100%",
          background: `linear-gradient(${gradientProgress}deg, #107C41 0%, #1E3A8A 50%, #7C3AED 100%)`,
          position: "absolute",
        }}
      />

      {/* Dark overlay */}
      <AbsoluteFill style={{ backgroundColor: "rgba(0, 0, 0, 0.3)" }} />

      {/* Rest of animation sequences... */}
    </AbsoluteFill>
  );
};
*/

// Hook text component with fade-in animation
const HookText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 0.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, 0.5 * fps], [50, 0], {
    extrapolateRight: "clamp",
  });

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
          fontSize: 72,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          textShadow: "2px 2px 4px rgba(0,0,0,0.5)",
          padding: "0 60px",
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// Main content with typewriter effect
const MainContent: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Typewriter effect
  const charsToShow = Math.floor(interpolate(frame, [0, 3 * fps], [0, text.length], {
    extrapolateRight: "clamp",
  }));

  const displayText = text.slice(0, charsToShow);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          fontSize: 56,
          fontWeight: 600,
          color: "white",
          textAlign: "center",
          textShadow: "2px 2px 4px rgba(0,0,0,0.5)",
          padding: "0 80px",
          lineHeight: 1.4,
        }}
      >
        {displayText}
      </div>
    </AbsoluteFill>
  );
};

// CTA with pulse animation
const CTAText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 0.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Pulse effect
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
          fontSize: 48,
          fontWeight: "bold",
          color: "#FFD700",
          textAlign: "center",
          textShadow: "2px 2px 4px rgba(0,0,0,0.5)",
          transform: `scale(${scale})`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

### Render Command

```bash
npx remotion render InstagramReel out/reel.mp4 --props='{"hookLine":"Did you know...","mainText":"Your insight","ctaText":"Follow for more!"}'
```

## Step 4: Post to Instagram via Browser

### Browser Automation Steps

1. **Navigate to Instagram**
   ```
   Navigate to: instagram.com
   Ensure logged in
   ```

2. **Open Post Creator**
   ```
   Click "+" (Create) icon in top navigation
   Or navigate to: instagram.com/create/style
   ```

3. **Upload Video**
   ```
   Find file input or drag-drop zone
   Use upload_image tool with:
   - imageId: [rendered video file]
   - coordinate: [upload zone center]
   ```

4. **Configure as Reel**
   ```
   Select "Reel" option
   Add cover image (optional)
   ```

5. **Add Caption**
   ```
   Find caption input
   Enter caption with:
   - Hook line
   - Key insight
   - Relevant hashtags (5-10)
   - CTA
   ```

6. **Post**
   ```
   Click "Share" or "Post"
   Wait for confirmation
   ```

### Caption Template

```
[HOOK LINE]

[MAIN INSIGHT - 2-3 sentences]

[CTA]

#[topic] #reels #trending #[niche] #[related]
```

## Positioning Context

Align content with:
- Agentic AI systems for SMEs
- Finance, ERP, CRM automation
- AI-native business OS vision
- Practical implementation over hype
- Democratizing AI for non-technical users

## Activity Log

**Log location:** `shared/logs/instagram-activity.md`

### On Each Run:
1. **Read log first** to check:
   - Recent posts (maintain 12-hour gap)
   - Topics already covered this week
2. **After posting**, update log:
   - Topic, timestamp, post URL
   - Engagement metrics (check later)

### What to Log:
```
| Date | Topic | Hook Line | Status | Post URL |
```

## Quality Checklist

Before posting:
- [ ] **Image visually represents the video topic** (not generic/irrelevant)
- [ ] Image is vertical (9:16) and high quality
- [ ] Text is readable on mobile with good contrast against image
- [ ] Hook captures attention in first 3 seconds
- [ ] Video is 15-30 seconds
- [ ] Caption includes relevant hashtags
- [ ] 12-hour gap from last post maintained
- [ ] Image prompt was customized for this specific topic (not using template as-is)

## Edge Cases

**Gentube image generation fails:**
```
ALWAYS TRY IMAGE GENERATION FIRST.

Troubleshooting steps:
1. Check if Gentube requires login/credits
2. Simplify prompt but keep it specific to the topic
3. Try different visual angle on same topic
4. Adjust technical requirements (less specific style details)
5. Retry with more generic but still relevant concept

FALLBACK OPTION (Last Resort Only):
If Gentube is completely unavailable or fails multiple times:
Use animated CSS gradient background in Remotion:
- Choose colors that thematically match the topic
- Example color combinations:
  * Excel/productivity: Green (#107C41) → Blue (#1E3A8A) → Purple (#7C3AED)
  * Tech disruption: Red (#DC2626) → Orange (#EA580C) → Purple (#7C3AED)
  * Finance/money: Gold (#F59E0B) → Green (#10B981) → Blue (#3B82F6)
  * AI/futuristic: Cyan (#06B6D4) → Blue (#3B82F6) → Purple (#8B5CF6)

Code: background: linear-gradient(${angle}deg, [COLOR1] 0%, [COLOR2] 50%, [COLOR3] 100%)

Note: While gradients work well, topic-specific images perform better.
Always prefer generating contextual images when possible.
```

**Instagram upload fails:**
```
1. Check video format (MP4, H.264)
2. Verify dimensions (1080x1920)
3. Ensure file size < 100MB
4. Try uploading manually as fallback
```

**No trending topics relevant:**
```
Options:
1. Use evergreen topic from content pillars
2. Create educational content on core expertise
3. Skip day, save for better timing
```

## Integration Points

| Skill | Purpose |
|-------|---------|
| x-trender | Get trending topic for content |
| linkedin-image-generator | Share Gentube workflow pattern |
| remotion-best-practices | Animation rules and patterns |
