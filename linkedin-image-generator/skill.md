---
name: linkedin-image-generator
description: Generate images for LinkedIn posts using Nano Banana MCP server with intelligent prompt recommendations. Use when linkedin-elite-post creates content that needs visual assets (schemas, diagrams, conceptual images). Uses nano-banana-prompts skill for curated prompt library and nanobanana MCP tools for generation.
---

# LinkedIn Image Generator

Generate professional images for LinkedIn posts using the Nano Banana MCP server (Google Gemini 2.5 Flash Image) with intelligent prompt recommendations from a 6000+ prompt library.

## Trigger

**Auto-trigger from linkedin-elite-post:**
- When a Save-Worthy Asset post is created (schema, diagram, PRD)
- When post content references visual elements
- When user requests image for a post

**Manual trigger:**
- "generate image for this post"
- "create visual for linkedin"
- "make an image for my post"
- "linkedin post image"

## Prerequisites

- Nano Banana MCP server configured (`nanobanana_mcp.py`)
- GEMINI_API_KEY environment variable set
- nano-banana-prompts skill installed (for prompt recommendations)

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

### Step 2: Get Prompt Recommendations

Use the **nano-banana-prompts** skill to find suitable prompts:

1. **Invoke nano-banana-prompts skill** with image need based on post analysis
2. **Skill searches** the 6000+ prompt library across relevant categories:
   - Infographic/Educational visuals for Save-Worthy Assets
   - Social Media posts for general LinkedIn content
   - Product Marketing for demos/features
3. **Receive 1-3 prompt recommendations** with sample images
4. **Select best prompt** or request custom generation if no match

**Example invocation:**
```
Skill: nano-banana-prompts
Args: "professional infographic showing AI agent workflow with 5 connected nodes for LinkedIn B2B audience"
```

### Step 3: Customize Prompt (if needed)

If using a template from the library:
- Adapt generic elements to your specific post topic
- Maintain professional style and LinkedIn-appropriate aesthetic
- Ensure 16:9 or 1:1 aspect ratio for best LinkedIn display

If generating custom prompt:
- Follow prompt engineering guidelines below
- Include style, composition, and technical details

### Step 4: Generate Image via Nano Banana MCP

**Use nanobanana MCP tools** to generate the image:

1. **Call nanobanana_generate_image tool:**
   ```
   mcp__nanobanana__generate_image(
     prompt="[Selected/customized prompt from Step 2-3]",
     model="gemini-2.5-flash-image",  # Fast, high quality
     image_size="2K",  # 2048x2048, good for LinkedIn
     aspect_ratio="16:9",  # LinkedIn recommended for posts
     output_path="./linkedin-image-generator/assets/generated/[topic]-image.png",
     response_format="markdown"
   )
   ```

2. **Tool handles:**
   - Sending request to Gemini API
   - Waiting for generation (10-30 seconds)
   - Downloading and saving image automatically
   - Returns image path and generation details

3. **Image saved to:**
   ```
   C:\Users\melve\.claude\skills\linkedin-image-generator\assets\generated\[topic]-image.png
   ```

### Step 5: Verify Generated Image

**Check the MCP tool response:**
- Image path confirmation
- Generation successful status
- Any warnings or notes

**Quality check:**
- Image matches prompt requirements
- Professional quality for LinkedIn
- Readable on mobile (high contrast)
- No unwanted elements

### Step 6: Return Image Path

Output to user:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ IMAGE GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: [Post topic]
Image type: [Diagram / Conceptual / Process]
Resolution: 2K (2048px)
Aspect Ratio: 16:9

📁 Saved to:
./linkedin-image-generator/assets/generated/[topic]-image.png

Ready for LinkedIn post scheduling.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Note:** The image file path can be used directly when scheduling the LinkedIn post via browser automation.

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
8. **Proceed to scheduling** via browser automation

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

## Browser Automation Element References

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
mcp__claude-in-chrome__upload_image(
  imageId="ss_xxxxxxxx",
  tabId=1234567,
  ref="ref_XX",  # ref of input[type="file"]
  filename="diagram.png"
)

# Method 2: Using coordinates (drag-drop to upload area)
mcp__claude-in-chrome__upload_image(
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
