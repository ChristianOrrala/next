#!/usr/bin/env python3
"""Check the A-files that track a repository's work.

AGENTS.md holds the rules and the index of the others; ACTIVE.md the work in
progress; ABILITIES.md every ability of the product; AHEAD.md everything not
started; ATLAS.md the architecture map. Each opens with a title and a one-line
contract and has a hot zone, the top of the file ended by the line
`<!-- hot zone ends -->`, that an agent reads at every session start.

It checks shape, not truth:

  - AGENTS.md and ACTIVE.md always exist (the small setup); ABILITIES.md, AHEAD.md
    and ATLAS.md are expected once the index of AGENTS.md lists them (a table
    row in its first 100 lines whose first cell is the file), the file exists,
    or it held identifiers in the last commit
  - every expected A-file exists and can be read (UTF-8), has its contract line
    and a hot zone within its cap; AGENTS.md stays under its total cap and names
    ACTIVE.md and every other A-file that exists in its first 100 lines
  - every section below a hot zone is named in that hot zone
  - links in a hot zone and paths in the atlas map point at something
  - ACTIVE.md has all of its fields
  - a Specs line of an ability: every link and backticked path points at a file
  - an A-file whose hot zone names a **Home:** (a tracking file kept at adoption):
    that is a file inside the project, and not an A-file or a guideline file
    under any name; the A-file's own fields, index, entries or map are not
    required
  - ABILITIES.md and AHEAD.md: identifiers in the right form, statuses and
    states from the list, no duplicates across all their index tables, every
    index row has its entry and every entry its row; an old entry that still
    carries a Status line agrees with its row (the row holds the status)
  - AHEAD.md keeps index rows in its hot zone; ABILITIES.md may keep none there
    when an index table below holds them (done abilities can move below); a
    table that lacks any of the ID, Ability and Status columns, such as an area
    summary, is not an index, and the check ignores it
  - no identifier present in the last commit is gone
  - an AHEAD item that is approved, next or started names an ability, and every
    ability an item names exists in ABILITIES.md (an item naming one when there
    is no ABILITIES.md is reported too, unless the file was already reported
    MISSING or UNREADABLE: the items do not report it again)

A run by hand reads the working tree. With --staged (the commit hook's mode) it
reads every A-file and every path it checks from the git index, as the commit
will hold them, compares their identifiers with the last commit, and notes an
A-file whose changes are not staged.

Output: `path:line: ERROR CODE: message` on stdout, one line per problem; notes
(`path: NOTE: message`, or a line about git) on stderr, which never count as
problems, so that stdout holds only the problem lines a paired specification
method reads (pairing P10). Exit 0 when it ran, whatever it found: the check reports and never
refuses a commit. With --strict, 1 on problems, for a repository that chooses a
strict pipeline. 2 on usage errors. 3 when it could not run: --staged without git
or outside a git repository.

On request, for a person or a program that must tell a clean run from one that inspected nothing (each read-only,
none changes the exit codes):

  - --summary ends the run with one line on stderr: the A-files it inspected, those absent or kept elsewhere, and
    how many problems it found (in place of the line that counts the problems)
  - --format json prints one JSON object on stdout instead of the problem lines and the notes: the check's version
    and the schema of the object, the files it inspected, its findings and notes, and what it parsed (the fields of
    ACTIVE's Now, the abilities and the AHEAD items with their columns and lines)
  - --version prints the version of the A-files this check belongs to

Usage:
    check_tracking.py [--root DIR] [--no-git] [--staged] [--strict] [--summary] [--format text|json]
    check_tracking.py --version

Requires Python 3.9+, standard library only; git for the comparison with the
last commit (skipped with a note when git, the repository or the last commit is
unavailable) and for --staged.
"""
import argparse
import codecs
import enum
import errno
import json
import os
import re
import subprocess
import sys
from collections import namedtuple

