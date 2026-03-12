# Read Reference (PDF Slide Reader)

Read large PDF planning documents (기획서) and store content in `.omc/reference/` for efficient reuse.
Handles both text and images via Claude's vision capability.

## Overview

Large PDFs exceed Claude's 20-page-per-read limit. This skill uses a 2-stage approach:

1. **Index Stage**: Parse table of contents → build section map
2. **Read Stage**: Read only the requested section's page range

All content is stored in `.omc/reference/` for later use without re-reading.

## Storage Structure

```
.omc/reference/
├── {filename}-index.md          ← TOC index (created in Stage 1)
└── {filename}/
    ├── 01-intro.md
    ├── 02-feature-design.md
    └── 03-timeline.md
```

## Stage 1: Index the PDF

Run this when first receiving a new PDF reference document.

### Step 1. Read the first pages (cover + TOC)

```
Read(file_path="{path/to/file.pdf}", pages="1-5")
```

Increase page range if the TOC spans more pages.

### Step 2. Extract section structure

From the TOC, identify:
- Section name
- Start page / end page (estimated from next section's start)
- Brief description (if visible)

### Step 3. Write the index file

Save to `.omc/reference/{filename}-index.md`:

```markdown
# {Document Title} — Index

**Source:** {original file path}
**Total pages:** {N}
**Indexed:** {date}

## Sections

| # | Section | Pages | Summary |
|---|---------|-------|---------|
| 01 | Introduction | 1–4 | Project background and goals |
| 02 | Feature Design | 5–18 | Core feature specs and UI flows |
| 03 | Timeline | 19–24 | Milestones and schedule |
| 04 | Appendix | 25–30 | Reference materials |
```

## Stage 2: Read a Section

Run this when a task requires the content of a specific section.

### Step 1. Check the index

```
Read(file_path=".omc/reference/{filename}-index.md")
```

Locate the section and its page range.

### Step 2. Read the section pages

Claude's limit is 20 pages per read. Split into chunks if needed:

```
# Single chunk (≤ 20 pages)
Read(file_path="{path/to/file.pdf}", pages="{start}-{end}")

# Multiple chunks (> 20 pages)
Read(file_path="{path/to/file.pdf}", pages="{start}-{start+19}")
Read(file_path="{path/to/file.pdf}", pages="{start+20}-{end}")
```

### Step 3. Process content (text + images)

Add a `**[이미지 설명]**` block immediately after the `## Page N` heading **only when the page contains visual elements** (UI mockups, diagrams, flowcharts, tables, icons, screenshots). Skip for pure text slides.

When writing a description, cover:
- **UI mockups**: layout structure, button labels, positions (top/bottom/left/right), badge positions, color highlights
- **Flowcharts/diagrams**: box count, flow direction (left→right / top→bottom), decision diamonds, branch paths
- **Tables**: column names, row count, highlighted rows, cell content summary
- **Icons/images**: subject, style, arrangement

Write descriptions in Korean. Be specific enough that the image can be understood without viewing it.

### Step 4. Write the section file

Save to `.omc/reference/{filename}/{##-section-name}.md`:

```markdown
# {Section Name} (pp. {start}–{end})

**Source:** {original file path}
**Pages:** {start}–{end}

---

## Page {N}

**[이미지 설명]**
{Korean description of all visual elements on this page — layout, colors, labels, flow direction, etc.}

{text content extracted from page}

---

## Page {N+1}

...
```

## Checklist

### Stage 1 (Index)
- [ ] First pages read (cover + full TOC)
- [ ] All sections listed with page ranges
- [ ] Index saved to `.omc/reference/{filename}-index.md`

### Stage 2 (Section Read)
- [ ] Index checked before reading
- [ ] Pages split into ≤ 20-page chunks if needed
- [ ] `**[이미지 설명]**` block added for every page with visual elements (UI, diagram, table, screenshot)
- [ ] Text-only pages have no image description block
- [ ] Descriptions are in Korean and specific enough to replace the image
- [ ] Section saved to `.omc/reference/{filename}/{##-name}.md`

## When to Use Each Stage

| Situation | Action |
|-----------|--------|
| First time receiving a PDF | Stage 1: Index only |
| Task needs specific content | Stage 2: Read relevant section |
| Unsure which section is relevant | Read index → identify section → Stage 2 |
| Section already saved | Read from `.omc/reference/` directly (no PDF re-read) |

## Anti-patterns

```
# ❌ Reading the whole PDF upfront
Read(pages="1-20")
Read(pages="21-40")
...  # Wastes context on irrelevant sections

# ✅ Index first, read only what's needed
Read(pages="1-5")  # TOC only
# → identify relevant section
Read(pages="12-18")  # That section only
```

```
# ❌ Skipping image description
## Page 7
(no description of the UI mockup shown)

# ✅ Describe all visual content
## Page 7
**[Image: Login screen mockup]**
Two-panel layout. Left: email/password fields with "Sign In" CTA.
Right: social login buttons (Google, Facebook). Error state shown below email field.
```

```
# ❌ Re-reading PDF every session
Read(file_path="spec.pdf", pages="5-18")  # Already read before

# ✅ Check .omc/reference/ first
Read(file_path=".omc/reference/spec/02-feature-design.md")  # Instant
```
