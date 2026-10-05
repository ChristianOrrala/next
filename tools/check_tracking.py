#!/usr/bin/env python3
"""Check the A-files that track a repository's work.

AGENTS.md holds the rules and the index of the others; ACTIVE.md the work in
progress; ABILITIES.md every ability of the product; AHEAD.md everything not
started; ATLAS.md the architecture map. Each opens with a title and a one-line
contract and has a hot zone, the top of the file ended by the line
`<!-- hot zone ends -->`, that an agent reads at every session start.

It checks shape, not truth:

  - every A-file exists, has its contract line and a hot zone within its cap;
    AGENTS.md stays under its total cap and names every A-file in its first
    100 lines
  - every section below a hot zone is named in that hot zone
  - links in a hot zone and paths in the atlas map point at something
  - ACTIVE.md has all of its fields
  - a Specs line of an ability: every link and backticked path points at a file
  - an A-file whose hot zone names a **Home:** (a tracking file kept at adoption):
    that is a file inside the project, and not an A-file or a guideline file
    under any name; the A-file's own fields, index, entries or map are not
    required
  - ABILITIES.md and AHEAD.md: identifiers in the right form, statuses and
    states from the list, no duplicates, every index row has its entry and
    every entry its row, the same status in both
  - no identifier present in the last commit is gone
  - an AHEAD item that is approved, next or started names an ability, and the
    ability exists

Output: `path:line: ERROR CODE: message`. Exit 0 clean, 1 problems, 2 usage.

Usage:
    check_tracking.py [--root DIR] [--no-git]

Requires Python 3.9+, standard library only; git for the comparison with the
last commit (skipped with a note when git or the last commit is unavailable).
"""
import argparse
import os
import re
import subprocess
import sys

MARKER = "<!-- hot zone ends -->"
# Every hot zone is read at each session start; 100 lines each keeps the
# warm-up near 400 lines with AGENTS.md.
HOT_CAP = 100
# The now-note is the most read and the most rewritten file; it stays shorter.
ACTIVE_HOT_CAP = 60
# Claude Code's guidance for an instruction file: under 200 lines.
AGENTS_CAP = 200
A_FILES = ("ACTIVE.md", "ABILITIES.md", "AHEAD.md", "ATLAS.md")
# The files an agent reads its instructions from; none of them can be the home of an A-file.
GUIDELINE_FILES = ("AGENTS.md", "CLAUDE.md")
ACTIVE_FIELDS = ("Current work", "Progress", "Next step", "Blocked by", "Waiting on owner", "Restart", "Plan", "Updated")
AB_STATUSES = ("planned", "in progress", "done", "retired")
AH_KINDS = ("idea", "research", "spike", "proposal")
AH_STATES = ("open", "approved", "next", "started", "dropped")
NEEDS_ABILITY = ("approved", "next", "started")
AB_ID = re.compile(r"\bAB-\d{3}\b")
AH_ID = re.compile(r"\bAH-\d{3}\b")
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TICKED = re.compile(r"`([^`\s]+)`")
# A field line, bulleted with - or * or not at all, as the skills' reader of the A-files reads it.
SPECS = re.compile(r"^\s*(?:[-*]\s*)?\*\*Specs:\*\*\s*(.*)$")
HOME = re.compile(r"^\s*(?:[-*]\s*)?\*\*Home:\*\*\s*(?:\[[^\]]*\]\()?`?([^`)\s]+)`?\)?")


class Report:
    def __init__(self, root):
        self.root = root
        self.items = []

    def error(self, name, line, code, message):
        self.items.append((name, line, code, message))

    def print(self):
        for name, line, code, message in sorted(self.items, key=lambda i: (i[0], i[1], i[2])):
            print("%s:%d: ERROR %s: %s" % (name, line, code, message))


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().split("\n")


def unfenced(lines):
    """The lines with everything inside fenced code blocks blanked, line numbers kept: the
    templates a file carries for itself are examples, not entries."""
    out, fence = [], None
    for line in lines:
        mark = re.match(r"^\s*(```|~~~)", line)
        if fence:
            out.append("")
            if mark and mark.group(1) == fence:
                fence = None
        elif mark:
            fence = mark.group(1)
            out.append("")
        else:
            out.append(line)
    return out