# The version of the A-files this check ships with; a test keeps it equal to the plugin's manifests.
A_FILES_VERSION = "1.8.1"
# The shape of the --format json object; it rises only when a key changes its meaning or goes away.
DATA_SCHEMA = 1
MARKER = "<!-- hot zone ends -->"
# Every hot zone is read at each session start; 100 lines each keeps the
# warm-up near 400 lines with AGENTS.md.
HOT_CAP = 100
# The now-note is the most read and the most rewritten file; it stays shorter.
ACTIVE_HOT_CAP = 60
# Claude Code's guidance for an instruction file: under 200 lines.
AGENTS_CAP = 200
A_FILES = ("ACTIVE.md", "ABILITIES.md", "AHEAD.md", "ATLAS.md")
# A small setup keeps only AGENTS.md and ACTIVE.md; these three are expected once the index of AGENTS.md lists one,
# the file exists, or it held identifiers in the last commit (so a file deleted with its index line is still reported).
OPTIONAL = ("ABILITIES.md", "AHEAD.md", "ATLAS.md")
# The files an agent reads its instructions from; none of them can be the home of an A-file.
GUIDELINE_FILES = ("AGENTS.md", "CLAUDE.md")
ACTIVE_FIELDS = ("Current work", "Progress", "Next step", "Blocked by", "Waiting on owner", "Restart", "Plan", "Updated")
AB_STATUSES = ("planned", "in progress", "done", "retired")
AH_KINDS = ("idea", "research", "spike", "proposal")
AH_STATES = ("open", "approved", "next", "started", "dropped")
NEEDS_ABILITY = ("approved", "next", "started")
AB_ID = re.compile(r"\bAB-\d{3}\b")
AH_ID = re.compile(r"\bAH-\d{3}\b")
ANY_ID = re.compile(r"\b(?:AB|AH)-\d{3}\b")
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TICKED = re.compile(r"`([^`\s]+)`")
# A field line, bulleted with - or * or not at all, as the skills' reader of the A-files reads it.
SPECS = re.compile(r"^\s*(?:[-*]\s*)?\*\*Specs:\*\*\s*(.*)$")
HOME = re.compile(r"^\s*(?:[-*]\s*)?\*\*Home:\*\*\s*(?:\[[^\]]*\]\()?`?([^`)\s]+)`?\)?")
# Any field line, `- **Label:** value`, for the data output.
FIELD = re.compile(r"^\s*(?:[-*]\s*)?\*\*([^*:\n]+):\*\*\s*(.*?)\s*$")


# Every git call here is local (no network); 60 seconds is the timeout the reference check (relink.py) and the
# specification scripts give the same calls, and a call that takes longer is treated as git being unavailable.
GIT_TIMEOUT_SECONDS = 60
# The mode git gives a submodule (a gitlink) in the index: a folder of another repository, not a file.
GITLINK_MODE = "160000"
# The stage of an index entry with no merge conflict; stages 1 to 3 are the sides of an unresolved conflict.
MERGED_STAGE = "0"
# The exit code of a check that could not run (git unavailable), apart from 2, a usage error.
COULD_NOT_RUN = 3


def git(root, *args):
    """The finished git command run in the root folder (stdout as bytes), or None when git cannot run."""
    try:
        return subprocess.run(["git"] + list(args), cwd=root, capture_output=True, timeout=GIT_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired):
        return None


class Git(enum.Enum):
    """What git can tell about the root folder."""
    UNAVAILABLE = "git is not installed, or this is not a git repository"
    NO_COMMIT = "no commit yet"
    READY = "ready"

    @classmethod
    def of(cls, root):
        done = git(root, "rev-parse", "--is-inside-work-tree")
        if done is None or done.returncode != 0 or done.stdout.strip() != b"true":
            return cls.UNAVAILABLE
        done = git(root, "rev-parse", "--verify", "-q", "HEAD^{commit}")
        return cls.READY if done is not None and done.returncode == 0 else cls.NO_COMMIT


# One file in the git index: its mode, its object name and its merge stage.
Entry = namedtuple("Entry", "mode object stage")


