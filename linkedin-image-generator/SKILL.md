---
name: linkedin-image-generator
description: Generate images for LinkedIn posts using Gemini via browser MCP (Chrome DevTools or Playwright). Use when linkedin-elite-post creates content that needs visual assets (schemas, diagrams, conceptual images). Automatically crafts effective prompts, navigates to Gemini, generates images, and saves them locally for post scheduling.
---

# LinkedIn Image Generator

Generate professional images for LinkedIn posts using Google Gemini via browser MCP (Chrome DevTools or Playwright) browser automation.

## Trigger

**Auto-trigger from linkedin-elite-post:**
- When a Save-Worthy Asset post is created (schema, diagram, PRD)
- When post content references visual elements
- When user requests image for a post

**Manual trigger:**
- "generate image for this post"
- "create visual for linkedin"
- "make an image for my post"
- "gemini image for linkedin"

## Prerequisites

- Chrome browser with Gemini tab available (gemini.google.com)
- User logged into Google account with Gemini access
- browser MCP (Chrome DevTools or Playwright) MCP tools available

## Image Types by Post Mode

| Post Mode | Image Type | Visual Style |
|-----------|------------|--------------|
| Save-Worthy Asset (Schema) | Database/system diagram | Clean, technical, dark theme |
| Save-Worthy Asset (Logic Map) | Flowchart/process diagram | Step-by-step, arrows, icons |
| Save-Worthy Asset (PRD) | Document/template preview | Professional, structured |
| Thought Leadership | Conceptual/abstract | Bold, modern, minimal text |
| Educational | Infographic style | Clear hierarchy, numbered steps |
| Evidence/Demo | Screenshot-style mockup | UI elements, realistic |

## Workflow

### Step 1: Analyze Post Content

Extract from the LinkedIn post:
1. **Core topic**: Main subject (e.g., "multi-agent orchestration")
2. **Key concepts**: Technical terms, frameworks mentioned
3. **Visual elements described**: Any schemas, diagrams, or visuals referenced
4. **Target audience**: Technical vs non-technical
5. **Post mode**: Save-Worthy Asset, Thought Leadership, etc.

### Step 2: Determine Image Strategy

Based on post analysis, select image approach:

**A. Technical Diagram** (for schemas, architectures)
- Clean, professional diagram
- Dark or light theme based on preference
- Labeled components
- Clear flow/relationships

**B. Conceptual Visual** (for thought leadership)
- Abstract representation of the concept
- Modern, professional aesthetic
- Minimal or no text in image
- Brand-appropriate colors

**C. Process/Flow Visual** (for educational)
- Step-by-step visualization
- Numbered or sequential
- Icons for each step
- Clear start/end points

### Step 3: Craft Gemini Prompt

**Prompt Template:**

```
Create a professional LinkedIn post image for [TOPIC].

Image requirements:
- Style: [Technical diagram / Conceptual illustration / Process flowchart]
- Theme: [Dark mode with blue accents / Light professional / Modern minimal]
- Dimensions: 1200x627 pixels (LinkedIn recommended)
- Text in image: [None / Minimal labels only / Key terms]

Content to visualize:
[KEY CONCEPTS FROM POST]

Visual elements to include:
[SPECIFIC ELEMENTS - e.g., "5 connected nodes showing agent workflow"]

Aesthetic:
- Clean, professional, suitable for B2B audience
- High contrast for mobile viewing
- No stock photo feel - should look like a custom diagram/illustration

Do NOT include:
- Watermarks
- Generic clip art
- Busy backgrounds
- Hard to read text
```

### Step 4: Generate Image via Gemini (browser MCP (Chrome DevTools or Playwright))

**Browser Automation Steps:**

1. **Get browser context**
   ```
   Use tabs_context_mcp to find existing Gemini tab or create new one
   ```

2. **Navigate to Gemini**
   ```
   Navigate to: https://gemini.google.com/app
   Wait for page load
   ```

3. **Input prompt**
   ```
   Find the text input field (prompt box)
   Enter the crafted image generation prompt
   Submit the prompt (Enter or click send button)
   ```

4. **Wait for generation**
   ```
   Wait for image to appear in response
   Gemini typically generates in 10-30 seconds
   Look for image element in the response area
   ```

5. **Capture image as screenshot (CRITICAL)**
   ```
   Click on the generated image to view it in full/expanded mode
   Use computer tool with action="screenshot" to capture the image
   SAVE THE SCREENSHOT ID (e.g., "ss_xxxxxxxx") - this is needed for LinkedIn upload
   ```

### Step 5: Store Screenshot ID

