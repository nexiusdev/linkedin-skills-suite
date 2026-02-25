---
name: reddit-feed-trends
description: Analyze Reddit to identify trending topics and discussions for content creation. Use when user says "find trending on Reddit", "what's hot on Reddit", "Reddit trends", "analyze Reddit", or wants to discover what discussions are resonating today. Works with Claude for Chrome - navigates to Reddit popular/all to find trending posts. Filters for high-engagement discussions from relevant subreddits (technology, business, AI, startups). Outputs trending topic recommendations with angle suggestions for cross-platform content creation.
---

# Reddit Trending Analysis

Analyze Reddit to identify trending topics and discussions worth creating content about. Designed for Claude for Chrome workflow.

## Trigger

Activate when user says:
- "find trending on Reddit"
- "what's hot on Reddit"
- "Reddit trends"
- "analyze Reddit"
- "trending topics on Reddit"

## Step 1: Navigate to Reddit

Using Claude for Chrome, navigate to Reddit:

**Primary sources (check in order):**
1. `reddit.com/r/popular` - Popular across all of Reddit
2. `reddit.com/r/all` - Everything trending

**Targeted subreddits for tech/AI content:**
- `reddit.com/r/artificial` - AI discussions
- `reddit.com/r/MachineLearning` - ML community
- `reddit.com/r/technology` - Tech news
- `reddit.com/r/startups` - Startup discussions
- `reddit.com/r/Entrepreneur` - Business topics
- `reddit.com/r/SaaS` - SaaS discussions
- `reddit.com/r/LocalLLaMA` - Local AI/LLM discussions

Sort by "Hot" or "Rising" for current trends.

## Step 2: Extract Trending Posts

From Reddit feeds, capture:

**Engagement Threshold (REQUIRED):**
- 500+ upvotes for r/popular or r/all
- 100+ upvotes for niche subreddits
- 50+ comments indicates active discussion

**Content Filter:**
- Discussion posts (text posts with debate/opinions)
- News/articles generating discussion
- Ask threads with high engagement
- Skip memes/image-only posts (unless highly relevant)
- Skip NSFW content
- Skip crypto/trading pump posts

**Quality Signals:**
- High comment-to-upvote ratio = active discussion
- Awards/gold = community validation
- Cross-posted to multiple subs = broad interest

## Step 3: Analyze Discussions

For each trending post, extract:

1. **Core Topic**: Main subject of discussion
2. **Subreddit Context**: Which community, their perspective/bias
3. **Discussion Angle**: What's the debate? (pro/con, how-to, news reaction)
4. **Top Comments**: Key viewpoints from top 3-5 comments
5. **Controversy Level**: Sorted by controversial? Split opinions?

**Categorize by Discussion Type:**
- NEWS REACTION: Community responding to announcement/news
- DEBATE: Split opinions, active argument
- HOW-TO: Practical advice thread
- EXPERIENCE: Personal stories/case studies
- ASK: Questions with valuable answers
- RANT: Frustration-driven (often reveals pain points)

## Step 4: Output Trending Topics Report

Present findings in this format:

```
========================================
REDDIT TRENDING ANALYSIS
========================================

Analyzed: [timestamp]
Sources: [subreddits checked]

========================================
TRENDING TOPIC #1: [Topic]
========================================

Subreddit: r/[subreddit]
Post Title: "[title]"
Discussion Type: [News/Debate/How-To/Experience/Ask/Rant]

Engagement:
- Upvotes: [X]
- Comments: [Y]
- Awards: [if any]

Top Perspectives:
1. [Summary of top comment viewpoint]
2. [Summary of contrarian/second viewpoint]
3. [Summary of practical insight]

Why It's Trending:
[Analysis of what sparked discussion]

Content Angle:
[Suggested unique perspective for your content]

Key Quotes Worth Noting:
- "[Notable quote from discussion]"

========================================
TRENDING TOPIC #2: [Topic]
========================================

[Same format]

========================================
TRENDING TOPIC #3: [Topic]
========================================

[Same format]
```

## Step 5: Content Opportunities

After presenting trends, identify content opportunities:

```
CONTENT OPPORTUNITIES
========================================

Pain Points Discovered:
- [Pain point from rant/complaint threads]
- [Frustration users expressed]

Questions Worth Answering:
- [Unanswered or poorly answered questions]
- [Recurring confusion in comments]

Contrarian Takes:
- [Popular opinion you could challenge]
- [Nuance missing from discussion]

Cross-Platform Potential:
- LinkedIn: [Which topics translate well]
- X Thread: [Which topics work as threads]
- Blog Deep-Dive: [Which need longer treatment]
```

## Step 6: Topic Selection

After presenting trends, ask:

```
Which Reddit discussion interests you? I can help you:

1. Create a response post/comment on Reddit
2. Turn the discussion into a LinkedIn post
3. Create an X thread with your take
4. Outline a blog post exploring the topic
5. Just save insights for later

Or tell me if you want to dive deeper into any subreddit.
```

## Positioning Context

When suggesting angles, align with user's positioning:
- Agentic AI systems for SMEs
- Finance, ERP, CRM automation
- AI-native business OS vision
- Practical implementation over hype
- Democratizing AI for non-technical users

**Reddit-specific positioning:**
- Redditors value authenticity and hate marketing-speak
- Lead with value, not promotion
- Acknowledge complexity and trade-offs
- Share real experience, not theory

## Quality Checklist

Before presenting report:
- All posts meet engagement thresholds
- Discussion context captured (not just headlines)
- Top comment perspectives included
- Content angles are authentic, not salesy
- Pain points and questions identified

## Edge Cases

**Subreddit is private/quarantined:**
```
r/[subreddit] is [private/quarantined].

Alternative subreddits for this topic:
- r/[alternative1]
- r/[alternative2]

Should I check those instead?
```

**Trends dominated by memes/off-topic:**
```
r/popular is currently dominated by [memes/sports/entertainment].

Would you like me to:
1. Check specific tech/business subreddits instead?
2. Search Reddit for specific topics?
3. Show general trends anyway?
```

**Low engagement day:**
```
Engagement is lower than usual today. Showing best available:
[List with lower thresholds noted]

Consider checking back later or searching for specific topics.
```

## Shared Activity Log

**Log location:** `shared/logs/reddit-activity.md`

### On Each Run:
1. **Read shared log first** to check:
   - Recent trend analysis (if <4 hours old, offer to reuse or refresh)
   - Saved discussions worth revisiting
   - Pain points previously identified
2. **After analysis**, update shared log:
   - Update trending topics table
   - Add notable discussions/insights

### What to Log:
```
| Topic | Subreddit | Post URL | Discussion Type | Key Insight | Timestamp |
```

**Pain Points Log:**
```
| Pain Point | Source Thread | Frequency | Content Opportunity |
```