class WorkTree:
    """The files as they are on disk: what a run by hand reads."""

    def __init__(self, root):
        self.root = root

    def missing_hint(self, path):
        """Nothing to add: on disk, a missing path is simply missing."""
        return ""

    def unstaged(self, names):
        """No staging to compare with: [(name, note)] is empty."""
        return []

    def read(self, name):
        """The file's lines, or None when it is not a file; OSError or UnicodeDecodeError when it cannot be read, a link
        that cannot be resolved in its place included, which is there and never a missing file."""
        path = os.path.join(self.root, name)
        if os.path.lexists(path) and not os.path.exists(path):
            try:
                target = " to %s" % os.readlink(path)
            except (OSError, ValueError, AttributeError):
                target = ""
            raise OSError(errno.ENOENT, "a link that cannot be resolved%s" % target, name)
        if not os.path.isfile(path):
            return None
        with open(path, encoding="utf-8") as handle:
            return handle.read().split("\n")

    def exists(self, path):
        return os.path.exists(path)

    def isfile(self, path):
        return os.path.isfile(path)

    def inside(self, path):
        real_root, real = os.path.realpath(self.root), os.path.realpath(path)
        return real.startswith(real_root + os.sep)

    def same_file(self, a, b):
        try:
            return os.path.samefile(a, b)
        except OSError:
            return False


class Index:
    """The files as the git index holds them: what the next commit will hold (--staged)."""

    def __init__(self, root, entries):
        self.root = root
        self.entries = entries                  # {path relative to the root: Entry}
        self.folders = {"/".join(path.split("/")[:n]) for path in entries for n in range(1, path.count("/") + 1)}

    @classmethod
    def load(cls, root):
        """The index of the repository the root is in, limited to the root folder; None when git cannot list it."""
        done = git(root, "ls-files", "-s", "-z")
        if done is None or done.returncode != 0:
            return None
        entries = {}
        for record in done.stdout.decode("utf-8", errors="surrogateescape").split("\0"):
            if "\t" in record:
                meta, path = record.split("\t", 1)
                entry = Entry(*meta.split(" "))
                if entry.stage != MERGED_STAGE or path not in entries:
                    entries[path] = entry
        return cls(root, entries)

    def missing_hint(self, path):
        """A hint for a path that the staged copy lacks and the working tree has."""
        return " (it is in the working tree but not staged)" if os.path.exists(path) else ""

    def unstaged(self, names):
        """[(name, note)] for each named file whose working copy differs from the staged one, as git sees it (its
        line-ending and other filters applied), or that only one of the two holds. A comparison git cannot make is
        said, never read as no change."""
        notes = []
        for name in names:
            if name in self.entries:
                done = git(self.root, "diff", "--quiet", "--", name)
                if done is None or done.returncode not in (0, 1):
                    why = "git is unavailable" if done is None else "git diff exited %d" % done.returncode
                    notes.append((name, "cannot tell whether it has unstaged changes: %s" % why))
                    continue
                changed = done.returncode == 1
            else:
                changed = os.path.lexists(os.path.join(self.root, name))
            if changed:
                notes.append((name, "has changes that are not staged: the check read the copy this commit holds"))
        return notes

    def relative(self, path):
        return os.path.relpath(os.path.normpath(path), self.root).replace(os.sep, "/")

    def blob(self, name):
        """The staged bytes of a file, or None when the index does not hold it; OSError when git cannot give them."""
        entry = self.entries.get(name)
        if entry is None:
            return None
        if entry.stage != MERGED_STAGE:
            raise OSError("the index holds unresolved conflicts for it")
        done = git(self.root, "cat-file", "blob", entry.object)
        if done is None or done.returncode != 0:
            raise OSError("git cannot read its staged copy")
        return done.stdout

    def read(self, name):
        blob = self.blob(name)
        if blob is None:
            return None
        # The line endings a run by hand sees: open() in text mode reads \r\n and \r as \n.
        return blob.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")

    def exists(self, path):
        rel = self.relative(path)
        return rel == "." or rel in self.entries or rel in self.folders

    def isfile(self, path):
        entry = self.entries.get(self.relative(path))
        return entry is not None and entry.mode != GITLINK_MODE

    def inside(self, path):
        rel = self.relative(path)
        return rel != "." and rel != ".." and not rel.startswith("../")

    def same_file(self, a, b):
        return self.relative(a) == self.relative(b)


