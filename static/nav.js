// Phone menu: the "=" button opens the full-screen nav list; tap again, pick a link or press Esc to close
(function () {
    var btn = document.querySelector(".nav-toggle");
    if (!btn) return;
    var root = document.documentElement;

    function setOpen(open) {
        root.classList.toggle("menu-open", open);
        btn.setAttribute("aria-expanded", String(open));
        btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }

    btn.addEventListener("click", function () {
        setOpen(!root.classList.contains("menu-open"));
    });
    document.querySelectorAll(".nav-item-big .nav-item").forEach(function (link) {
        link.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") setOpen(false);
    });
    // back on a wider screen the menu is just the normal nav again
    window.matchMedia("(max-width: 666px)").addEventListener("change", function () { setOpen(false); });
})();
