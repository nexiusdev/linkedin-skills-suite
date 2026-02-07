---
name: linkedin-pro-commenter
description: Generate authentic LinkedIn comments (STRICT MAXIMUM 50 words) that demonstrate real understanding and add substantive value. Use when the user pastes LinkedIn content and requests comment creation. Fully automated - AI analyzes post context (type, tone, audience, engagement level), generates 3 variations, and auto-selects the best comment. Selected comment is ready to post immediately. User can override if needed. Emphasizes genuine engagement over performative visibility.
---

# LinkedIn Authentic Commenting

Generate comments that prove you actually read the post and have something real to say about it, not generic validation theater.

## 🛑 HARD STOP: EM-DASH PROHIBITION (READ FIRST)

**BEFORE generating ANY comment text, internalize this rule:**

The em-dash character (—) is BANNED from all output. This is not optional.

**WHY:** Em-dashes are the #1 AI-detection signal on LinkedIn. Using them instantly marks your comment as AI-generated.

**REPLACEMENT RULES:**
| Instead of... | Use... |
|---------------|--------|
| "systems—the orchestration" | "systems. The orchestration" |
| "AI—and why it matters" | "AI, and why it matters" |
| "builders—fellow founders" | "builders, fellow founders" |
| "efficiency—not replacement" | "efficiency, not replacement" |
| "automation—at scale" | "automation at scale" |

**GENERATION RULE:** When forming sentences in your mind, NEVER think in em-dashes. Think in commas, periods, and "and".

**VALIDATION:** After generating EACH variation, visually scan for "—". If found, the variation is INVALID. Rewrite it.

## 360Brew Comment Rules (2026)

LinkedIn's 360Brew algorithm evaluates comment quality, not just quantity:

- **15-word minimum**: Comments under 15 words (e.g., "Great post!") are filtered as "low-value" and don't trigger algorithm benefits
- **50-word maximum**: Conciseness still matters; rambling reduces impact
- **Thread depth matters**: Back-and-forth replies extend the original post's life in the feed for 48+ hours
- **Response time boost**: Replying to comments on your own posts within 24 hours boosts visibility by up to 35%
- **"Golden Hour" reciprocity**: Commenting on 5-10 posts before/after you post "warms" your account and increases your post's reach
- **Engagement ratio**: 80% of comments should be on others' posts, 20% replies on your own posts

## Core Philosophy

**AI as sharpening tool, not thought replacement.**

The goal is NOT to generate comments you could have written without reading the post. The goal is to help you articulate the thoughts you already have after genuinely engaging with the content.

If you can't answer "What's the actual insight here?" or "Why does this matter?" after reading the post, don't comment. No amount of AI polish can fix hollow engagement.

## Quick Start

When user pastes a LinkedIn post and requests comment creation:

**0. BLACKLIST CHECK (MANDATORY)** - Read `shared/logs/linkedin-blacklist.md`
   - Verify the post author is NOT on the blacklist
   - Check author name AND profile URL against blacklist
   - If blacklisted → STOP immediately, do NOT generate comment, inform user
   - This check applies BEFORE any comment generation

**CRITICAL: NEVER USE EM-DASHES (—) IN COMMENTS**
   - Em-dashes are a strong AI-generated signal
   - Use commas, periods, or rewrite the sentence instead
   - Final validation: Search comment for "—" before posting
   - If em-dash found → Rewrite that sentence immediately

1. **Actually understand the post** - What's the core argument? What's the insight? What's being overlooked?
2. **Identify your genuine response** - Agreement, disagreement, extension, question, challenge?
3. **Generate 2-3 articulation variations** - Different ways to express that genuine response, each STRICTLY under 50 words, NO EM-DASHES
4. **Verify authenticity** - Could this comment only be written by someone who read and understood the post?
5. **FINAL EM-DASH CHECK** - Scan selected comment for "—" character before posting. If found, replace with comma or period.

## Authenticity Framework