def hot_end(lines):
    """Line number (1-based) of the marker, or None."""
    return next((i + 1 for i, line in enumerate(lines) if line.strip() == MARKER), None)


def tables(lines, start=0, end=None):
    """Markdown tables: [(header cells, [(line number, {header: cell})])]."""
    end = len(lines) if end is None else end
    found, i = [], start
    while i < end - 1:
        line, below = lines[i].strip(), lines[i + 1].strip()
        if line.startswith("|") and re.match(r"^\|?\s*:?-{3,}", below):
            header = [c.strip() for c in line.strip("|").split("|")]
            rows, j = [], i + 2
            while j < end and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                rows.append((j + 1, dict(zip(header, cells))))
                j += 1
            found.append((header, rows))
            i = j
        else:
            i += 1
    return found


def is_path(token):
    if token.startswith(("http:", "https:", "mailto:", "#")) or any(c in token for c in "<>*{}$"):
        return False
    return "/" in token or re.search(r"\.[A-Za-z0-9]{1,5}$", token) is not None


def exists(root, base, target, test=os.path.exists):
    target = target.split("#", 1)[0]
    if not target:
        return True
    return test(os.path.normpath(os.path.join(base, target))) or test(os.path.join(root, target))


def is_file(root, base, target):
    """A link or path that points at a file (a folder is not a specification or a home)."""
    return exists(root, base, target, os.path.isfile)


def inside(root, path):
    real_root, real = os.path.realpath(root), os.path.realpath(path)
    return real.startswith(real_root + os.sep)


def same_file(a, b):
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def check_common(report, name, lines, cap, contract=True):
    end = hot_end(lines)
    if contract and not any(line.startswith("> ") for line in lines[1:6]):
        report.error(name, 1, "NO_CONTRACT", "the file must open with its title and a one-line contract in a quotation block (> ...)")
    if end is None:
        report.error(name, 1, "NO_HOT_ZONE_END", "no line %r ends the hot zone" % MARKER)
        return None
    if end - 1 > cap:
        report.error(name, end, "HOT_ZONE_TOO_LONG", "the hot zone has %d lines; the cap is %d" % (end - 1, cap))
    hot = "\n".join(lines[:end]).lower()
    for i, line in enumerate(lines[end:], start=end + 1):
        if line.startswith("## ") and line[3:].strip().lower() not in hot:
            report.error(name, i, "UNPOINTED_SECTION", "section %r is below the hot zone and not named in it" % line[3:].strip())
    base = os.path.dirname(os.path.join(report.root, name))
    for i, line in enumerate(lines[:end], start=1):
        for target in LINK.findall(line):
            if is_path(target) and not exists(report.root, base, target):
                report.error(name, i, "BROKEN_LINK", "%s points at nothing" % target)
    return end


