# LinkedIn Autonomous Workflow Optimization

**Last Updated:** 30 Jan 2026

This document defines enhanced auto-selection logic and fail-safe mechanisms for fully autonomous LinkedIn workflow execution.

## Core Principle

**ZERO USER INTERACTION REQUIRED**
- No questions asked during execution
- AI makes all decisions based on documented criteria
- Graceful degradation when optimal data unavailable
- Always complete the workflow, never block

---

## Auto-Selection Logic by Component

### 1. Trending Topic Selection (linkedin-trender)

**Decision Criteria (Weighted):**
| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| Cross-platform potential | 30% | Works well on Instagram/LinkedIn/X |
| Narrative strength | 25% | Clear story arc, emotional hook |
| Timeliness | 20% | Breaking news or anniversary timing |
| Visual potential | 15% | Can be visualized effectively |
| Positioning alignment | 10% | Relevance to Agentic AI for SMEs |

**Selection Algorithm:**
```
FOR each trending topic:
  score = 0

  # Cross-platform potential (30%)
  IF topic has visual elements OR tutorial potential:
    score += 30
  ELSE IF topic is abstract/philosophical:
    score += 15

  # Narrative strength (25%)
  IF topic has clear problem → solution arc:
    score += 25
  ELSE IF topic has emotional hook (shock/surprise/inspiration):
    score += 20
  ELSE:
    score += 10

  # Timeliness (20%)
  IF topic is breaking news (<24h old):
    score += 20
  ELSE IF topic is timeless evergreen:
    score += 15
  ELSE:
    score += 5

  # Visual potential (15%)
  IF topic can be diagram/schema/screenshot:
    score += 15
  ELSE IF topic needs only text:
    score += 5

  # Positioning alignment (10%)
  IF topic mentions AI/automation/ERP/CRM/SME:
    score += 10
  ELSE IF topic is tangentially related:
    score += 5

SELECT topic with highest score
```

**Fail-Safe:**
- If no topics score >60 → Use backup evergreen topic: "3 signs your SME needs agentic automation"
- If trending API fails → Generate post from recent saved topics (linkedin-activity.md)

---

### 2. Post Variation Selection (linkedin-elite-post)

**Decision Criteria (Weighted):**
| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| Hook strength | 35% | First 2 lines grab attention |
| Value density | 25% | Insight-to-word ratio |
| Engagement triggers | 20% | Questions, lists, bold formatting |
| Call-to-action clarity | 15% | Clear next step |
| Brevity | 5% | <300 words preferred |

**Selection Algorithm:**
```
FOR each post variation:
  score = 0

  # Hook strength (35%)
  hook_words = first_two_lines.split()
  IF contains_question(hook) OR contains_number(hook):
    score += 35
  ELSE IF starts_with_bold_statement(hook):
    score += 25
  ELSE:
    score += 15

  # Value density (25%)
  insights = count_actionable_items(post)
  word_count = len(post.split())
  density = insights / word_count * 100
  IF density > 0.03:  # 3+ insights per 100 words
    score += 25
  ELSE IF density > 0.02:
    score += 15
  ELSE:
    score += 5

  # Engagement triggers (20%)
  triggers = 0
  IF has_question: triggers += 1
  IF has_numbered_list: triggers += 1
  IF has_bold_text: triggers += 1
  IF has_line_breaks_for_readability: triggers += 1
  score += triggers * 5

  # CTA clarity (15%)
  IF has_explicit_cta ("Comment", "Share", "DM me"):
    score += 15
  ELSE IF has_implicit_cta ("What's your experience?"):
    score += 10
  ELSE:
    score += 0

  # Brevity (5%)
  IF word_count < 250:
    score += 5
  ELSE IF word_count < 350:
    score += 3

SELECT variation with highest score
```

**Fail-Safe:**
- If all variations score <50 → Regenerate with "make more concise and actionable" prompt
- If regeneration fails → Use variation 1 (thought leadership mode default)

