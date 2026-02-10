# Claude Skills Project Memory

## Key Learnings

### Activity Log Update - MANDATORY Evening Block Step (08 Feb 2026)
- **CRITICAL FIX:** Activity log was going stale (16-day gap Jan 23 → Feb 8) because there was no enforced logging step
- **Root cause:** To-do files were created and tasks completed, but no process to transfer completed tasks to activity log
- **THE FIX:** Added 🔴 MANDATORY step at start of Evening Block in `linkedin-daily-planner/skill.md`
  - Reads today's to-do file (`to-do_DDMMYYYY.md`)
  - Extracts all `[x]` completed tasks with timestamps
  - Updates `shared/logs/linkedin-activity.md` → Today's Summary section
  - Updates prospect touch counts in `icp-prospects.md`
  - Marks "Last updated: YYYY-MM-DD HH:MM SGT" timestamp
- **Why MANDATORY:** Activity log is source of truth for all skills - daily limits, touch tracking, weekly metrics all depend on it
- **Enforcement:** Made it FIRST STEP in Evening Block autonomous workflow + added to Quality Checklist
- **Time budget:** Only 2-3 minutes - no excuse to skip
- **Verification:** Activity log should NEVER go more than 24 hours without update
- **Documentation:** Full details in `linkedin-daily-planner/FIX-ACTIVITY-LOG-UPDATE.md`

### Connection Status - Always Update On Profile Visit (07 Feb 2026)
- **RULE:** Every time you visit ANY prospect's profile for ANY reason, observe the action button and update Connection Status
  - "Message" button = connected | "Follow"/"Connect" button = none | "Pending" = pending
- **Root cause of stale data:** Connection acceptances were only checked during Evening Block, so status drifted
- **Jan 22-23 batch example:** 9/15 showed "none" in file but were actually "connected" on LinkedIn
- **Added to skill.md:** CONNECTION STATUS OBSERVATION RULE under CACHE-FIRST RULE section

### CRM Incremental Sync - Use CLI, Never crm_sync_all (10 Feb 2026)
- **RULE:** NEVER call `crm_sync_all` during routine daily blocks (Afternoon/Evening)
- **Primary method:** `python crm-integration/cli_sync.py sync "Name1" "Name2"` via Bash
- **Why CLI:** MCP tools are deferred and may not load. CLI always works.
- **Track changes during session:** As you modify prospects, remember which records changed
- **At end of block:** Run CLI sync for each changed prospect by name
- **When to use `crm_sync_all`:** Only for initial setup, data migration, or weekly full reconciliation (Friday audit)
- **Files:** `crm-integration/cli_sync.py` (CLI wrapper), `crm-integration/hubspot_mcp.py` (MCP server + shared logic)

### MCP Tools Are Deferred - Use CLI Fallback for CRM (10 Feb 2026)
- **RULE:** With 8+ MCP servers, Claude Code defers tool loading to save context (Tool Search feature)
- Only ~3 servers' tools load per session (playwright, kling, claude-in-chrome typically)
- hubspot-crm, gdrive, chrome-devtools, HeyGen, mcp-veo3, google-sheets are deferred
- **CRM SYNC FIX:** Use CLI script instead of MCP tools:
  - `python crm-integration/cli_sync.py sync "Name1" "Name2"` — always works
  - `python crm-integration/cli_sync.py pipeline` — pipeline summary
  - `python crm-integration/cli_sync.py lookup "Name"` — contact lookup
  - API keys loaded automatically from `.mcp.json` env block
- **Parser bug fixed:** Escaped pipes (`\|`) in Touch History column caused column misalignment
  - Email field got LinkedIn URL, LinkedIn field got "none" — all syncs for affected rows failed
  - Fix: Replace `\|` with placeholder before splitting, restore after

### Chrome DevTools MCP - evaluate_script
- Use `function` parameter (NOT `expression`) with arrow function syntax: `() => { ... }`
- LinkedIn **feed page** uses **TipTap/ProseMirror** → `.ProseMirror[contenteditable="true"]`
- LinkedIn **activity pages** still use **Quill** → `.ql-editor[data-placeholder="Add a comment…"]`
- Always check which editor type exists: `const editor = document.querySelector('.ql-editor') || document.querySelector('.ProseMirror')`
- Use `document.execCommand('insertText', false, text)` after `.focus()`
- **CRITICAL:** When multiple comment boxes open, use DOM index mapping, NOT "find first empty"

### Comment Dedup Rule - One Comment Per Post (08 Feb 2026)
- **RULE:** NEVER comment on the same post twice (top-level comments only; replying to your own thread is OK)
- **Pre-flight:** At session start, scrape `/in/melverick/recent-activity/comments/` → build "already commented" set
- **Set key:** `author_slug + first_60_chars_of_post_text`
- **Before each comment:** Check post against set → SKIP if match found → find replacement post
- **After each comment:** Add to set + log to `shared/logs/linkedin-activity.md`
- **Skills updated:** linkedin-daily-planner (all blocks), linkedin-pro-commenter (workflow + quality checklist), linkedin-icp-warmer (Step 4)
- **Root cause:** Without dedup, same author's popular posts can appear in feed and prospect warming, leading to accidental double-commenting

