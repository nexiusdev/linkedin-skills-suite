# Evergreen LinkedIn Topics (Fail-Safe Content)

**Purpose:** Backup topics to use when trending analysis fails or returns no suitable content.

These are proven, high-engagement topics that work any time of year and align with your positioning.

---

## Tier 1: Highest Engagement (Use First)

### 1. Signs Your SME Needs Agentic Automation
**Hook:** "3 signs your finance team is drowning in spreadsheets (and how agentic AI fixes it)"

**Angle:** Problem identification → Solution preview

**Visual:** Before/after comparison diagram

---

### 2. The Hidden Cost of Manual Processes
**Hook:** "Your SME loses 15 hours/week to manual data entry. Here's the actual dollar cost."

**Angle:** Quantified pain point → ROI of automation

**Visual:** Cost breakdown infographic

---

### 3. Agentic ERP vs Traditional ERP
**Hook:** "Traditional ERP: You adapt to the software. Agentic ERP: Software adapts to you."

**Angle:** Paradigm shift explanation

**Visual:** Side-by-side comparison table

---

## Tier 2: Educational Content

### 4. What is Agentic AI? (Non-Technical)
**Hook:** "Agentic AI explained like you're the CEO of a 50-person company"

**Angle:** Simple explanation, SME context

**Visual:** Simple process flow diagram

---

### 5. When NOT to Use AI Automation
**Hook:** "5 business processes where manual work beats automation every time"

**Angle:** Contrarian, builds trust through honesty

**Visual:** Decision tree: automate vs keep manual

---

### 6. The AI-Native SME Playbook
**Hook:** "Building an AI-native business from day one: lessons from 10 startups in your target market"

**Angle:** Case study compilation

**Visual:** Framework diagram

---

## Tier 3: Tactical How-To

### 7. Quick Win: Automate Your First Workflow
**Hook:** "Pick ONE process to automate first. Here's how to choose wisely."

**Angle:** Practical first-step guide

**Visual:** Decision flowchart

---

### 8. Data Schema Design for Non-Coders
**Hook:** "How to design your database structure without writing a single line of code"

**Angle:** Empowering non-technical founders

**Visual:** Sample schema visualization

---

### 9. Integration Architecture 101
**Hook:** "Connecting your finance, CRM, and inventory systems: A visual guide"

**Angle:** Technical made accessible

**Visual:** Integration map

---

## Tier 4: Thought Leadership

### 10. The Democratization of Enterprise Software
**Hook:** "Why 2026 is the year SMEs get enterprise capabilities at startup budgets"

**Angle:** Industry trend prediction

**Visual:** Timeline graphic

---

### 11. AI's Impact on SME Job Roles
**Hook:** "Agentic AI won't replace your team. It will upgrade them to strategic roles."

**Angle:** Reassuring + visionary

**Visual:** Job evolution map

---

### 12. The Frontier Firm Advantage
**Hook:** "Being a 'frontier firm' in your market: Early adopter wins in AI-native business"

**Angle:** Positioning your audience as innovators

**Visual:** Adoption curve with competitive advantage zones

---

## Topic Selection for Autonomous Mode

**Algorithm:**
```
current_day = get_day_of_week()

IF monday:
  USE Tier 1 topic (problem-focused)
ELSE IF tuesday:
  USE Tier 3 topic (tactical how-to)
ELSE IF wednesday:
  USE Tier 2 topic (educational)
ELSE IF thursday:
  USE Tier 4 topic (thought leadership)
ELSE IF friday:
  USE personal story/reflection (not from this list)

ROTATE through unused topics to avoid repetition
LOG last used topic + date
```

**Rotation Tracking:**
Store in `shared/logs/linkedin-activity.md` under "Evergreen Topics Used" section

---

## Usage Notes

- **When to use:** Only when linkedin-trender fails or returns no suitable trending topics
- **Don't overuse:** Max 1 evergreen post per week (prefer trending topics)
- **Customize:** Adapt hook and angle to recent news or your experience
- **Visual generation:** Use linkedin-image-generator with topic as prompt

---

## Refresh Schedule

**Review quarterly:**
- Remove low-performing evergreen topics
- Add new proven topics based on recent high-engagement posts
- Update hooks to match current LinkedIn style trends
