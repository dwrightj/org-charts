# Org Charts

## Project
Static site with three self-contained HTML files (each embeds its own CSS/JS; only `assets/` is shared):
- `index.html` — landing page linking to the two company charts below. Branded with Delta Thermal's own logo/favicon (this is our internal hub, not a Hyper or Winegard page).
- `hyper.html` — Hyper org chart (~300KB, some employee cards use embedded base64 photos).
- `winegard.html` — Winegard Manufacturing org chart (~90KB, avatars are colored initials only, no photos).

Reference spreadsheets (LinkedIn exports used to cross-check chart completeness — noisy, contain many non-employees and duplicate/stale entries, not authoritative on their own):
- `hyper-members.xlsx`
- `winegard-members.xlsx`

Every HTML/subpage links back to `index.html` via a fixed `.home-link` ("← All Org Charts") in the top-left corner — keep this on any new subpage.

`add_employee.py` — CLI for adding a regular department member to either chart without hand-editing HTML or forgetting to update a count. See "Workflow for adding an employee" below.

### `assets/` — pulled brand assets
Logos/favicons pulled directly from each company's live site, kept as their original file type (SVG where the source had one):
- `hyper-favicon.svg`, `hyper-logo.svg` — from hyper.com (`<link rel="icon">` and the theme's header logo asset). The logo is the white-on-transparent variant (source also has a blue variant, not used, since hyper.html's theme is dark).
- `hyper-icon.svg` — the globe/network mark only, no "HYPER" wordmark, extracted from `hyper-logo.svg` (its ~57 dot/network paths all start at x<45 in that file's viewBox, vs the wordmark paths which start at x>50 — that's how they were told apart). Used for the square badge icon on `index.html`'s Hyper card.
- `winegard-logo.svg` — from winegardmfg.com's Wix-hosted favicon shape asset. That source SVG bundles the full illustrated logo (robot arm + wordmark) as ~86 paths; this file keeps only the circular navy "W" mark (extracted its exact path + a tight viewBox) since that's the only piece that reads at icon size. Used as the favicon, the header icon in `winegard.html`, and the badge icon on `index.html`'s Winegard card — one file, three jobs.
- `delta-logo.png`, `delta-favicon.png` — from deltathermalinc.com (WordPress media library), used only on `index.html`.

