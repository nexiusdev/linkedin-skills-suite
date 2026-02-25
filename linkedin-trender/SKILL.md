---
name: linkedin-trender
description: Analyze LinkedIn feed to identify trending topics for content creation. Use when user says "find trending topics", "what should I post about", "analyze my feed", or wants to discover what's resonating on LinkedIn today. Works with browser MCP (Chrome DevTools or Playwright) - user pastes feed content. Filters for high-engagement posts (20+ likes, 10+ comments) from individual thought leaders only (excludes company pages, brands, organizations, articles). Outputs trending topic recommendations with angle suggestions, then integrates with linkedin-elite-posts skill to generate the actual post.
---

# LinkedIn Feed Trends

Analyze your LinkedIn feed to identify trending topics worth posting about today. Designed for browser MCP (Chrome DevTools or Playwright) workflow.

## 360Brew Algorithm Context (2026)

LinkedIn's 360Brew algorithm has shifted from "virality" to "Topic Authority." When identifying trends:

- **Profile-Topic Alignment**: Only recommend topics that align with your profile's stated expertise (Agentic AI, SME automation, AI-native systems). Off-topic posts get flagged as "Low Authority."
- **Save-Worthy Content Wins**: Posts with high Save rates indicate "Referenceable" expertise. Look for posts where comments mention "saving for later."
- **Semantic Reasoning**: 360Brew evaluates quality of argument, not just keywords. Logically structured posts outperform engagement-bait.
- **Zero-Shot Capability**: New profiles with high-value niche content can trend without large followings. Look for emerging voices, not just established influencers.

## Trigger

Activate when user says:
- "find trending topics"
- "what should I post about"
- "analyze my feed"
- "what's trending on LinkedIn"
- Or pastes LinkedIn feed content for analysis

## Step 1: Request Feed Content

Ask user to share their LinkedIn feed:

```
To find trending topics, I need to see your LinkedIn feed. Please:

1. Open LinkedIn in Chrome
2. Scroll through your feed for the past 24 hours (load ~30-50 posts)
3. Select all the feed content and paste it here

I'll analyze engagement patterns and identify topics worth posting about.
```

## Step 2: Parse & Filter Posts

From the pasted content, extract posts and apply filters:

**Engagement Threshold (REQUIRED):**
- ✅ 20+ likes/reactions AND 10+ comments
- ❌ Skip posts below threshold

