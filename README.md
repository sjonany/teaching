# teaching

Course websites, served by GitHub Pages at <https://sjonany.github.io/teaching/>.

Plain static HTML — no build step, no Jekyll (`.nojekyll` is present), no
JavaScript. What you see in the file is what ships.

## Layout

```
index.html              landing page listing courses
site/css/main.css       shared styling (nav bar, typography)
site/css/calendar.css   month-grid calendar styling, loaded only by calendar pages
cs442-au2026/
    nav.js               the nav bar, defined once for this course
    index.html           Home      -> /teaching/cs442-au2026/
    calendar/index.html  Calendar  -> /teaching/cs442-au2026/calendar/  (generated)
    calendar/generate.py builds that page from the schedule data
    resources/           Resources -> /teaching/cs442-au2026/resources/
    assets/              syllabus and handouts linked from the pages
```

Homework is linked from the calendar rather than getting its own tab.

## The calendar

`calendar/index.html` is **generated** — never edit it by hand.

```
cd cs442-au2026/calendar
python3 generate.py          # rebuild the page
python3 generate.py --ids    # list every id you can attach files to
```

`schedule.py` holds the data: lecture topics per week, the quiz list, homework
list, holidays, which Fridays are mock interviews versus lectures, one-off
dates, and attachments. `generate.py` holds the rendering and never needs
editing for routine updates.

Quiz attempt dates are computed rather than listed — each quiz runs Monday and
Wednesday of its week plus the following Monday. An attempt landing on a
holiday, the midterm, or finals week is **pushed to the next Monday/Wednesday
slot** rather than dropped, so a quiz keeps all three attempts and its last
chance can fall later than that pattern suggests. Only a quiz that runs out of
quarter ends up with two attempts; the script prints which ones every run.

### Attaching handouts, notes, and readings

Every item that lands in a cell has a stable id: `hw3`, `quiz7`, `mock2`,
`lec-2026-10-05`, `midterm`, `finals`. Run `generate.py --ids` to see them all
with their dates.

Each homework appears twice: **`hw<N>` is the Monday "HW N out" block, and that
is where the handout goes**; `hw<N>-due` is the Friday reminder of the Sunday
deadline. Hang files off an id in `schedule.py`:

```python
ATTACHMENTS = {
    "lec-2026-09-21": [
        ("slides", "01-divide-and-conquer.pdf"),
        ("annotated", "01-divide-and-conquer-ink.pdf"),
        ("reading", "https://www.algorithmsilluminated.org/"),
    ],
    "hw1": [
        ("handout", "hw1-div.pdf"),
    ],
}
```

A target starting with `http` becomes an external link; anything else is a
filename in `assets/`. Attachments land inside that specific item's block, so a
homework's handout and a lecture's notes stay separate even on the same day.

The build **fails** rather than shipping a broken link if an id doesn't exist or
a named file isn't in `assets/`. It also lists files sitting in `assets/` that
nothing references.

### The weekly loop

Drop the week's files in `assets/`, add their ids to `ATTACHMENTS`, run
`generate.py`, check the diff, push.

## Tabs

Tabs are defined once, in the `TABS` array at the top of `cs442-au2026/nav.js`.
Add, remove, rename, or reorder them there and every page picks it up — no page
needs editing. The course name and quarter shown in the bar live in the same
file.

Each page includes the nav where it should appear:

```html
<script src="nav.js"    data-base="."  data-tab="home"></script>      <!-- course root -->
<script src="../nav.js" data-base=".." data-tab="calendar"></script>  <!-- one level down -->
```

`data-base` is the relative path from that page back to the course root;
`data-tab` is the `key` of the tab to highlight.

`nav.js` is per-course rather than shared in `site/`, so copying a course
directory copies its nav with it and editing this quarter's tabs can't disturb
an archived quarter.

The nav is written synchronously at the script's own position, so it renders
before the rest of the page parses — no fetch, no flash. The tradeoff is that
the nav requires JavaScript; with JS disabled the page content still renders but
the nav bar is absent.

Styling is adapted from the UW CSE course template (CSE 421, 26sp). To change
the header color, edit `--brand` in `site/css/main.css`.

## Preview locally

```
python3 -m http.server 8000
```

then open <http://localhost:8000/>. Use the server rather than opening the files
directly — the nav links are directory URLs (`calendar/`), which only resolve to
`index.html` over HTTP.

## Adding a new course

Copy `cs442-au2026/`, rename it, and update the course number, quarter, and
footer in each page. Add a line to the course list in the root `index.html`.

## Publishing rules

This repo is **public**. Read `.gitignore` before adding files — PDFs are
ignored unless named `*-public.pdf`, so publishing a handout is a deliberate
rename. Solutions belong on Canvas, never in this repo. A leaked commit cannot
be reliably erased from GitHub after the fact.