class Report:
    def __init__(self, root, tree=None):
        self.root = root
        self.tree = tree or WorkTree(root)
        self.items = []
        self.notes = []
        # What the check read, for --summary and --format json: {A-file: {present, readable, home}}, and the registers.
        self.files = {}
        self.parsed = {"active": {"fields": {}}, "abilities": [], "ahead_items": []}
        # The registers whose rows the check read: an empty list means "no rows" only for these.
        self.registers_read = set()

    def error(self, name, line, code, message):
        self.items.append((name, line, code, message))

    def note(self, name, message):
        self.notes.append((name, message))

    def findings(self):
        return sorted(self.items, key=lambda i: (i[0], i[1], i[2]))

    def print(self):
        for name, line, code, message in self.findings():
            print("%s:%d: ERROR %s: %s" % (name, line, code, message))
        for name, message in self.notes:
            print("%sNOTE: %s" % (name + ": " if name else "", message), file=sys.stderr)

    def summary(self):
        """One line: the A-files inspected, those absent or kept elsewhere, and the number of problems."""
        parts = []
        for name in ("AGENTS.md",) + A_FILES:
            state = self.files.get(name, {})
            if not state.get("present"):
                parts.append("%s absent" % name)
            elif not state.get("readable"):
                parts.append("%s unreadable" % name)
            elif state.get("home"):
                parts.append("%s (kept in %s)" % (name, state["home"]))
            else:
                parts.append(name)
        count = len(self.items)
        return "checked %s: %d problem%s" % (", ".join(parts), count, "" if count == 1 else "s")

    def data(self, staged, compared):
        """Everything the run found and read, as one object for --format json."""
        return {
            "schema": DATA_SCHEMA,
            "a_files_version": A_FILES_VERSION,
            "mode": "staged" if staged else "working tree",
            "compared_with_last_commit": compared,
            "files": [dict(file=name, **self.files.get(name, {"present": False, "readable": False, "home": None}))
                      for name in ("AGENTS.md",) + A_FILES],
            "problems": len(self.items),
            "findings": [{"file": name, "line": line, "severity": "error", "code": code, "message": message}
                         for name, line, code, message in self.findings()],
            "notes": [{"file": name, "message": message} for name, message in self.notes],
            "active": self.parsed["active"],
            "abilities": self.parsed["abilities"],
            "ahead_items": self.parsed["ahead_items"],
            "registers": {key: self.register_state(name, key)
                          for key, name in (("abilities", "ABILITIES.md"), ("ahead_items", "AHEAD.md"))},
        }

    def register_state(self, name, key):
        """Whether the rows of a register were read, and why not: so that a register with no rows can be told from
        one whose rows the check could not read as a register."""
        if key in self.registers_read:
            return {"read": True, "reason": None}
        state = self.files.get(name, {})
        if not state.get("present"):
            reason = "absent"
        elif not state.get("readable"):
            reason = "unreadable"
        elif state.get("home"):
            reason = "kept_elsewhere"
        else:
            reason = "no_hot_zone"      # without the marker the check cannot tell the index from the entries
        return {"read": False, "reason": reason}


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


class Reference:
    """A link or path as a file writes it, read in a tree: relative to the folder of the file that names it, or
    to the root."""

    def __init__(self, tree, base, target):
        self.tree = tree
        target = target.split("#", 1)[0]
        self.places = [os.path.normpath(os.path.join(base, target)), os.path.join(tree.root, target)] if target else []

    def exists(self):
        return not self.places or any(self.tree.exists(path) for path in self.places)

    def is_file(self):
        """It points at a file (a folder is not a specification or a home)."""
        return not self.places or any(self.tree.isfile(path) for path in self.places)

    def hint(self):
        return next((hint for hint in map(self.tree.missing_hint, self.places) if hint), "")


def fields(lines, start=0, end=None):
    """The field lines `- **Label:** value` from line start to end (0-based, end excluded), each with the indented
    lines below it that continue it, joined by newlines: {label: {"value", "line"}}, the first of a label kept."""
    end = len(lines) if end is None else end
    found, running = {}, None
    for i in range(start, end):
        line = lines[i]
        match = FIELD.match(line)
        if match:
            label = match.group(1).strip()
            running = None if label in found else {"value": match.group(2), "line": i + 1}
            if running is not None:
                found[label] = running
            continue
        if running is not None and line[:1] in " \t" and line.strip():
            running["value"] = (running["value"] + "\n" + line.strip()).strip()
        elif line.strip():
            running = None
    return found


def now_fields(lines, end):
    """The fields of ACTIVE's Now: its `## Now` section in the hot zone, or the whole hot zone without one."""
    hot = lines[:end] if end else lines
    start = next((i + 1 for i, line in enumerate(hot) if re.match(r"^##\s+Now\s*$", line)), None)
    if start is None:
        return fields(hot)
    stop = next((i for i in range(start, len(hot)) if hot[i].startswith("## ")), len(hot))
    return fields(hot, start, stop)


