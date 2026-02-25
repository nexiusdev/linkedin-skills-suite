---
name: whatsapp-community-ai
description: Manage the "{{CLIENT_COMMUNITY_NAME}}" WhatsApp community group by posting AI news content and driving engagement. Use when user says "post ai news", "whatsapp community", "share ai update", "ai ignite", or wants to drive engagement in the {{CLIENT_COMMUNITY_NAME}} group with latest AI developments. Integrates with x-trender and linkedin-trender to find news-worthy content from past 24 hours. Posts include source URLs from major news platforms. Multiple posts are spaced 4 hours apart. Also monitors chat for unanswered questions and auto-replies with thoughtful responses. Use "monitor ai ignite" or "check ai ignite" to scan for questions needing answers.
---

# WhatsApp Community AI News Manager

Drive engagement in the **{{CLIENT_COMMUNITY_NAME}}** WhatsApp community by sharing curated AI news and encouraging member reactions and discussions. Designed for browser MCP (Chrome DevTools or Playwright) workflow.

**Target Group: {{CLIENT_COMMUNITY_NAME}}** (only post to this group)

## Trigger

Activate when user says:
- "post ai news"
- "whatsapp community"
- "share ai update"
- "ai news for whatsapp"
- "community engagement"
- "post to whatsapp group"
- "find ai news to share"
- "ai ignite"
- "post to ai ignite"

## Core Objectives

1. **Drive Engagement**: Encourage community members to share their POV and reactions
2. **Curate AI News**: Share latest developments across all aspects of AI
3. **Source Attribution**: Always include URL links from major news platforms
4. **Optimal Spacing**: Space multiple posts 4 hours apart for maximum engagement

## Step 1: Gather AI News from Trend Sources

Before posting, collect news-worthy content from multiple sources:

### 1A: Run x-trender (X.com/Twitter)

Invoke the `x-trender` skill to find:
- AI-related trending topics from past 24 hours
- High-engagement posts from AI thought leaders
- Breaking AI news and announcements
- Viral AI discussions

**X.com Filter for AI News:**
- Keywords: AI, artificial intelligence, ChatGPT, Claude, GPT, LLM, machine learning, neural network, agentic AI, AI agents, automation, robotics
- Source priority: Individual thought leaders > News outlets > Company announcements
- Engagement threshold: 100+ likes, 20+ retweets

### 1B: Run linkedin-trender (LinkedIn)

Invoke the `linkedin-trender` skill to find:
- Professional AI discussions from past 24 hours
- Industry insights and analysis
- Enterprise AI developments
- AI implementation stories

**LinkedIn Filter for AI News:**
- Keywords: Same as X.com filters
- Source priority: Individual experts > Company pages
- Engagement threshold: 20+ likes, 10+ comments

### 1C: Check Major News Platforms

If trend sources lack breaking news, search these platforms:
- TechCrunch (techcrunch.com/tag/artificial-intelligence)
- The Verge (theverge.com/ai-artificial-intelligence)
- Ars Technica (arstechnica.com/ai)
- VentureBeat (venturebeat.com/category/ai)
- MIT Technology Review (technologyreview.com/artificial-intelligence)
- Wired (wired.com/tag/artificial-intelligence)
- Reuters Technology (reuters.com/technology/artificial-intelligence)

**Priority Order for News Selection:**
1. Breaking announcements (new AI models, major releases)
2. Regulatory/policy developments
3. Industry adoption stories
4. Technical breakthroughs
5. AI ethics and safety discussions
6. AI in business applications
7. AI research papers with practical implications

## Step 2: Evaluate News-Worthiness

Score each potential news item:

**High Priority (Post Immediately):**
- Breaking: Major AI model releases (GPT-5, Claude updates, Gemini, etc.)
- Industry-shifting announcements (regulations, major acquisitions)
- Viral discussions with broad implications
- Score: 8-10/10