If a source site changes its branding, re-pull with `curl`/`grep` for `<link rel="icon">` and logo `<img>`/`background` refs in the page source — see the git history around when these were added for the exact commands used per site (Wix sites in particular don't expose a clean `<img>` tag for the header logo; you have to inspect rendered SVG shapes in a real browser and find the fill-color paths, e.g. via `mcp__Claude_Browser__javascript_tool`).

## Dev server
Defined in `.claude/launch.json`. Start with the "Static File Server" configuration (Python 3.12, port 3000). Serves the whole directory, so all three HTML files are reachable directly.

## Git
Remote uses SSH: `git@github.com:dwrightj/org-charts.git`
Commit email: `4613846+dwrightj@users.noreply.github.com`

## hyper.html structure

### Leadership tiers (top of chart)
- CEO: `<div class="card ceo">` inside `.ceo-row` (~line 170).
- C-suite: `<div class="card csuite">` inside the first `.exec-row` (~line 196).
- VP row: `<div class="card vp">` inside the second `.exec-row` (~line 237).
Each leadership card has a `ci-wrap` div for contact icons (email/phone) where available.

Immediately below the VP row sits `.eo-block-standalone` (~line 272) — a normal `.dept` block (data-dept="Executive Office & Strategy", holding Anand Krishna and Kimberly Baker) that's just centered under the VPs with `margin-top`, not connected to the CEO/C-suite by any line. It used to hang off the C-suite row via an absolutely-positioned `.eo-connector`/`.eo-side` pair; that broke (content overflowed the viewport horizontally) once tried at the VP tier, so it was simplified to plain centered flow instead. If you need to reposition it again, prefer flow-based centering over absolute positioning flanking a row — the row's own width plus a flanking side-panel easily exceeds the viewport at normal screen widths, and an absolutely-positioned sibling's `height:100%`/`top:0` only resolves against the nearest *positioned ancestor*, not a sibling, so a flanking-box approach needs the shared parent (not the row itself) to hold `position:relative`.

### Department sections
Departments start ~line 222. Each dept is `<div class="dept ..." data-dept="Name">` with:
- `dept-header` — contains `dept-name` and `dept-count` (must be kept accurate — this is plain text like `"9 members"` or `"Reports to CFO · 6 members"`, not auto-computed)
- `dept-body > dept-list` — contains `dept-person` divs

Current department line numbers: Executive Office & Strategy 274 (now centered under the VP row, not up by the C-suite — see the Leadership tiers note above), Engineering 297, Operations & Manufacturing 329, Supply Chain 349, Product 371, Quality 385, Sales & Revenue 401, Finance & Accounting 417, Marketing 431, Service 441, Legal 452, Human Resources 461. Re-`grep -n 'data-dept="'` after edits since insertions shift everything below.

### Employee card levels
| Class | Used for |
|---|---|
| `lvl-director` | Directors |
| `lvl-vp` | VPs (in dept sections, not the VP row) |
| `lvl-manager` | Managers |
| `lvl-senior` | Senior staff |
| `lvl-staff` | Staff / Specialists |

### Employee card template (no photo)
```html
<div class="dept-person lvl-staff"><div class="dp-avatar">AB</div><div class="dp-info"><div class="dp-name">First Last</div><div class="dp-title">Job Title</div></div><div class="ci-wrap"><a href="mailto:email@hyper.com" class="ci" title="email@hyper.com">EMAIL_SVG</a><a href="tel:8001234567" class="ci" title="Work: (800) 123-4567">PHONE_SVG</a></div><div class="dp-level">Staff</div></div>
```
`dp-avatar` initials = first letter of first name + first letter of last name.
`dp-level` text matches the level: Director / Manager / Senior / Staff.

### Contact icon SVGs (shared by both hyper.html and winegard.html)
**Email:**
```html
<svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M3 4a2 2 0 00-2 2v1.161l8.441 4.221a1.25 1.25 0 001.118 0L19 7.162V6a2 2 0 00-2-2H3z"/><path d="M19 8.839l-7.77 3.885a2.75 2.75 0 01-2.46 0L1 8.839V14a2 2 0 002 2h14a2 2 0 002-2V8.839z"/></svg>
```
**Phone:**
```html
<svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
```
**LinkedIn** (same `.ci` treatment, just a 24x24 viewBox — used on leadership/VP cards when we have someone's profile URL; add `target="_blank" rel="noopener"` since it's external):
```html
<a href="https://www.linkedin.com/in/USERNAME/" class="ci" title="LinkedIn" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.446-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
```
If the person has no `ci-wrap` yet (no email/phone on file), add one just for the LinkedIn link, same as any other `ci-wrap`.

For pulling a real headshot from a LinkedIn profile URL: an anonymous fetch of the profile page (`curl` with a browser User-Agent) usually gets blocked into a sign-up wall, but the page's `<meta property="og:image">` tag still carries their public profile-photo URL (`media.licdn.com/...`) even when the rest of the page is gated — `grep -o '<meta property="og:image"[^>]*>'` on the curl'd HTML. Crop/resize to 100x100 (`sips -z 100 100`) to match the existing embedded-photo convention before base64-encoding.

### Photo cards
When a headshot is available, replace the `dp-avatar` initials div with:
```html
<img src="data:image/jpeg;base64,BASE64_HERE" class="dp-avatar" style="width:30px;height:30px;border-radius:50%;object-fit:cover;flex-shrink:0;" />
```
Generate base64: `base64 -i photo.jpg | tr -d '\n'`

### Pie chart data
~Line 472. JS array `const data=[...]` — each entry has `name`, `count`, and `color`. **Update `count` whenever dept OR leadership-tier headcount changes** — `"Executive Leadership"` covers CEO + C-suite + VP row combined, so it's easy to forget when adding/moving an exec.

### Header team count
The `.count` badge near the top (`"89 Team Members · Henrico / Glen Allen, Virginia"`) is plain static text — it does **not** auto-total from the cards. Recompute and update it manually whenever headcount changes.

## winegard.html structure

Different template from hyper.html (built independently) — same idea, different class names. Avatars default to colored-initial divs; a photo has been added for at least one person (Dean Kostan) by replacing that div with the same `<img class="avatar" style="object-fit:cover;">` pattern hyper.html uses (the shared `.avatar` class already sets width/height/border-radius, so no extra sizing is needed) — same base64-embed convention as hyper.html, just not the default here.

### Leadership tier
Exec cards use `class="card"` with `card-name` / `card-title` (not `dp-name`/`dept-person-name`), around line 759 onward, one row of CEO/President/CFO/VPs/Directors together (no separate CEO/C-suite/VP tiers like Hyper).

### Department sections
Grouped into two `.dept-tier` wrappers (~line 835 and ~1254). Each dept is `<div class="dept">` with `dept-name` (no per-dept `dept-count` element — unlike Hyper, member counts aren't displayed per department, only in the global stats block).

Current department line numbers: Engineering 839, Software & IT 1082, Sales & Business Development 1167, Operations & Manufacturing 1258, Supply Chain & Logistics 1369, Quality 1492, Marketing 1541, Technical & Field Services 1616, Finance & Administration 1703, Customer Service 1752, Facilities & Safety 1789. Re-`grep -n '<span class="dept-name">'` after edits.

### Employee card template (no photo)
```html
<div class="dept-person">
    <div class="dept-person-header">
        <div class="avatar" style="background: #HEXCOLOR;">AB</div>
        <div class="dept-person-info">
            <div class="dept-person-name">First Last</div>
            <div class="dept-person-title">Job Title</div>
        </div>
    </div>
    <span class="badge staff">Staff</span>
<div class="contact-info"><a href="mailto:email@winegard.com" class="ci" title="email@winegard.com">EMAIL_SVG</a></div>
</div>
```
Badge classes: `badge vp`, `badge director`, `badge manager`, `badge lead`, `badge senior`, `badge staff` (see `.badge.*` CSS rules ~line 323 for the level list). Avatar background colors are arbitrary distinct hex values, not tied to level.

### Stats block
`.stats-container` (~line 738) has three static numbers: Total Team Members, Departments, Leadership. **Update "Total Team Members" whenever headcount changes** — like Hyper, this is plain text, not computed.

## Workflow for adding an employee (either chart)

### Preferred: `add_employee.py`
For a regular department member (not a leadership-tier add — see below), use the script instead of hand-editing:
```
python3 add_employee.py --company hyper --dept Engineering \
    --name "Jane Doe" --title "Software Engineer" --level staff \
    --email jdoe@hyper.com --phone "(804) 555-1212"

python3 add_employee.py --company winegard --dept Engineering \
    --name "Jane Doe" --title "Software Engineer" --level staff \
    --email jane.doe@winegard.com
```
It inserts the card (matching the exact per-site template, including a photo via `--photo path.jpg` for hyper.html) and updates every derived count in the same run: `dept-count`, the pie chart entry, and the header/stats team total (hyper.html) or just the stats total (winegard.html — it has no per-dept count or pie chart). `--level` is one of `director|manager|senior|lead|staff`; `--dept` must match one of the existing department names exactly (`--list-depts` prints the valid list per company; a typo fails loudly rather than silently misfiling someone). Run with `--dry-run` first to preview the count changes before it writes anything. Still `git diff` the result before committing — the script gets the mechanics right, but doesn't know whether this is a genuine new hire vs. a duplicate name-variant already in the chart (see the cross-checking section below).

Out of scope for the script: the CEO/C-suite/VP rows (hyper.html) and the flat exec row (winegard.html) — those use different one-off templates. Add those by hand (or ask Claude) following the same manual steps below, and remember the pie chart's `"Executive Leadership"` entry covers CEO + C-suite + VP combined.

### Manual (leadership-tier adds, or if you'd rather not use the script)
1. `grep -n 'data-dept="DeptName"'` (hyper.html) or `grep -n '<span class="dept-name">DeptName'` (winegard.html) to find the section.
2. Read that section (small enough ranges are fine directly; avoid reading a whole hyper.html photo-heavy section at once — base64 blobs blow up token counts, so `sed -n` + strip `data:image/...` or target narrow line ranges).
3. Insert the new card via Edit, matching the existing template exactly (avatar/initials, level badge, contact icons if email/phone known).
4. Update `dept-count` (hyper.html only).
5. Update the matching entry in the pie chart `const data` array (hyper.html only).
6. Update the header `.count` team total (hyper.html) or `.stats-container` total (winegard.html).
7. Commit and push.

## Cross-checking against the LinkedIn export spreadsheets
Both xlsx files are raw LinkedIn scrapes: heavy on duplicate name variants (e.g. "Ben Schnurbusch" vs "Benjamin Schnurbusch"), personal-brand headlines instead of real titles, and unrelated people who merely share a name or a loose LinkedIn connection (e.g. Winegard family members with careers at other companies, teachers, other companies' employees). Don't add a row just because it's in the sheet — only add entries with a clearly Winegard/Hyper-specific title, or a company email address, and check first whether they're already in the chart under a name variant.
