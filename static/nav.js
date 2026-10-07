// One teal hairline under the nav: rests on the current page, slides to whatever is hovered
(function () {
    document.querySelectorAll(".nav-item-big").forEach(function (bar) {
        var items = bar.querySelectorAll(".nav-item");
        if (!items.length) return;
        var line = document.createElement("span");
        line.className = "nav-indicator";
        bar.appendChild(line);
        bar.classList.add("has-indicator");
        var current = bar.querySelector('.nav-item[aria-current="page"]');

        function moveTo(item, animate) {
            if (!item) { line.classList.remove("on"); return; }
            // first placement snaps; later moves slide
            if (!animate) line.style.transition = "none";
            var pad = parseFloat(getComputedStyle(item).paddingLeft);
            line.style.width = (item.offsetWidth - pad * 2) + "px";
            line.style.transform = "translateX(" + (item.offsetLeft + pad) + "px)";
            if (!animate) { line.offsetWidth; line.style.transition = ""; }
            line.classList.add("on");
        }

        items.forEach(function (item) {
            item.addEventListener("mouseenter", function () {
                moveTo(item, line.classList.contains("on"));
            });
        });
        bar.addEventListener("mouseleave", function () { moveTo(current, true); });
        window.addEventListener("resize", function () { moveTo(current, false); });
        document.fonts.ready.then(function () { moveTo(current, false); });
    });
})();