**IMPORTANT:** Do NOT download the image to a file. Instead:

1. The screenshot ID from Step 4 is your image reference
2. Store this ID for use with the `upload_image` MCP tool
3. This bypasses the native file picker limitation

**Screenshot ID format:**
```
ss_[random_string]

Example: ss_7312xts41
```

### Step 6: Upload to LinkedIn via upload_image Tool

**Why this approach:**
- Native OS file pickers cannot be controlled by browser automation
- The `upload_image` MCP tool can upload a screenshot directly to a file input
- This creates a seamless, fully automated workflow

**Upload workflow:**

1. **Navigate to LinkedIn post composer**
   ```
   Navigate to linkedin.com/feed
   Click "Start a post"
   Enter post content
   ```

2. **Open image upload dialog**
   ```
   Click the image/media icon in the composer
   The "Editor" modal appears with "Upload from computer" button
   ```

3. **Find the file input element**
   ```
   Use read_page tool with filter="interactive" to find the hidden file input
   Look for input[type="file"] element and note its ref_id
   ```

4. **Upload using upload_image tool**
   ```
   Use mcp__playwright__browser_file_upload with:
   - imageId: [screenshot ID from Step 5, e.g., "ss_7312xts41"]
   - tabId: [current LinkedIn tab ID]
   - ref: [file input ref_id] OR coordinate: [drop zone coordinates]
   - filename: "[topic]-diagram.png"
   ```

5. **Verify upload and continue**
   ```
   Wait for image to appear in the composer
   Click "Next" or "Done" to confirm
   Proceed to scheduling
   ```

### Step 7: Return Status

Output to user:
```
========================================
IMAGE GENERATED & ATTACHED
========================================
Topic: [Post topic]
Image type: [Diagram / Conceptual / Process]
Screenshot ID: [ss_xxxxxxxx]
Status: ATTACHED to LinkedIn post

Ready to schedule your post.
========================================
```

## Prompt Engineering for LinkedIn Images

### For Technical Schemas (Save-Worthy Assets)

```
Create a clean technical diagram showing [SYSTEM/SCHEMA].

Visual structure:
- [X] main components as labeled boxes/nodes
- Arrows showing data flow / relationships
- Color coding: [primary action = blue, data = green, etc.]

Style: Professional technical documentation
Background: Dark (#1a1a2e) with light elements
No decorative elements - pure information design

Components to show:
1. [Component 1]: [Description]
2. [Component 2]: [Description]
3. [Component 3]: [Description]

Relationships:
- [Component 1] → [Component 2]: [Label]
- [Component 2] → [Component 3]: [Label]
```

### For Thought Leadership (Conceptual)

```
Create an abstract professional illustration representing [CONCEPT].

Mood: [Innovative / Transformative / Strategic / Technical]
Style: Modern, minimal, suitable for LinkedIn B2B audience
Colors: Professional palette (blues, teals, subtle gradients)

Visual metaphor suggestions:
- [Metaphor 1 related to concept]
- [Metaphor 2 related to concept]

Do NOT include:
- Text or words
- Generic business imagery (handshakes, globes)
- Clip art style elements

Should feel: Custom, thoughtful, aligned with AI/tech industry
```

### For Process/Educational

```
Create a process flow visualization for [PROCESS NAME].

Steps to show:
1. [Step 1]: [Brief description]
2. [Step 2]: [Brief description]
3. [Step 3]: [Brief description]
[Continue for all steps]

Visual style:
- Horizontal or vertical flow
- Each step as a distinct node/card
- Icons representing each step's action
- Connecting arrows between steps

Colors:
- Steps: Gradient progression (light to dark)
- Arrows: Subtle, not overpowering
- Background: Clean, light or dark theme

Labels: Minimal - just step numbers or 1-2 word labels
```

## Integration with linkedin-elite-post

**Fully automated workflow - no user selection required:**

```
linkedin-elite-post → AI auto-selects best variation → linkedin-image-generator
→ Gemini generates image → Screenshot captured → upload_image attaches to LinkedIn
→ Schedule post with image already attached
```

When linkedin-elite-post generates a Save-Worthy Asset or any post needing visuals:

1. **linkedin-elite-post generates variations** and **auto-selects the best one**
2. **Auto-detect visual need** from selected post content:
   - References to "schema," "diagram," "framework," "map"
   - "[Attach: PDF/Image of schema]" placeholder in output
   - Save-Worthy Asset mode selected
