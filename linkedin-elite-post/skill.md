---
name: linkedin-elite-posts
description: Generate elite LinkedIn posts optimized for engagement, thought leadership, and conversions. Use when the user requests LinkedIn content creation, post writing, or social media content for professional audiences. Creates 2-3 variations across different modes (thought leadership, educational, engagement, lead generation) following proven frameworks for hooks, formatting, and conversion optimization.
---

# LinkedIn Elite Posts

Generate high-performing LinkedIn posts that drive engagement, establish thought leadership, and convert readers into leads using proven frameworks for hooks, formatting, and psychological triggers.

## 360Brew Algorithm Compliance (2026)

LinkedIn's 360Brew algorithm evaluates "Topic Authority" and Profile-Content alignment using NLP. Key rules:

- **Profile-to-Post Alignment**: 80% of content must align with keywords/entities in your profile. Off-topic posts get flagged as "Low Authority" and limited distribution.
- **"See More" Hook**: First 2 lines determine if users expand the post. If they don't click "See More," algorithm assumes low quality.
- **Saves > Likes**: A Save is valued 5x more than a Like, 2x more than a Comment. Create "Save-worthy" assets (schemas, frameworks, PRDs).
- **Hashtags Obsolescent**: The AI reads full text; hashtags no longer provide significant boost.
- **External Links Penalized**: Links in main post reduce reach by ~60%. Put links in first comment instead.
- **Golden Hour**: Engage with 5-10 posts immediately before/after posting (60-90 min window). This "warms" topical relevance for 4 hours of distribution.
- **Depth Score**: Algorithm now measures dwell time (how long users engage), not just clicks. Longer-form valuable content is rewarded.
- **Single Images Underperform**: Single image posts get ~30% less reach than text-only. Use PDF carousels or native video instead.

## LinkedIn Character Limit Enforcement