**Author Filter (REQUIRED):**
- ✅ Individual profiles only (person's photo, job title in headline, linkedin.com/in/...)
- ❌ Skip company pages (logo, "X followers" without job title, linkedin.com/company/...)
- ❌ Skip brand accounts
- ❌ Skip organizations
- ❌ Skip LinkedIn articles (long-form content with article thumbnail)

**Content Filter:**
- ✅ Native LinkedIn posts (text, images, carousels, videos)
- ❌ Skip reshares without original commentary
- ❌ Skip job postings
- ❌ Skip event promotions

## Step 3: Extract Topics & Themes

For each qualifying post, extract:

1. **Core Topic**: Main subject (e.g., "AI agents in customer service")
2. **Angle/Hook**: What made it resonate (contrarian take, personal story, framework, prediction)
3. **Engagement Driver**: Why it got engagement (controversy, relatability, actionable insight)
4. **Author Context**: Who posted and their authority on the topic

## Step 4: Identify Trending Patterns

Group extracted topics to find trends:

**Trending Signal Indicators:**
- Multiple posts on same topic from different authors
- High engagement velocity (recent posts with rapid engagement)
- Topics adjacent to your expertise (Agentic AI, SME automation, AI-native systems)
- Emerging conversations vs saturated topics
- **High Save indicators** (comments mentioning "saving this", "bookmarking", etc.)
- **Thread depth** (posts with long back-and-forth comment threads = algorithm favors them)

**Categorize by Trend Type:**
- 🔥 **Hot Now**: Multiple high-engagement posts in last 24h
- 📈 **Rising**: Emerging topic with growing engagement
- 🎯 **Your Lane**: Directly relevant to your positioning
- 💡 **Adjacent Opportunity**: Related topic you can add unique perspective to

## Step 5: Output Trending Topics Report

Present findings in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN FEED TRENDS ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Feed Summary
Posts analyzed: [X]
Posts meeting threshold (20+ likes, 10+ comments): [Y]
Individual authors only: [Z]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 TRENDING TOPIC #1: [Topic Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trend Type: [Hot Now / Rising / Your Lane / Adjacent]

Evidence:
• [Author 1] - [Post summary] - [X likes, Y comments]
• [Author 2] - [Post summary] - [X likes, Y comments]

Why It's Working:
[Analysis of engagement driver]

Your Angle:
[Suggested unique perspective based on {{CLIENT_BRAND_PRIMARY}} positioning]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 TRENDING TOPIC #2: [Topic Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Same format]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TRENDING TOPIC #3: [Topic Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Same format]
```

## Step 6: Topic Selection & Post Generation

After presenting trends, ask:

```
Which topic would you like to post about? I'll use the linkedin-elite-posts skill to generate 2-3 post variations.

Or tell me if you want to:
• Combine multiple trending topics
• Take a contrarian angle on any topic
• Focus on a specific aspect
```

**When user selects a topic:**

1. Confirm the selected topic and angle
2. Invoke linkedin-elite-posts skill with:
   - Topic: [Selected trending topic]
   - Angle: [User's chosen or recommended angle]
   - Context: [Evidence from feed analysis]
3. Generate post variations following linkedin-elite-posts workflow

## Positioning Context

When suggesting angles, align with {{CLIENT_FOUNDER_NAME}}'s {{CLIENT_BRAND_PRIMARY}} positioning:
- Agentic AI systems for SMEs
- Finance, ERP, CRM automation
- Natural language → agent execution
- AI-native business OS vision
- Non-coder empowerment through AI

**Strong angles for this positioning:**
- Practical implementation over hype
- SME-specific challenges vs enterprise solutions
- Real deployment experience with SME implementations
- Democratizing AI for non-technical users
- Intent-based systems vs menu-driven software

**360Brew Content Rules to Apply:**
- Opening hook must be a "Topic Signal" (e.g., "In agentic AI systems, the bottleneck isn't...")
- 80% of content must align with profile keywords (Agentic AI, SME automation)
- Create Save-worthy assets: schemas, frameworks, PRD templates
- No external links in post body (reduces reach 50%); put in first comment
- Hashtags are obsolescent; algorithm reads full text

## Quality Checklist

Before presenting report:
- ✅ All posts meet 20+ likes AND 10+ comments threshold
- ✅ No company pages, brands, or organizations included
- ✅ No articles included (native posts only)
- ✅ Topics grouped by trend patterns
- ✅ Each topic has suggested angle aligned with positioning
- ✅ Clear path to linkedin-elite-posts integration
- ✅ Recommended topics align with profile keywords (360Brew Profile-Content Alignment)
- ✅ Save-worthy content format suggested for each topic
- ✅ Topic Signal hook example provided for each recommendation

## Edge Cases

**Not enough qualifying posts:**
```
Your feed has [X] posts but only [Y] meet the engagement threshold (20+ likes, 10+ comments) from individual authors.

Options:
1. Lower threshold to 10+ likes, 5+ comments?
2. Scroll further back and paste more content?
3. Analyze what's available and note limited data?
```

**No clear trends:**
```
I found [X] qualifying posts but no clear trending patterns (topics appear once each).

Top performing individual topics:
[List top 3 by engagement]

Would you like to pick one of these, or should I suggest evergreen topics in your lane?
```

## Shared Activity Log (Token Optimization)

**Check the shared log first before requesting fresh feed content.**

**Log location:** `shared/logs/linkedin-activity.md`

### On Each Run:
1. **Read shared log first** to check:
   - "Feed Insights Cache" for recently identified trends (if <4 hours old, reuse)
   - "High-Engagement Posts Saved" for content inspiration
   - Today's post status (avoid duplicate content)
2. **Only request fresh feed content** if:
   - Cache is stale (>4 hours)
   - User explicitly requests fresh analysis
3. **After analysis**, update shared log:
   - Update "Feed Insights Cache > Trending Topics" table
   - Add high-engagement posts to "High-Engagement Posts Saved"

### What to Log:
**Trending topics:**
```
| Topic | Author | Post URL | Engagement Level | Your Angle |
```

**Saved posts:**
```
| Author | Profile URL | Post URL | Topic | Engagement | Saved For |
```
**Always capture Profile URL and Post URL** for quick navigation later.

### Read from Log Instead of LinkedIn:
- Check "Feed Insights Cache" before requesting feed paste
- Check "High-Engagement Posts Saved" for content ideas
- Reuse cached trends if still relevant (<4 hours old)
