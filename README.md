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
    nav.js              the nav bar, defined once for this course
    index.html          Home      -> /teaching/cs442-au2026/
    calendar/index.html Calendar  -> /teaching/cs442-au2026/calendar/
    resources/          Resources -> /teaching/cs442-au2026/resources/
    assets/             syllabus and handouts linked from the pages
```

Homework is linked from the calendar rather than getting its own tab.

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
