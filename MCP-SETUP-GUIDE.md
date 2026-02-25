# MCP Setup Guide for LinkedIn Skills Suite

This guide will help you set up the Model Context Protocol (MCP) servers required to run the LinkedIn Skills Suite with full automation capabilities.

## Overview

The LinkedIn Skills Suite uses MCP servers to extend Codex's capabilities for browser automation, CRM integration, and optional video creation. Not all MCPs are required - choose based on your needs.

## MCP Requirements by Priority

### ✅ Required: Browser Automation
**Primary: Chrome DevTools MCP** (Recommended)
- Enables LinkedIn automation (posting, commenting, profile visits)
- Best user experience with visual feedback
- **Fallback: Playwright MCP** (automatic if Chrome DevTools MCP unavailable)

### 🔵 Optional: CRM Integration
**HubSpot CRM MCP**
- Syncs LinkedIn prospects to HubSpot
- Tracks engagement and pipeline stages
- Requires HubSpot account + API key

### ⚪ Optional: Video Creation
**Kling AI MCP**
- Generates AI videos for Instagram Reels and short-form content
- Only needed if using video creation skills
- Requires Kling AI API key

---

## Quick Start: API Keys Setup

**Before installing any MCPs**, set up your API keys:

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your API keys:**
   - All API keys go in this ONE file
   - The file is already in `.gitignore` (safe from git)
   - See `.env.example` for all available options

3. **Which keys do you need?**
   - **Browser automation:** No API keys needed (Chrome DevTools MCP extension handles it)
   - **HubSpot CRM:** Get from HubSpot Settings → Private Apps
   - **Email finder:** Pick ONE service (Apollo, Hunter, Snov.io, etc.)
   - **Video creation:** Optional - only if using video skills

---

## Installation Instructions

### 1. Install Chrome DevTools MCP (Primary Browser Automation)

**Step 1: Install the Chrome Extension**
1. Open Chrome browser
2. Visit the Chrome Web Store
3. Search for "Chrome DevTools MCP"
4. Click "Add to Chrome"
5. Pin the extension to your toolbar

**Step 2: Configure Codex Code Integration**
1. Open Codex Code CLI
2. The extension should auto-detect and connect
3. Test by running: `/skill linkedin-onboarding`
4. If prompted, authorize the extension connection

**Verification:**
```bash
# You should see browser automation tools available
codex --list-tools | grep "mcp__chrome-devtools"
```

---

### 2. Install Playwright MCP (Fallback Browser Automation)

Playwright is automatically used as a fallback if Chrome DevTools MCP is unavailable. No additional setup required - it's built into Codex Code.

**Verification:**
```bash
# Check if Playwright tools are available
codex --list-tools | grep "mcp__playwright"
```

---

### 3. Install HubSpot CRM MCP (Optional)

**Prerequisites:**
- HubSpot account (free or paid)
- HubSpot Private App with API key

**Step 1: Get HubSpot API Key**
1. Log in to HubSpot
2. Go to Settings → Integrations → Private Apps
3. Click "Create a private app"
4. Name it "Codex LinkedIn Skills Suite"
5. Grant scopes:
   - `crm.objects.contacts` (Read/Write)
   - `crm.objects.companies` (Read/Write)
   - `crm.objects.deals` (Read/Write)
   - `crm.schemas.contacts.write` (for custom properties)
6. Generate and copy the API key

**Step 2: Setup API Keys**

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Open `.env` and add your API keys:
```bash
# Edit .env file
HUBSPOT_API_KEY=your_actual_hubspot_key_here
HUBSPOT_PORTAL_ID=your_actual_portal_id_here

# Optional: Add email enrichment keys (you only need one)
APOLLO_API_KEY=your_apollo_key_here
# ... or any other email finder service
```

**Step 3: Install the MCP Server**

The HubSpot CRM MCP is included in the repository under `crm-integration/`.

1. Install Python dependencies:
```bash
cd crm-integration
pip install -r requirements.txt
```

**Step 4: Register with Codex Code**

1. Copy the MCP configuration template:
```bash
cp .mcp.json.example .mcp.json
```

2. Edit `.mcp.json` and update the path to your installation:

**For Windows**:
```json
{
  "mcpServers": {
    "hubspot-crm": {
      "command": "python",
      "args": [
        "C:\\path\\to\\linkedin-skills-suite\\crm-integration\\hubspot_mcp.py"
      ],
      "env": {
        "HUBSPOT_API_KEY": "${HUBSPOT_API_KEY}",
        "HUBSPOT_PORTAL_ID": "${HUBSPOT_PORTAL_ID}"
      }
    }
  }
}
```

**For Mac/Linux**:
```json
{
  "mcpServers": {
    "hubspot-crm": {
      "command": "python3",
      "args": [
        "/path/to/linkedin-skills-suite/crm-integration/hubspot_mcp.py"
      ],
      "env": {
        "HUBSPOT_API_KEY": "${HUBSPOT_API_KEY}",
        "HUBSPOT_PORTAL_ID": "${HUBSPOT_PORTAL_ID}"
      }
    }
  }
}
```

