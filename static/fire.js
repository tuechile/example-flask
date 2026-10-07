// A small fire crackle on every click of something interactive.
// Synthesized with Web Audio (filtered noise + a few pops), so there's no sound file.
(() => {
    const INTERACTIVE = 'a[href], button, input, select, textarea, label, summary, [role="button"], [onclick], [tabindex]:not([tabindex="-1"])';
    let ctx = null;
    let noise = null;

    function noiseBuffer() {
        const len = ctx.sampleRate;
        const buf = ctx.createBuffer(1, len, ctx.sampleRate);
        const data = buf.getChannelData(0);
        for (let i = 0; i < len; i++) data[i] = Math.random() * 2 - 1;
        return buf;
    }

    function burst(t, dur, freq, q, gain, type) {
        const src = ctx.createBufferSource();
        src.buffer = noise;
        src.playbackRate.value = 0.8 + Math.random() * 0.4;
        const filter = ctx.createBiquadFilter();
        filter.type = type;
        filter.frequency.value = freq;
        filter.Q.value = q;
        const env = ctx.createGain();
        env.gain.setValueAtTime(0.0001, t);
        env.gain.exponentialRampToValueAtTime(gain, t + Math.min(0.01, dur / 4));
        env.gain.exponentialRampToValueAtTime(0.0001, t + dur);
        src.connect(filter).connect(env).connect(ctx.destination);
        src.start(t, Math.random() * 0.5, dur + 0.05);
    }

    function fire() {
        if (!ctx) {
            const AC = window.AudioContext || window.webkitAudioContext;
            if (!AC) return;
            ctx = new AC();
            noise = noiseBuffer();
        }
        if (ctx.state === 'suspended') ctx.resume();
        const t = ctx.currentTime + 0.005;
        // Soft whoosh of the flame catching
        burst(t, 0.28, 600, 0.7, 0.12, 'lowpass');
        // A few crackles scattered over it
        const pops = 3 + Math.floor(Math.random() * 3);
        for (let i = 0; i < pops; i++) {
            burst(t + Math.random() * 0.22, 0.015 + Math.random() * 0.02,
                  1800 + Math.random() * 2500, 3, 0.18 + Math.random() * 0.12, 'bandpass');
        }
    }

    document.addEventListener('pointerdown', (e) => {
        if (e.button !== 0) return;
        const el = e.target;
        if (!(el instanceof Element)) return;
        if (el.closest(INTERACTIVE) || getComputedStyle(el).cursor === 'pointer') fire();
    }, { capture: true, passive: true });
})();
