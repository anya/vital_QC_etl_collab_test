#!/usr/bin/env python3
"""Build INDEX.md, FIELD-VIEW.md and catalog.csv from rule page headers,
and check the repository for consistency.

Run from the repository root:  python scripts/build_catalog.py
Exit code 1 if any error was found.
Requires Python 3 and PyYAML (pip install pyyaml).

Naming conventions enforced
  Rule page      rules/<FOLDER>/PE01-short-slug.md      header  id: PE01
  Overview page  rules/<FOLDER>/PE-overview.md          header  id: PE-overview, type: hub
  <FOLDER> is either the prefix (PE) or the full table name in capitals (PERSON).
  The prefix of every ID must be listed in PREFIX_LIST below.
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

import yaml

# ---------------------------------------------------------------------------
# EDIT THIS LIST when a table gets its first rule page.
# (prefix, home_table): prefix is 2 to 5 letters, upper or lower case, written
# exactly as it appears in IDs and file names (for example "PrOc"). home_table is
# the lowercase OMOP table name, or one of gen / vocab / pop. Each prefix must be
# unique, ignoring case (Windows and macOS treat PE and Pe as the same name), and
# each table has one prefix.
# Watch for clashes: DEATH and DRUG_EXPOSURE cannot both be "DE".
# ---------------------------------------------------------------------------
PREFIX_LIST = [
    ("Pe", "person"),
    ("ViOc", "visit_occurrence"),
    ("ViDe", "visit_detail"),
    ("ObPe", "observation_period"),
    ("CaSi", "care_site"),
    ("Lo", "location"),
    ("LoHi", "location_history"),
    ("De", "death"),
    ("CoOc", "condition_occurrence"),
    ("PrOc", "procedure_occurrence"),
    ("DrEx", "drug_exposure"),
    ("DeEx", "device_exposure"),
    ("Me", "measurement"),
    ("Ob", "observation"),
    ("Sp", "specimen"),
    ("FaRe", "fact_relationship"),
    ("Pr", "provider"),
    ("No", "note"),
    ("NoNl", "note_nlp"),
    ("GEN", "gen"),
    ("VOCAB", "vocab"),
    ("POP", "pop"),
]
NUM_DIGITS = 3            # N digits in rule numbering: Pe001
HUB_SUFFIX = "-overview"  # Overview page format: PE-overview.md

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "rules"
SITES_CSV = ROOT / "sites" / "conformance.csv"
FIELDS_CSV = ROOT / "scripts" / "omop_fields.csv"

STATUSES = {"draft", "ratified", "under-revision", "retired", "rejected"}
IN_FORCE = {"ratified", "under-revision"}
CLOSED = {"retired", "rejected"}
SHOWN_IN_FIELD_VIEW = {"draft", "ratified", "under-revision"}
TYPES = {"field", "table", "relationship", "global", "vocabulary", "population", "hub"}
SITE_STATUSES = {"not-started", "in-progress", "implemented", "deviation", "not-applicable"}
LIST_KEYS = ["fields", "also_tables", "depends_on", "affects", "supersedes", "superseded_by"]
REQUIRED = ["id", "title", "type", "status", "home_table"]
FIELD_RE = re.compile(r"^[a-z_]+\.[a-z_0-9]+$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PLACEHOLDERS = ["TABLE-NN", "XXNN", "YYYY-MM-DD", "#NN", "#__"]
ISSUE_LINK_PREFIX = "../../../../issues"  # pages live in rules/<FOLDER>/, two folders deep


def build_prefix_maps():
    to_table, to_prefix = {}, {}
    for prefix, table in PREFIX_LIST:
        if not re.fullmatch(r"[A-Za-z]{2,5}", prefix):
            sys.exit(f"PREFIX_LIST: '{prefix}' must be 2 to 5 letters")
        for other in to_table:
            if other.lower() == prefix.lower() and other != prefix:
                sys.exit(f"PREFIX_LIST: '{other}' and '{prefix}' differ only by case; Windows and "
                         "macOS treat file and folder names that differ only by case as the same")
        if table != table.lower():
            sys.exit(f"PREFIX_LIST: table '{table}' must be lowercase")
        if prefix in to_table:
            sys.exit(f"PREFIX_LIST: prefix '{prefix}' is used twice "
                     f"({to_table[prefix]} and {table})")
        if table in to_prefix:
            sys.exit(f"PREFIX_LIST: table '{table}' has two prefixes "
                     f"({to_prefix[table]} and {prefix})")
        to_table[prefix] = table
        to_prefix[table] = prefix
    return to_table, to_prefix


PREFIX_TO_TABLE, TABLE_TO_PREFIX = build_prefix_maps()
_PREFIX_ALT = "|".join(sorted(PREFIX_TO_TABLE, key=len, reverse=True))
RULE_ID_RE = re.compile(rf"^([A-Za-z]{{2,5}})(\d{{{NUM_DIGITS}}})$")
HUB_ID_RE = re.compile(rf"^([A-Za-z]{{2,5}}){re.escape(HUB_SUFFIX)}$")
# Case-insensitive on purpose: a link that spells an ID with the wrong case (proc01 for PrOc01)
# is reported as a mismatch instead of slipping through.
ID_IN_TEXT = re.compile(rf"\b(?:{_PREFIX_ALT})\d{{{NUM_DIGITS}}}\b", re.IGNORECASE)

errors = []
warnings = []


def err(path, msg):
    errors.append(f"{path}: {msg}")


def warn(path, msg):
    warnings.append(f"{path}: {msg}")


def parse_front_matter(path, text):
    rel = path.relative_to(ROOT)
    if not text.startswith("---"):
        err(rel, "no front matter at top of file (is the template's comment block still there?)")
        return None
    end = text.find("\n---", 3)
    if end == -1:
        err(rel, "front matter not closed with ---")
        return None
    try:
        data = yaml.safe_load(text[3:end])
    except yaml.YAMLError as exc:
        err(rel, f"front matter is not valid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        err(rel, "front matter is empty or not key: value lines")
        return None
    return data


def as_list(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def check_id_and_location(rel, path, rid, is_hub, home):
    """Checks tied to the naming convention: id shape, file name, prefix, folder, home_table."""
    if is_hub:
        m = HUB_ID_RE.match(rid)
        if not m:
            err(rel, f"overview page id should look like PE{HUB_SUFFIX} "
                     f"(prefix + '{HUB_SUFFIX}'), got '{rid}'")
        elif rid != path.stem:
            err(rel, f"id '{rid}' should equal the file name without .md ('{path.stem}')")
    else:
        m = RULE_ID_RE.match(rid)
        if not m:
            err(rel, f"id '{rid}' does not look like PE01 "
                     f"(2 to 5 letter prefix + {NUM_DIGITS} digits, no dash)")
        elif not path.name.startswith(rid + "-"):
            err(rel, f"file name should start with '{rid}-' (for example {rid}-short-slug.md)")
    if not m:
        return
    prefix = m.group(1)
    table = PREFIX_TO_TABLE.get(prefix)
    if table is None:
        same_but_case = [p for p in PREFIX_TO_TABLE if p.lower() == prefix.lower()]
        if same_but_case:
            err(rel, f"prefix '{prefix}' has the wrong case: PREFIX_LIST spells it "
                     f"'{same_but_case[0]}'")
        else:
            err(rel, f"unknown prefix '{prefix}': add it to PREFIX_LIST at the top of "
                     "scripts/build_catalog.py")
        return
    if home and home != table:
        err(rel, f"home_table is '{home}' but prefix {prefix} stands for '{table}'")
    allowed_folders = {prefix, table.upper()}
    if path.parent.name not in allowed_folders:
        err(rel, f"folder '{path.parent.name}' does not match prefix {prefix} "
                 f"(expected {' or '.join(sorted(allowed_folders))})")


def load_rules():
    rules = {}
    for path in sorted(RULES_DIR.rglob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        data = parse_front_matter(path, text)
        if data is None:
            continue
        rtype = data.get("type")
        name_is_hub = path.name.endswith(HUB_SUFFIX + ".md")
        is_hub = name_is_hub or rtype == "hub"
        if rtype is not None and (rtype == "hub") != name_is_hub:
            if rtype == "hub":
                err(rel, f"type is hub but the file name does not end with '{HUB_SUFFIX}.md'")
            else:
                err(rel, f"file name ends with '{HUB_SUFFIX}.md' but type is '{rtype}', not hub")
        for key in REQUIRED:
            if key == "status" and is_hub:
                continue  # overview pages are guides, not rules
            if not data.get(key):
                err(rel, f"missing required header field '{key}'")
        rid = str(data.get("id", ""))
        entry = {"path": rel, "data": data, "id": rid, "text": text, "is_hub": is_hub}
        for key in LIST_KEYS:
            entry[key] = as_list(data.get(key))

        if rtype is not None and rtype not in TYPES:
            err(rel, f"type '{rtype}' not allowed (see ALLOWED-VALUES.md)")

        status = data.get("status")
        if not is_hub:
            if status is not None and status not in STATUSES:
                err(rel, f"status '{status}' not allowed (see ALLOWED-VALUES.md)")
            if status in IN_FORCE and not data.get("ratified_on"):
                err(rel, f"status is {status} but ratified_on is empty")
            if status == "under-revision" and not data.get("revision_issue"):
                err(rel, 'status is under-revision but revision_issue is empty '
                         '(put the issue number in quotes, e.g. "#31"; unquoted, YAML treats it as a comment)')
            if status != "under-revision" and data.get("revision_issue"):
                err(rel, "revision_issue is set but status is not under-revision "
                         "(remove it once the revision is decided)")
            if entry["superseded_by"] and status != "retired":
                err(rel, "superseded_by is only for retired rules")
            if status == "draft" and data.get("ratified_on"):
                warn(rel, "status is draft but ratified_on is set")
            if "## Change log" not in text:
                warn(rel, "no '## Change log' section")

        home = str(data.get("home_table", ""))
        if home and home != home.lower():
            err(rel, f"home_table '{home}' must be lowercase")
        if rid:
            check_id_and_location(rel, path, rid, is_hub, home)
            if rid in rules:
                err(rel, f"duplicate id {rid} (also in {rules[rid]['path']})")
        for f in entry["fields"]:
            if not FIELD_RE.match(f):
                err(rel, f"field '{f}' must be qualified and lowercase, e.g. person.gender_concept_id")
        if rid:
            rules[rid] = entry
    return rules


def status_of(rules, rid):
    return rules[rid]["data"].get("status")


def check_links(rules):
    for rid, r in rules.items():
        for key in ("depends_on", "affects", "supersedes", "superseded_by"):
            for target in r[key]:
                if target not in rules:
                    err(r["path"], f"{key} points to unknown rule '{target}'")
        if rid in r["depends_on"]:
            err(r["path"], "rule depends on itself")
        for target in r["superseded_by"]:
            if target in rules and status_of(rules, target) in CLOSED:
                err(r["path"], f"superseded_by points to {target}, which is itself "
                               f"{status_of(rules, target)}")
        if status_of(rules, rid) in CLOSED:
            continue  # stale links on closed rules do not matter
        for key in ("depends_on", "affects"):
            for target in r[key]:
                if target in rules and status_of(rules, target) in CLOSED:
                    warn(r["path"], f"{key} points to {target}, which is {status_of(rules, target)}; "
                                    "update or remove the link")


def load_all_fields():
    fields = defaultdict(list)
    if not FIELDS_CSV.exists():
        return fields
    with FIELDS_CSV.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            fields[row["table"]].append(row["field"])
    return fields


def check_conformance(rules):
    if not SITES_CSV.exists():
        return
    with SITES_CSV.open(newline="", encoding="utf-8") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            where = f"sites/conformance.csv line {n}"
            if row["rule_id"] not in rules:
                err("sites/conformance.csv", f"line {n}: unknown rule_id '{row['rule_id']}'")
            elif status_of(rules, row["rule_id"]) == "retired" and row["status"] != "not-applicable":
                warn(where, f"{row['rule_id']} is retired; its rows should be 'not-applicable'")
            if row["status"] not in SITE_STATUSES:
                err("sites/conformance.csv", f"line {n}: status '{row['status']}' not allowed")
            if row["status"] == "deviation" and not row["deviation_reason"].strip():
                err("sites/conformance.csv", f"line {n}: deviation without a reason")


def status_cell(r):
    d = r["data"]
    s = d.get("status", "")
    if s == "under-revision" and d.get("revision_issue"):
        return f"under-revision ({d['revision_issue']})"
    if s == "retired" and r["superseded_by"]:
        return "retired -> " + ", ".join(r["superseded_by"])
    return s


def write_catalog(rules):
    real = [r for r in rules.values() if not r["is_hub"]]
    real.sort(key=lambda r: (r["data"].get("home_table", ""), r["id"]))
    columns = ["id", "title", "type", "status", "home_table", "fields", "also_tables",
               "depends_on", "affects", "superseded_by", "ratified_on", "revision_issue",
               "discussion", "path"]
    with (ROOT / "catalog.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(columns)
        for r in real:
            d = r["data"]
            w.writerow([
                r["id"], d.get("title", ""), d.get("type", ""), d.get("status", ""),
                d.get("home_table", ""), ";".join(r["fields"]), ";".join(r["also_tables"]),
                ";".join(r["depends_on"]), ";".join(r["affects"]), ";".join(r["superseded_by"]),
                d.get("ratified_on") or "", d.get("revision_issue") or "",
                d.get("discussion") or "", str(r["path"]),
            ])

    counts = defaultdict(int)
    for r in real:
        counts[r["data"].get("status", "?")] += 1
    lines = [
        "# Rule index",
        "",
        "> Generated by `scripts/build_catalog.py`. Do not edit by hand; edit the rule pages.",
        "> For a sortable/filterable version, open `catalog.csv` in a spreadsheet.",
        "",
        "**Rules by status:** " + (", ".join(f"{s}: {counts[s]}" for s in sorted(counts)) or "none")
        + f" (total {len(real)})",
        "",
    ]
    sections = [
        ("In force", "Implement these. `under-revision` rules stay in force while a change is decided.",
         IN_FORCE),
        ("Draft (not yet agreed)", "Do not implement yet.", {"draft"}),
        ("Closed", "Retired or rejected. Do not implement.", CLOSED),
    ]
    for title, note, wanted in sections:
        lines += [f"## {title}", "", note, ""]
        rows = [r for r in real if r["data"].get("status") in wanted]
        if not rows:
            lines += ["None.", ""]
            continue
        lines += ["| ID | Title | Type | Status | Table | Fields | Ratified on |",
                  "|---|---|---|---|---|---|---|"]
        for r in rows:
            d = r["data"]
            link = f"[{r['id']}]({str(r['path']).replace(chr(92), '/')})"
            fields = ", ".join(f.split(".", 1)[1] if "." in f else f for f in r["fields"])
            lines.append(f"| {link} | {d.get('title', '')} | {d.get('type', '')} | "
                         f"{status_cell(r)} | {d.get('home_table', '')} | {fields} | "
                         f"{d.get('ratified_on') or ''} |")
        lines.append("")
    (ROOT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def write_field_view(rules):
    real = [r for r in rules.values() if not r["is_hub"]]
    by_field = defaultdict(list)
    for r in real:
        for f in r["fields"]:
            if "." not in f:
                continue  # malformed; already reported as an error by load_rules
            by_field[f].append(r)
    global_rules = [r for r in real if r["data"].get("home_table") == "gen"
                    and r["data"].get("status") in SHOWN_IN_FIELD_VIEW]
    all_fields = load_all_fields()

    def cell_for(rs):
        shown = [r for r in rs if r["data"].get("status") in SHOWN_IN_FIELD_VIEW]
        if not shown:
            return "*default (no network rule)*"
        return "; ".join(f"[{r['id']}]({str(r['path'])}) ({status_cell(r)})"
                         for r in sorted(shown, key=lambda x: x["id"]))

    lines = [
        "# Field view: which rules govern which field",
        "",
        "> Generated by `scripts/build_catalog.py`. Do not edit by hand.",
        "",
        "Rules in `GEN` apply to every field unless a field rule says otherwise: " +
        (", ".join(f"[{r['id']}]({str(r['path'])}) ({r['data'].get('status')})" for r in global_rules)
         or "none yet") + ".",
        "",
        "Fields with **no network rule** follow the OMOP CDM specification and Themis defaults.",
        "`draft` rules are not yet agreed; `under-revision` rules are still in force. "
        "Retired and rejected rules are not shown here; see INDEX.md.",
        "",
    ]
    tables = set(all_fields) | {f.split(".")[0] for f in by_field}
    for table in sorted(tables):
        lines += [f"## {table}", "", "| Field | Rules (status) |", "|---|---|"]
        names = list(all_fields.get(table, []))
        for f in by_field:
            t, name = f.split(".", 1)
            if t == table and name not in names:
                names.append(name)
        for name in names:
            lines.append(f"| `{name}` | {cell_for(by_field.get(f'{table}.{name}', []))} |")
        lines.append("")
    lines += ["## Not yet settled", "",
              "Drafts, and rules in force that have a change being decided, by table:", ""]
    pending = defaultdict(list)
    for r in real:
        if r["data"].get("status") in ("draft", "under-revision"):
            pending[r["data"].get("home_table")].append(r)
    if not pending:
        lines.append("None.")
    for table in sorted(pending):
        items = ", ".join(f"[{r['id']}]({str(r['path'])}) ({status_cell(r)})"
                          for r in sorted(pending[table], key=lambda x: x["id"]))
        lines.append(f"- **{table}:** {items}")
    (ROOT / "FIELD-VIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for f in by_field:
        table = f.split(".")[0]
        if all_fields and table in all_fields and f.split(".", 1)[1] not in all_fields[table]:
            warn("rules", f"field '{f}' is not in scripts/omop_fields.csv (typo, or list incomplete?)")


def check_page_texts(rules):
    """Run after the generated files exist, so links to INDEX.md resolve."""
    for rid, r in rules.items():
        rel, text = r["path"], r["text"]
        for ph in PLACEHOLDERS:
            if ph in text:
                warn(rel, f"template placeholder '{ph}' is still in the page")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if "/issues" in target or target.startswith("issues"):
                if not target.startswith(ISSUE_LINK_PREFIX):
                    err(rel, f"issue link '{target}' should start with {ISSUE_LINK_PREFIX} "
                             "(pages live two folders deep)")
                if not r["is_hub"]:
                    for other in set(ID_IN_TEXT.findall(unquote(target))):
                        if other != rid:
                            err(rel, f"link mentions {other} but this page is {rid} "
                                     "(copied from another page?)")
                continue
            path_part = target.split("#", 1)[0]
            if path_part and not ((ROOT / rel).parent / path_part).resolve().exists():
                err(rel, f"broken link: {target}")


def main():
    rules = load_rules()
    check_links(rules)
    check_conformance(rules)
    write_catalog(rules)
    write_field_view(rules)
    check_page_texts(rules)
    print(f"Read {len(rules)} pages; wrote INDEX.md, FIELD-VIEW.md, catalog.csv")
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:  ", e)
    if errors:
        print(f"\n{len(errors)} error(s) found.")
        sys.exit(1)
    print("No errors.")


if __name__ == "__main__":
    main()
