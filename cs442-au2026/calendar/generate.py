#!/usr/bin/env python3
"""
Builds index.html in this directory from the data in schedule.py.

    python3 generate.py          rebuild the calendar page
    python3 generate.py --ids    list every item id you can attach files to

WARNING: this OVERWRITES index.html. Put your changes in schedule.py, not in
the generated HTML.

Every item that lands in a calendar cell gets a stable id (hw3, quiz7,
lec-2026-10-05, ...). schedule.py's ATTACHMENTS maps those ids to files in
../assets/ or to external URLs, which is how a specific homework or a specific
lecture gets its own handouts and readings.

Layout follows the UW CSE 421 calendar: one Monday-Friday table per month, with
each week-row filed under the month its Monday falls in.
"""

import datetime as dt
import os
import sys
from collections import defaultdict

import schedule as S

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
ASSETS_HREF = "../assets"

# Order in which entries stack inside one day cell.
PRIORITY = {"holiday": 0, "lecture": 1, "exam": 2, "quiz": 3,
            "mock": 4, "other": 5, "hw": 6}


class Item:
    """One coloured block inside one day cell."""

    def __init__(self, id, day, kind, lines, label):
        self.id = id          # stable handle for ATTACHMENTS
        self.day = day
        self.kind = kind      # css class, also the legend colour
        self.lines = lines    # already-escaped html fragments, joined by <br>
        self.label = label    # human description, shown by --ids

    @property
    def sort_key(self):
        return (PRIORITY[self.kind], self.id)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def summary(text):
    return f'<span class="summary">{esc(text)}</span>'


def location(text):
    return f'<span class="location">{esc(text)}</span>'


def description(text):
    return f'<span class="description">{esc(text)}</span>'


def monday_of(week):
    return S.QUARTER_START + dt.timedelta(weeks=week - 1)


# ------------------------------------------------------------- building items

def quiz_attempt_days(first_monday, blocked, count=3):
    """The days a quiz's attempts actually land on.

    Attempts want the Monday and Wednesday of the quiz's week and then the
    following Monday. A slot falling on a holiday, the midterm, or finals week
    is skipped and that attempt moves to the next Monday/Wednesday slot, so a
    quiz keeps all three attempts unless the quarter runs out of slots first.
    """
    days = []
    day = first_monday
    while len(days) < count and day <= S.QUARTER_END:
        if day not in blocked:
            days.append(day)
        # Monday -> Wednesday of the same week -> Monday of the next.
        day += dt.timedelta(days=2 if day.weekday() == 0 else 5)
    return days