**Medium Priority (Queue for Later):**
- Interesting developments with professional relevance
- Thought-provoking analyses from experts
- Practical AI implementation stories
- Score: 5-7/10

**Low Priority (Skip or Save):**
- Niche technical papers without broad appeal
- Rehashed topics with no new angle
- Promotional content disguised as news
- Score: 1-4/10

## Step 3: Format WhatsApp Message

Create engaging messages that drive discussion:

### Message Template

```
[EMOJI] [HEADLINE/HOOK]

[2-3 sentence summary of the news - what happened and why it matters]

[OPTIONAL: Key takeaway or implication for the audience]

[DISCUSSION PROMPT - Question to encourage POV sharing]

[SOURCE URL]

#AI #[RelevantTag]
```

### Emoji Guide by Topic

| Topic | Emoji |
|-------|-------|
| Breaking News | 🚨 or ⚡ |
| AI Models/Releases | 🤖 or 🧠 |
| Business/Enterprise | 💼 or 📈 |
| Research/Papers | 🔬 or 📚 |
| Ethics/Safety | ⚖️ or 🛡️ |
| Automation | ⚙️ or 🔄 |
| Coding/Development | 💻 or 🛠️ |
| Opinion/Analysis | 💭 or 🎯 |
| Regulation/Policy | 📋 or 🏛️ |

### Discussion Prompts (Rotate These)

**For Breaking News:**
- "What's your take on this?"
- "How do you see this impacting [industry/work]?"
- "Surprised or expected?"
- "Game-changer or overhyped?"

**For Technical Topics:**
- "Anyone tried this yet? Share your experience!"
- "How would you apply this in your work?"
- "What problems could this solve for you?"
- "Technical folks - is this as big as it sounds?"

**For Opinion/Analysis:**
- "Agree or disagree with this take?"
- "What's missing from this perspective?"
- "Hot take: [provocative statement]. Thoughts?"
- "Where do you stand on this?"

**For Practical Applications:**
- "Who's already doing something similar?"
- "Would this work in ASEAN markets?"
- "What's stopping wider adoption?"
- "Share your use case if you've tried this!"

## Step 4: Check Posting Schedule

Before posting, verify timing:

### 4-Hour Rule

**CRITICAL: Minimum 4 hours between posts to avoid flooding.**

Check shared log for last post time:

```
1. Read shared log → WhatsApp Posts table → Get last post timestamp
2. Calculate: hours_since_last = current_time - last_post_time
3. If hours_since_last < 4:
   → next_valid_time = last_post_time + 4 hours
   → Queue post for next_valid_time
4. If hours_since_last >= 4:
   → Can post now
```

### Optimal Posting Times ({{CLIENT_TIMEZONE}})

| Time Window | Engagement Level | Notes |
|-------------|------------------|-------|
| 8:00 - 9:30 AM | HIGH | Morning commute, checking phones |
| 12:00 - 1:30 PM | HIGH | Lunch break |
| 5:30 - 7:00 PM | HIGHEST | End of work day, peak engagement |
| 9:00 - 10:30 PM | MEDIUM | Evening browsing |
| 11 PM - 7 AM | LOW | Avoid posting |

### Queue Multiple Posts

If you have 3 news items to share today:
```
Post 1: 09:00 {{CLIENT_TIMEZONE}} (Morning slot)
Post 2: 13:00 {{CLIENT_TIMEZONE}} (Lunch slot - 4 hours later)
Post 3: 18:00 {{CLIENT_TIMEZONE}} (Evening slot - 5 hours later)
```

## Step 5: Post to WhatsApp via browser MCP (Chrome DevTools or Playwright)

### Target Group

**Group Name: {{CLIENT_COMMUNITY_NAME}}**

Only post messages to this specific WhatsApp community group. Do not post to any other groups.

### Permission