**CRITICAL: All posts MUST stay within 2700 characters (90% of LinkedIn's 3000 character limit).**

This ensures:
- No truncation in LinkedIn's post composer
- Reliable browser automation (fill tool works better with shorter content)
- Better mobile reading experience
- Margin for last-minute edits

**Character counting rules:**
- Count ALL characters including spaces, line breaks, and special characters (━, •, →, etc.)
- Line breaks count as 1 character each
- Unicode characters (like bullet points and arrows) count as 1 character each

**If a post exceeds 2700 characters:**
- Trim unnecessary words and filler phrases
- Consolidate similar points
- Shorten examples
- Remove redundant section dividers
- Keep the core value and framework intact

## Core Workflow

When the user requests a LinkedIn post:

1. **Gather Requirements**
   - Topic and key points to cover (user will provide)
   - Automatically generate 2-3 variations across different modes
   - Modes: Thought Leadership, Educational, Engagement, Lead Generation, **Save-Worthy Asset**

2. **Consult the Framework**
   - Read `references/linkedin-framework.md` for complete writing guidelines
   - Apply hook formulas, formatting principles, and mode-specific structures

3. **Generate Variations**
   - Create 2-3 complete post variations, each in a different mode
   - Each variation must include:
     - Compelling hook (first 1-2 lines optimized for mobile preview)
     - Well-structured body with strategic formatting
     - Mode-appropriate CTA
     - Mode label for easy identification
   - **CRITICAL: Each variation MUST be ≤2700 characters total**

4. **Formatting Requirements**
   - Use lots of white space and line breaks
   - Vary formatting every ~8 lines (lists, short paragraphs, Unicode bold headers)
   - Write for mobile (concise sentences)
   - Never use rigid, repetitive formatting
   - Stagger sentence lengths in hooks for rhythm
   - **CRITICAL: Use Unicode bold characters for headers, NOT ** markdown syntax**
   - **Keep total character count ≤2700** (including all spaces, line breaks, and special characters)

5. **Quality Standards**
   - Tone: Professional, engaging, inspiring, educational
   - Priority: Thought leadership with authentic voice
   - Avoid: Generic advice, wall of text, weak hooks
   - Focus: Genuine insights, specific frameworks, actionable value
   - **Length: Maximum 2700 characters per post**

6. **⚠️ CRITICAL: NO EM-DASHES (—) IN POSTS**
   - Em-dashes (—) are a STRONG AI-detection signal on LinkedIn
   - NEVER use em-dashes in any post content
   - Use commas, periods, colons, or "and" instead
   - Before finalizing: Search all text for "—" and REPLACE if found
   - Examples of BAD → GOOD:
     - BAD: "AI agents—the future of work" → GOOD: "AI agents: the future of work"
     - BAD: "efficiency—and scale" → GOOD: "efficiency and scale"
     - BAD: "automation—not replacement" → GOOD: "automation, not replacement"
   - **Final validation step:** If em-dash found → Rewrite that sentence immediately

7. **⚠️ CRITICAL: NO BOX-DRAWING LINE CHARACTERS IN POSTS**
   - Box-drawing lines (━━━━━━━) make posts look AI-generated and overly templated
   - NEVER use decorative line characters (━, ═, ─, etc.) in post content
   - Use simple formatting instead:
     - Unicode bold characters for section headers (see Unicode Bold Formatting section below)
     - Line breaks for spacing
     - Bullet points (•) sparingly
     - Natural paragraph breaks
   - Examples of BAD → GOOD:
     - BAD: "━━━━━━━ THE FRAMEWORK ━━━━━━━" → GOOD: "𝗧𝗛𝗘 𝗙𝗥𝗔𝗠𝗘𝗪𝗢𝗥𝗞" or just "The Framework:"
     - BAD: Using lines to separate sections → GOOD: Use double line breaks
   - **Goal:** Keep posts looking organic, not template-based

8. **⚠️ CRITICAL: LINKEDIN FORMATTING - USE UNICODE BOLD, NOT MARKDOWN**
   - LinkedIn does NOT support standard Markdown formatting (no `**bold**` or `__italic__`)
   - NEVER use `**text**` syntax in post content - it won't render as bold
   - NEVER use ALL CAPS with ** markdown like `**THE FRAMEWORK**` - LinkedIn shows the asterisks literally
   - USE Unicode mathematical bold characters for headers and emphasis instead
   - Unicode bold renders properly on LinkedIn without any special syntax

   **Unicode Bold Character Reference:**
   ```
   𝗔 𝗕 𝗖 𝗗 𝗘 𝗙 𝗚 𝗛 𝗜 𝗝 𝗞 𝗟 𝗠 𝗡 𝗢 𝗣 𝗤 𝗥 𝗦 𝗧 𝗨 𝗩 𝗪 𝗫 𝗬 𝗭
   𝗮 𝗯 𝗰 𝗱 𝗲 𝗳 𝗴 𝗵 𝗶 𝗷 𝗸 𝗹 𝗺 𝗻 𝗼 𝗽 𝗾 𝗿 𝘀 𝘁 𝘂 𝘃 𝘄 𝘅 𝘆 𝘇
   𝟬 𝟭 𝟮 𝟯 𝟰 𝟱 𝟲 𝟳 𝟴 𝟵
   ```

   **Examples of BAD → GOOD:**
   - BAD: `**THE FRAMEWORK**` → GOOD: `𝗧𝗛𝗘 𝗙𝗥𝗔𝗠𝗘𝗪𝗢𝗥𝗞`
   - BAD: `**Layer 1: Intent Mapping**` → GOOD: `𝗟𝗮𝘆𝗲𝗿 𝟭: 𝗜𝗻𝘁𝗲𝗻𝘁 𝗠𝗮𝗽𝗽𝗶𝗻𝗴`
   - BAD: `**Key Implementation**` → GOOD: `𝗞𝗲𝘆 𝗜𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻`

   **When to Use Unicode Bold:**
   - Section headers (e.g., `𝗧𝗛𝗘 𝗙𝗥𝗔𝗠𝗘𝗪𝗢𝗥𝗞`, `𝗦𝗠𝗘 𝗜𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻`)
   - Layer labels (e.g., `𝗟𝗮𝘆𝗲𝗿 𝟭`, `𝗟𝗮𝘆𝗲𝗿 𝟮`, `𝗟𝗮𝘆𝗲𝗿 𝟯`)
   - Key framework components
   - Call-to-action headers (e.g., `𝗦𝗔𝗩𝗘 𝗧𝗛𝗜𝗦`)

   **How to Generate Unicode Bold:**
   - For full words: Convert each letter individually using the reference above
   - For mixed case: Use uppercase bold for emphasis, lowercase bold for readability
   - For numbers: Use bold numbers (𝟬-𝟵) in technical content

   **Final validation step:** Before finalizing, check that NO `**text**` markdown remains in the post

## Output Format

Present variations clearly with **character counts**, then **auto-select the best one**:

```
**VARIATION 1: [MODE NAME]**
Character count: [XXXX]/2700 ✅

[Post content with proper formatting]


**VARIATION 2: [MODE NAME]**
Character count: [XXXX]/2700 ✅

[Post content with proper formatting]


**VARIATION 3: [MODE NAME]**
Character count: [XXXX]/2700 ✅

[Post content with proper formatting]
```

**IMPORTANT:** Display a ⚠️ warning instead of ✅ if any variation exceeds 2700 characters.

### AI Auto-Selection

After generating variations, **automatically select the best variation** based on:

| Criteria | Weight | Evaluation |
|----------|--------|------------|
| Hook strength | 30% | Pattern interrupt, curiosity gap, topic signal clarity |
| 360Brew alignment | 25% | Profile-keyword match, save-worthiness potential |
| Content depth | 20% | Actionable value, specific frameworks/examples |
| Engagement potential | 15% | Question hooks, comment-worthy angles |
| Day-content fit | 10% | Match with optimal posting day for content type |

**Output after selection:**

```
**✅ SELECTED: VARIATION [X] - [MODE NAME]**
Character count: [XXXX]/2700 ✅

Selection rationale: [Brief 1-2 sentence explanation]

[Full post content of selected variation]


**📊 CHARACTER COUNT VERIFICATION**
Total characters: [XXXX]/2700
Status: ✅ Within limit / ⚠️ Exceeds limit (trim required)
```

Then include the **Schedule Recommendation** and proceed to **image generation** (if visual needed).

User can override: "use variation 2 instead" or "refine the selected post"

## Key Principles

**Hook Mastery:**
- First 1-2 lines determine if post is read (triggers "See More" click)
- Opening hook must be a "Topic Signal" telling 360Brew exactly who should see the post
- Use proven formulas: Pain→Solution or Topic+Audience
- Keep hooks concise and powerful (no wasted preview space)
- Example: "In agentic AI systems, the bottleneck isn't the LLM..." tells algorithm the niche

**Strategic Formatting:**
- Change formatting every ~8 lines to maintain attention
- White space is your friend
- Mobile-first: tight, concise sentences
- Lists for processing, prose for flow
- Use Unicode bold characters (𝗧𝗛𝗘 𝗙𝗥𝗔𝗠𝗘𝗪𝗢𝗥𝗞) for section headers, not ** markdown
- Never use `**text**` syntax - LinkedIn displays it literally with asterisks

**Mode Differentiation:**
- Thought Leadership: Insights, frameworks, unique perspectives
- Educational: Teaching, breaking down complexity, actionable steps
- Engagement: Questions, experiences, community building
- Lead Generation: Direct, solution-focused, qualified prospect filtering
- **Save-Worthy Asset**: Practical artifacts (schemas, diagrams, PRDs) users save for future reference

**Authenticity:**
- Avoid generic AI-sounding advice
- Use specific examples and frameworks
- Balance authority with relatability
- Make every word earn its place

**Content Mix (40/40/20 Rule):**
- 40% Educational: Teach frameworks, break down complexity
- 40% Evidence/Stories: Case studies, build-in-public updates, lessons from deployments
- 20% Engagement/Perspective: Polls, contrarian takes to spark debate

**High-Value Formats for 360Brew:**
- Native Video (60-90s): +69% performance boost. Use for technical demos.
- PDF Carousels: Highly effective for step-by-step guides (must be mobile-friendly)
- Save-worthy assets: SQL schemas, JSON import logic, PRD frameworks drive "Saves"

**Posting Frequency:**
- Optimal: 3-5 posts per week (120% reach increase vs 1 post/week)
- Never put external links in post body; use first comment instead

## Optimal Posting Schedule

> **Note:** Read your timezone from `references/linkedin-strategy.md`. All times below are examples; adjust to your local timezone.

**Do NOT post immediately. Schedule for optimal windows based on content type.**

| Day | Primary Window | Secondary Window | Best Content Type |
|-----|----------------|------------------|-------------------|
| **Monday** | 10:00 AM - 11:30 AM | 4:00 PM - 5:30 PM | Week-starters, strategy, planning frameworks |
| **Tuesday** | 8:30 AM - 10:30 AM | 12:00 PM - 1:30 PM | **Major Demos** (peak day for technical reach) |
| **Wednesday** | 9:00 AM - 11:00 AM | 3:00 PM - 5:00 PM | Educational "Save-worthy" assets (Schemas/SQL) |
| **Thursday** | 10:00 AM - 12:00 PM | 1:00 PM - 2:30 PM | Thought leadership, "Frontier Firm" perspectives |
| **Friday** | 8:30 AM - 10:00 AM | No afternoon slot | Light reflections, "Build-in-Public" wins, team highlights |
| **Weekend** | Avoid posting | - | Engagement only, no new content |

### Schedule Recommendation Output

After generating post variations, always include:

```
**📅 RECOMMENDED SCHEDULE**

Content Type: [Educational / Thought Leadership / Demo / Reflection]
Best Day: [Day based on content type]
Primary Window: [Time range] (your timezone)
Secondary Window: [Time range] (your timezone, if available)

Current time: [Now]
Recommendation: Schedule for [Day], [Time] (your timezone) (use LinkedIn's Schedule feature)

Pre-post checklist:
- [ ] 15 mins engagement before posting (Golden Hour warm-up)
- [ ] External links moved to first comment
- [ ] Use LinkedIn's SCHEDULE feature (never post immediately)
- [ ] Scheduled for optimal window above
```

### Content-Day Alignment

Match your content type to the optimal day:

| Content Type | Best Day | Why |
|--------------|----------|-----|
| SQL Schema / JSON / PRD | Wednesday | Mid-week "Save-worthy" peak |
| Video Demo / Technical | Tuesday | Highest technical audience reach |
| Strategy / Framework | Monday or Thursday | Professional planning mindset |
| Thought Leadership | Thursday | End-of-week reflection mode |
| Personal Story / Win | Friday | Light, human content performs well |

## Browser Automation: Schedule Post Workflow

**Browser automation uses Claude for Chrome if available, otherwise falls back to Chrome DevTools. See linkedin-daily-planner skill for detailed tool mapping.**

**MANDATORY: Never click "Post" immediately. Always use LinkedIn's "Schedule" feature.**

When using browser automation to publish content, follow this workflow:

### Step 1: Open Post Composer
1. Navigate to LinkedIn homepage
2. Click "Start a post" to open the composer modal

### Step 2: Enter Post Content
1. Paste the approved post content into the text area
2. Add any images, PDFs, or attachments as needed
3. If external links are needed, prepare them for the first comment (not in main post)

### Step 3: Access Schedule Feature
1. Look for the **clock icon** (🕐) at the bottom of the post composer
2. Click the clock icon to open the scheduling options
3. DO NOT click the blue "Post" button

### Step 4: Set Schedule Time
1. Select the **date** based on content type (see Content-Day Alignment table)
2. Select the **time** within the optimal window:
   - Use Primary Window times when possible
   - Fall back to Secondary Window if Primary is unavailable
3. Confirm the scheduled time

### Step 5: Schedule the Post
1. Click "Schedule" (NOT "Post")
2. Verify the scheduled post appears in your scheduled posts queue
3. Note the scheduled time for the shared activity log

### Schedule Verification Checklist
```
Before scheduling:
- [ ] Content pasted correctly with proper formatting
- [ ] Attachments added (if applicable)
- [ ] Clock icon clicked (NOT Post button)
- [ ] Date matches optimal day for content type
- [ ] Time within Primary or Secondary window
- [ ] "Schedule" button clicked (NOT "Post")

After scheduling:
- [ ] Confirmed in scheduled posts queue
- [ ] Logged to shared activity log with scheduled time
- [ ] External link ready for first comment (to add when post goes live)
```

### Element References for Automation

When automating via Claude for Chrome:
- **Post composer trigger**: "Start a post" button on homepage
- **Schedule icon**: Clock icon (🕐) in composer toolbar, typically bottom-left
- **Date picker**: Calendar interface after clicking clock icon
- **Time picker**: Dropdown or input field for selecting hour
- **Schedule button**: Replaces "Post" button after setting schedule time

**Critical**: If the clock/schedule icon is not visible, scroll within the composer or look for a "more options" menu. Never publish immediately if schedule option cannot be found.

## Save-Worthy Asset Mode (360Brew Priority)

In the 360Brew environment, "Save-worthy" assets are the single most important factor for building **Topic Authority**. When users click "Save," the algorithm interprets this as "Referenceable Knowledge" rather than "Disposable Content." This:
- Boosts profile weight in search results
- Keeps post active in feed for up to 14 days
- Values 5x more than a Like, 2x more than a Comment

### The Utility Test

Every Save-Worthy Asset must pass this test: **"Can the reader use this to save 2 hours of work today?"**

If the answer is no, it's not save-worthy.

### Three Core Asset Formats

**A. Modular Schema (SQL/JSON)**

Share actual database schemas for specific modules (Inventory, Lead Scoring, etc.)

Why it gets saved: Developers and technical founders save it as reference for their own builds.

Hook template:
```
Don't start your Agentic CRM from scratch.

Here is the SQL schema I used to handle multi-agent state management.

[Schema content or image]
```

**B. Agentic Logic Diagram**

Visual map showing how an AI Agent "thinks": Trigger → Retrieval → Reasoning → Action → Feedback Loop

Why it gets saved: Non-coders and business owners save it to explain concepts to stakeholders or as a workflow blueprint.

Hook template:
```
Most [target market] automations fail because they lack a feedback loop.

Here is the 5-step logic map we use at [Your Company].

[Diagram image]
```

**C. Rapid PRD Template**

Structured Product Requirements Document template specifically for AI tools.

Why it gets saved: Product managers and founders looking for better prompt-engineering approaches.

Hook template:
```
I've turned 5 years of building into this 1-page PRD template for AI Agents.

Save this for your next build.

[PRD template content or image]
```

### Save-Optimization Layout

Structure every Save-Worthy Asset post with these 4 elements:

```
𝟭. 𝗧𝗛𝗘 𝗖𝗢𝗡𝗧𝗘𝗫𝗧 (𝗧𝗵𝗲 "𝗪𝗵𝘆")
Identify a specific friction point.
Example: "Manual data entry in SMEs is a $X billion waste."


𝟮. 𝗧𝗛𝗘 𝗦𝗢𝗟𝗨𝗧𝗜𝗢𝗡 (𝗧𝗵𝗲 "𝗔𝘀𝘀𝗲𝘁")
Explicitly state what you're sharing.
Example: "I've documented the [Schema/PRD/Logic] below."


𝟯. 𝗧𝗛𝗘 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗙𝗢𝗥𝗠𝗔𝗧

𝗣𝗥𝗘𝗙𝗘𝗥𝗥𝗘𝗗: Text-based asset in the post (no image penalty, full reach)
- Format schema/code with proper spacing and structure
- Use simple bullet points (•) and arrows (→) for visual hierarchy
- Keep well-formatted and readable on mobile
- Use Unicode bold for headers, not decorative lines

𝗔𝗟𝗧𝗘𝗥𝗡𝗔𝗧𝗜𝗩𝗘: PDF carousel or external link
- Multi-slide PDF (better than single image)
- Link to full asset in first comment (preserves main post reach)

𝗔𝗩𝗢𝗜𝗗: Single images (30% reach penalty)


𝟰. 𝗧𝗛𝗘 𝗖𝗧𝗔 (𝗦𝗮𝘃𝗲-𝗙𝗼𝗰𝘂𝘀𝗲𝗱)
Instead of "Like this post," use:
- "Save this post so you can refer back to the schema when you start your next build."
- "Bookmark this for your next automation project."
- "Save this template you'll need it when scaling."
```

### Save-Worthy Asset Output Format

When generating a Save-Worthy Asset variation:

```
**VARIATION X: SAVE-WORTHY ASSET**
Asset Type: [Modular Schema / Logic Diagram / PRD Template]
Character count: [XXXX]/2700 ✅

[HOOK - 1-2 lines identifying the friction point]

[CONTEXT - Why this matters, the pain it solves]

[ASSET INTRODUCTION - "Here's the [schema/diagram/template]..."]

[ASSET CONTENT - The actual schema, diagram structure, or template]
Format as text in the post (no image - full reach, no algorithm penalty)
- Use proper spacing, line breaks, and simple formatting
- Make it scannable and readable on mobile
- Keep schema/framework inline in the post text
- Use Unicode bold for headers (e.g., 𝗟𝗮𝘆𝗲𝗿 𝟭, 𝗧𝗛𝗘 𝗙𝗥𝗔𝗠𝗘𝗪𝗢𝗥𝗞)
- Use bullets (•) and arrows (→) for structure
- NEVER use ** markdown - LinkedIn doesn't support it

[CTA - Save-focused call to action]


**Character limit note:** Save-Worthy Assets often include detailed content. If approaching 2700 character limit:
- Condense the asset to key elements (users can ask for full version)
- Use abbreviated syntax for schemas (e.g., `id INT PRIMARY KEY` instead of full SQL)
- Focus on the framework structure, not exhaustive details
- Add note: "Full schema/template available - DM me" (drives conversation)
```

### Using Save-Worthy Assets in Outreach

When connecting with ICP prospects, reference your saved assets:

```
"Hi [Name], I noticed you're scaling your ops.

I recently posted a Workflow Logic Map for automating finance tasks in SMEs that a few others found useful.

Thought it might be worth a save for your team."
```

## Image Generation Integration

**IMPORTANT: LinkedIn penalizes single image posts (~30% less reach than text-only). Avoid images unless explicitly requested by user.**

### When NOT to Use Images (Default)

- **Educational posts** - Text-only performs better
- **Thought leadership** - Text-only maintains authority
- **Engagement posts** - Text-only encourages discussion
- **Lead generation** - Text-only focuses on message
- **Save-Worthy Assets with inline content** - Text schemas/frameworks are save-worthy on their own

### When Images Are Acceptable (User Request Only)

Only generate images if:
- **User explicitly requests** an image or visual
- **User specifically asks** for a diagram, schema, or visual representation
- Never auto-invoke linkedin-image-generator based on post mode alone

### Alternative to Single Images

For Save-Worthy Assets that truly need visuals:
- **Text-based frameworks** in the post (preferred - full reach)
- **PDF carousels** (multi-slide, higher engagement than single images)
- **Native video** (60-90s, +69% performance boost)
- **External link in first comment** to full visual asset (preserves main post reach)

### Workflow IF User Requests Image

1. Generate post variations (this skill)
2. **AI auto-selects best variation** (based on selection criteria)
3. **Ask user**: "LinkedIn penalizes single image posts. Do you still want to generate an image, or prefer text-only for better reach?"
4. Only if user confirms: Invoke linkedin-image-generator
5. Image saved to `linkedin-image-generator/assets/generated/`
6. Schedule post via Claude for Chrome (attach image)

### Text-Only Posts (Default)

All posts are generated as text-only by default for maximum reach:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 RECOMMENDED SCHEDULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Content Type: [Type]
Best Day: [Day]
Primary Window: [Time] (your timezone)
Format: Text-only ✅ (Full reach, no image penalty)

Pre-post checklist:
- [ ] 15 mins engagement before posting (Golden Hour warm-up)
- [ ] External links moved to first comment
- [ ] Use LinkedIn's SCHEDULE feature
- [ ] Scheduled for optimal window
- [ ] Text-only format (no images)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Additional Resources

- `references/linkedin-framework.md` - Complete framework with hook formulas, formatting principles, conversion psychology, and mode specifications
- `references/saved-asset.md` - Detailed guide on creating Save-Worthy Assets
- `linkedin-image-generator` skill - Generate visuals for posts via Gemini

## Shared Activity Log (Token Optimization)

**Check the shared log before creating new posts.**

**Log location:** `shared/logs/linkedin-activity.md`

### On Each Run:
1. **Read shared log first** to check:
   - "Posts Published" for today's content status (avoid duplicate posts)
   - "Feed Insights Cache" for trending topics to reference
   - "High-Engagement Posts Saved" for content inspiration
2. **After scheduling**, update shared log:
   - Add to "Posts Published" table with scheduled time, type, topic
   - Note: Log the SCHEDULED time, not the time you scheduled it
   - Update engagement metrics when post goes live

### What to Log:
**Published posts:**
```
| HH:MM | Type (Evidence/Strategy/Reflection) | Topic | Post URL | Initial Engagement |
```
**Always capture Post URL** for tracking engagement later.

### Read from Log Instead of LinkedIn:
- Check "Posts Published" to see if already posted today
- Check "Feed Insights Cache" for trending topics (avoid stale angles)
- Check "High-Engagement Posts Saved" for inspiration and hooks