def register_data(lines, rows, pattern, wanted):
    """The register as the check parsed it: one record per identifier, its first index row (line, the `## ` section
    it sits under, its columns) and its entry (heading line, and each wanted field as {value, line} or None); an
    entry with no row has line and section None and no columns. wanted: {key: field label}."""
    under, current = [], None
    for line in lines:
        heading = re.match(r"^##\s+(.*?)\s*$", line)
        current = heading.group(1) if heading else current
        under.append(current)
    heads = entries(lines, pattern)

    def record(identifier, number, columns):
        entry_line = heads[identifier][0][0] if identifier in heads else None
        found = {}
        if entry_line is not None:
            stop = next((i for i in range(entry_line, len(lines)) if lines[i].startswith("#")), len(lines))
            found = fields(lines, entry_line, stop)
        item = {"id": identifier, "line": number, "section": under[number - 1] if number else None,
                "columns": columns, "entry_line": entry_line}
        item.update({key: found.get(label) for key, label in wanted.items()})
        return item

    items = [record(identifier, found[0][0], dict(found[0][1])) for identifier, found in rows.items()
             if pattern.fullmatch(identifier)]
    items += [record(identifier, None, {}) for identifier in heads if identifier not in rows]
    return items


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
            reference = Reference(report.tree, base, target)
            if is_path(target) and not reference.exists():
                report.error(name, i, "BROKEN_LINK", "%s points at nothing%s" % (target, reference.hint()))
    return end


def last_commit_text(root, name):
    """The file as the last commit holds it, or None. `./` reads it relative to the root folder, which may be a
    folder inside the repository."""
    done = git(root, "show", "HEAD:./" + name)
    return done.stdout.decode("utf-8", errors="replace") if done is not None and done.returncode == 0 else None


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


def check_register(report, name, lines, pattern, columns, status_column, allowed, end, use_git, rows_below=False):
    """rows_below: the hot zone may hold no row when an index table below it holds them (ABILITIES.md)."""
    rows = index_rows(lines, pattern, columns)
    if not any(n <= end or rows_below for ids in rows.values() for n, _ in ids):
        where = "the file has no index table with a row" if rows_below else "the hot zone has no index table"
        report.error(name, end, "NO_INDEX", "%s with columns %s" % (where, ", ".join(columns)))
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
            reference = Reference(report.tree, report.root, target)
            if is_path(target) and not reference.is_file():
                report.error("ABILITIES.md", i, "BROKEN_SPEC", "%s: %s points at nothing%s"
                             % (current or "an ability", target, reference.hint()))


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
                     if os.path.normpath(home) == other or report.tree.same_file(path, os.path.join(report.root, other))]
            if taken:
                report.error(name, i, "INVALID_HOME", "%s cannot be the home of %s: name the tracking file that was kept" % (home, name))
                return None
            if not (report.tree.isfile(path) and report.tree.inside(path)):
                report.error(name, i, "MISSING_HOME", "%s is named as the home and is not a file in the project%s"
                             % (home, report.tree.missing_hint(path)))
            return home
    return None


def held_identifiers(root, name, use_git):
    """Whether the last commit's copy of the file held an identifier outside its fenced examples."""
    before = last_commit_text(root, name) if use_git else None
    return before is not None and ANY_ID.search("\n".join(unfenced(before.split("\n")))) is not None


def listed(lines):
    """The A-files the index of AGENTS.md lists. The index is a table in its first 100 lines whose rows start with
    an A-file's name (in backticks or as a link); a name elsewhere (the warm-up, keep in step, naming) is not a
    listing. An AGENTS.md with no such table names its files in prose, and every A-file named there is listed."""
    found = set()
    for header, rows in tables(lines, 0, min(len(lines), HOT_CAP)):
        for _, row in rows:
            cell = re.sub(r"\]\([^)]*\)", "", row.get(header[0], "")).strip("[]` ")
            found.add(cell[2:] if cell.startswith("./") else cell)
    found &= set(A_FILES)
    if found:
        return found
    first = "\n".join(lines[:HOT_CAP])
    return {name for name in A_FILES if name in first}