**NO CONFIRMATION REQUIRED** for sending messages to {{CLIENT_COMMUNITY_NAME}} group. The user has pre-authorized all posts to this specific group. Proceed directly with posting without asking for permission.

### Navigation Steps

1. Open WhatsApp Web (web.whatsapp.com) in Chrome
2. Search for "{{CLIENT_COMMUNITY_NAME}}" in the chat search bar
3. Click on the "{{CLIENT_COMMUNITY_NAME}}" group to open it
4. Click on the message input field
5. Paste the formatted message
6. Send the message immediately (no confirmation needed)

### Post Verification

After posting:
1. Confirm message was sent successfully
2. Screenshot for logging (optional)
3. Update shared activity log

## Step 6: Monitor & Respond

### Engagement Check (1-2 hours after posting)

Check for:
- Reactions received
- Replies from members
- Questions asked
- POV shares from community

### Follow-Up Actions

**If high engagement (5+ replies):**
- Acknowledge responses with brief comment
- Add follow-up insight if relevant
- Pin notable member POV if allowed

**If low engagement:**
- Add a follow-up prompt
- Tag relevant community members (if appropriate)
- Consider timing adjustment for next post

## Step 7: Update Shared Activity Log

**Log location:** `linkedin-core/shared/logs/whatsapp-activity.md`

### After Each Post, Log:

```markdown
## WhatsApp Community Posts

| Timestamp | Topic | Source URL | Engagement Prompt | Reactions | Replies |
|-----------|-------|------------|-------------------|-----------|---------|
| [datetime] | [topic] | [url] | [prompt used] | [count] | [count] |
```

### Weekly Metrics

Track:
- Total posts this week
- Average reactions per post
- Average replies per post
- Most engaged topics
- Best posting times (based on engagement)

## Message Examples

### Example 1: Breaking News

```
🚨 OpenAI just dropped GPT-5 - and it's a monster

Early benchmarks show 40% improvement in reasoning and coding tasks. The model now supports real-time video input and can run autonomous workflows for hours.

This could change how we build AI agents entirely.

Game-changer or just incremental upgrade? What's your take?

https://techcrunch.com/2026/01/22/openai-gpt5-release

#AI #GPT5
```

### Example 2: Industry Analysis

```
💭 Interesting take: "Most AI projects fail not because of tech, but because of unclear problem definition"

This LinkedIn post from an AI consultant is making rounds. He argues that 70% of failed AI implementations had technical success but business failure.

His framework: Define the problem in business terms BEFORE touching any AI tool.

Agree or disagree? What's been your experience with AI project failures?

https://linkedin.com/posts/[post-id]

#AI #Implementation
```

### Example 3: Practical Application

```
⚙️ This startup is using Claude to automate 80% of their customer support

They shared their exact workflow: Claude reads emails → classifies intent → drafts responses → human reviews only exceptions

Cost savings: 60%. Customer satisfaction: Actually improved.

Would this work for your business? What's stopping you from trying?

https://venturebeat.com/ai/startup-ai-customer-support-case-study

#AI #Automation
```

### Example 4: Research/Technical

```
🔬 New paper: AI agents can now teach themselves new skills without human input

Researchers at DeepMind created agents that discover and master new capabilities through self-play. Think: AI that figures out how to use new tools on its own.

The implications for agentic AI are huge - agents that adapt to YOUR workflow, not the other way around.

Technical folks - is this as significant as it sounds? Link to paper:

https://arxiv.org/abs/2026.xxxxx

#AI #Research
```

## Quality Checklist

Before posting:
- [ ] News is from past 24 hours (not stale)
- [ ] Source URL is included and valid
- [ ] Source is a major/reputable platform
- [ ] Discussion prompt encourages POV sharing
- [ ] 4-hour spacing from last post respected
- [ ] Posted during optimal time window
- [ ] Message is under 500 words (WhatsApp readability)
- [ ] No promotional/spam content
- [ ] Topic has broad appeal to community

