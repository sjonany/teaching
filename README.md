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
    index.html          Home        -> /teaching/cs442-au2026/
    calendar/index.html Calendar    -> /teaching/cs442-au2026/calendar/
    assignments/        Assignments -> /teaching/cs442-au2026/assignments/
    resources/          Resources   -> /teaching/cs442-au2026/resources/
```

Each page carries its own copy of the nav bar, with `class="active"` on the
current tab. Adding a tab means editing all four pages — deliberate tradeoff for
having no build step at four pages.

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
