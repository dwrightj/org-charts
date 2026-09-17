# Hyper Solutions Org Chart

## Project
Single-file HTML org chart for Hyper Solutions (`index.html`, ~260KB). All employee cards, styles, and scripts are embedded in one file.

## Dev server
Defined in `.claude/launch.json`. Start with the "Static File Server" configuration (Python 3.12, port 3000).

## Git
Remote uses SSH: `git@github.com:dwrightj/org-charts.git`
Commit email: `4613846+dwrightj@users.noreply.github.com`

## index.html structure

### VP row (top of chart)
Around line 238. VP cards use `class="card vp"` inside `<div class="exec-row">`. Each card has a `ci-wrap` div for contact icons.

### Department sections
Departments start around line 282. Each dept is a `<div class="dept ...">` with:
- `dept-header` — contains `dept-name` and `dept-count` (must be kept accurate)
- `dept-body > dept-list` — contains `dept-person` divs

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

### Contact icon SVGs
**Email:**
```html
<svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M3 4a2 2 0 00-2 2v1.161l8.441 4.221a1.25 1.25 0 001.118 0L19 7.162V6a2 2 0 00-2-2H3z"/><path d="M19 8.839l-7.77 3.885a2.75 2.75 0 01-2.46 0L1 8.839V14a2 2 0 002 2h14a2 2 0 002-2V8.839z"/></svg>
```
**Phone:**
```html
<svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
```

### Photo cards
When a headshot is available, replace the `dp-avatar` initials div with:
```html
<img src="data:image/jpeg;base64,BASE64_HERE" class="dp-avatar" style="width:30px;height:30px;border-radius:50%;object-fit:cover;flex-shrink:0;" />
```
Generate base64: `base64 -i photo.jpg | tr -d '\n'`

### Pie chart data
Around line 472. JS array `const data=[...]` — each entry has `name`, `count`, and `color`. **Update `count` whenever dept headcount changes.**

## Workflow for adding an employee
1. `grep -n "dept-name.*DeptName" index.html` to find the department section line.
2. `sed -n 'START,ENDp' index.html` to read the section and find the right insertion point.
3. Use a Python script for the actual string replacement (file is too large for direct Edit on some lines).
4. Update `dept-count` in the dept header.
5. Update the matching entry in the pie chart `const data` array.
6. Commit and push.

## Departments and approximate line numbers
| Department | ~Line |
|---|---|
| Executive Leadership (VP row) | 238 |
| Executive Office & Strategy | 225 |
| Engineering | 287 |
| Operations & Manufacturing | 319 |
| Supply Chain | 336 |
| Product | 356 |
| Quality | 373 |
| Sales & Revenue | 389 |
| Finance & Accounting | 405 |
| Marketing | ~430 |
| Service | ~440 |
| Legal | ~455 |
| Human Resources | ~460 |