---

### 3. Comment Selection (linkedin-pro-commenter)

**Decision Criteria (Weighted):**
| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| Substantive value | 40% | Adds insight, not just praise |
| Brevity | 25% | 15-50 words (40-45 optimal) |
| Question quality | 20% | Thoughtful, not generic |
| Authenticity | 15% | Natural tone, no buzzwords |

**Selection Algorithm:**
```
FOR each comment variation:
  score = 0

  # Substantive value (40%)
  IF adds_new_perspective OR shares_specific_example:
    score += 40
  ELSE IF asks_thoughtful_question:
    score += 30
  ELSE IF shows_genuine_understanding:
    score += 20
  ELSE:  # Generic praise
    score += 5

  # Brevity (25%)
  word_count = len(comment.split())
  IF 40 <= word_count <= 45:
    score += 25  # Optimal length
  ELSE IF 35 <= word_count < 40 OR 45 < word_count <= 50:
    score += 20  # Good length
  ELSE IF 15 <= word_count < 35:
    score += 10  # Too short
  ELSE:
    score += 0   # Too long (>50) or way too short (<15)

  # Question quality (20%)
  IF has_question:
    IF question_is_specific_to_post:
      score += 20
    ELSE IF question_is_generic:
      score += 5
  ELSE:
    score += 10  # Not having question is okay

  # Authenticity (15%)
  buzzwords = count_buzzwords(comment)  # "synergy", "leverage", "circle back"
  IF buzzwords == 0:
    score += 15
  ELSE IF buzzwords == 1:
    score += 5
  ELSE:
    score += 0

SELECT comment with highest score
```

**Fail-Safe:**
- If all comments score <40 → Regenerate with "make more specific and concise" prompt
- If regeneration fails → Use comment with highest brevity score

---

### 4. Prospect Engagement Priority (linkedin-icp-warmer)

**Decision Criteria (Weighted):**
| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| Touch count | 40% | 2 touches > 1 touch > 0 touches |
| Last engagement age | 30% | Older = higher priority |
| ICP fit strength | 20% | Score from icp-prospects.md |
| Post freshness | 10% | Recent posts preferred |

**Selection Algorithm:**
```
FOR each prospect:
  score = 0

  # Touch count (40%) - Prioritize near-ready
  IF touches == 2:
    score += 40  # One more touch = ready to connect
  ELSE IF touches == 1:
    score += 30
  ELSE:  # touches == 0
    score += 20

  # Last engagement age (30%)
  days_since_last_touch = (today - last_touch_date).days
  IF days_since_last_touch >= 7:
    score += 30  # Definitely ready for re-engagement
  ELSE IF days_since_last_touch >= 3:
    score += 20  # Ready for re-engagement
  ELSE:
    score += 0   # Too recent, skip

  # ICP fit strength (20%)
  IF icp_score >= 80:
    score += 20  # Hot prospect
  ELSE IF icp_score >= 60:
    score += 15  # Warm prospect
  ELSE:
    score += 5

  # Post freshness (10%)
  IF has_post_from_last_24h:
    score += 10
  ELSE IF has_post_from_last_7d:
    score += 5

SORT prospects by score DESC
ENGAGE with top N prospects (respecting daily limits)
```

**Fail-Safe:**
- If no prospects score >40 → Run linkedin-icp-finder to discover new prospects
- If icp-finder returns empty → Engage with Peers/Thought Leaders instead

---

### 5. ICP Classification (linkedin-icp-finder)

