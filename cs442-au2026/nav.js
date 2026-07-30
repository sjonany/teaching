/*
 * Renders the nav bar shared by every page of this course.
 *
 * Each page includes this once, at the spot where the nav should appear:
 *
 *   <script src="nav.js"    data-base="."  data-tab="home"></script>      (course root)
 *   <script src="../nav.js" data-base=".." data-tab="calendar"></script>  (one level down)
 *
 *   data-base : relative path from that page back to the course root
 *   data-tab  : key of the tab to highlight; omit for none
 *
 * To add, remove, rename, or reorder tabs, edit TABS below. That is the only
 * place tabs are listed, so no page needs to change.
 *
 * This file is per-course on purpose. Copying a course directory copies its
 * nav with it, so editing the current quarter's tabs never disturbs an
 * archived quarter.
 *
 * The nav is written synchronously at this script's own position in the
 * document, so it exists before the rest of the page parses. There is no
 * fetch and no flash of unstyled content.
 */
(function () {
    const COURSE_NAME = "CS 442: Algorithm Design and Analysis";
    const QUARTER = "Fall 2026";

    const TABS = [
        { key: "home",      label: "Home",      path: "" },
        { key: "calendar",  label: "Calendar",  path: "calendar/" },
        { key: "resources", label: "Resources", path: "resources/" },
    ];

    const script = document.currentScript;
    const base = script.dataset.base || ".";
    const currentTab = script.dataset.tab || "";

    // base is "." at the course root, ".." one level down, and so on.
    const url = (path) => base + "/" + path;

    const items = TABS.map((tab) => {
        const active = tab.key === currentTab ? ' class="active"' : "";
        return `<li><a href="${url(tab.path)}"${active}>${tab.label}</a></li>`;
    }).join("\n        ");

    script.insertAdjacentHTML("beforebegin", `<nav id="top-nav">
    <a class="navbar-brand" href="${url("")}"><h1>${COURSE_NAME}</h1></a>
    <ul class="navbar-nav">
        ${items}
    </ul>
    <span id="course-quarter">${QUARTER}</span>
</nav>`);
})();