**Note:** The `${VARIABLE}` syntax tells Codex Code to read values from your `.env` file.

**Step 4: Setup HubSpot Properties**

Run the setup command to create custom LinkedIn pipeline properties:
```
In Codex Code: "setup hubspot properties"
```

This creates custom fields:
- `linkedin_profile` (LinkedIn URL)
- `lead_classification` (PROSPECT/THOUGHT LEADER/PEER)
- `touch_count` (Engagement count)
- `last_touch_date` (Last engagement)
- `connection_status` (none/pending/connected/rejected)

**Verification:**
```bash
# In Codex Code, check if HubSpot tools are available
/tools | grep "hubspot"
```

---

### 4. Install Kling AI MCP (Optional - Video Creation)

Only install this if you plan to use video creation skills (`instagram-reel-creator`, `short-video-creator`).

**Prerequisites:**
- Kling AI account
- Kling AI API key

**Step 1: Get Kling AI API Key**
1. Sign up at https://klingai.com
2. Navigate to API settings
3. Generate an API key
4. Copy the key

**Step 2: Install Kling MCP**
```bash
# Install via npm
npm install -g @modelcontextprotocol/server-kling
```

**Step 3: Configure Codex Code**

Add to your `mcp.json`:
```json
{
  "mcpServers": {
    "mcp-kling": {
      "command": "mcp-server-kling",
      "env": {
        "KLING_API_KEY": "your_kling_api_key_here"
      }
    }
  }
}
```

**Verification:**
```bash
# Check if Kling tools are available
/tools | grep "kling"
```

---

## Skill Capabilities by MCP Setup

### Without Any MCPs:
✅ Content generation (posts, comments)
✅ Strategy analysis
✅ ICP profiling
❌ Browser automation (posting, commenting on LinkedIn)
❌ CRM sync
❌ Video creation

### With Chrome DevTools MCP Only:
✅ Everything above, plus:
✅ Automated LinkedIn posting
✅ Automated commenting
✅ Profile scanning and classification
✅ Feed analysis
✅ Connection requests
❌ CRM sync
❌ Video creation

### With Chrome DevTools MCP + HubSpot CRM:
✅ Everything above, plus:
✅ Auto-sync prospects to HubSpot
✅ Pipeline tracking
✅ Engagement logging as CRM notes
✅ Deal stage automation

### With Chrome DevTools MCP + Kling AI:
✅ Everything above, plus:
✅ AI-generated Instagram Reels
✅ Short-form video creation
✅ Video content from trending topics

---

## Testing Your Setup

Run these commands in Codex Code to verify each integration:

**Test Browser Automation:**
```
In Codex: "Check if browser automation is available"
```

**Test HubSpot CRM (if installed):**
```
In Codex: "Get my HubSpot pipeline summary"
```

**Test Video Creation (if installed):**
```
In Codex: "Check Kling AI connection"
```

---

## Troubleshooting

### Chrome DevTools MCP Not Connecting
1. Ensure Chrome extension is installed and pinned
2. Check if extension is enabled in Chrome settings
3. Restart Codex Code
4. Try clicking the extension icon and selecting "Connect to Codex Code"

### HubSpot CRM Tools Not Available
1. Verify API key is correct in `mcp.json`
2. Check HubSpot Private App has correct scopes
3. Ensure Python dependencies are installed
4. Check MCP server logs: `~/.codex/logs/mcp-hubspot-crm.log`

### Playwright Fallback Not Working
- Playwright is built-in to Codex Code, no action needed
- If skills fail, ensure Codex Code is updated to latest version

### Kling AI Not Responding
1. Verify API key is valid
2. Check account has available credits
3. Test API key directly: https://klingai.com/api/docs

---

## Skill Onboarding

After setting up MCPs, run the onboarding skill to customize the suite for your business:

```
In Codex Code: "/skill linkedin-onboarding"
```

This will guide you through configuring:
- Your ICP (Ideal Customer Profile)
- Geographic focus
- Industry/niche
- Content pillars
- Engagement strategy

---

## Support

**Documentation:** https://github.com/<your-org>/linkedin-skills-suite/wiki
**Issues:** https://github.com/<your-org>/linkedin-skills-suite/issues
**Community:** [Your Discord/Slack link]

---

## Next Steps

1. ✅ Install required browser automation (Chrome DevTools MCP)
2. ⚙️ Run `/skill linkedin-onboarding` to customize
3. 🚀 Start with: `In Codex: "start linkedin"` for daily automation
4. 📊 Optional: Install HubSpot CRM for pipeline tracking
5. 🎥 Optional: Install Kling AI for video content creation

Happy automating! 🤖