### The "Did I Actually Read This?" Test

Before generating ANY comment, answer these questions:

**Content Understanding:**
- What's the specific insight or argument the author is making?
- What evidence or examples do they provide?
- What assumptions underlie their position?

**Your Genuine Response:**
- Do I agree, disagree, or partially agree? Why specifically?
- What does this remind me of from hands-on experience building these systems?
- What's being overlooked or could be challenged?
- What question does this raise that's worth exploring?

**The Litmus Test:**
Could someone write this exact comment without reading the post? If yes → it's performative garbage, start over.

### Engagement Modes (Based on Real Thought, Not Strategy)

Generate comments that reflect actual intellectual engagement:

**1. Extension/Building** - "Yes, and here's what this connects to..."
- Takes the author's point and extends it with specific insight
- Adds a dimension they didn't explore
- Shows you understood AND had a related thought

**2. Challenge/Reframe** - "I see it differently because..."
- Respectfully pushes back with concrete reasoning
- Offers alternative perspective from real experience
- Shows you engaged critically with the argument

**3. Question/Probe** - "This raises an interesting question about..."
- Identifies a tension or unexplored implication
- Asks something that shows deep reading
- Creates dialogue, not just reaction

**4. Pattern Recognition** - "This matches what I'm seeing where..."
- Connects to specific deployment experience
- Validates with concrete parallel example
- Shows you're actively thinking across contexts

## Comment Articulation (Not Generation)

You're not generating comments from scratch. You're helping articulate thoughts that come from actually reading the post.

### The Process

1. **Read the post completely** - Not skimming for keywords, actually understanding the argument
2. **Form your own response** - What do you actually think about this?
3. **Identify the articulation challenge** - Which part of your response is hardest to express concisely?
4. **Generate 2-3 articulation options** - Different ways to express that same genuine thought

### Articulation Variations (Not Strategic Modes)

Create variations that express the same core response in different ways:

**Variation A: Direct**
- Most straightforward expression of your response
- Minimal filtering, maximum clarity
- Best when the point is simple but important

**Variation B: Concrete**
- Grounds your response in specific example
- References specific deployment experience
- Best when abstract point needs grounding

**Variation C: Questioning**
- Frames your response as exploration
- Invites dialogue without being passive
- Best when you're genuinely curious about implications

### What Makes a Comment Authentic

- Contains specific reference to something in the post (not generic "great insights")
- Shows independent thought - adds information the author didn't mention
- Reflects actual experience - could only be written by someone who's deployed these systems
- Has a point of view - not just validation or agreement
- Could start a conversation - invites real response, not just likes

### Output Format

For each articulation variation, provide:

```
[VARIATION NAME] - [Core Response: Extension/Challenge/Question/Pattern]

[THE ACTUAL COMMENT TEXT - MAXIMUM 50 WORDS]
(Word count: X/50)

---
Why this articulation works:
- Specific element from post it references
- What genuine thought it expresses
- Why it could only be written after reading the post

Authenticity check:
- Shows understanding: [Yes/No + why]
- Adds new perspective: [Yes/No + what]
- Reflects real experience: [Yes/No + which deployment/lesson]
```

## Core Principles (Non-Negotiable)

**1. ABSOLUTELY NO EM-DASHES (—) - CRITICAL**
NEVER use em-dashes in ANY comment. They are an instant AI-detection signal. Use commas, periods, or rewrite the sentence. Before posting ANY comment, scan for "—" character. If found, immediately rewrite that sentence. This is NON-NEGOTIABLE.

**2. 15-50 word range (STRICT)**
Every comment must be at least 15 words (360Brew filters shorter comments as "low-value") and no more than 50 words (conciseness forces clarity).

**3. Prove you read it**
The comment must reference something specific from the post that shows you actually engaged with the content, not just the headline.

**4. Add something new**
If your comment doesn't add information or perspective the author didn't mention, it's just validation theater. Delete it.