def build_items():
    items = []
    reduced = []

    no_quiz = set(S.NO_CLASS) | {S.MIDTERM} | {
        monday_of(12) + dt.timedelta(days=n) for n in range(5)
    }

    # lectures
    for week, topic in S.TOPICS.items():
        if topic is None:
            continue
        mon = monday_of(week)
        for offset in (0, 2):
            day = mon + dt.timedelta(days=offset)
            if day in S.NO_CLASS or day == S.MIDTERM:
                continue
            items.append(Item(
                f"lec-{day}", day, "lecture",
                [f"{S.MW_TIME} {summary('Lecture')}", location(S.MW_ROOM),
                 description(topic)],
                f"lecture: {topic}"))
        friday = mon + dt.timedelta(days=4)
        if week in S.FRIDAY_LECTURE_WEEKS and friday not in S.NO_CLASS:
            items.append(Item(
                f"lec-{friday}", friday, "lecture",
                [f"{S.FR_TIME} {summary('Lecture')}", location(S.FR_ROOM),
                 description(topic)],
                f"lecture: {topic}"))

    # quizzes; attachments render on the first attempt only
    for num, topic, week in S.QUIZZES:
        days = quiz_attempt_days(monday_of(week), no_quiz)
        if len(days) < 3:
            reduced.append((num, topic, len(days)))
        for i, day in enumerate(days, start=1):
            last = " (last chance)" if i == len(days) else ""
            items.append(Item(
                f"quiz{num}" if i == 1 else f"quiz{num}-attempt{i}",
                day, "quiz",
                [summary(f"Quiz {num}: {topic}"),
                 description(f"attempt {i} of {len(days)}{last}")],
                f"quiz {num}: {topic}, attempt {i}"))

    # mock interviews
    for n, week in enumerate(S.MOCK_WEEKS, start=1):
        day = monday_of(week) + dt.timedelta(days=4)
        items.append(Item(
            f"mock{n}", day, "mock",
            [f"{S.FR_TIME} {summary(f'Mock interview {n}')}", location(S.FR_ROOM)],
            f"mock interview {n}"))

    # homework: goes out Monday, due the following Sunday. The Monday item is
    # the one handouts hang off, so it takes the plain `hw<N>` id.
    for num, topic, week in S.HOMEWORK:
        mon = monday_of(week)
        friday = mon + dt.timedelta(days=4)
        sunday = mon + dt.timedelta(days=6)
        due = f"due Sun {sunday:%b %-d}, {S.HW_DUE_TIME}"
        items.append(Item(
            f"hw{num}", mon, "hw",
            [summary(f"HW {num} out"), description(topic), due],
            f"homework {num} out: {topic}"))
        items.append(Item(
            f"hw{num}-due", friday, "hw",
            [summary(f"HW {num} due"), description(topic), due],
            f"homework {num} due: {topic}"))

    # exams
    items.append(Item("midterm", S.MIDTERM, "exam",
                      [f"{S.MW_TIME} {summary('Midterm')}", location(S.MW_ROOM)],
                      "midterm"))
    items.append(Item(
        "finals", S.FINAL_EXAM, "exam",
        [f"{S.FINAL_EXAM_TIME} {summary('Final exam')}",
         location(S.FINAL_EXAM_ROOM),
         description("No regular classes during finals week")],
        "final exam"))

    # holidays
    for day, label in S.NO_CLASS.items():
        items.append(Item(f"noclass-{day}", day, "holiday",
                          [summary("No class"), description(label)],
                          f"no class: {label}"))

    # one-offs
    for key, (day, kind, summ, desc) in S.EXTRAS.items():
        lines = [summary(summ)] + ([description(desc)] if desc else [])
        items.append(Item(key, day, kind, lines, summ))

    return items, reduced


# --------------------------------------------------------------- attachments

def attachment_span(item_id):
    """The <span class="materials"> line for an item, or None."""
    entries = S.ATTACHMENTS.get(item_id)
    if not entries:
        return None
    links = []
    for text, target in entries:
        href = (target if target.startswith(("http://", "https://"))
                else f"{ASSETS_HREF}/{target}")
        links.append(f'<a href="{href}">{esc(text)}</a>')
    return '<span class="materials">' + ", ".join(links) + "</span>"


