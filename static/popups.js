// Hover a card with data-previews="url|url|..." and its pictures pop up at random spots on screen.
// Pops are instant (no fades); everything disappears the moment the mouse leaves.
(function () {
    if (!window.matchMedia("(hover: hover)").matches) return;
    var EVERY = 650, MAX_ON_SCREEN = 4;
    var layer = document.createElement("div");
    layer.className = "pop-layer";
    document.body.appendChild(layer);

    document.querySelectorAll("[data-previews]").forEach(function (card) {
        var urls = card.dataset.previews.split("|").filter(Boolean);
        if (!urls.length) return;
        var pics = null, timer = null, last = -1;

        function pop() {
            var ready = pics.filter(function (p) { return p.complete && p.naturalWidth; });
            if (!ready.length) return;
            var n = Math.floor(Math.random() * ready.length);
            if (ready.length > 1 && ready[n] === pics[last]) n = (n + 1) % ready.length;
            var src = ready[n];
            last = pics.indexOf(src);

            var w = Math.round(180 + Math.random() * 140);
            var h = Math.round(w * src.naturalHeight / src.naturalWidth);
            var el = document.createElement("img");
            el.className = "pop";
            el.src = src.src;
            el.alt = "";
            el.style.width = w + "px";
            el.style.left = Math.round(Math.random() * Math.max(0, innerWidth - w)) + "px";
            el.style.top = Math.round(Math.random() * Math.max(0, innerHeight - h)) + "px";
            layer.appendChild(el);
            while (layer.children.length > MAX_ON_SCREEN) layer.removeChild(layer.firstChild);
        }

        card.addEventListener("mouseenter", function () {
            if (!pics) {
                // load on first hover; each picture pops as soon as it arrives
                pics = urls.map(function (u) {
                    var im = new Image();
                    im.onload = function () { if (timer) pop(); };
                    im.src = u;
                    return im;
                });
            }
            timer = setInterval(pop, EVERY);
            pop();
        });

        card.addEventListener("mouseleave", function () {
            clearInterval(timer);
            timer = null;
            layer.innerHTML = "";
        });
    });
})();
