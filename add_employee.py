#!/usr/bin/env python3
"""
Add an employee to hyper.html or winegard.html, keeping every derived number
(dept-count, pie chart, header/stats total) in sync in one shot.

Scope: regular department members only (the .dept-person / .dept-members
lists). The CEO/C-suite/VP rows (hyper.html) and the flat exec row
(winegard.html) use different, one-off templates and are NOT handled here —
add those by hand (or ask Claude), same as before.

Usage:
    python3 add_employee.py --company hyper --dept Engineering \
        --name "Jane Doe" --title "Software Engineer" --level staff \
        --email jdoe@hyper.com --phone "(804) 555-1212"

    python3 add_employee.py --company winegard --dept Engineering \
        --name "Jane Doe" --title "Software Engineer" --level staff \
        --email jane.doe@winegard.com

Run with --dry-run first to preview without writing anything.
"""
import argparse
import base64
import html
import mimetypes
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

EMAIL_SVG = '<svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M3 4a2 2 0 00-2 2v1.161l8.441 4.221a1.25 1.25 0 001.118 0L19 7.162V6a2 2 0 00-2-2H3z"/><path d="M19 8.839l-7.77 3.885a2.75 2.75 0 01-2.46 0L1 8.839V14a2 2 0 002 2h14a2 2 0 002-2V8.839z"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>'

HYPER_LEVELS = {
    "director": "Director",
    "manager": "Manager",
    "senior": "Senior",
    "lead": "Lead",
    "staff": "Staff",
}
WINEGARD_LEVELS = {
    "director": "Director",
    "manager": "Manager",
    "senior": "Senior",
    "lead": "Lead",
    "staff": "Staff",
}
WINEGARD_PALETTE = [
    "#45B7D1", "#4ECDC4", "#6C5CE7", "#6C63FF", "#74B9FF", "#85C1E2",
    "#98D8C8", "#A3E4D7", "#BB8FCE", "#D5F4E6", "#F7DC6F", "#F8B88B",
    "#FADBD8", "#FDCB6E", "#FF6B6B", "#FF8C42", "#FFA07A",
]

HYPER_DEPTS = [
    "Executive Office & Strategy", "Engineering", "Operations & Manufacturing",
    "Supply Chain", "Product", "Quality", "Sales & Revenue",
    "Finance & Accounting", "Marketing", "Service", "Legal", "Human Resources",
]
WINEGARD_DEPTS = [
    "Engineering", "Software & IT", "Sales & Business Development",
    "Operations & Manufacturing", "Supply Chain & Logistics", "Quality",
    "Marketing", "Technical & Field Services", "Finance & Administration",
    "Customer Service", "Facilities & Safety",
]


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def initials(name):
    parts = name.split()
    if len(parts) == 1:
        return (parts[0][:2]).upper()
    return (parts[0][0] + parts[-1][0]).upper()