**Auto-Classification Logic:**
```
# Step 1: Location Check
IF location in [target countries from references/icp-profile.md]:
  geographic_match = TRUE
ELSE:
  SKIP - Not target geography

# Step 2: Role Check
roles = ["CEO", "Founder", "COO", "CFO", "CTO", "Director", "Head of", "VP"]
IF role contains any(roles):
  decision_maker = TRUE
ELSE:
  decision_maker = FALSE

# Step 3: Company Size Check
IF company_size between 10-500 employees:
  sme_size = TRUE
ELSE:
  sme_size = FALSE

# Classification Decision Tree
IF geographic_match AND decision_maker AND sme_size:
  classification = "PROSPECT"
  icp_score = 80 + role_strength_bonus + industry_fit_bonus

ELSE IF followers >= 10000:
  classification = "THOUGHT LEADER"

ELSE IF followers between 1000-10000 AND same_niche:
  classification = "PEER"

ELSE:
  classification = "NON-ICP"
  action = SKIP
```

**Fail-Safe:**
- If profile data incomplete → Classify as NON-ICP, skip
- If API rate limit hit → Cache for next run, don't block workflow

---

## Fail-Safe Mechanisms

### 1. Browser Automation Failures

**Scenario:** LinkedIn page doesn't load, element not found, etc.

**Response:**
```
TRY:
  Navigate to LinkedIn
EXCEPT timeout/error:
  WAIT 10 seconds
  RETRY once
  IF still fails:
    LOG error to linkedin-activity.md
    SKIP this task
    CONTINUE with next task
```

**Never block the entire workflow due to one task failure.**

---

### 2. Daily Limit Reached

**Scenario:** Comments = 30/30, cannot comment more

**Response:**
```
IF comments_today >= 30:
  LOG "Comment limit reached" to activity log
  SKIP remaining comment tasks
  MOVE to next task type (connections, DMs, etc.)

IF connections_today >= 15:
  SKIP connection requests
  CONTINUE with other tasks
```

---

### 3. No Content to Work With

**Scenario:** No trending topics found, no prospects to engage

**Response:**
```
IF linkedin-trender returns empty:
  USE backup evergreen topics from references/evergreen-topics.md

IF linkedin-icp-warmer returns no prospects:
  ENGAGE with Peers/Thought Leaders instead (maintain visibility)

IF linkedin-post-finder returns no posts:
  USE saved high-quality posts from previous runs
```

---

### 4. API/Tool Failures

**Scenario:** yfinance down, Telegram API error, etc.

**Response:**
```
FOR each API call:
  TRY:
    result = api_call()
  EXCEPT:
    LOG error
    IF critical (blocks workflow):
      USE cached data from previous run
    ELSE:
      SKIP this specific item
      CONTINUE with next item
```

---

## Autonomous Execution Checklist

Before starting autonomous workflow, verify:

- [ ] Account config read (`shared/linkedin-account-config.md`)
- [ ] Daily limits status checked (`shared/logs/linkedin-activity.md`)
- [ ] Profile cache available (`shared/logs/icp-prospects.md`)
- [ ] Blacklist checked (`shared/logs/linkedin-blacklist.md`)
- [ ] Browser automation ready (Chrome DevTools MCP)

During execution, never:

- [ ] ❌ Ask user which variation to use
- [ ] ❌ Ask user which prospect to engage
- [ ] ❌ Ask user to confirm actions
- [ ] ❌ Wait for user input mid-workflow
- [ ] ❌ Block on single task failure

Always:

- [ ] ✅ Auto-select best options using scoring algorithms
- [ ] ✅ Skip blocked tasks, continue workflow
- [ ] ✅ Log all decisions to activity log
- [ ] ✅ Report summary at end (not during)
- [ ] ✅ Complete the workflow, no matter what

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Autonomous completion rate | >95% (completes without questions) |
| Average execution time | <25 minutes per block |
| Decision accuracy | >80% (auto-selected = user would select) |
| Graceful degradation | 100% (never crashes, always completes) |

---

## Emergency Stop

**Only stop the workflow if:**
1. LinkedIn account shows "restricted" warning
2. Temporary action block detected (24-72h ban)
3. User explicitly cancels (Ctrl+C)

**Otherwise, always complete the workflow.**
