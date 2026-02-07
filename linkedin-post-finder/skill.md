---
name: linkedin-post-finder
description: Discover high-engagement LinkedIn posts about Agentic AI from individual thought leaders (not company pages) from the past 24 hours. Use when the user wants to find posts about agentic AI, autonomous systems, AI agents, or related topics from practitioners, founders, and experts. Excludes company/organization pages like MIT Sloan, LandingAI, etc.
---

# LinkedIn Post Finder

This skill helps discover high-quality, highly-engaged LinkedIn posts about Agentic AI from **individual thought leaders** (not company/organization pages) from the past 24 hours for knowledge acquisition and staying current with industry trends and conversations.

## 360Brew Algorithm Context (2026)

LinkedIn's 360Brew algorithm now prioritizes "Topic Authority" over raw engagement. When finding posts:

- **Topical Leaders**: Authors whose profile aligns with their post content get higher distribution
- **Save-Worthy Content**: Posts with high Save rates (schemas, frameworks, PRDs) indicate "Referenceable" expertise
- **Zero-Shot Capability**: New profiles with high-value niche content can go viral without large followings
- **Semantic Reasoning**: Quality of argument matters more than keywords; logically structured posts outperform engagement-bait

## Core Workflow

### Step 1: Navigate to LinkedIn Feed

Direct the user to scroll through their LinkedIn feed from the past 24 hours. The goal is to review the natural flow of content that appears in their feed, not to search for specific keywords.

### Step 2: Scan Feed for Agentic AI Content

As the user scrolls through their feed, identify posts that discuss:

**Core Agentic AI Topics:**
- Agentic AI systems, architectures, and frameworks
- AI agents and autonomous systems
- Multi-agent systems and agent orchestration
- Agentic workflows and decision-making
- Production deployments of AI agents

**Related Technical Topics:**
- AI automation and intelligent automation
- LLM applications and integrations
- Tool-calling and function-calling patterns
- AI-native software architecture
- Agent evaluation and reliability

**Business Applications:**
- AI for business operations and workflows
- Enterprise AI adoption and implementation
- AI transformation case studies
- ROI and impact of agentic systems

**Industry Trends:**
- New agentic AI products or frameworks
- Research breakthroughs in agent systems
- Market shifts toward autonomous AI
- Thought leadership on AI future

### Step 3: Filter by Engagement Level

Focus on posts with significant engagement, as these indicate important conversations and valuable insights:

**High-Value Engagement Signals:**
- 100+ reactions (likes, celebrates, etc.)
- 20+ thoughtful comments (not just emojis)
- 10+ shares or reposts
- **High Save indicators** (360Brew values Saves 5x more than Likes; look for posts with "Save for later" mentions in comments)
- Engagement from recognized industry experts
- Viral posts showing exponential growth

**Quality Engagement Indicators:**
- Substantive comment threads with technical discussion
- Comments from founders, CTOs, or senior technical leaders
- Cross-pollination across different professional communities
- Debates or diverse perspectives in comments

**Filter Out:**
- Generic motivational content with AI buzzwords
- Pure promotional posts without substance
- Posts with high engagement but low relevance to agentic AI
- Engagement-bait posts without real insights
- **Company/Organization pages** (e.g., MIT Sloan, LandingAI, DeepLearning.AI) - only include posts from individual people

