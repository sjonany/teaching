---
name: start-server
description: Start (or restart) a local HTTP server for previewing this static teaching site, and report the URLs to open. Use when the user asks to serve, preview, or debug the site locally, or types /start-server.
---

# Start the local preview server

This repo is plain static HTML served by GitHub Pages. Previewing needs a real
HTTP server, not `file://` — the nav links are directory URLs (`calendar/`),
which only resolve to `index.html` over HTTP.

## Steps

1. **Pick a port.** Default to `8000`. If it is already in use, check whether it
   is already this server:

   ```bash
   ss -ltnp 2>/dev/null | grep -E ':(8000)\s' || echo free
   curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/
   ```

   If an old instance of this same server is running, kill it before starting a
   fresh one (stale processes serve stale directory listings after renames):

   ```bash
   pkill -f 'http.server 8000' || true
   ```

   If some unrelated process owns the port, use `8001` instead and say so.

2. **Start it detached**, rooted at the repo root so both `/` and
   `/cs442-au2026/` resolve the same way they do on GitHub Pages:

   ```bash
   cd /home/stephen/Code/personal/teaching
   LOG="${CLAUDE_JOB_DIR:-/tmp}/teaching-server.log"
   setsid nohup python3 -m http.server 8000 > "$LOG" 2>&1 < /dev/null &
   ```

   The log holds one line per request — useful for spotting a 404 on an asset
   the page silently failed to load.

   Use `setsid nohup` so the server outlives this session — the user is
   debugging in their own browser. Do **not** use the Bash tool's
   `run_in_background`, which ties the process to the session.

3. **Verify** it actually serves before reporting success:

   ```bash
   curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/
   curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/cs442-au2026/
   curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/cs442-au2026/calendar/
   ```

   All three should be `200`. A `404` on a directory URL means that directory is
   missing its `index.html`.

4. **Report the URLs** the user cares about, and how to stop it:

   - Landing page: <http://localhost:8000/>
   - CS 442 home: <http://localhost:8000/cs442-au2026/>
   - Calendar: <http://localhost:8000/cs442-au2026/calendar/>
   - Resources: <http://localhost:8000/cs442-au2026/resources/>
   - Stop with `pkill -f 'http.server 8000'`

## Notes

- No build step — edits to `.html` and `.css` show on a plain browser reload.
- The **calendar is generated**. After editing `calendar/schedule.py`, rerun
  `python3 cs442-au2026/calendar/generate.py` (from inside `calendar/`); the
  server picks up the new `index.html` on reload with no restart.
- `python3 -m http.server` does not send no-cache headers. If a CSS change does
  not appear, hard-reload (Ctrl+Shift+R) before suspecting the server.
