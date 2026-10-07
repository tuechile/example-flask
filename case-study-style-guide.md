# Case Study Style Guide

The layouts used across Pirenily's case studies, written down once so every case study is built the same way.

- **Template:** `templates/case_study.html` (page shell)
- **Building blocks:** `templates/partials/case_blocks.html` (one Jinja macro per layout below; each macro is tagged with its § number)
- **Styles:** `static/css/ux.css`

Pages built on it: `Projects/2ft.html`, `Projects/commonspirit.html`, `Projects/cs171.html`, `collab websites/hackharvard.html`, `collab websites/merch.html`, `personal websites/afvs.html`.

---

## Page anatomy

Every case study follows the same order. Only the hero is required.

```
progress bar           (automatic, from the template)
left rail              (automatic: back link, title, numbered section index; hidden under 1000px)
§1  Hero               kicker, title, subtitle, meta grid from "Label: value" tags
§4  Preview figure     the "money shot", directly under the hero
§8  TL;DR callout      3 numbered points max (UX case studies)
──  case-page body ──
    §2 Section → visuals (§4–§7) → caption (§10), repeated
    Stats              hard numbers, if there are any
    §11 Try it / CTA   near the end, if there's a live link
    §2 Reflection      always last
next case study        (automatic)
scripts                (automatic: rail, lightbox, progress)
```

The system, in one breath: small uppercase kickers (`.cs-kicker`, `--fs-kicker`) label everything,
big regular-weight Crimson lines carry the story, hairline panels hold the scannable bits, and teal
only marks numbers (section numbers, figure numbers, list numbers, the active rail dot). Nothing fades in.

Starter page:

```jinja
{% extends "case_study.html" %}
{% import "partials/case_blocks.html" as cs %}

{% block title %}| Project Name{% endblock %}

{% block case %}
{{ cs.hero("Project Name", "One sentence on what this is.", tags=["Role: …", "Scope: …"]) }}
{{ cs.figure(img('ux', 'project/preview.png'), "Describe the image", zoom=False) }}
{{ cs.callout("TL;DR", points=["…", "…", "…"]) }}

{% call cs.body() %}
    {% call cs.section("Context", lead="One bold line that sums up the section") %}
    <p>Body copy…</p>
    {% endcall %}
    …
{% endcall %}
{% endblock %}
```

Optional template blocks: `case_css` for page-only CSS, `case_scripts` for page-only JS.

---

## §1 Hero

Open, left-aligned header closed by a hairline. It opens every case study and names the rail.

| Part | Rule |
|---|---|
| `eyebrow` | Kicker above the title; defaults to "Case study" (e.g. "Ongoing \| CS 1710"). |
| `title` | The project name, `--fs-display`, regular weight. Use `×` for partner projects ("T4SG × 2ft Prosthetics"). |
| `subtitle` | One italic sentence. (`subtitle_size` is kept for old calls and ignored.) |
| `meta` | Optional date line, shown as a kicker on the right ("March–May 2026"). |
| `tags` | `Label: value` tags become the **meta grid** (Role, Team, Scope, Research, Constraint…); the value splits onto lines at ` + ` and ` · `, so write "5 designers & engineers" when it shouldn't split. Tags without a colon stay chips. |
| `href` | Turns the title into an outbound link (used for a secondary project on the same page; a second hero also gets its own rail entry). |

```jinja
{{ cs.hero("Merch", "Crests, logos and goods for student organizations.", tags=["HPAIR", "CNN Olympics"]) }}
```

## §2 Section

The main reading unit: a numbered eyebrow, a big line, then prose (66ch max).

- `heading`: the eyebrow ("01 · Context") and the section's rail entry. Keep it short: Context, Research, Ideation, My Contribution, Reflection. The number is added by the script.
- `lead`: the big `h2` under the eyebrow (`--fs-heading`). It's the takeaway, so write it as a sentence. Without a lead, the heading itself becomes the big line.
- `index`: a shorter rail label when the heading is long (`index="Iteration"`).
- No heading: a continuation of the previous section, with no number or rail entry.
- Body copy: `<p>` in `--text-secondary`. Lists are written as `<br>— item` lines or `1.` numbered lines inside a `<p>`.
- A heading-only section (no body) works as a divider before a group of visuals.

```jinja
{% call cs.section("Research", lead="Translating technical history into usable story units") %}
<p>…</p>
{% endcall %}
{{ cs.section("Campaign") }}   {# divider #}
```

## §3 Chapter

Centered opener for a multi-part art piece (afvs). Small theme line, `h2`, then an animated teal/white gradient poem.

```jinja
{{ cs.chapter("Chapter 1: A pig's death", theme="Theme: A view of my world",
              poem="I cannot see the world<br>The world is seeing what I cannot see") }}
```

## §4 Figure

One image in a media card, centered.

| Size | Max width | Use for |
|---|---|---|
| *(default)* | 750px | Preview / hero shots |
| `sm` | 420px | Diagrams beside text, small boards |
| `md` | 600px | Sticker sheets, single objects |
| `lg` | 800px | Key art, final screens, full-bleed moments |

- Images are click-to-zoom (`lightboxable`) by default; the top preview uses `zoom=False`.
- Cards are 18% grayscale until hover. Don't fight it with inline filters.
- `caption=` adds a §10 caption underneath.

```jinja
{{ cs.figure(img('design', 'hackharvard/banner.jpg'), "Banner with a domed tower", size="lg", caption="Campaign banner.") }}
```

## §5 Rows (multi-image)

Several media cards side by side. Pick the layout by count and intent:

| `layout` | Columns | Phone | Use for |
|---|---|---|---|
| `pair` | 2 equal | **stays 2-up** | Before/after, A vs B, two posters |
| `equal` | 2 equal | stacks | Two placeholders or large pieces that need full width on phone |
| `auto` | 1.1fr / 0.9fr | stacks | Two process shots of different sizes |
| `3` | 3 equal | stacks | Three states / three screens |
| `quad` | 4 equal | stacks | Angles, logo sets, merch lineups |

Cells are `cs.card(...)`, `cs.video_card(...)` or `cs.placeholder(...)`.

```jinja
{% call cs.row("pair", caption="Key art and event mark.") %}
    {{ cs.card(img('design', 'hackharvard/keyart.jpg'), "Key art") }}
    {{ cs.card(img('design', 'hackharvard/mark.png'), "Event mark") }}
{% endcall %}
```

- **Placeholder** (`cs.placeholder("Coming soon")`): dashed, italic box for work that isn't ready. Never leave a broken image. On its own, wrap it in `{% call cs.block() %}`.
- **Video** (`cs.video_card(src, types=[...])`): autoplay, muted, looped, inline. Use it for motion pieces, never with sound.

## §6 Mockup strip

Bare screenshots (no card) that wrap in a centered strip, 260–420px each. Use for 2–3 UI screens at the same fidelity (lo-fi, hi-fi, iterations).

```jinja
{{ cs.mockups([(img('ux', 't4sg/hifi view.png'), "Hi-fi view"), (img('ux', 't4sg/hifi edit.png'), "Hi-fi edit")],
              caption="(1) View component, (2) Edit component") }}
```

## §7 Media + text

A small image beside a text column, for "here's the artifact, here's what it means" (impact/effort maps, storyboards, user flows).

- Default: image column slightly wider (1.1 / 0.9).
- `flow=True`: text column wider (0.85 / 1.15), for when the explanation is longer than the diagram is tall.
- Stacks on screens under 880px.

```jinja
{% call cs.media_text(img('ux', 't4sg/userflow.png'), "User flow", heading="Flow Breakdown", lead="View Component", flow=True) %}
<p>…</p>
{% endcall %}
```

## §8 Callouts

Hairline panel on the frosted `--glass` fill, for content that should be scannable rather than read.

- **TL;DR / Goals / Principles:** a kicker title plus 3 points, numbered 01–03 in teal (each point one sentence). `display` is ignored now: BHN Cinema stays in the logo.
- Panels fill the reading column (`wide` is kept for old calls).
- `text=` for a single paragraph instead of bullets.
- **Compare** (`cs.compare([...])`): two equal callouts side by side, such as "What we observed / What we changed" or "What wasn't working / What changed". Always two.

```jinja
{{ cs.callout("TL;DR", points=["…", "…", "…"]) }}
{{ cs.compare([
     {"title": "What we observed", "points": ["…", "…"]},
     {"title": "What we changed",  "points": ["…", "…"]},
   ]) }}
```

## Stats

Results with hard numbers: a row of big figures, each over a hairline with an italic label. Up to four.

```jinja
{{ cs.stats([("200%", "higher social engagement"), ("2×", "applications, year over year")], title="Results") }}
```

## §9 Rollout grid

Phased cards (Phase 1/2/3) that read left to right. Use for feature roadmaps or project stages. Each phase has a label, a bold title and one line.

```jinja
{{ cs.rollout([("Phase 1", "Core Inventory Reliability", "Simple viewing, terminology, edit component.")]) }}
```

## §10 Caption

The `caption=` argument on figures, rows and mockups: a small italic line under the visual, numbered "Fig. 01, 02…" in teal. A bare `cs.img_caption(text)` is an unnumbered note (pass `fig=True` to number it). Write it as a sentence fragment that tells the reader what to notice ("Draft code → actual projection."), not a filename. Every multi-image row should have one.

## §11 Call to action

Link out to a live prototype, repo or press: a hairline panel with the site's host as a kicker, the label, and ↗. Lives inside a §2 section near the end. Label format: "Open the …" (a trailing " →" is dropped).

```jinja
{% call cs.section("Try It", lead="Explore the site") %}
<p>…</p>
{{ cs.cta("https://github.com/…", "Open the live project →") }}
{% endcall %}
```

## §12 Bespoke blocks

Some pieces stay hand-written HTML inside the template: the 2ft **Interview Insights explorer** (persona tabs, theme chips, expandable cards, "so what" strip) and the afvs **p5.js sketch**. Wrap anything bespoke in `{% call cs.block() %}` so it gets the same spacing as everything else, and put its JS in `{% block case_scripts %}`.

---

## Rules

1. **Build from the blocks.** If a layout isn't in this guide, add a macro and a section here first, then use it.
2. **No inline styles.** Every old one-off (`style="text-align:left; max-width:920px"`, `style="font-family:'BHN Cinema'"`, …) is now a class. Add a class to `ux.css` instead.
3. **Colors come from `:root` tokens** in `ux.css` (`--accent`, `--text-primary/secondary/tertiary`, `--bg-panel`, `--highlight`). Add a token rather than a hex.
4. **Every image gets real alt text** describing what's in it, not "Placeholder".
5. **Captions under rows, leads under headings.** Readers skim; those two lines carry the story.
6. **One accent.** Teal marks numbers and the active rail dot, never headings or body text.
7. **Bump `ASSET_VERSION`** in `app.py` after touching `ux.css` or the template.
8. **No fades.** Blocks are simply there; hover is the 1px blur.