**How to Identify Company vs Individual Posts:**
- **Company pages**: Show company logo (not a person's face), display "X followers" without a personal job title/headline, URL pattern is linkedin.com/company/...
- **Individual profiles**: Show a person's photo, have a personal headline (e.g., "CEO at X", "Founder of Y", "Senior Engineer at Z"), URL pattern is linkedin.com/in/...
- If unsure, check if the author name is a person's name (first + last name) vs an organization name

### Step 4: Extract Post Information

For each highly-engaged, relevant post, extract and present:

1. **Author name and headline** - Who is sharing this insight?
2. **Post content** - The full post or key excerpt
3. **Engagement metrics** - Specific numbers (reactions, comments, shares)
4. **Post timestamp** - When it was published (within last 24 hours)
5. **Link to post** - Direct URL for access
6. **Key insight** - What makes this post worth reading?
7. **Trending indicator** - Is this part of a larger conversation?

### Step 5: Identify 5 Top Posts

From all posts discovered in the feed, select the 5 most valuable posts based on:

1. **Individual author only** - MUST be from a person (not a company/organization page)
2. **Engagement level** - Higher engagement = more important conversation
3. **Content quality** - Substantive insights, not fluff
4. **Relevance to Agentic AI** - Direct connection to core topics
5. **Novelty** - New information, fresh perspectives, or emerging trends
6. **Author credibility** - Known experts, practitioners, or thought leaders

**IMPORTANT**: Only include posts from individual LinkedIn profiles (linkedin.com/in/...). Exclude all company pages (linkedin.com/company/...) even if they have high engagement. The goal is to find thought leaders and practitioners, not corporate marketing content.

Prioritize posts that will genuinely expand knowledge or provide valuable industry insights.

## Content Evaluation Criteria

Posts are valuable for knowledge and trend tracking when they provide:

**Technical Insights:**
- Novel approaches to agent architectures or frameworks
- Real-world implementation experiences and lessons learned
- Technical challenges and solutions in production agentic systems
- Comparative analysis of different agentic AI approaches
- Performance metrics and benchmarking results

**Industry Trends:**
- Emerging patterns in agentic AI adoption
- New product launches or framework releases
- Shifts in how companies are deploying agents
- Market signals about the future of autonomous systems
- Regulatory or ethical discussions affecting the space

**Thought Leadership:**
- Strategic perspectives from recognized experts
- Predictions about the evolution of agentic AI
- Analysis of current state and future direction
- Debates about best practices and methodologies
- Cross-industry applications and insights

**Practical Knowledge:**
- Use cases and application examples
- ROI data and business impact metrics
- Integration patterns and tooling recommendations
- Training and skill development approaches
- Organizational change management for AI adoption

## Output Format

Present the top 5 posts in this structure:

```
## Top 5 Agentic AI Posts - [Date]

### Post 1: [Author Name] - [Headline]
**Engagement:** [X reactions, Y comments, Z shares]
**Posted:** [Timestamp]
**Link:** [URL]

**Why it's valuable:**
[1-2 sentences explaining what makes this post worth reading - the key insight, trend, or knowledge it provides]

**Key excerpt:**
"[Most insightful portion of the post]"

**What you'll learn:**
[Specific takeaway or knowledge gain from reading this post]

---

### Post 2: [Author Name] - [Headline]
[Same structure...]

---

### Post 3: [Author Name] - [Headline]
[Same structure...]

---

### Post 4: [Author Name] - [Headline]
[Same structure...]

---

### Post 5: [Author Name] - [Headline]
[Same structure...]

---

## Trend Summary
[Brief 2-3 sentence summary of common themes, emerging patterns, or notable shifts across these top posts]
```

## Best Practices

- **Individual authors only**: Always verify the post is from a person's profile (linkedin.com/in/...), not a company page (linkedin.com/company/...). Skip MIT Sloan, LandingAI, DeepLearning.AI, and similar organizational accounts.
- **Engagement signals quality**: Posts with 100+ reactions and substantive comments typically contain valuable insights worth reading
- **Look for debates**: Posts with diverse perspectives in comments often indicate important industry conversations
- **Author credibility matters**: Posts from practitioners, founders, and technical leaders tend to be more substantive
- **Trend identification**: Look for multiple posts discussing similar themes - this indicates emerging industry trends
- **Skip the noise**: Filter out generic motivational content, pure promotional posts, and engagement-bait
- **Recency matters**: Focus strictly on posts from the last 24 hours to capture current conversations
- **Quality over quantity**: 5 high-value posts with real insights beat 20 mediocre posts with AI buzzwords
- **Read the comments**: Sometimes the most valuable insights are in the comment threads, not the original post
- **Cross-reference**: When multiple respected voices discuss the same topic, it signals an important development