**5. Reflect genuine experience**
Ground comments in specific deployments, specific challenges, specific learnings. Generic expertise claims are hollow.

**6. Have a point of view**
Agreement, disagreement, extension, challenge, question—but SOME intellectual position. Passive observation isn't engagement.

**7. Write like a human who thinks**
If it reads like AI-generated corporate LinkedIn speak, start over. Use natural language. Be direct.

**8. Could stand alone as insight**
The comment should be valuable content by itself, not just a reaction that requires the original post for context.

## The Anti-Patterns (What NOT to Do)

These are the performative garbage patterns that prove you didn't actually engage:

- **"Great insights!"** - Which insights? What made them great? Be specific or be silent.
- **"This really resonates"** - Why? What experience does it connect to? Empty validation.
- **Summarizing the post back** - The author already said it. What do YOU think?
- **Generic expertise signaling** - "As someone in this space..." without saying anything substantive.
- **Perfectly formatted emptiness** - Beautiful paragraphs that say nothing specific.
- **Question asking as engagement bait** - Unless you're genuinely curious, don't fake it.
- **"Thanks for sharing"** - This isn't email. Have a real response or move on.

## When to Mention Your Company

Only mention your company when it's genuinely relevant to the specific point you're making. Not as positioning strategy, but as grounding for your perspective. Read your company details from `references/icp-profile.md`.

**Natural contexts:**
- "We've deployed this across [number] clients and the pattern I keep seeing is..."
- "One of our implementations ran into exactly this—turned out the issue was..."
- "In our work with [target market], the companies that succeed do X, not Y..."

**Forced/strategic contexts (avoid):**
- "At [Company], we help companies with this" - Sales pitch, not thought
- "This is why we built our platform around..." - Not about the post
- "We've seen this across many deployments" - Generic credential drop

**The test:** Would removing the company name make the comment weaker? If not, remove it. If yes, it's probably genuine context.

## Tone Calibration

Match the post's energy and audience, but always maintain authenticity:

**Startup/Founder Posts:**
- Direct, action-oriented
- Share specific wins and failures
- Less polish, more honesty

**Enterprise/Corporate Posts:**
- Professional but not stiff
- Reference frameworks and patterns
- Back assertions with specific data

**Technical/Developer Posts:**
- Implementation details matter
- Show the actual code/architecture decisions
- Respect technical precision

**SME/Small Business Posts:**
- Cut the buzzwords
- Practical, immediate value
- Acknowledge resource constraints

## Reference Files

Load these as needed for deeper guidance:

- **references/selection-guide.md** - Detailed selection heuristics, decision tree, and examples for choosing best variation
- **references/strategy-guide.md** - Core LinkedIn engagement strategy and principles
- **references/comment-patterns.md** - 7 proven comment patterns with examples
- **references/icp-profile.md** - Your business positioning, expertise areas, and target market

## Automatic AI Selection of Best Variation

After generating 3 comment variations, AI automatically analyzes the post context and selects the optimal comment. The recommended comment is presented first with explicit reasoning, followed by two alternatives for edge cases where user judgment may differ.

### Selection Framework

**1. Analyze Post Context**

Before selecting, evaluate:
- **Post Type**: Thought leadership, case study, announcement, controversy, question, celebration
- **Author Persona**: Founder/CEO, practitioner, educator, influencer, newcomer
- **Engagement Level**: High engagement (100+ comments) vs. emerging conversation
- **Tone**: Technical, inspirational, controversial, educational, celebratory
- **Audience**: Founders, technical audience, general business, specific industry

**2. Match Variation to Context**

Select based on these heuristics:

**THOUGHT LEADERSHIP POSTS** (author sharing frameworks, insights, principles)
→ **SELECT: Extension/Building**
- Best: Variations that add a complementary dimension or practical application
- Why: Shows you engaged deeply and can extend their thinking
- Avoid: Simple agreement or questions that don't add new dimension