3. **This skill auto-invoked** with selected post content
4. **Generate image in Gemini**
5. **Capture screenshot** of the generated image (store screenshot ID)
6. **Navigate to LinkedIn** and open post composer
7. **Use upload_image tool** to attach the screenshot directly
8. **Proceed to scheduling** via browser MCP (Chrome DevTools or Playwright)

User can override at any point: "use variation 2" or "regenerate image"

**Key technical detail:**
The `upload_image` MCP tool bypasses the native OS file picker by:
- Taking a screenshot ID (from any previous screenshot action)
- Uploading directly to a file input element or drag-drop zone
- No manual file selection required

**Update post output** with attachment status:
   ```
   ========================================
   IMAGE ATTACHED
   ========================================
   Screenshot ID: ss_xxxxxxxx
   Status: Uploaded to LinkedIn composer

   Ready to schedule the post.
   ========================================
   ```

## browser MCP (Chrome DevTools or Playwright) Element References

**Gemini interface elements:**

| Element | Description | How to Find |
|---------|-------------|-------------|
| Prompt input | Main text area for prompts | Large text input at bottom of page |
| Send button | Submit prompt | Arrow/send icon next to input |
| Response area | Where images appear | Main content area above input |
| Image element | Generated image | `<img>` within response, or canvas element |
| Download option | Save image | Right-click menu or hover options on image |

**LinkedIn post composer elements:**

| Element | Description | How to Find / Use |
|---------|-------------|-------------------|
| Post composer | Main modal | Click "Start a post" on feed |
| Image icon | Opens media upload | First icon in toolbar (photo icon) |
| Editor modal | Upload interface | Appears after clicking image icon |
| Upload button | "Upload from computer" | Blue button in Editor modal |
| File input | Hidden input element | Use read_page to find input[type="file"] |
| Drop zone | Drag-drop area | Center of Editor modal (~693, 300) |

**Using upload_image for LinkedIn:**

```
# Method 1: Using ref (if file input found)
mcp__playwright__browser_file_upload(
  imageId="ss_xxxxxxxx",
  tabId=1234567,
  ref="ref_XX",  # ref of input[type="file"]
  filename="diagram.png"
)

# Method 2: Using coordinates (drag-drop to upload area)
mcp__playwright__browser_file_upload(
  imageId="ss_xxxxxxxx",
  tabId=1234567,
  coordinate=[693, 300],  # Center of upload area
  filename="diagram.png"
)
```

**Automation notes:**
- Gemini may require scrolling to see full response
- Image generation shows loading indicator first
- Multiple images may be generated - select best one
- If generation fails, retry with simplified prompt
- For LinkedIn: Method 2 (coordinates) often more reliable than ref

## Troubleshooting

**"Gemini can't generate that image"**
- Simplify the prompt
- Remove any potentially flagged terms
- Make request more generic, add specifics in follow-up

**Image quality issues**
- Request specific dimensions (1200x627)
- Ask for "high resolution" or "crisp, detailed"
- Avoid complex scenes with many elements

**upload_image tool fails**
- Ensure the screenshot ID is valid and recent (from current session)
- Try using coordinates instead of ref if file input is hidden
- Use drag-drop approach: find the drop zone and use coordinate parameter
- Verify tabId is correct (use tabs_context_mcp to confirm)

**Can't find file input element**
- LinkedIn may hide the actual input[type="file"] element
- Use read_page with depth=15 to find nested elements
- Alternative: Use coordinate-based drag-drop to the upload area
- The "Upload from computer" button area accepts drag-drop

**Screenshot doesn't capture full image**
- Click on the image to expand it before taking screenshot
- Use the zoom action to capture a specific region
- Ensure the browser window is large enough

**LinkedIn upload area not responding**
- Wait for the Editor modal to fully load
- Scroll to ensure the upload area is visible
- Try clicking "Upload from computer" first, then use upload_image

## Quality Checklist

Before uploading image:
- [ ] Image matches post topic/theme
- [ ] Professional quality (not cartoonish unless appropriate)
- [ ] Readable on mobile (high contrast)
- [ ] No unwanted text/watermarks
- [ ] Screenshot captured at full size (click to expand in Gemini)
- [ ] Screenshot ID saved for upload_image tool

After uploading to LinkedIn:
- [ ] Image appears correctly in composer
- [ ] No cropping issues
- [ ] Ready to proceed to scheduling

## Screenshot ID Management

**Session-based approach:**
- Screenshot IDs are valid only for the current browser session
- No need to manage files on disk
- If session ends, regenerate the image and take a new screenshot

**Best practice:**
- Take screenshot immediately after image generates
- Keep the screenshot ID handy (note it or use immediately)
- Complete the LinkedIn upload in the same session
