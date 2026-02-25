---
name: linkedin-company-pages
description: Manage daily LinkedIn posts for 3 company pages ({{CLIENT_BRAND_PRIMARY}}, {{CLIENT_BRAND_SECONDARY}}, {{CLIENT_COMMUNITY_NAME}}). Use when user says "post to company pages", "company page posts", "manage company pages", or "daily company content". Fully autonomous workflow - finds trending topics via x-trender, selects 1 topic per page based on positioning, generates posts, and publishes via browser automation (browser MCP (Chrome DevTools or Playwright) or DevTools fallback). No approval needed.
---

# LinkedIn Company Pages Manager

**Browser automation uses browser MCP (Chrome DevTools or Playwright) if available, otherwise falls back to Chrome DevTools. See linkedin-daily-planner skill for detailed tool mapping.**

Autonomous daily content creation and posting for 3 company pages with distinct positioning.

## Company Pages

| Page | LinkedIn ID | URL Slug | Focus | Content Pillars |
|------|-------------|----------|-------|-----------------|
| **{{CLIENT_BRAND_PRIMARY}}** | 105886234 | nexius-labs | Agentic AI ERP for SMEs | Product updates, AI automation wins, SME transformation stories |
| **{{CLIENT_BRAND_SECONDARY}}** | 109310332 | nexius-academy | AI workshops for non-coders | Learning tips, workshop highlights, non-coder success stories |
| **{{CLIENT_COMMUNITY_NAME}}** | 104472305 | aiignite2022 | AI events for business leaders | Industry insights, event announcements, AI implementation trends |

## Autonomous Workflow

### Step 1: Find Trending Topics

Invoke `x-trender` skill to scan X.com for trending AI/tech topics.

### Step 2: Topic-to-Page Matching

Match each trending topic to the most relevant company page:

| Topic Type | Best Page | Rationale |
|------------|-----------|-----------|
| AI automation, ERP, SME ops | {{CLIENT_BRAND_PRIMARY}} | Product-aligned |
| Learning, tutorials, no-code | {{CLIENT_BRAND_SECONDARY}} | Education-focused |
| Industry trends, leadership, events | {{CLIENT_COMMUNITY_NAME}} | Thought leadership |

**Rules:**
- Each page gets exactly 1 topic per day
- Never duplicate topics across pages
- If topic fits multiple pages, assign to page with fewer recent posts

### Step 3: Generate Posts

For each page, generate a post using `linkedin-elite-post` framework adapted for company voice:

**{{CLIENT_BRAND_PRIMARY}} Voice:**
- Professional, solution-focused
- Emphasize practical AI benefits for SMEs
- Include product tie-ins where relevant

**{{CLIENT_BRAND_SECONDARY}} Voice:**
- Encouraging, educational
- Break down complex AI into simple steps
- Invite engagement ("What workflow would you automate first?")

**{{CLIENT_COMMUNITY_NAME}} Voice:**
- Thought leadership, industry perspective
- Forward-looking, trend-focused
- Call to action for events/networking

### Step 4: Post to Each Page

Use browser automation to post to each company page:

1. Navigate to `linkedin.com/company/[url-slug]/`
2. Click "Start a post" button
3. Enter post content
4. Click "Post" (company pages don't need scheduling for daily posts)
5. Log to activity log

**Admin URLs:**
- {{CLIENT_BRAND_PRIMARY}}: `linkedin.com/company/105886234/admin/`
- {{CLIENT_BRAND_SECONDARY}}: `linkedin.com/company/109310332/admin/`
- {{CLIENT_COMMUNITY_NAME}}: `linkedin.com/company/104472305/admin/`

## Post Format by Page

### {{CLIENT_BRAND_PRIMARY}} Post Template
```
[Hook about AI/automation trend]

Here's what this means for SMEs:

[2-3 bullet points on practical implications]

At {{CLIENT_BRAND_PRIMARY}}, we're building the Agentic ERP that handles this automatically.

[Question to drive engagement]
```

### {{CLIENT_BRAND_SECONDARY}} Post Template
```
[Hook about learning/building AI]

The best way to learn AI? Build something real.

[3-step breakdown or tip]

No coding required. Just curiosity.

What would you build first?
```

### {{CLIENT_COMMUNITY_NAME}} Post Template
```
[Hook about AI trend/insight]

Forward-thinking leaders are paying attention to this.

[Why it matters - 2-3 sentences]

This is exactly what we explore at {{CLIENT_COMMUNITY_NAME}} events.

[CTA or thought-provoking question]
```

## Daily Execution

When triggered:
1. Check shared activity log for today's posts (avoid duplicates)
2. Run x-trender for fresh topics
3. Match 1 topic to each page
4. Generate 3 posts (one per page)
5. Post to each company page sequentially
6. Log all posts to activity log

## Activity Logging

**Log location:** `shared/logs/company-pages-activity.md`

After each post:
```
| Date | Page | Topic | Post Summary | Post URL | Engagement (24h) |
```

## Error Handling

- If x-trender fails: Use recent industry news or product updates
- If posting fails: Screenshot error, retry once, log failure
- If page access denied: Alert user, skip page

## Integration Points

- **x-trender**: Source for trending topics
- **linkedin-elite-post**: Post writing framework
- **shared/logs/**: Activity logging