**CASE STUDY/RESULTS POSTS** (specific wins, metrics, implementations)
→ **SELECT: Pattern Recognition**
- Best: Variations that connect to your parallel experience with specific examples
- Why: Validates their results while adding comparative data point
- Avoid: Generic congratulations or asking obvious questions

**CONTROVERSIAL/PROVOCATIVE POSTS** (challenging status quo, hot takes)
→ **SELECT: Challenge/Reframe**
- Best: Variations that respectfully offer counterpoint with concrete reasoning
- Why: Adds intellectual value to debate, shows independent thinking
- Avoid: Piling on agreement or dismissive disagreement

**QUESTION POSTS** (seeking input, genuine inquiry)
→ **SELECT: Concrete/Direct**
- Best: Variations that answer directly with specific example from deployments
- Why: Provides immediate practical value they're explicitly seeking
- Avoid: Asking more questions or abstract responses

**ANNOUNCEMENT POSTS** (product launches, career moves, company news)
→ **SELECT: Pattern Recognition or Direct**
- Best: Variations that connect to how this impacts the space based on your experience
- Why: Adds perspective beyond congratulations, shows strategic thinking
- Avoid: Pure celebration without added insight

**TECHNICAL IMPLEMENTATION POSTS** (architecture, code, system design)
→ **SELECT: Concrete**
- Best: Variations that reference specific deployment experience or technical nuance
- Why: Demonstrates actual implementation knowledge, not just theory
- Avoid: Generic validation or questions that reveal surface-level understanding

**HIGH ENGAGEMENT POSTS** (already 50+ substantive comments)
→ **SELECT: Challenge/Question**
- Best: Variations that introduce unexplored angle or productive tension
- Why: Adds new dimension to saturated conversation
- Avoid: Repeating points already made in comments

**3. Selection Decision Matrix**

When multiple variations could work, prioritize in this order:

1. **Uniqueness**: Will this comment add something not yet said in the discussion?
2. **Grounding**: Does it reference specific deployment/experience vs. generic expertise?
3. **Reciprocity**: Does it invite meaningful follow-up conversation?
4. **Authenticity**: Could it ONLY be written by someone with real implementation experience?

**4. Final Verification**

Before presenting selection, confirm:
- Selected variation is ≤50 words
- Selection reasoning is explicitly tied to post analysis
- Alternative variations offer meaningfully different approaches
- All variations pass authenticity checks

### Output Format for Autonomous Mode

**In AUTONOMOUS mode (default):**
- Generate 3 variations internally
- Auto-select best variation based on post context
- IMMEDIATELY post the selected comment using browser automation
- DO NOT present alternatives or wait for confirmation

**Internal decision-making only** - alternatives are evaluated but not shown to user.

The skill should:
1. Generate comment variations silently
2. Select best one
3. Post it immediately
4. Only then show what was posted in the completion report

## Workflow (FULLY AUTONOMOUS)

1. **BLACKLIST CHECK** - Verify author is not on blacklist (MANDATORY first step)
2. **Post Analysis** - Automatically identify post type, author persona, tone, audience, engagement level
3. **Deep read** - What's the actual argument? What's the insight? What's being missed?
4. **Genuine response formation** - What would be the authentic intellectual response after reading this?
5. **Generate 3 articulation variations** - Create 3 distinct ways to express that response
6. **AI auto-selects best variation** - Uses selection framework to identify optimal comment for post context
7. **IMMEDIATELY POST THE SELECTED COMMENT** - Use browser automation to post without asking
8. **Log to shared activity log** - Update activity log with comment details

**CRITICAL: This is FULLY AUTONOMOUS mode.**
- DO NOT ask user to confirm before posting
- DO NOT wait for user approval
- DO NOT present alternatives and wait for selection
- Auto-select best variation and IMMEDIATELY post it using browser automation
- Comment field should already be open when this skill is invoked
- Just fill the text and click Post button immediately

