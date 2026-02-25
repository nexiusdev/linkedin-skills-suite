# LinkedIn Skills Suite for Codex

A comprehensive LinkedIn outreach automation suite built as Codex-compatible skills. Fully autonomous daily workflow: prospect discovery, content creation, engagement, connection requests, and pipeline warming.

Built on the **360Brew algorithm strategy** for maximum reach and engagement while staying within LinkedIn's safety limits.

## Prerequisites

Before running this suite, make sure you have:

1. Install dependencies first (Git, Python 3.10+, Node.js) using CLI **or** installer/UI:

```bash
# Windows (PowerShell, via winget)
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
winget install --id OpenJS.NodeJS.LTS -e

# macOS (Homebrew)
brew install git python node

# Ubuntu/Debian
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip nodejs npm
```

If you prefer non-CLI setup, install Git, Python, and Node.js from their official installers/apps, then continue below.

2. Verify dependencies:

```bash
git --version
python --version
node --version
npm --version
```

3. Install Codex CLI (via terminal command or your environment's installer method).
4. Verify Codex CLI is available:

```bash
codex --version
```

5. Browser automation MCP available (`chrome-devtools` or `playwright`)
6. A LinkedIn account you will operate from (Free, Premium, or Sales Navigator)
7. Optional integrations ready if needed:
   - HubSpot account + private app token (for CRM sync)
   - Google Cloud service account (for Google Sheets workflows)
   - Email enrichment provider API keys (Apollo/Hunter/Snov/GetProspect/Prospeo)

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/nexiusdev/linkedin-skills-suite.git
cd linkedin-skills-suite

# 2. Run setup to create local config files
# Windows (PowerShell):
.\setup.ps1
# Mac/Linux:
chmod +x setup.sh && ./setup.sh

# 3. Open Codex and personalize
linkedin-onboarding

# 4. Start the daily workflow
start linkedin
```

The onboarding skill asks ~16 questions about your business, target market, and geography, then generates personalized reference files that all other skills read from. No code changes needed.

## Receiving Updates

Your config and activity logs are **gitignored** — they live only on your machine. To get skill updates safely:

```bash
# Windows (PowerShell):
.\update.ps1
# Mac/Linux:
chmod +x update.sh && ./update.sh
```

The update script automatically stashes any local skill edits you've made, pulls the latest updates, then restores your edits on top. If your changes conflict with an upstream update, it lists the conflicted files and tells you how to resolve them.

Your personalized config in `linkedin-core/references/`, `linkedin-core/shared/logs/`, and account settings is never touched — those files are gitignored.

See [UPDATING.md](UPDATING.md) for detailed step-by-step instructions with screenshots of every outcome.

## Skills

### Core Workflow

| Skill | Description |
|-------|-------------|
| **linkedin-daily-planner** | Orchestrates the full daily workflow across 5 time blocks (morning, content, midday, afternoon, evening). Runs autonomously with `start linkedin`. |
| **linkedin-onboarding** | First-time setup. Collects your ICP, geography, timezone, industry, and content pillars to personalize all skills. |

### Content Creation

| Skill | Description |
|-------|-------------|
| **linkedin-elite-post** | Generates 2-3 post variations across modes (thought leadership, educational, engagement, lead gen) with proven hook frameworks. |
| **linkedin-trender** | Scans your LinkedIn feed for trending topics to write about. Filters for high-engagement posts from individual thought leaders. |
| **linkedin-image-generator** | Creates visual assets for posts using AI image generation (Nano Banana MCP). |
| **linkedin-company-pages** | Autonomous posting to your company pages with distinct positioning per page. |

### Prospecting & ICP

| Skill | Description |
|-------|-------------|
| **linkedin-icp-finder** | Discovers and classifies contacts (Prospect, Peer, Thought Leader) using geography, role, company size, and industry filters. |
| **linkedin-profile-icp** | Analyzes a LinkedIn profile to extract ICP targeting criteria. |
| **web-icp-scanner** | Finds ICP prospects outside LinkedIn through web searches, news, directories, and events. |
| **linkedin-post-finder** | Discovers high-engagement posts from thought leaders in your niche (past 24h). |

### Engagement & Warming

| Skill | Description |
|-------|-------------|
| **linkedin-pro-commenter** | Generates authentic comments (max 50 words) that add genuine value. Auto-selects best variation. |
| **linkedin-icp-warmer** | Manages the warming pipeline (0-touch to 3+ touches) for ICP prospects before connection requests. |
| **linkedin-connect-timer** | Determines optimal timing for connection requests based on the 2-3 Touch Rule and engagement history. |

### Monitoring & Trends

| Skill | Description |
|-------|-------------|
| **linkedin-algorithm-monitor** | Weekly scan for LinkedIn algorithm changes. Compares findings against your current strategy and proposes updates. |
| **x-trender** | Analyzes X.com/Twitter trends for cross-platform content ideas. |

### Utilities

| Skill | Description |
|-------|-------------|
| **mcp-builder** | Build MCP servers to integrate external APIs. |

## How It Works

```
linkedin-onboarding     Configure once for your business
        |
   start linkedin        Launches daily autonomous workflow
        |
   Morning Block         Feed discovery, algorithm training, 9 comments
        |                (3 Peers, 3 Prospects, 3 Thought Leaders)
   Content Block         Trending topic analysis -> post generation -> schedule
        |
   Midday Block          Golden Hour engagement, reply to comments
        |
   Afternoon Block       Connection requests, DMs, outreach
        |
   Evening Block         Daily audit, metrics review, inbound screening
```

## Daily Limits (360Brew Compliant)

| Action | Daily Limit |
|--------|-------------|
| Posts | 1-2 (12h gap) |
| Comments | 30 max |
| Connection requests | 15 max |
| DMs | 25 max |
| Profile views | 80 max |

## Project Structure

```
linkedin-skills-suite/
├── linkedin-core/
│   ├── references/              # Personalized config generated by onboarding
│   │   ├── icp-profile.md
│   │   ├── linkedin-strategy.md
│   │   ├── contact-classification.md
│   │   ├── connect-request.md
│   │   ├── saved-asset.md
│   │   └── company-pages-config.md
│   └── shared/
│      ├── linkedin-account-config.md
│      ├── logs/                 # Activity tracking
│      └── references/           # Shared workflows
├── linkedin-daily-planner/      # Main orchestrator
├── linkedin-elite-post/         # Post generation
├── linkedin-pro-commenter/      # Comment generation
├── linkedin-icp-finder/         # Prospect discovery
├── linkedin-icp-warmer/         # Pipeline warming
├── linkedin-connect-timer/      # Connection timing
├── linkedin-trender/            # Feed trend analysis
├── linkedin-company-pages/      # Company page management
├── linkedin-algorithm-monitor/  # Algorithm change tracking
├── linkedin-onboarding/         # First-time setup
│   └── references/templates/    # Onboarding templates
└── ...
```

## Requirements

- Codex-compatible agent runtime
- Browser automation MCP (for example `chrome-devtools` or `playwright`)
- LinkedIn account (Free, Premium, or Sales Navigator supported)

## Skill Format

- Skills are folder-based and use `SKILL.md` as the entry file.
- Legacy top-level `*.skill` files are not used.
- Each skill must include frontmatter with `name` and `description`.

## Client Personalization

- Onboarding now writes `linkedin-core/references/client-profile.json` with client-specific values.
- Tokenized files use `{{CLIENT_*}}` placeholders that are rendered from that profile.
- Apply rendering manually (or from onboarding) with:

```bash
python linkedin-core/shared/scripts/render-client-config.py --profile linkedin-core/references/client-profile.json
```

## Configuration

All personalization lives in `linkedin-core/references/` files generated by `linkedin-onboarding`. To reconfigure:

1. Run `linkedin-onboarding` again
2. Or edit reference files directly

No hardcoded geography, company names, or industry — everything reads from your config files dynamically.

## For Skill Authors

Client data files (config, logs, account settings) are listed in `.gitignore` and are **not tracked** by git. When you push updates:

- All `SKILL.md` files, scripts, templates, and shared references update normally
- Client config in `linkedin-core/references/` and `linkedin-core/shared/logs/` is never touched
- New clients run `setup.ps1` / `setup.sh` after cloning to create placeholder files

To add a new client-generated file: add its path to `.gitignore` and add a placeholder entry in both `setup.ps1` and `setup.sh`.

## License

Private use. Not for redistribution.
