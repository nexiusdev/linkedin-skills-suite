---
name: linkedin-company-pages
description: Manage daily LinkedIn posts for your company pages. Use when user says "post to company pages", "company page posts", "manage company pages", or "daily company content". Fully autonomous workflow - finds trending topics via x-trender, selects 1 topic per page based on positioning, generates posts, and publishes via browser automation (Claude for Chrome or DevTools fallback). No approval needed.
---

# LinkedIn Company Pages Manager

**Browser automation uses Claude for Chrome if available, otherwise falls back to Chrome DevTools. See linkedin-daily-planner skill for detailed tool mapping.**

Autonomous daily content creation and posting for your company pages with distinct positioning.

## Company Pages Configuration

> **Read your company pages from `references/company-pages-config.md`.**
> If not configured, prompt the user to run `linkedin-onboarding` or provide page details manually.

**Expected format in `references/company-pages-config.md`:**

| Page | LinkedIn ID | URL Slug | Focus | Content Pillars |
|------|-------------|----------|-------|-----------------|
| **[Page Name 1]** | [ID] | [slug] | [Focus area] | [Pillars] |
| **[Page Name 2]** | [ID] | [slug] | [Focus area] | [Pillars] |
| **[Page Name 3]** | [ID] | [slug] | [Focus area] | [Pillars] |

If `references/company-pages-config.md` does not exist or is empty, ask the user:
1. "Do you manage LinkedIn company pages?"
2. If yes, collect: Page name, LinkedIn numeric ID, URL slug, focus area, and content pillars for each page
3. Save to `references/company-pages-config.md`

## Autonomous Workflow

### Step 1: Find Trending Topics

Invoke `x-trender` skill to scan X.com for trending topics relevant to your niche (read from `references/icp-profile.md`).

### Step 2: Topic-to-Page Matching

Match each trending topic to the most relevant company page based on each page's focus area and content pillars (from `references/company-pages-config.md`).

**Rules:**
- Each page gets exactly 1 topic per day
- Never duplicate topics across pages
- If topic fits multiple pages, assign to page with fewer recent posts

### Step 3: Generate Posts

For each page, generate a post using `linkedin-elite-post` framework adapted for that page's voice.

Each page should have a distinct voice matching its focus area. Generate the voice guidelines from the page's focus and content pillars defined in the config file.

**General post structure:**
```
[Hook about trending topic]

[2-3 bullet points on practical implications relevant to page focus]

[Tie-in to page's positioning]

[Question to drive engagement]
```

### Step 4: Post to Each Page

Use browser automation to post to each company page:

1. Navigate to `linkedin.com/company/[url-slug]/`
2. Click "Start a post" button
3. Enter post content
4. Click "Post" (company pages don't need scheduling for daily posts)
5. Log to activity log

**Admin URLs:** Read from `references/company-pages-config.md` and construct as:
`linkedin.com/company/[linkedin-id]/admin/`

## Daily Execution

When triggered:
1. Load company pages config from `references/company-pages-config.md`
2. Check shared activity log for today's posts (avoid duplicates)
3. Run x-trender for fresh topics
4. Match 1 topic to each page
5. Generate posts (one per page)
6. Post to each company page sequentially
7. Log all posts to activity log

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
- If company pages not configured: Prompt user to run `linkedin-onboarding` or provide page details

## Integration Points

- **x-trender**: Source for trending topics
- **linkedin-elite-post**: Post writing framework
- **references/company-pages-config.md**: Company page configuration
- **references/icp-profile.md**: Your niche and positioning
- **shared/logs/**: Activity logging