**Autonomous Flow:**
```
Blacklist Check → Generate 3 variations (NO EM-DASHES) → Auto-select best → FINAL EM-DASH SCAN → Fill comment field → Click Post → Log → Report completion
```

**Mandatory pre-posting check:**
- Scan selected comment for "—" character
- If found → Replace with comma/period and regenerate
- Only post after confirming zero em-dashes

**No user interaction required.** The skill executes end-to-end autonomously.

## Quality Checklist

Before delivering any comment, verify:

**Authenticity:**
- References something specific from the post (not just topic)
- Could only be written by someone who actually read it
- Expresses a genuine intellectual response (not performative agreement)
- Reflects real experience from deployments, not generic expertise

**Substance:**
- Adds new information or perspective the author didn't mention
- Has a clear point of view (agreement, challenge, extension, question)
- Grounds assertions in specific examples or data
- Could stand alone as valuable micro-content

**Technical:**
- **NO EM-DASHES (—) - MANDATORY CHECK** - Scan comment for "—" before posting. If found, immediately rewrite. Use commas or periods instead. Em-dashes = AI-detection signal.
- **15-50 word range** - Minimum 15 words (algorithm requirement), maximum 50 words
- Reads like natural human thought, not AI corporate speak
- Written for entire audience, not just author
- Company mention (if any) is genuinely relevant, not strategic positioning
- Ask a question to encourage thread depth (extends post reach 48+ hours)

## Grounding Your Comments in Real Experience

Your hands-on production experience gives you something most LinkedIn commenters don't have: actual pattern recognition from real implementations.

**Use specific deployment learnings:**
- "When we automated accounts payable for a 50-person firm, the adoption pattern was..."
- "Three of our ERP implementations failed at the same point: when we tried to..."
- "The companies where AI agents actually work share one thing: they..."

**Reference concrete metrics:**
- "12%→94% adoption" (actual improvement from your deployments)
- "3.7x ROI" (measured impact)
- "Reduced close time from 2 weeks to 3 days" (specific outcome)

**Acknowledge what doesn't work:**
- "We tried this approach in 5 implementations—it sounds good but breaks when..."
- "The theory is elegant. In practice, the error handling is a nightmare because..."
- "This assumes clean data. Real ERP migrations are 60% data archaeology."

The most valuable comments come from actually doing the work, not from having opinions about the work.

## Daily Commenting Strategy (360Brew Optimized)

**Reference:** See `references/contact-classification.md` for full classification criteria.

**The 3-3-3 Rule (Minimum):**
- 3 comments on **PEER** posts (1K-10K followers, fellow builders in AI/automation)
- 3 comments on **PROSPECT** posts (potential ICP, decision-makers at SMEs)
- 3 comments on **THOUGHT LEADER** posts (10K+ followers, visibility boost)

**Growth Baseline:** 5-15 high-quality comments/day

### Contact-Type Comment Strategies

**STRICT: No em-dashes (—) in ANY comments.** Use commas or periods instead.

**PEER (1K-10K followers, same niche):**
- Tone: Collaborative, collegial, "we're in this together"
- Strategy: Share complementary insights, extend their thinking
- Goal: Build relationship, potential collaboration, mutual support
- Patterns to use: Extension/Building, Pattern Recognition
- Example: "We hit the same wall with [X]. What worked for us was [Y]. Curious if you've tried [Z]?"

**THOUGHT LEADER (10K+ followers):**
- Tone: Respectful but confident, add unique POV
- Strategy: Stand out from generic comments, ask thoughtful questions
- Goal: Visibility boost, get noticed, credibility by association
- Patterns to use: Challenge/Reframe, Question/Probe
- Example: "Interesting framing. In production, I've seen [counter-pattern]. Is that an edge case or am I missing something?"

**PROSPECT (ICP match, any follower count):**
- Tone: Empathetic, demonstrate expertise without pitching
- Strategy: Mirror their pain, add insight, low-friction question
- Goal: Plant seeds, establish credibility for future connection
- Patterns to use: Empathy + Reframe, Validation + Insight
- Example: "That [pain point] resonates. Most teams I work with find the bottleneck isn't [obvious thing]. It's [underlying cause]. What's your current workaround?"

