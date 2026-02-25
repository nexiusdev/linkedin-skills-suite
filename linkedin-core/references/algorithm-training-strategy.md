# LinkedIn Algorithm Training Strategy

Complete guide to training the LinkedIn algorithm to surface your ICP prospects' content in your feed.

## The Core Problem

**Challenge:** You have prospects in your ICP list, but their posts don't appear in your LinkedIn feed, making it hard to find content to engage with.

**Solution:** Train the LinkedIn algorithm through behavioral signals so it prioritizes showing you their content.

---

## How LinkedIn's Algorithm Works (2026)

LinkedIn's 360Brew algorithm learns who matters to you through **engagement signals**:

### Primary Signals (Strongest)

| Signal | Weight | How It Works |
|--------|--------|--------------|
| **Profile visits** | 10x | Algorithm tracks who you view and shows their content |
| **Following** | 8x | Direct signal: "I want to see this person's content" |
| **Saves** | 5x | Bookmarking posts = strong interest signal |
| **Comments** | 3x | Especially within first hour of posting |
| **Bell notifications** | 15x | Strongest signal: "Show me EVERYTHING from this person" |

### Secondary Signals (Medium)

| Signal | Weight | How It Works |
|--------|--------|--------------|
| **Reactions (Like/etc)** | 1x | Basic engagement, minimal impact |
| **Search behavior** | 2x | Searching for their name signals interest |
| **Dwell time** | 3x | Spending 30+ seconds on their profile/posts |
| **Network overlap** | 4x | Engaging with their connections clusters you together |

### The Compounding Effect

**Key insight:** After 3-4 engagements with someone, LinkedIn treats you as part of their "network cluster" and prioritizes their content in your feed.

```
Touch 1: Profile visit + Follow = Occasional appearance in feed
Touch 2: Comment on post = More frequent appearance
Touch 3: Save post + Visit again = Regular appearance
Touch 4+: LinkedIn assumes strong relationship = Feed dominance
```

**Timeline:**
- Week 1: Occasional posts appear (10-20% of their content)
- Week 2-3: Regular appearance (40-60% of their content)
- Week 4+: Feed dominated by trained prospects (70-90% visibility)

---

## The 3-Phase Training System

### Phase 1: Discovery (Week 1-2)

**Goal:** Find 50-100 ICP prospects