## Edge Cases

### No News-Worthy Content

```
I've checked X.com, LinkedIn, and major news platforms. No significant AI news in the past 24 hours.

Options:
1. Share an evergreen AI insight or tip
2. Post a discussion question without news hook
3. Resurface a recent story with new angle
4. Skip posting today
```

### Multiple Breaking News Items

```
Found 4 high-priority news items in the past 24 hours. Scheduling:

1. [Most urgent] - Post NOW
2. [Second priority] - Queue for [time + 4h]
3. [Third priority] - Queue for [time + 8h]
4. [Fourth priority] - Save for tomorrow AM

Proceed with this schedule?
```

### Source URL Not Available

If direct source URL isn't available:
- Search for the news on Google News
- Find coverage from reputable outlet
- If no URL found, clearly state source: "Via @[handle] on X.com" or "Reported by [publication]"

## Autonomous Mode

When triggered with "start whatsapp news" or "autonomous whatsapp":

```
1. Check current time → Determine if in posting window
2. Read shared log → Check last post time → Verify 4h spacing
3. Run x-trender → Collect AI news from X.com
4. Run linkedin-trender → Collect AI news from LinkedIn
5. Evaluate all items → Score for news-worthiness
6. For top 1-3 items:
   a. Format WhatsApp message
   b. Navigate to WhatsApp Web
   c. Post to community group
   d. Log to shared activity log
   e. Wait 4 hours before next post (or queue)
7. Report summary when complete
```

### Autonomous Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 WHATSAPP AI NEWS - AUTONOMOUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[10:00] Starting news collection...
[10:01] ✓ x-trender: Found 5 AI-related posts
[10:02] ✓ linkedin-trender: Found 3 AI-related posts
[10:03] ✓ Evaluated 8 items, 2 news-worthy

[10:04] Posting Item 1/2: "OpenAI GPT-5 Release"
[10:05] ✓ Posted to WhatsApp community
[10:05] ✓ Logged to shared activity log