### LinkedIn Comment Posting Flow (DevTools)
1. Navigate to post URL
2. Take snapshot → find Comment button uid
3. Click Comment button
4. Take snapshot → find comment textbox
5. Use evaluate_script with JS to insert text
6. Take snapshot → find Submit/Post button (new uid prefix)
7. Click Submit button
8. Take snapshot → verify comment posted (check comment count increment)

### Sub-Agent Optimization
- Use `model: "haiku"` for quick research/filtering tasks (prospect lists, duplicate checks, daily limits)
- Use `model: "sonnet"` for complex analysis (feed classification, multi-file cross-checks)
- Launch research agents in parallel at block start to save ~50K tokens vs reading large files in main context
- Sub-agent results for prospect filtering often need validation against actual LinkedIn state

### Weekend Engagement Session Pattern
- Saturday/Sunday = engagement only, no posting
- Priority: (1) Reply to post comments, (2) PROSPECT re-engagement, (3) Inbound signal screening, (4) Feed discovery, (5) Bulk Follow Sprint
- Feed quality is lower on weekends - fewer ICP posts visible
- Bulk Follow Sprint effectiveness depends on data accuracy in icp-prospects.md

### Google Sheets Sync (Trigger: "sync to googlesheet")
- **Spreadsheet ID:** `1-3Ua8O6vwqHtuUe17VepNpWPWPeT0eeL8jXfN40lfKc`
- **Drive Folder ID:** `1PAvNtv07W2wsLkAgIr93xxPCeoINjAnX`
- **Service Account:** `claude-sheets@gen-lang-client-0759962377.iam.gserviceaccount.com`
- **Credentials file:** `gen-lang-client-0759962377-207882157ce2.json` (in project root)
- **Script:** `shared/scripts/sync-prospects-to-sheets.py`
- **Command:** `python shared/scripts/sync-prospects-to-sheets.py`
- **Source:** Reads markdown table from `shared/logs/icp-prospects.md` (NOT CSV)
- **CSV Backups:** Auto-saved to `shared/logs/backups/` with format `icp-prospects_YYYYMMDDHHMM.csv`
- **Dependencies:** `gspread`, `google-auth` (pip installed)
- **APIs enabled:** Google Drive API + Google Sheets API on project `gen-lang-client-0759962377`
- **Sheet shared with SA as Editor** — do NOT revoke or the sync breaks
- **Gotcha:** Service account Drive storage quota is limited — cannot create new sheets, only write to existing shared ones

### Autonomous Operation Mode (08 Feb 2026)
- **RULE:** Always proceed autonomously without asking user for decisions/confirmations
- **Decision-making:** Use AI judgment to select best options, prioritize tasks, and execute workflows end-to-end
- **Examples:**
  - Warmup opportunities → Auto-select top prospects and engage
  - Content creation → Auto-select best variation and post
  - Daily planning → Auto-execute tasks in priority order
- **User preference:** "make all decisions to proceed autonomously and not ask me any questions"
- **Skills affected:** linkedin-daily-planner, linkedin-icp-warmer, linkedin-pro-commenter, all content creation skills

### Push Skills to nexiusdev (Trigger: "push skills to nexiusdev")
- **Private repo:** `origin` = melkizac/claude-skills (dev branch, has personal data)
- **Public repo:** `public` = nexiusdev/linkedin-skills-suite (master only, skills only)
- **Workflow:**
  1. `git worktree add <temp-dir> public/master`
  2. Copy ONLY skill files from current working dir (use `git show public/dev:` or direct copy)
  3. **EXCLUDE:** `shared/logs/icp-prospects.md`, `shared/logs/linkedin-activity.md`, `shared/logs/whatsapp-activity.md`, `shared/logs/video-activity.md`, `shared/linkedin-account-config.md`, `linkedin-daily-planner/to-do_*.md`, `to-do_*.md`, `**/logs/activity-log.md`, `**/logs/warmup-runs.md`, `.claude/settings.local.json`, `references/icp-profile.md`, `references/connect-request.md`, `references/contact-classification.md`, `references/linkedin-strategy.md`, `references/saved-asset.md`, any `data/` dirs with personal config
  4. **INCLUDE:** `*/skill.md`, `*/SKILL.md`, `*.skill`, scripts, references (generic), README, templates
  5. Commit, push to `public master`, remove worktree
- **NEVER push dev branch to nexiusdev** — it contains prospect names, emails, LinkedIn URLs
