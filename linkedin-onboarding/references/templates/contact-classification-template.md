# LinkedIn Contact Classification

Framework for classifying LinkedIn contacts into three categories for targeted engagement strategy.

## Classification Criteria

### Peer (Fellow Builders)
**Follower Range:** 1K - 10K

**Identifying Signals:**
{{PEER_SIGNALS}}

**Profile Keywords:**
{{PEER_KEYWORDS}}

**Examples:**
{{PEER_EXAMPLES}}

---

### Thought Leader (Industry Authority)
**Follower Range:** 10K+

**Identifying Signals:**
- Established authority in {{DOMAIN}}/tech/business
- High engagement on posts (100+ reactions typical)
- LinkedIn Top Voice badge
- Published author, speaker, or recognized expert
- Content gets wide distribution
- Often quoted or referenced by others

**Profile Keywords:**
- Top Voice, Creator, Influencer
- Author, Speaker, Advisor
- "Followed by X people"
- VP, Director, C-level at major companies
- "Featured in...", "As seen in..."

**Examples:**
{{THOUGHT_LEADER_EXAMPLES}}

---

### Prospect (ICP - Ideal Customer Profile)
**Follower Range:** Any (role-based, not follower-based)

**Identifying Signals:**
- Decision-maker or budget holder
- Works at {{TARGET_COMPANY_TYPE}}
- Pain points align with {{SOLUTION_AREA}}
- Industry: {{TARGET_INDUSTRIES}}
- Shows interest in {{INTEREST_SIGNALS}}

**Target Roles:**
{{TARGET_ROLES}}

**Target Industries:**
{{TARGET_INDUSTRIES_LIST}}

**Pain Point Signals in Content:**
{{PAIN_SIGNALS}}

**Geographic Focus:** {{GEOGRAPHY}}

---

## Quick Classification Flowchart

```
START: New LinkedIn Profile
         |
         v
+-----------------------------+
| Is this person a potential  |
| CUSTOMER for {{SOLUTION}}?  |
| ({{TARGET_COMPANY_TYPE}}    |
|  decision-maker with        |
|  operational pain points)   |
+-----------------------------+
         |
    YES  |  NO
         v
   +-----+-----+
   |           |
   v           v
PROSPECT   Check Followers
              |
              v
      +---------------+
      | 10K+ followers |
      +---------------+
              |
         YES  |  NO
              v
        +-----+-----+
        |           |
        v           v
   THOUGHT      +---------------+
   LEADER       | 1K-10K + same |
                | niche/builder |
                +---------------+
                      |
                 YES  |  NO
                      v
                +-----+-----+
                |           |
                v           v
              PEER      GENERAL
                        (lower priority)
```

---

## Engagement Priority Matrix

| Category | Daily Target | Priority | ROI Focus |
|----------|--------------|----------|-----------|
| Prospect | 3 comments | HIGH | Lead generation |
| Peer | 3 comments | MEDIUM | Network building, collaboration |
| Thought Leader | 3 comments | MEDIUM | Visibility, credibility |

---

## Comment Formatting Rules

**STRICT: No em-dashes (—) in comments.**
- Em-dashes feel overly polished and AI-generated
- Use commas, periods, or rewrite the sentence instead
- This applies to ALL comment types (Peer, Thought Leader, Prospect)

---

## Connection Request Rules (2-3 Touch Rule)

**Minimum 2-3 separate engagements before sending connection request.**

| Touches | Approach | Notes |
|---------|----------|-------|
| 1 | DO NOT CONNECT | Still warming up, need more engagement |
| 2 | Asset-led note | Minimum threshold, offer value in note |
| 3+ | Blank request | Strong signal, blank performs 12% better |

**What counts as a "touch":**
- Comment on their post (15+ words)
- Like/reaction on their post
- Save their post
- Follow their profile
- Reply to their comment on someone else's post

**Timing:** First touch must be 48+ hours ago before connecting.

## Integration with Skills

| Skill | How Classification is Used |
|-------|---------------------------|
| `linkedin-pro-commenter` | Adjusts comment tone and strategy per category |
| `linkedin-icp-finder` | Screens and classifies contacts in comment sections |
| `linkedin-icp-warmer` | Finds re-engagement opportunities for warming prospects |
| `linkedin-connect-timer` | Prioritizes connection requests by category |
| `linkedin-daily-planner` | Allocates commenting targets per category |