def check(root, use_git, tree=None):
    report = Report(root, tree)
    # first_lines: the text of AGENTS.md's first 100 lines; in_index: the A-files its index lists;
    # reported: the A-files already reported MISSING or UNREADABLE, so that the item check does not report them again
    # (ATLAS.md's MISSING_PATH may still name such a file as a path it lists).
    files, present, first_lines, in_index, reported = {}, set(), "", set(), set()
    for name in ("AGENTS.md",) + A_FILES:
        try:
            lines = report.tree.read(name)
        except (OSError, UnicodeDecodeError) as exc:
            # A file the check cannot read or decode is a problem like the others; its other checks are skipped.
            report.error(name, 0, "UNREADABLE", "cannot read the file: %s" % exc)
            report.files[name] = {"present": True, "readable": False, "home": None}
            present.add(name)
            reported.add(name)
            continue
        report.files[name] = {"present": lines is not None, "readable": lines is not None, "home": None}
        if lines is None:
            hint = report.tree.missing_hint(os.path.join(root, name))
            if name not in OPTIONAL or name in in_index:
                report.error(name, 1, "MISSING", "the file does not exist%s" % hint)
                reported.add(name)
            elif held_identifiers(root, name, use_git):
                report.error(name, 1, "MISSING", "the file does not exist%s, and it held identifiers in the last commit" % hint)
                reported.add(name)
            continue
        files[name] = unfenced(lines)
        present.add(name)
        if name == "AGENTS.md":
            first_lines, in_index = "\n".join(files[name][:HOT_CAP]), listed(files[name])
    for name, message in report.tree.unstaged(("AGENTS.md",) + A_FILES):
        report.note(name, message)

    lines = files.get("AGENTS.md")
    if lines is not None:
        if len(lines) > AGENTS_CAP:
            report.error("AGENTS.md", AGENTS_CAP, "AGENTS_TOO_LONG", "%d lines; the cap is %d" % (len(lines), AGENTS_CAP))
        end = check_common(report, "AGENTS.md", lines, HOT_CAP, contract=False)
        for name in A_FILES:
            # ACTIVE.md always; another A-file once it exists. One already reported MISSING is not asked for twice.
            if (name == "ACTIVE.md" or name in present) and name not in first_lines:
                report.error("AGENTS.md", 1, "NOT_INDEXED", "%s is not named in the first %d lines" % (name, HOT_CAP))

    lines = files.get("ACTIVE.md")
    if lines is not None:
        end = check_common(report, "ACTIVE.md", lines, ACTIVE_HOT_CAP)
        hot = lines[:end] if end else lines
        active_home = end and home_of(report, "ACTIVE.md", lines, end)
        report.files["ACTIVE.md"]["home"] = active_home or None
        if not active_home:
            report.parsed["active"]["fields"] = now_fields(lines, end)
        for field in (() if active_home else ACTIVE_FIELDS):
            if not any(re.match(r"^\s*-\s*\*\*%s:\*\*" % re.escape(field), line) for line in hot):
                report.error("ACTIVE.md", 1, "MISSING_FIELD", "the field **%s:** is missing from the hot zone" % field)

        if not active_home:
            for number, line in enumerate(hot, 1):
                match = re.match(r"^\s*-\s*\*\*Blocked by:\*\*\s*(.*)", line, re.I)
                if not match:
                    continue
                value = match.group(1).strip()
                if (not value or re.fullmatch(r"(?:nothing|none)[^\w\s]*", value, re.I)
                        or re.search(r"<[^>]+>", value)):
                    continue
                if not (re.search(r"\b\d{4}-\d{2}-\d{2}\b", value)
                        or re.search(r"\b(?:UC|BR)-\d+\b", value, re.I)
                        or re.search(r"(?:[\w.-]+/)*[\w.-]+\.(?:md|markdown|ya?ml|json)\b", value, re.I)
                        or re.search(r"\bfailing check:\s*\S+", value, re.I)):
                    report.error("ACTIVE.md", number, "BLOCKER_WITHOUT_SOURCE",
                                 "name a dated owner message (YYYY-MM-DD), specification ID or file path, or failing check: <name>")

    abilities, abilities_kept = {}, False
    lines = files.get("ABILITIES.md")
    if lines is not None:
        end = check_common(report, "ABILITIES.md", lines, HOT_CAP)
        home = end and home_of(report, "ABILITIES.md", lines, end)
        report.files["ABILITIES.md"]["home"] = home or None
        abilities_kept = bool(home)
        if end and not abilities_kept:
            abilities = check_register(report, "ABILITIES.md", lines, AB_ID, ("ID", "Ability", "Status"), "Status", AB_STATUSES, end,
                                       use_git, rows_below=True)
            report.parsed["abilities"] = register_data(lines, abilities, AB_ID,
                                                       {"known_limits": "Known limits", "evidence": "Evidence"})
            report.registers_read.add("abilities")
            check_specs(report, lines)

    lines = files.get("AHEAD.md")
    if lines is not None:
        end = check_common(report, "AHEAD.md", lines, HOT_CAP)
        home = end and home_of(report, "AHEAD.md", lines, end)
        report.files["AHEAD.md"]["home"] = home or None
        if end and not home:
            items = check_register(report, "AHEAD.md", lines, AH_ID, ("ID", "Title", "Kind", "State", "Ability"), "State", AH_STATES, end, use_git)
            report.parsed["ahead_items"] = register_data(lines, items, AH_ID, {"belongs_to": "Belongs to"})
            report.registers_read.add("ahead_items")
            for identifier, found in items.items():
                line, row = found[0]
                kind = row.get("Kind", "").strip("` ")
                if kind not in AH_KINDS:
                    report.error("AHEAD.md", line, "BAD_KIND", "%s: kind %r is not one of %s" % (identifier, kind, ", ".join(AH_KINDS)))
                item_abilities = AB_ID.findall(row.get("Ability", ""))
                if row.get("State", "").strip("` ") in NEEDS_ABILITY and not item_abilities:
                    report.error("AHEAD.md", line, "NO_ABILITY", "%s is %s and names no ability (AB-0xx)" % (identifier, row.get("State", "").strip()))
                for ability in item_abilities:
                    if abilities_kept or "ABILITIES.md" in reported:
                        continue                 # kept elsewhere, or reported MISSING or UNREADABLE already
                    if "ABILITIES.md" not in present:
                        report.error("AHEAD.md", line, "UNKNOWN_ABILITY", "%s names %s, and there is no ABILITIES.md" % (identifier, ability))
                    elif ability not in abilities:
                        report.error("AHEAD.md", line, "UNKNOWN_ABILITY", "%s names %s, which ABILITIES.md does not have" % (identifier, ability))
                write_up = row.get("Write-up", "")
                for target in LINK.findall(write_up) + [t for t in TICKED.findall(write_up) if is_path(t)]:
                    reference = Reference(report.tree, root, target)
                    if not reference.exists():
                        report.error("AHEAD.md", line, "BROKEN_LINK", "%s: write-up %s points at nothing%s"
                                     % (identifier, target, reference.hint()))
            hot = "\n".join(lines[:end])
            next_up = hot.split("## Next up", 1)[1].split("\n## ", 1)[0] if "## Next up" in hot else ""
            for identifier in AH_ID.findall(next_up):
                if identifier not in items:
                    report.error("AHEAD.md", 1, "UNKNOWN_ITEM", "Next up names %s, which has no index row" % identifier)

    lines = files.get("ATLAS.md")
    if lines is not None:
        end = check_common(report, "ATLAS.md", lines, HOT_CAP)
        home = end and home_of(report, "ATLAS.md", lines, end)
        report.files["ATLAS.md"]["home"] = home or None
        if end and not home:
            maps = [(h, r) for h, r in tables(lines, 0, end) if "Part" in h and "Works through" in h]
            if not maps:
                report.error("ATLAS.md", end, "NO_MAP", "the hot zone has no map table (Part, What it does, Works through, ...)")
            for header, rows in maps:
                for number, row in rows:
                    for column in ("Works through", "Checked by"):
                        for token in TICKED.findall(row.get(column, "")):
                            reference = Reference(report.tree, root, token)
                            if is_path(token) and not reference.exists():
                                report.error("ATLAS.md", number, "MISSING_PATH", "%s: %s does not exist%s"
                                             % (row.get("Part", "?"), token, reference.hint()))
    return report