**The 15/15 Rule:**
- 15 minutes engaging before you post your content
- 15 minutes engaging after you post
- This "warms" your topical relevance for 4 hours of distribution

**Avoid Shadow-Ban Triggers:**
- Don't post 30+ short comments/day (interpreted as automation)
- Don't "Post and Ghost" (posting without engaging with others is penalized)
- Don't use "Comment YES" tactics (downranked in 2026)

## When NOT to Comment

Sometimes the best engagement is no engagement:

**Skip if:**
- You didn't actually read the post completely
- You don't have a genuine response beyond agreement
- The post is outside your domain and you'd be guessing
- You'd be commenting just for visibility/positioning
- Your only contribution would be generic validation
- The conversation is fully explored and you'd be repeating points

**Remember:** Every comment is a micro-representation of your thinking. A few thoughtful comments > many performative ones.

## Browser Automation Workflow

**Browser automation uses Claude for Chrome if available, otherwise falls back to Chrome DevTools. See linkedin-daily-planner skill for detailed tool mapping.**

When using browser automation to post comments or replies on LinkedIn:

### Critical Steps (DO NOT SKIP):

**When Commenting on a Post:**
1. Navigate to the LinkedIn post URL
2. **LIKE the post** (click the "Like" button/reaction)
3. Click into the comment text field
4. Type the comment
5. **CLICK THE "Post" OR "COMMENT" BUTTON** to submit (DO NOT just type and leave)
6. Wait for confirmation that comment posted successfully

**When Replying to a Comment:**
1. Navigate to the LinkedIn post with the comment
2. Find the specific comment to reply to
3. **LIKE the comment** (click the like icon on the comment)
4. Click "Reply" on that comment
5. Type the reply text in the reply field
6. **CLICK THE "Reply" OR "POST" BUTTON** to submit (DO NOT just type and leave)
7. Wait for confirmation that reply posted successfully

### Common Mistakes to Avoid:
- ❌ Typing comment/reply but NOT clicking the Post/Reply button
- ❌ Forgetting to like the post before/after commenting
- ❌ Forgetting to like the comment before/after replying
- ❌ Not waiting for confirmation before moving to next task

### Automation Checklist:
```
FOR EACH COMMENT:
[ ] Navigate to post URL
[ ] Like the post
[ ] Click comment field
[ ] Type comment text
[ ] Click "Post" button ← CRITICAL
[ ] Confirm comment appeared
[ ] Log to shared activity log

FOR EACH REPLY:
[ ] Navigate to post URL
[ ] Find the comment to reply to
[ ] Like the comment
[ ] Click "Reply" on that comment
[ ] Type reply text in reply field
[ ] Click "Reply" button ← CRITICAL
[ ] Confirm reply appeared
[ ] Log to shared activity log
```

## Shared Activity Log (Token Optimization)

**ALWAYS read from the shared log first before generating comments.**

**Log location:** `shared/logs/linkedin-activity.md`

### On Each Run:
1. **Read shared log first** to check:
   - Today's comment count (target: 9-15 per day)
   - Which authors you've already engaged with today
   - Contact classification context (Peer/Thought Leader/Prospect)
2. **After generating and posting comment**, update shared log:
   - Add to "Comments Made" table with time, author, topic, preview
   - Note any high-value interactions for follow-up

### What to Log:
```
| HH:MM | Author Name | Profile URL | Post URL | Post Topic (brief) | Comment preview (10 words) | Impressions |
```
**Always capture URLs** for quick navigation later.

### Read from Log Instead of LinkedIn:
- Check "High-Value Interactions" before deciding who to engage
- Check "Prospect Pipeline" for warming engagement context
- Check "Feed Insights Cache" for trending topics to reference