**Methods:**
1. **Feed Discovery** - Scan LinkedIn feed daily, classify authors on-the-fly
2. **Hashtag Discovery** - Monitor topic hashtags (#SMEAutomation, #DigitalTransformation)
3. **Sales Navigator** - Use "Posted on LinkedIn" filter to find active prospects
4. **Inbound signals** - Profile viewers, followers, post reactors

**Daily target:** 5-10 new prospects discovered and added to icp-prospects.md

**Output:** Prospect list with Source column populated

### Phase 2: Training (Week 2-3)

**Goal:** Systematically train algorithm on all discovered prospects

**Method:** Train Algorithm mode in linkedin-icp-finder

**Daily target:** Train 5-7 prospects per session (5 minutes)

**Training checklist per prospect:**
```
□ Visit profile (30-45 seconds dwell time)
□ Scroll profile (Read headline, about section)
□ Follow (if not already following)
□ Bell notifications (HIGH priority only - top 10-15 prospects)
□ Navigate to recent activity page
□ Save 1-2 most recent posts
□ Wait 10-15 seconds (appear human)
□ Update icp-prospects.md (Algorithm Trained = ✅ YES)
```

**Priority order:**
1. HIGH: Connected prospects (1st degree) - Already have relationship
2. MEDIUM: Touches >=2 (actively warming) - Building pipeline
3. LOW: Touches <2 (cold prospects) - Just discovered

### Phase 3: Maintenance (Week 4+)

**Goal:** Engage when their posts appear naturally in feed

**Method:** Feed shows trained prospect content → Engage → Reinforces signal

**Daily workflow:**
1. Open LinkedIn feed
2. Scan for trained prospect posts (you'll recognize names)
3. Engage immediately when you see them (within first hour)
4. This reinforces to algorithm: "Yes, keep showing me this person"

**Re-training schedule:**
- Re-visit profiles every 30 days to maintain priority
- Update "Last Trained" timestamp in icp-prospects.md
- Re-save recent posts to refresh interest signal

---

## Training Session Protocol

### Pre-Session Checklist

```
□ Read icp-prospects.md → Get list of prospects to train
□ Filter: Algorithm Trained = ❌ NO or ⏳ PENDING
□ Filter: Activity Status = ACTIVE (skip inactive posters)
□ Prioritize: Connected > Touches >=2 > Cold prospects
□ Select 5-7 prospects for this session
```

### During Training (Per Prospect)

**Step 1: Navigate to profile**
```
- URL format: https://www.linkedin.com/in/[username]/
- Wait for page to fully load
```

**Step 2: Dwell time (30-45 seconds)**
```
- Scroll slowly down profile
- Read headline (algorithm tracks eye movement patterns via scroll behavior)
- Read about section (shows genuine interest)
- Scroll to experience section
```

**Step 3: Follow (if not already)**
```
- Check button status: "Follow" or "Following"
- If "Follow" → Click it
- Wait for confirmation (button changes to "Following")
```

**Step 4: Bell notifications (selective)**
```
ONLY enable for:
- Connected prospects (1st degree)
- High-value accounts (>$10K potential)
- Active posters (3+ posts per week)
- Strategic relationships

HOW TO:
- Click bell icon next to "Following" button
- Select "All" from dropdown
- Use SPARINGLY - max 10-15 prospects total
```

**Step 5: Save recent posts**
```
- Navigate to /recent-activity/all/
- Find 1-2 most recent posts (last 7 days)
- Click bookmark icon on each
- Saves signal strong interest to 360Brew
```

**Step 6: Update tracking**
```
- Open icp-prospects.md
- Find this prospect's row
- Update: Algorithm Trained = ✅ YES
- Update: Last Trained = today (DDMon format)
- Update: Notes = "Followed" or "Followed + Bell ON"
- Save file
```

**Step 7: Human pacing**
```
- Wait 10-15 seconds before next profile
- Prevents spam detection
- Appears organic to LinkedIn
```

### Post-Session Actions

**Log training session:**
```
File: shared/logs/linkedin-activity.md
Section: Algorithm Training

Format:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALGORITHM TRAINING SESSION
Date: 28Jan 09:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROSPECTS TRAINED: 7

HIGH PRIORITY (Bell enabled):
1. Su Mei Toh - CEO, SME Republic
2. David Cheang - CEO, DC13 Group

MEDIUM PRIORITY:
3. Amy Tan - CFO, FinCo
4. John Lee - COO, OpsCo
5. Sarah Lim - Director Ops, GrowthSG

LOW PRIORITY:
6. Michael Wong - Manager, TechMY
7. Lisa Chen - Director, ScalePH

ACTIONS:
- Profiles visited: 7
- New follows: 5
- Bell notifications: 2
- Posts saved: 11

NEXT SESSION: 28Feb (30-day re-training)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Bell Notification Strategy

**⚠️ Use bell notifications SPARINGLY - they're the nuclear option.**

### When to Enable

```
ENABLE BELLS FOR:
✓ Connected prospects (1st degree) you're actively warming
✓ High-value accounts ($10K+ potential revenue)
✓ Active posters (3+ times per week)
✓ Strategic relationships (potential partners, influencers)

MAX 10-15 total across entire prospect list
```

### When NOT to Enable

```
❌ DON'T enable bells for:
✗ Cold prospects (not yet connected)
✗ Inactive posters (post <1x per month)
✗ Low-priority prospects
✗ Thought leaders (they post too frequently)
✗ More than 15 people total (notification overload)
```

### How to Enable

```
1. Go to their profile
2. Click bell icon (next to "Following" button)
3. Select "All" from dropdown options
4. Confirmation: Bell icon turns solid blue
```

### Managing Bell Notifications

**If overwhelmed:**
1. Review who has bells enabled
2. Disable for prospects who:
   - Haven't posted in 30+ days
   - Post too frequently (>1x per day)
   - No longer fit ICP
3. Keep only top 5-10 most valuable prospects

---

## Feed Discovery Integration

**Purpose:** Discover new prospects WHILE training algorithm on them

### Workflow

```
STEP 1: Scan LinkedIn feed (5 minutes daily)
├─ Navigate to https://www.linkedin.com/feed/
├─ Scan first 10-15 posts (don't scroll endlessly)
├─ For each post:
│  ├─ Quick ICP check:
│  │  ✓ Target geography location (from references/icp-profile.md)
│  │  ✓ Decision-maker role (Manager+, C-suite)
│  │  ✓ SME company size signals
│  │  ✓ Post discusses pain points
│  ├─ If ICP match:
│  │  → Like post
│  │  → Generate comment (linkedin-pro-commenter)
│  │  → Post comment
│  │  → Add to icp-prospects.md (Source = "Feed Discovery")
│  └─ If not ICP: Skip
└─ RESULT: 2-3 new prospects + first engagement done

STEP 2: Train algorithm on newly discovered prospects
├─ These prospects have Algorithm Trained = ⏳ PENDING
├─ Schedule for next "train algorithm" session
├─ Will visit profile + follow + save to complete training
└─ RESULT: Full algorithm training within 24 hours
```

**Why this works:**
- You're engaging with content LinkedIn ALREADY showed you (high relevance)
- First engagement (comment) while discovering them
- Follow-up training (profile visit + follow) within 24 hours
- Two-touch initial signal = faster feed priority

---

## Hashtag Discovery Integration

**Purpose:** Find prospects discussing specific topics + train algorithm

### Daily Hashtag Rotation

```
Monday: #SMEAutomation
Tuesday: #DigitalTransformation
Wednesday: #CFOChallenges
Thursday: #ERPImplementation
Friday: #OperationsExcellence
Saturday: #BusinessAutomation
Sunday: #ScalingChallenges
```

### Workflow

```
STEP 1: Search for today's hashtag
├─ URL: https://www.linkedin.com/search/results/content/?keywords=%23[hashtag]
├─ Filter: "Posts" + "Past 24 hours"
├─ Scan first 10-15 results
└─ Look for HIGH pain signals in post content

STEP 2: Screen posts for ICP fit
├─ Target geography match (from references/icp-profile.md)
├─ Decision-maker role
├─ Pain point explicitly mentioned in post
└─ Stop when you find 1-2 HOT prospects

STEP 3: Engage + Train simultaneously
├─ Comment on post (reference their specific pain point)
├─ Visit author profile
├─ Follow them
├─ Save 1-2 recent posts
├─ Add to icp-prospects.md:
│  ├─ Source = "Hashtag: #[tag]"
│  ├─ Algorithm Trained = ✅ YES (profile visited + followed)
│  ├─ Touches = 1
│  └─ Notes = "Pain: [specific challenge mentioned]"
└─ RESULT: New prospect + fully trained in one workflow
```

**Why this works:**
- Self-selected prospects (they're posting about your topic)
- Pain points visible in post content (better comment context)
- Immediate engagement + full training = strong initial signal
- Topic clustering = algorithm shows you similar posts

---

## Troubleshooting

### Problem: Feed still not showing prospect content after 2 weeks

**Diagnosis:**
- Check: Have you engaged with their posts 3-4 times?
- Check: Are you following them?
- Check: Did you save any of their posts?

**Solution:**
1. Re-visit their profiles (refresh the signal)
2. Save 2-3 of their recent posts (strong interest signal)
3. Engage with next 2-3 posts that DO appear
4. Search for their name (search behavior signal)

### Problem: Too many prospects to train daily

**Diagnosis:**
- You have 100+ prospects with Algorithm Trained = NO
- Can only train 5-7 per day (5 minutes)
- Would take 15-20 days to train all

**Solution:**
1. Prioritize HIGH-value prospects first
2. Train connected prospects (1st degree) before cold prospects
3. Skip inactive prospects (Activity Status = INACTIVE)
4. Focus on prospects with Touches >=2 (warming pipeline)
5. Train others gradually over 4-6 weeks

### Problem: Bell notifications overwhelming

**Diagnosis:**
- Enabled bells for too many people (>15)
- Getting notifications every hour
- Can't keep up with all posts

**Solution:**
1. Review who has bells enabled
2. Keep only top 5-10 most valuable
3. Disable bells for:
   - People who post >1x per day
   - Lower-priority prospects
   - Thought leaders (they post frequently)

### Problem: Following too many people

**Diagnosis:**
- Following 500+ people
- Feed is noisy, can't see prospect content

**Solution:**
1. Don't unfollow trained prospects (resets signal)
2. Instead: Use bell notifications for top prospects (surfaces their content above noise)
3. Or: Mute thought leaders and peers (keep following but hide from feed)
4. Or: Use LinkedIn's "Sort by: Recent" view to see chronological posts

---

## Success Metrics

### Week 1-2 (Discovery Phase)

```
✅ SUCCESS INDICATORS:
- 50-100 prospects in icp-prospects.md
- Source column populated (Feed, Hashtag, SalesNav, etc.)
- 5-10 new prospects discovered daily
- Algorithm Trained column shows mix of YES/PENDING/NO
```

### Week 2-3 (Training Phase)

```
✅ SUCCESS INDICATORS:
- 70-80% of prospects have Algorithm Trained = ✅ YES
- Training sessions logged 5x per week
- 5-7 prospects trained per session
- Following 80-100+ prospects total
```

### Week 4+ (Maintenance Phase)

```
✅ SUCCESS INDICATORS:
- 60-70% of feed posts are from trained prospects
- Engaging with prospect posts 5-10x per day naturally
- Minimal need for discovery (feed surfaces content)
- Re-training sessions 1x per month (30-day cycle)
```

### ROI Metrics

**Time savings:**
- Without training: 2-3 minutes per prospect to find posts (profile visit + scroll)
- With training: 30 seconds per prospect (post appears in feed)
- **Savings: 75% reduction in prospecting time**

**Engagement quality:**
- Without training: Random search, often engage with stale posts
- With training: Engage within first hour (algorithm loves this)
- **Result: Better comment positioning + higher visibility**

---

## Best Practices

### DO ✅

- Train 5-7 prospects per day consistently
- Prioritize connected prospects (1st degree)
- Follow EVERY trained prospect (core signal)
- Save posts regularly (5x weight signal)
- Use bell notifications for top 10-15 only
- Re-train every 30 days (refresh signal)
- Engage within first hour when posts appear
- Log training sessions for tracking
- Update "Algorithm Trained" column immediately

### DON'T ❌

- Don't train 20+ prospects in one day (spam signal)
- Don't skip the dwell time (30-45 seconds)
- Don't enable bells for 50+ people (notification overload)
- Don't train inactive prospects (waste of time)
- Don't unfollow trained prospects (resets signal)
- Don't forget to save posts (missed strong signal)
- Don't rush between profiles (appears bot-like)
- Don't train without updating tracking file

---

## Integration with Other Skills

### With linkedin-icp-finder

```
USER: "train algorithm"
SKILL: Executes Mode 1: Train Algorithm
      → Reads icp-prospects.md
      → Filters for Algorithm Trained = NO/PENDING
      → Trains 5-7 prospects
      → Updates tracking
      → Logs session
```

### With linkedin-daily-planner

```
MORNING BLOCK (Autonomous mode):
1. Feed Discovery (5 min) → Find + engage 2-3 new prospects
2. Algorithm Training (5 min) → Train 5-7 pending prospects
3. Hashtag Discovery (5 min) → Topic-based prospecting
4. Standard Engagement (15 min) → Peer/Prospect/Leader comments

RESULT: Discovery + Training happens automatically every morning
```

### With linkedin-icp-warmer

```
After algorithm training:
→ Prospects' posts start appearing in feed
→ linkedin-icp-warmer finds posts to engage with (uses cached URLs)
→ Engages 3-4 times (network cluster effect)
→ Feed shows even MORE of their content (compounding)
```

---

## Quick Reference

### Training Checklist (Copy-Paste)

```
□ Navigate to profile URL
□ Dwell 30-45 seconds (scroll + read)
□ Check Following status → Follow if not already
□ Bell notification (HIGH priority only)
□ Go to /recent-activity/all/
□ Save 1-2 most recent posts
□ Update icp-prospects.md:
  □ Algorithm Trained = ✅ YES
  □ Last Trained = [today]
  □ Notes = "Followed" or "Followed + Bell ON"
□ Wait 10-15 seconds
□ Next prospect
```

### Priority Matrix

| Prospect Type | Train Priority | Why |
|---------------|----------------|-----|
| Connected (1st) + Active | 🔥🔥🔥 URGENT | Warm relationship, best ROI |
| Touches >=2 + Active | 🔥🔥 HIGH | Warming pipeline |
| Cold + Active | 🔥 MEDIUM | New prospects |
| Any + Inactive | ❌ SKIP | Waste of time, they don't post |

### Re-Training Schedule

```
DAY 1: Train initial batch (50 prospects over 10 days = 5/day)
DAY 30: Re-train first 5 prospects (refresh signal)
DAY 31: Re-train next 5 prospects
...continue 30-day rolling re-training
```

---

## Additional Resources

- `references/linkedin-strategy.md` - Full 360Brew algorithm documentation
- `references/contact-classification.md` - How to classify Peer/Prospect/Leader
- `shared/logs/icp-prospects.md` - Master prospect tracking file
- `shared/logs/linkedin-activity.md` - Activity log with training sessions