def last_commit_text(root, name):
    try:
        done = subprocess.run(["git", "show", "HEAD:" + name], cwd=root, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout if done.returncode == 0 else None


def check_removed(report, name, lines, pattern, use_git):
    if not use_git:
        return
    before = last_commit_text(report.root, name)
    if before is None:
        return
    now = set(pattern.findall("\n".join(lines)))
    for identifier in sorted(set(pattern.findall("\n".join(unfenced(before.split("\n"))))) - now):
        report.error(name, 1, "REMOVED_ID", "%s was in the last commit and is gone; identifiers are never removed" % identifier)


def index_rows(lines, pattern, columns):
    """Rows of every table whose header has the columns, keyed by identifier: {id: [(line, row)]}."""
    rows = {}
    for header, table_rows in tables(lines):
        if all(c in header for c in columns):
            for number, row in table_rows:
                identifier = row.get("ID", "").strip()
                rows.setdefault(identifier, []).append((number, row))
    return rows


def entries(lines, pattern):
    """`### <id> ...` headings: {id: (line, status or state from the entry, or None)}."""
    found = {}
    for i, line in enumerate(lines):
        match = re.match(r"^###\s+(\S+)", line)
        if match and pattern.fullmatch(match.group(1)):
            status = None
            for following in lines[i + 1:i + 12]:
                if following.startswith("#"):
                    break
                field = re.match(r"^\s*-\s*\*\*(?:Status|State):\*\*\s*(.+?)\s*$", following)
                if field:
                    status = field.group(1).strip("` ")
                    break
            found.setdefault(match.group(1), []).append((i + 1, status))
    return found


def check_register(report, name, lines, pattern, columns, status_column, allowed, end, use_git):
    rows = index_rows(lines, pattern, columns)
    if not any(n <= end for ids in rows.values() for n, _ in ids):
        report.error(name, end, "NO_INDEX", "the hot zone has no index table with columns %s" % ", ".join(columns))
    heads = entries(lines, pattern)
    for identifier, found in rows.items():
        line = found[0][0]
        if not pattern.fullmatch(identifier):
            report.error(name, line, "BAD_ID", "%r is not an identifier of the form %s" % (identifier, pattern.pattern.strip("\\b")))
            continue
        if len(found) > 1:
            report.error(name, found[1][0], "DUPLICATE_ID", "%s is listed more than once" % identifier)
        value = found[0][1].get(status_column, "").strip("` ")
        if value not in allowed:
            report.error(name, line, "BAD_STATUS", "%s: %s %r is not one of %s" % (identifier, status_column.lower(), value, ", ".join(allowed)))
        if identifier not in heads:
            report.error(name, line, "NO_ENTRY", "%s has an index row but no entry (### %s ...)" % (identifier, identifier))
        elif heads[identifier][0][1] is not None and heads[identifier][0][1] != value:
            report.error(name, heads[identifier][0][0], "STATUS_MISMATCH", "%s is %r in the index and %r in its entry" % (identifier, value, heads[identifier][0][1]))
    for identifier, found in heads.items():
        if len(found) > 1:
            report.error(name, found[1][0], "DUPLICATE_ID", "%s has more than one entry" % identifier)
        if identifier not in rows:
            report.error(name, found[0][0], "NOT_IN_INDEX", "%s has an entry but no index row" % identifier)
    check_removed(report, name, lines, pattern, use_git)
    return rows


def check_specs(report, lines):
    """A Specs line names identifiers or links; every link and backticked path in it must point at a file."""
    current = None
    for i, line in enumerate(lines, start=1):
        heading = re.match(r"^###\s+(AB-\d{3})\b", line)
        if heading:
            current = heading.group(1)
            continue
        match = SPECS.match(line)
        if not match:
            continue
        value = match.group(1)
        for target in LINK.findall(value) + [t for t in TICKED.findall(value) if is_path(t)]:
            if is_path(target) and not is_file(report.root, report.root, target):
                report.error("ABILITIES.md", i, "BROKEN_SPEC", "%s: %s points at nothing" % (current or "an ability", target))


def home_of(report, name, lines, end):
    """The tracking file an A-file delegates to (**Home:** in its hot zone), or None.

    A home that names an A-file or a guideline file is an error and no home; a home that is not a file inside the
    project is an error, and the A-file still counts as kept."""
    for i, line in enumerate(lines[:end], start=1):
        match = HOME.match(line)
        if match:
            home = match.group(1).rstrip(".,;:") or match.group(1)    # a sentence's punctuation, not the name's
            path = os.path.join(report.root, home)
            taken = [other for other in GUIDELINE_FILES + A_FILES
                     if os.path.normpath(home) == other or same_file(path, os.path.join(report.root, other))]
            if taken:
                report.error(name, i, "INVALID_HOME", "%s cannot be the home of %s: name the tracking file that was kept" % (home, name))
                return None
            if not (os.path.isfile(path) and inside(report.root, path)):
                report.error(name, i, "MISSING_HOME", "%s is named as the home and is not a file in the project" % home)
            return home
    return None


def check(root, use_git):
    report = Report(root)
    files = {}
    for name in ("AGENTS.md",) + A_FILES:
        path = os.path.join(root, name)
        if not os.path.isfile(path):
            report.error(name, 1, "MISSING", "the file does not exist")
            continue
        files[name] = unfenced(read(path))

    lines = files.get("AGENTS.md")
    if lines is not None:
        if len(lines) > AGENTS_CAP:
            report.error("AGENTS.md", AGENTS_CAP, "AGENTS_TOO_LONG", "%d lines; the cap is %d" % (len(lines), AGENTS_CAP))
        end = check_common(report, "AGENTS.md", lines, HOT_CAP, contract=False)
        first = "\n".join(lines[:HOT_CAP])
        for name in A_FILES:
            if name not in first:
                report.error("AGENTS.md", 1, "NOT_INDEXED", "%s is not named in the first %d lines" % (name, HOT_CAP))

    lines = files.get("ACTIVE.md")
    if lines is not None:
        end = check_common(report, "ACTIVE.md", lines, ACTIVE_HOT_CAP)
        hot = lines[:end] if end else lines
        for field in (() if end and home_of(report, "ACTIVE.md", lines, end) else ACTIVE_FIELDS):
            if not any(re.match(r"^\s*-\s*\*\*%s:\*\*" % re.escape(field), line) for line in hot):
                report.error("ACTIVE.md", 1, "MISSING_FIELD", "the field **%s:** is missing from the hot zone" % field)

    abilities, abilities_kept = {}, False
    lines = files.get("ABILITIES.md")
    if lines is not None:
        end = check_common(report, "ABILITIES.md", lines, HOT_CAP)
        abilities_kept = bool(end and home_of(report, "ABILITIES.md", lines, end))
        if end and not abilities_kept:
            abilities = check_register(report, "ABILITIES.md", lines, AB_ID, ("ID", "Ability", "Status"), "Status", AB_STATUSES, end, use_git)
            check_specs(report, lines)

    lines = files.get("AHEAD.md")
    if lines is not None:
        end = check_common(report, "AHEAD.md", lines, HOT_CAP)
        if end and not home_of(report, "AHEAD.md", lines, end):
            items = check_register(report, "AHEAD.md", lines, AH_ID, ("ID", "Title", "Kind", "State", "Ability"), "State", AH_STATES, end, use_git)
            for identifier, found in items.items():
                line, row = found[0]
                kind = row.get("Kind", "").strip("` ")
                if kind not in AH_KINDS:
                    report.error("AHEAD.md", line, "BAD_KIND", "%s: kind %r is not one of %s" % (identifier, kind, ", ".join(AH_KINDS)))
                named = AB_ID.findall(row.get("Ability", ""))
                if row.get("State", "").strip("` ") in NEEDS_ABILITY and not named:
                    report.error("AHEAD.md", line, "NO_ABILITY", "%s is %s and names no ability (AB-0xx)" % (identifier, row.get("State", "").strip()))
                for ability in named:
                    if "ABILITIES.md" in files and not abilities_kept and ability not in abilities:
                        report.error("AHEAD.md", line, "UNKNOWN_ABILITY", "%s names %s, which ABILITIES.md does not have" % (identifier, ability))
                write_up = row.get("Write-up", "")
                for target in LINK.findall(write_up) + [t for t in TICKED.findall(write_up) if is_path(t)]:
                    if not exists(root, root, target):
                        report.error("AHEAD.md", line, "BROKEN_LINK", "%s: write-up %s points at nothing" % (identifier, target))
            hot = "\n".join(lines[:end])
            next_up = hot.split("## Next up", 1)[1].split("\n## ", 1)[0] if "## Next up" in hot else ""
            for identifier in AH_ID.findall(next_up):
                if identifier not in items:
                    report.error("AHEAD.md", 1, "UNKNOWN_ITEM", "Next up names %s, which has no index row" % identifier)

    lines = files.get("ATLAS.md")
    if lines is not None:
        end = check_common(report, "ATLAS.md", lines, HOT_CAP)
        if end and not home_of(report, "ATLAS.md", lines, end):
            maps = [(h, r) for h, r in tables(lines, 0, end) if "Part" in h and "Works through" in h]
            if not maps:
                report.error("ATLAS.md", end, "NO_MAP", "the hot zone has no map table (Part, What it does, Works through, ...)")
            for header, rows in maps:
                for number, row in rows:
                    for column in ("Works through", "Checked by"):
                        for token in TICKED.findall(row.get(column, "")):
                            if is_path(token) and not exists(root, root, token):
                                report.error("ATLAS.md", number, "MISSING_PATH", "%s: %s does not exist" % (row.get("Part", "?"), token))
    return report


def main(argv):
    parser = argparse.ArgumentParser(description="Check the A-files that track a repository's work.")
    parser.add_argument("--root", default=".", help="the repository's root folder")
    parser.add_argument("--no-git", action="store_true", help="skip the comparison with the last commit")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.root):
        print("no such folder: %s" % args.root, file=sys.stderr)
        return 2
    report = check(os.path.abspath(args.root), not args.no_git)
    report.print()
    if report.items:
        print("%d problem(s)" % len(report.items), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