def main(argv):
    parser = argparse.ArgumentParser(description="Check the A-files that track a repository's work.")
    parser.add_argument("--root", default=".", help="the repository's root folder")
    parser.add_argument("--no-git", action="store_true", help="skip the comparison with the last commit")
    parser.add_argument("--staged", action="store_true",
                        help="read the A-files and the paths they name from the git index, as the commit will hold them")
    parser.add_argument("--strict", action="store_true", help="exit 1 on problems (default: exit 0, problems are reported)")
    parser.add_argument("--summary", action="store_true",
                        help="end with one line on stderr: the A-files inspected and the number of problems")
    parser.add_argument("--format", choices=("text", "json"), default="text",
                        help="json: one object on stdout with the files inspected, the findings and the registers read")
    parser.add_argument("--version", action="version", version="a-files %s" % A_FILES_VERSION,
                        help="print the version of the A-files this check belongs to")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.root):
        print("no such folder: %s" % args.root, file=sys.stderr)
        return 2
    if args.staged and args.no_git:
        print("--staged reads the git index; it cannot run with --no-git", file=sys.stderr)
        return 2
    root = os.path.abspath(args.root)
    state = None if args.no_git else Git.of(root)
    tree = None
    if args.staged:
        tree = Index.load(root) if state is not Git.UNAVAILABLE else None
        if tree is None:
            print("--staged reads the git index and could not run: git is not installed, or %s is not in a git "
                  "repository" % args.root, file=sys.stderr)
            return COULD_NOT_RUN
    report = check(root, state is Git.READY, tree)
    if state in (Git.UNAVAILABLE, Git.NO_COMMIT):
        report.note(None, "%s: identifiers are not compared with the last commit" % state.value)
    if args.format == "json":
        print(json.dumps(report.data(args.staged, state is Git.READY), indent=2))
    else:
        report.print()
    if args.summary:
        print(report.summary(), file=sys.stderr)
    elif report.items and args.format == "text":
        print("%d problem(s)" % len(report.items), file=sys.stderr)
    if report.items:
        # The problems are the output; only a strict run turns them into a failure.
        return 1 if args.strict else 0
    return 0


