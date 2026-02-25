---
name: x-trender
description: Analyze X.com (Twitter) to identify trending topics for content creation. Use when user says "find trending on X", "what's trending on Twitter", "X trends", "analyze X feed", or wants to discover what's resonating on X.com today. Works with browser MCP (Chrome DevTools or Playwright) - navigates to X.com/explore to find trending topics. Filters for high-engagement posts from individual thought leaders (excludes brands, news outlets, promotional content). Outputs trending topic recommendations with angle suggestions for cross-platform content creation.
---

# X.com Feed Trends

Analyze X.com (Twitter) to identify trending topics worth creating content about. Designed for browser MCP (Chrome DevTools or Playwright) workflow.

## Trigger

Activate when user says:
- "find trending on X"
- "what's trending on Twitter"
- "X trends"
- "analyze X feed"
- "trending topics on X.com"

## Step 1: Navigate to X.com Explore

Using browser MCP (Chrome DevTools or Playwright), navigate to X.com explore page:

1. Go to `x.com/explore` or `x.com/explore/tabs/trending`
2. Check the "Trending" and "For You" tabs
3. Scroll to load 20-30 trending topics/posts

If user is not logged in, trends may be limited to location-based. Note this in output.

## Step 2: Extract Trending Topics

From X.com explore, capture:

**Trending Topics Section:**
- Topic name/hashtag
- Category (if shown: Technology, Business, Entertainment, etc.)
- Tweet volume (e.g., "125K posts")
- Sample tweet snippets if visible

**Engagement Threshold (for individual posts):**
- 100+ likes AND 20+ retweets for relevance
- Skip posts below threshold

**Author Filter (REQUIRED):**
- Individual profiles only (person's name, bio with job/role)
- Skip brand accounts
- Skip news outlet accounts
- Skip promotional/ad content
- Skip crypto/NFT spam

## Step 3: Categorize & Analyze Trends

For each trending topic, extract:

1. **Core Topic**: Main subject (e.g., "AI regulation debate")
2. **Trend Type**: Breaking news, ongoing conversation, viral moment, industry discussion
3. **Engagement Driver**: Why it's trending (controversy, news event, viral thread, influencer take)
4. **Relevance Score**: How relevant to your content pillars

**Categorize by Trend Type:**
- BREAKING: News-driven, time-sensitive
- VIRAL: Meme or moment spreading rapidly
- INDUSTRY: Professional/business discussion
- TECH: Technology-focused conversation
- CULTURE: Social/cultural commentary

## Step 4: Output Trending Topics Report

Present findings in this format:

```
========================================
X.COM TRENDING ANALYSIS
========================================

Analyzed: [timestamp]
Location: [detected location or "Global"]
Login Status: [Logged in / Not logged in]

========================================
TRENDING TOPIC #1: [Topic/Hashtag]
========================================

Category: [Tech/Business/Culture/etc.]
Volume: [X posts in last Y hours]
Trend Type: [Breaking/Viral/Industry/Tech/Culture]

Top Voices:
- @[handle] - [summary] - [likes/retweets]
- @[handle] - [summary] - [likes/retweets]

Why It's Trending:
[Analysis of engagement driver]

Content Angle:
[Suggested unique perspective for your content]

Cross-Platform Potential: [High/Medium/Low]
[Note if topic works for LinkedIn, blog, etc.]

========================================
TRENDING TOPIC #2: [Topic/Hashtag]
========================================

[Same format]

========================================
TRENDING TOPIC #3: [Topic/Hashtag]
========================================

[Same format]
```

## Step 5: Cross-Platform Recommendations

After presenting X trends, suggest cross-platform opportunities:

```
CROSS-PLATFORM OPPORTUNITIES
========================================

For LinkedIn:
- [Topic] can be adapted as: [angle suggestion]

For Blog/Newsletter:
- [Topic] deeper dive opportunity: [angle suggestion]

For X Thread:
- [Topic] thread opportunity: [structure suggestion]
```

## Step 6: Topic Selection

After presenting trends, ask:

```
Which trending topic interests you? I can help you:

1. Create an X thread on this topic
2. Adapt it for LinkedIn (using linkedin-elite-posts)
3. Outline a blog post
4. Just save it for later

Or tell me if you want to explore any topic deeper.
```

## Positioning Context

When suggesting angles, align with user's positioning:
- Agentic AI systems for SMEs
- Finance, ERP, CRM automation
- AI-native business OS vision
- Practical implementation over hype
- Democratizing AI for non-technical users

## Quality Checklist

Before presenting report:
- All topics verified as actually trending (not stale)
- No brand/promotional content included
- Each topic has suggested content angle
- Cross-platform potential noted
- Time-sensitivity flagged for breaking news

## Edge Cases

**Not logged in:**
```
You're not logged in to X.com. Trending topics shown are based on [location] and may not reflect your interests.

Options:
1. Log in for personalized trends?
2. Continue with location-based trends?
3. Search for specific topic trends?
```

**Trends dominated by news/sports:**
```
Current trends are heavily news/sports focused:
- [List breaking news topics]

Would you like me to:
1. Filter for tech/business trends only?
2. Search for specific industry hashtags?
3. Show these anyway for awareness?
```

## Shared Activity Log

**Log location:** `linkedin-core/shared/logs/x-activity.md`

### On Each Run:
1. **Read shared log first** to check:
   - Recent trend analysis (if <2 hours old, offer to reuse or refresh)
   - Saved high-engagement posts for inspiration
2. **After analysis**, update shared log:
   - Update trending topics table
   - Add notable posts/threads worth revisiting

### What to Log:
```
| Topic | Category | Volume | Your Angle | Timestamp |
```