def find_matching_close(s, start):
    """Given the index of a '<div' tag's opening '<', return the index just
    past its matching '</div>'."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", s[start:]):
        depth += 1 if m.group() == "<div" else -1
        if depth == 0:
            return start + m.end()
    return -1


def phone_href(phone):
    return re.sub(r"\D", "", phone)


def build_hyper_person(name, title, level, email, phones, photo_b64, photo_mime):
    lvl_class = f"lvl-{level}"
    dp_level = HYPER_LEVELS[level]
    name_esc = html.escape(name)
    title_esc = html.escape(title)

    if photo_b64:
        avatar = (f'<img src="data:{photo_mime};base64,{photo_b64}" class="dp-avatar" '
                  f'style="width:30px;height:30px;border-radius:50%;object-fit:cover;flex-shrink:0;" />')
    else:
        avatar = f'<div class="dp-avatar">{initials(name)}</div>'

    ci_wrap = ""
    if email or phones:
        links = []
        if email:
            links.append(f'<a href="mailto:{email}" class="ci" title="{html.escape(email)}">{EMAIL_SVG}</a>')
        for p in phones:
            links.append(f'<a href="tel:{phone_href(p)}" class="ci" title="{html.escape(p)}">{PHONE_SVG}</a>')
        ci_wrap = f'<div class="ci-wrap">{"".join(links)}</div>'

    return (f'<div class="dept-person {lvl_class}">{avatar}<div class="dp-info">'
            f'<div class="dp-name">{name_esc}</div><div class="dp-title">{title_esc}</div></div>'
            f'{ci_wrap}<div class="dp-level">{dp_level}</div></div>\n')


def build_winegard_person(name, title, level, email, phones):
    badge_label = WINEGARD_LEVELS[level]
    name_esc = html.escape(name)
    title_esc = html.escape(title)
    color = random.choice(WINEGARD_PALETTE)

    contact_info = ""
    if email or phones:
        links = []
        if email:
            links.append(f'<a href="mailto:{email}" class="ci" title="{html.escape(email)}">{EMAIL_SVG}</a>')
        for p in phones:
            links.append(f'<a href="tel:{phone_href(p)}" class="ci" title="{html.escape(p)}">{PHONE_SVG}</a>')
        contact_info = f'<div class="contact-info">{"".join(links)}</div>\n'

    return (
        '                        <div class="dept-person">\n'
        '                            <div class="dept-person-header">\n'
        f'                                <div class="avatar" style="background: {color};">{initials(name)}</div>\n'
        '                                <div class="dept-person-info">\n'
        f'                                    <div class="dept-person-name">{name_esc}</div>\n'
        f'                                    <div class="dept-person-title">{title_esc}</div>\n'
        '                                </div>\n'
        '                            </div>\n'
        f'                            <span class="badge {level}">{badge_label}</span>\n'
        f'{contact_info}'
        '                        </div>\n'
    )


def add_to_hyper(args):
    path = ROOT / "hyper.html"
    html_src = path.read_text(encoding="utf-8")

    dept_html = html.escape(args.dept).replace("'", "&#39;")
    marker = f'data-dept="{dept_html}"'
    dept_start = html_src.find(marker)
    if dept_start == -1:
        die(f"department {args.dept!r} not found in hyper.html (looked for {marker!r})")

    dept_list_start = html_src.find('class="dept-list">', dept_start)
    if dept_list_start == -1:
        die("could not find dept-list for this department")
    div_open = html_src.rfind("<div", 0, dept_list_start)
    dept_list_close = find_matching_close(html_src, div_open)
    insert_at = html_src.rfind("</div>", 0, dept_list_close)

    person_html = build_hyper_person(
        args.name, args.title, args.level, args.email, args.phone,
        args.photo_b64, args.photo_mime,
    )

    new_html = html_src[:insert_at] + person_html + html_src[insert_at:]

    # dept-count: scope the search to this department's header only
    header_region_end = html_src.find("dept-body", dept_start)
    count_m = re.search(r'(dept-count">(?:[^<]*?)(\d+)( members))',
                         new_html[dept_start:header_region_end + 200])
    if not count_m:
        die("could not find dept-count for this department")
    old_count = int(count_m.group(2))
    new_count = old_count + 1
    abs_start = dept_start + count_m.start(2)
    abs_end = dept_start + count_m.end(2)
    new_html = new_html[:abs_start] + str(new_count) + new_html[abs_end:]

    # pie chart entry (plain "&", not "&amp;")
    js_name = html.unescape(args.dept)
    pie_m = re.search(r'(name:"' + re.escape(js_name) + r'",count:)(\d+)', new_html)
    if not pie_m:
        die(f"could not find pie chart entry for {js_name!r}")
    old_pie = int(pie_m.group(2))
    new_html = new_html[:pie_m.start(2)] + str(old_pie + 1) + new_html[pie_m.end(2):]

    # header team total
    total_m = re.search(r'("count">)(\d+)( Team Members)', new_html)
    if not total_m:
        die("could not find header team total")
    old_total = int(total_m.group(2))
    new_html = new_html[:total_m.start(2)] + str(old_total + 1) + new_html[total_m.end(2):]

    return path, new_html, {
        "dept-count": (old_count, new_count),
        "pie chart": (old_pie, old_pie + 1),
        "header total": (old_total, old_total + 1),
    }


def add_to_winegard(args):
    path = ROOT / "winegard.html"
    html_src = path.read_text(encoding="utf-8")

    marker = f'<span class="dept-name">{html.escape(args.dept)}</span>'
    dept_start = html_src.find(marker)
    if dept_start == -1:
        die(f"department {args.dept!r} not found in winegard.html (looked for {marker!r})")

    members_start = html_src.find('class="dept-members">', dept_start)
    if members_start == -1:
        die("could not find dept-members for this department")
    div_open = html_src.rfind("<div", 0, members_start)
    members_close = find_matching_close(html_src, div_open)
    insert_at = html_src.rfind("</div>", 0, members_close)

    person_html = build_winegard_person(args.name, args.title, args.level, args.email, args.phone)
    new_html = html_src[:insert_at] + person_html + html_src[insert_at:]

    total_m = re.search(
        r'(<div class="stat-number">)(\d+)(</div>\s*<div class="stat-label">Total Team Members</div>)',
        new_html,
    )
    if not total_m:
        die("could not find 'Total Team Members' stat")
    old_total = int(total_m.group(2))
    new_html = new_html[:total_m.start(2)] + str(old_total + 1) + new_html[total_m.end(2):]

    return path, new_html, {"stats total": (old_total, old_total + 1)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--company", required=True, choices=["hyper", "winegard"])
    ap.add_argument("--dept", required=True, help="Exact department name (see --list-depts)")
    ap.add_argument("--name", required=True, help="Full name")
    ap.add_argument("--title", required=True, help="Job title")
    ap.add_argument("--level", required=True, choices=["director", "manager", "senior", "lead", "staff"])
    ap.add_argument("--email", default=None)
    ap.add_argument("--phone", action="append", default=[], help="Repeatable; e.g. --phone \"Work: (804) 555-1212\"")
    ap.add_argument("--photo", default=None, help="Path to a headshot image (hyper.html only)")
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing the file")
    ap.add_argument("--list-depts", action="store_true", help="Print valid department names for --company and exit")
    args = ap.parse_args()

    if args.list_depts:
        depts = HYPER_DEPTS if args.company == "hyper" else WINEGARD_DEPTS
        print("\n".join(depts))
        return

    valid_depts = HYPER_DEPTS if args.company == "hyper" else WINEGARD_DEPTS
    if args.dept not in valid_depts:
        die(f"{args.dept!r} is not a valid department for {args.company}. "
            f"Valid options:\n  " + "\n  ".join(valid_depts))

    if args.photo and args.company == "winegard":
        die("winegard.html doesn't use photos (initials-only avatars) — drop --photo")

    args.photo_b64 = None
    args.photo_mime = None
    if args.photo:
        photo_path = Path(args.photo)
        if not photo_path.is_file():
            die(f"photo not found: {args.photo}")
        mime, _ = mimetypes.guess_type(str(photo_path))
        args.photo_mime = mime or "image/jpeg"
        args.photo_b64 = base64.b64encode(photo_path.read_bytes()).decode("ascii")

    if args.company == "hyper":
        path, new_html, changes = add_to_hyper(args)
    else:
        path, new_html, changes = add_to_winegard(args)

    print(f"Adding {args.name} ({args.title}, {args.level}) to {args.company}/{args.dept}")
    for label, (old, new) in changes.items():
        print(f"  {label}: {old} -> {new}")

    if args.dry_run:
        print("\n--dry-run: no files written")
        return

    path.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {path.name}. Review the diff, then commit.")


if __name__ == "__main__":
    main()