# The error handlers that never end a write in an encoding error. Every other one can: strict, surrogateescape (which
# a C locale gives standard output), surrogatepass on an encoding other than UTF, and any a program registers.
SAFE_ERRORS = ("backslashreplace", "namereplace", "xmlcharrefreplace", "replace", "ignore")
ESCAPED = "+backslashreplace"


def _escaping(errors):
    """The name of an error handler that writes a character as the handler errors writes it, and as its Python escape
    (\\u2192) where that handler would end the write in an error; registered on first use."""
    name = errors + ESCAPED
    try:
        codecs.lookup_error(name)
    except LookupError:
        original = codecs.lookup_error(errors)

        def handler(exc):
            if not isinstance(exc, UnicodeEncodeError):
                return original(exc)
            one = UnicodeEncodeError(exc.encoding, exc.object, exc.start, exc.start + 1, exc.reason)
            try:
                return original(one)
            except UnicodeEncodeError:
                return codecs.backslashreplace_errors(one)

        codecs.register_error(name, handler)
    return name


def writable_output(*streams):
    """Let standard output and standard error (or the streams given) write any text: a character their encoding cannot
    write, as on a legacy Windows code page or under a C locale, is written as its Python escape (\\u2192 for an
    arrow) instead of ending the run in an encoding error. A stream keeps what its error handler does where that
    handler writes a character: under surrogateescape, a name that is not text in the encoding is still written as its
    bytes. A handler that never raises, and UTF with surrogatepass, are left as they are."""
    for stream in streams or (sys.stdout, sys.stderr):
        errors, encoding = getattr(stream, "errors", None), getattr(stream, "encoding", None) or ""
        if not errors or errors in SAFE_ERRORS or errors.endswith(ESCAPED) or not hasattr(stream, "reconfigure"):
            continue
        try:
            if errors == "surrogatepass" and codecs.lookup(encoding).name.startswith("utf"):
                continue
            stream.reconfigure(errors="backslashreplace" if errors == "strict" else _escaping(errors))
        except (LookupError, ValueError, OSError):
            pass


if __name__ == "__main__":
    writable_output()
    sys.exit(main(sys.argv[1:]))