def validate(items):
    """Refuse to build on an unknown id or a missing file. Returns warnings."""
    ids = {i.id for i in items}
    errors, warnings = [], []

    for key, entries in S.ATTACHMENTS.items():
        if key not in ids:
            errors.append(f"ATTACHMENTS key {key!r} matches no calendar item. "
                          f"Run `python3 generate.py --ids` for the full list.")
            continue
        for text, target in entries:
            if target.startswith(("http://", "https://")):
                continue
            if not os.path.exists(os.path.join(ASSETS, target)):
                errors.append(f"{key}: attachment {target!r} is not in assets/")

    referenced = {t for entries in S.ATTACHMENTS.values()
                  for _, t in entries
                  if not t.startswith(("http://", "https://"))}
    if os.path.isdir(ASSETS):
        on_disk = {f for f in os.listdir(ASSETS) if not f.startswith(".")}
        for extra in sorted(on_disk - referenced):
            warnings.append(f"assets/{extra} is not linked from the calendar "
                            f"(it may be linked from another page)")

    if errors:
        print("BUILD FAILED", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    return warnings


# ------------------------------------------------------------------ rendering

def render_day(day, by_day):
    entries = sorted(by_day.get(day, []), key=lambda i: i.sort_key)
    num = f'<span class="datespan" aria-hidden="true">{day.day:02d}</span>'
    aria = day.strftime("%A %B %d").replace(" 0", " ")
    if not entries:
        return (f'<td class="noevent" id="{day}" '
                f'aria-label="{aria}, no events">{num}</td>')
    blocks = []
    for item in entries:
        lines = list(item.lines)
        span = attachment_span(item.id)
        if span:
            lines.append(span)
        blocks.append(f'<div class="{item.kind}" aria-label="{item.kind}">'
                      + "<br>".join(lines) + "</div>")
    return (f'<td class="eventtd" id="{day}" aria-label="{aria}">{num}\n'
            + "\n".join(blocks) + "\n</td>")


def render(items):
    by_day = defaultdict(list)
    for item in items:
        by_day[item.day].append(item)

    weeks = []
    day = S.QUARTER_START
    while day <= S.QUARTER_END:
        weeks.append(day)
        day += dt.timedelta(weeks=1)

    by_month = defaultdict(list)
    for monday in weeks:
        by_month[(monday.year, monday.month)].append(monday)

    out = []
    for (year, month), mondays in by_month.items():
        name = dt.date(year, month, 1).strftime("%B")
        out.append('<table class="monthtable">')
        out.append("    <thead>")
        out.append(f'        <tr><th colspan="5" class="month-header" '
                   f'scope="colgroup">{name} {year}</th></tr>')
        out.append("        <tr>")
        for weekday in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
            out.append(f'            <th class="day-header" scope="col">{weekday}</th>')
        out.append("        </tr>")
        out.append("    </thead>")
        out.append("    <tbody>")
        for monday in mondays:
            out.append("        <tr>")
            for offset in range(5):
                out.append(render_day(monday + dt.timedelta(days=offset), by_day))
            out.append("        </tr>")
        out.append("    </tbody>")
        out.append("</table>")
    return "\n".join(out)


LEGEND = """    <ul class="cal-legend">
        <li><div class="lecture">Lecture</div></li>
        <li><div class="quiz">Mastery quiz</div></li>
        <li><div class="mock">Mock interview</div></li>
        <li><div class="hw">Homework due</div></li>
        <li><div class="exam">Exam</div></li>
        <li><div class="other">Deadline</div></li>
        <li><div class="holiday">No class</div></li>
    </ul>"""

PAGE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CS 442 &middot; Calendar</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,600">
    <link rel="stylesheet" href="../../site/css/main.css">
    <link rel="stylesheet" href="../../site/css/calendar.css">
</head>

<body>

<script src="../nav.js" data-base=".." data-tab="calendar"></script>

<main class="container">
    <!-- GENERATED BY generate.py from schedule.py - do not edit by hand. -->
    <h2>Calendar</h2>

    <p>Each homework goes out on <strong>Monday</strong> and is due the
       following <strong>Sunday at {hw_due_time}</strong>. The Monday cell carries the
       handout; the deadline is repeated in that week's Friday cell.</p>

    <p>Each mastery quiz can be attempted up to three times, on the Monday and
       Wednesday of the week it is introduced and again the following Monday. If
       one of those days is a holiday, the midterm, or in finals week, that
       attempt moves to the next class day a quiz can run on rather than being
       lost, so the last attempt is sometimes later than that pattern suggests.
       Every cell says which attempt it is and flags the last chance.</p>

{legend}

{calendar}
</main>

</body>

</html>
"""


def main():
    items, reduced = build_items()

    if "--ids" in sys.argv:
        print("Attachment ids, by date. Use these as keys in "
              "schedule.py ATTACHMENTS.\n")
        for item in sorted(items, key=lambda i: (i.day, i.sort_key)):
            attached = S.ATTACHMENTS.get(item.id)
            mark = f"   <- {len(attached)} attached" if attached else ""
            print(f"  {item.day:%a %b %d}  {item.id:<22} {item.label}{mark}")
        return

    warnings = validate(items)
    html = PAGE.format(legend=LEGEND, calendar=render(items), hw_due_time=S.HW_DUE_TIME)
    path = os.path.join(HERE, "index.html")
    with open(path, "w") as f:
        f.write(html)

    attached = sum(len(v) for v in S.ATTACHMENTS.values())
    print(f"wrote {path}")
    print(f"{len(items)} items, {attached} attachments across "
          f"{len(S.ATTACHMENTS)} cells")
    if reduced:
        print("\nquizzes with fewer than 3 attempts "
              "(no slot left in the quarter to push to):")
        for num, topic, n in reduced:
            print(f"  Quiz {num} ({topic}): {n} attempts")
    if warnings:
        print("\nnotes:")
        for w in warnings:
            print("  " + w)


if __name__ == "__main__":
    main()