[10:05] Item 2/2: "Claude Agent SDK Launch"
[10:05] ⏳ Queued for 14:00 {{CLIENT_TIMEZONE}} (4h spacing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SESSION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Posts sent: 1
Posts queued: 1
Next post: 14:00 {{CLIENT_TIMEZONE}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Integration with Other Skills

| Need | Skill to Use |
|------|--------------|
| Find X.com/Twitter AI news | `x-trender` |
| Find LinkedIn AI discussions | `linkedin-trender` |
| Deep-dive on specific topic | `WebSearch` or `WebFetch` |
| Create follow-up LinkedIn post | `linkedin-elite-post` |

## Community Engagement Best Practices

1. **Be Consistent**: Post at similar times each day
2. **Quality Over Quantity**: 1-2 excellent posts > 5 mediocre ones
3. **Engage Back**: Respond to member comments within 2 hours
4. **Celebrate POV**: Highlight great member contributions
5. **Ask, Don't Lecture**: Frame posts as discussions, not broadcasts
6. **Credit Sources**: Always attribute and link
7. **Stay On Topic**: AI news only - don't dilute the community focus

---

## Chat Monitoring & Auto-Reply System

### Trigger

Activate monitoring when user says:
- "monitor ai ignite"
- "check ai ignite"
- "watch whatsapp"
- "auto-reply whatsapp"
- "start monitoring"

### Monitoring Frequency

**Default: Every 15 minutes**

Can be run:
- Manually via trigger commands
- Automatically via Windows Task Scheduler (see Automation Setup below)

### Permission

**NO CONFIRMATION REQUIRED** for sending replies in {{CLIENT_COMMUNITY_NAME}} group. The user has pre-authorized all responses to this specific group. Auto-reply immediately without asking for permission.

### What to Monitor

#### 1. Unanswered Questions (HIGHEST PRIORITY)

Detect questions that have NO replies yet:

**Question Indicators:**
- Messages ending with `?`
- Messages starting with: "how", "what", "why", "when", "where", "who", "can", "does", "is", "are", "has", "have", "should", "would", "could"
- Messages containing: "anyone know", "any idea", "help with", "looking for", "recommend", "suggestion"

**Skip if:**
- Message already has a reply (someone responded below it)
- Message is older than 2 hours (likely already seen and ignored)
- Message is from yourself
- Message was already replied to by the bot (check log)

#### 2. Replies to Your Posts

Monitor for:
- Direct replies to your news posts
- Mentions of your name
- Follow-up questions on topics you posted

**Action:** Acknowledge with thoughtful follow-up, add value or clarification.

#### 3. Member Posts - Share Your POV (HIGH PRIORITY)

Engage with interesting messages from other members by sharing thoughtful perspectives:

**What to Look For:**
- AI news shared by members (add your analysis)
- Opinions or hot takes on AI topics (agree/disagree with nuance)
- Experiences or case studies shared (relate with your own insight)
- Industry developments or announcements (provide context or implications)
- Technical discussions (add practical perspective)

**Context Check Before Replying (CRITICAL):**
1. Read the FULL message and any replies below it
2. Understand the member's intent and tone
3. Check if there's already an active discussion thread
4. Identify what value YOU can add (don't repeat what's been said)
5. Consider timing - is this still relevant?

**When to Share POV:**
- Message is about AI/tech topics within your expertise
- Your perspective adds genuine value (not just agreement)
- The conversation could benefit from a different angle
- No more than 2 hours old (stay relevant)
- Not already heavily discussed (5+ replies = skip)

**When NOT to Share POV:**
- Message is personal/off-topic (non-AI)
- Already many replies covering similar points
- Message is clearly meant for specific person
- You already replied to this member recently (avoid overengagement)
- Message is just a link share with no discussion prompt

**POV Response Quality Standards:**
- Must be THOUGHTFUL: Show you understood the context
- Must be INTELLIGENT: Add insight, not just reaction
- Must be SUBSTANTIVE: 2-4 sentences of real value
- Must be CONVERSATIONAL: Not preachy or lecturing

#### 4. Topic Mentions (Your Expertise Areas)

Keywords to watch:
- "agentic AI", "AI agents", "autonomous AI"
- "Claude", "Anthropic", "GPT", "OpenAI"
- "automation", "workflow automation"
- "SME", "small business AI"
- "ERP", "CRM", "finance automation"

**Action:** Offer helpful insight if the conversation could benefit from your expertise.

### Message Detection Logic

```
1. Open WhatsApp Web → {{CLIENT_COMMUNITY_NAME}} group
2. Scroll up to load messages from last 30 minutes
3. For each message, check:
   a. Is it from myself? → SKIP
   b. Is it in the "Already Replied" log? → SKIP
   c. Is it a question with no replies? → Queue for ANSWER
   d. Is it an interesting AI-related post? → Queue for POV

4. PRIORITY ORDER:
   - First: Answer unanswered questions (helpful)
   - Second: Share POV on interesting member posts (engaging)

5. For QUESTIONS:
   - Generate helpful, direct answer
   - Send immediately
   - Log to avoid duplicates

6. For POV SHARING:
   - Read full context (message + any replies)
   - Identify what unique value you can add
   - Generate thoughtful, intelligent perspective
   - Send only if it genuinely adds to the conversation
   - Log to avoid overengagement

7. Rate limit: Max 3 POV responses per monitoring cycle
```

### Response Generation Guidelines

**Tone:** Helpful, knowledgeable, conversational (not preachy or robotic)

**Length:** 2-4 sentences max. Concise but valuable.

**Structure:**
```
[Direct answer or insight]
[Supporting detail or example if relevant]
[Optional: Follow-up question to keep discussion going]
```

**DO:**
- Answer the actual question asked
- Provide actionable information
- Share relevant experience or examples
- Ask clarifying questions if needed
- Be genuinely helpful

**DON'T:**
- Give generic or vague responses
- Over-explain or lecture
- Promote yourself or your services
- Reply to rhetorical questions
- Respond to messages clearly meant for specific people

### Response Examples

**Question:** "Has anyone tried Claude for customer support automation?"

**Good Response:**
```
Yes! Claude works well for support - especially ticket classification and draft responses. The key is starting with a narrow use case (like FAQ responses) before expanding. What type of support are you looking to automate?
```

**Question:** "What's the difference between RAG and fine-tuning?"

**Good Response:**
```
RAG retrieves external docs at query time (good for current info, no retraining needed). Fine-tuning adjusts model weights (good for style/format, needs data + compute). For most business cases, RAG is easier to start with and maintain.
```

**Question:** "Any recommendations for AI tools for small businesses?"

**Good Response:**
```
Depends on the use case! For docs/writing: Claude or ChatGPT. For no-code automation: Make.com or Zapier with AI steps. For customer comms: Intercom or Freshdesk AI. What specific workflow are you trying to improve?
```

### POV Response Examples

**Member shares news:** "OpenAI is reportedly working on a $20B data center project"

**Good POV Response:**
```
The scale is wild but makes sense strategically. Compute is the moat now - whoever controls the chips and power controls AI's trajectory. Curious if this accelerates their push away from being just an API company toward full vertical integration.
```

**Member shares opinion:** "I think RAG is overhyped. Most companies don't need it."

**Good POV Response:**
```
Partially agree - RAG gets oversold as a silver bullet. But for companies with proprietary docs that change frequently, it's genuinely useful. The real issue is people implementing RAG when simple prompt engineering would suffice. What's your experience been?
```

**Member shares experience:** "Just spent 3 months building an AI agent and it still hallucinates on edge cases"

**Good POV Response:**
```
3 months is actually fast for production-grade agents. The hallucination problem is real - we've found success with guardrails that force citation of sources and a human-in-the-loop for anything customer-facing. What domain are you building for?
```

**Member shares announcement:** "Google just launched their Universal Commerce Protocol for AI shopping"

**Good POV Response:**
```
This is huge for agentic commerce. Standardized APIs mean AI agents can actually complete purchases without custom integrations per retailer. The race is on for who controls the AI shopping layer - Google, Amazon, or someone new entirely.
```

### Monitoring Workflow

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 AI IGNITE MONITOR - START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[HH:MM] Opening WhatsApp Web...
[HH:MM] Navigating to {{CLIENT_COMMUNITY_NAME}}...
[HH:MM] Loading recent messages (last 30 mins)...
[HH:MM] Scanning for unanswered questions...
[HH:MM] Scanning for POV opportunities...

📋 UNANSWERED QUESTIONS (2 found):

1. [Member A] "How do I integrate Claude API with my app?"
   → Generating answer...
   → Sent ✓

2. [Member B] "What's everyone using for AI image generation?"
   → Generating answer...
   → Sent ✓

💭 POV OPPORTUNITIES (3 found, responding to top 2):

1. [Member C] shared: "OpenAI reportedly raising at $300B valuation"
   → Context check: No replies yet, AI funding topic
   → Generating thoughtful POV...
   → Sent ✓

2. [Member D] shared: "Just tried Claude's new computer use - mind blown"
   → Context check: 1 reply agreeing, can add technical insight
   → Generating thoughtful POV...
   → Sent ✓

3. [Member E] shared: "AI will replace 50% of jobs by 2030"
   → Context check: Already 6 replies debating, skip
   → Skipped (conversation already active)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ MONITOR COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Questions answered: 2
POV responses: 2
Skipped: 1 (active thread)
Next check: [HH:MM + 15 mins]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Logging Replied Messages

**Log location:** `linkedin-core/shared/logs/whatsapp-activity.md`

After each auto-reply, log to the "Auto-Replies Sent" table:

```markdown
## Auto-Replies Sent

| Timestamp | Member | Original Question | Response Summary | Status |
|-----------|--------|-------------------|------------------|--------|
| [datetime] | [name] | [question text] | [brief summary] | Sent ✓ |
```

This prevents duplicate replies to the same message.

### Rate Limiting

To avoid appearing spammy:

**Questions (Answering):**
- Maximum 5 question answers per 15-minute check
- If more than 5 unanswered questions, prioritize:
  1. Questions directly about AI/your expertise
  2. Questions from members who engaged with your posts
  3. Most recent questions first

**POV Responses (Engaging):**
- Maximum 3 POV responses per 15-minute check
- Prioritize:
  1. Posts about topics you have unique insight on
  2. Posts from active community members
  3. Posts that would benefit from a different perspective
- Skip if conversation already has 5+ replies

**General:**
- Wait 2-3 seconds between each message
- Don't respond to same member twice in one cycle
- Total max responses per cycle: 8 (5 answers + 3 POV)

### Edge Cases

**Message is a reply chain:**
- Only respond to the original question if unanswered
- Don't jump into ongoing conversations unless directly relevant

**Question is too vague:**
- Ask a clarifying question instead of guessing
- Example: "Could you share more about your use case? Happy to point you in the right direction."

**Question is off-topic (not AI-related):**
- Skip. Don't respond to non-AI questions.

**Member asks for 1-on-1 help:**
- Respond publicly with general guidance
- If they need more, suggest: "Feel free to DM me for specifics!"

### Automation Setup (Windows Task Scheduler)

#### News Posting Automation (10 AM & 8 PM, Weekdays)

**Script:** `scripts/post-ai-news.ps1`
**Task Name:** `AI-Ignite-News-Poster`
**Schedule:** 10:00 AM and 8:00 PM {{CLIENT_TIMEZONE}}, Monday-Friday only

To set up, run:
```powershell
powershell -ExecutionPolicy Bypass -File "{{CLIENT_WORKSPACE_ROOT}}\whatsapp-community-ai\scripts\setup-news-scheduler.ps1"
```

Task management:
```powershell
# Verify task
Get-ScheduledTask -TaskName 'AI-Ignite-News-Poster'

# Disable task
Disable-ScheduledTask -TaskName 'AI-Ignite-News-Poster'

# Remove task
Unregister-ScheduledTask -TaskName 'AI-Ignite-News-Poster'
```

#### Monitoring Automation (Every 15 mins)

**Note:** Codex CLI requires an interactive terminal, so Windows Task Scheduler won't work. Use the continuous loop script instead.

**Option 1: Continuous Loop (Recommended)**

Keep a terminal window open that monitors every 15 minutes:

```powershell
# Double-click to start:
{{CLIENT_WORKSPACE_ROOT}}\whatsapp-community-ai\scripts\start-monitor.bat

# Or run directly:
powershell -ExecutionPolicy Bypass -File "{{CLIENT_WORKSPACE_ROOT}}\whatsapp-community-ai\scripts\monitor-loop.ps1"
```

Features:
- Runs every 15 minutes while terminal is open
- Active hours: 7 AM - 11 PM {{CLIENT_TIMEZONE}} (sleeps outside)
- Press Ctrl+C to stop
- Shows cycle count and next run time

**Option 2: Manual Checks**

Run monitoring manually anytime:
```
claude "monitor ai ignite"
```

**Scripts Location:**
```
scripts/
├── start-monitor.bat      # Double-click to start loop
├── monitor-loop.ps1       # Continuous 15-min loop
└── monitor-ai-ignite.ps1  # Single run (for manual use)
```

### Manual Override

User can always:
- Say "stop monitoring" to pause auto-replies
- Say "skip this question" to ignore specific messages
- Say "check ai ignite" to run an immediate scan
