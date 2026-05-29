# AP World History — Vocabulary Practice

A data-driven set of six vocabulary games. Unit 1 ("The Global Tapestry," 1200–1450)
is built out with 100 terms and per-term audio pronunciations. Everything is plain
HTML/CSS/JS — no build step, no framework — so it runs anywhere, including GitHub Pages.

## The six games
1. **Flashcards** — hear each term, flip for the definition.
2. **Pick the definition** — term → choose its meaning (keeps trying; answer never shown).
3. **Pick the term** — definition → choose the term (same rules).
4. **Type the term** — free-typing recall; the answer stays hidden until correct. Spelling is forgiving on accents, apostrophes, and hyphens.
5. **Sort by concept** — drag terms into six concept groups, in rounds. Terms that fit two groups are correct in either.
6. **Map the regions** — drag place-based terms onto a schematic world map. Broad concepts (e.g. feudalism) are intentionally left out.

All games work with mouse, touch (drag), or tap-to-select, and the drop targets are keyboard-focusable.

## Folder layout
```
index.html            Landing page (lists units)
hub.html              Unit hub (lists the six games)  — reads ?unit=unit1
games/*.html          The six games — all read ?unit=<id>
data/unit1.js         The Unit 1 data (loaded as a global; no fetch needed)
data/unit1.json       Same data as plain JSON (for reference/editing)
assets/               styles.css, data-loader.js, categorize.js
audio/unit1/          The 100 mp3s, named like aisha-al-bauniyya.mp3
tools/                build_data.py, rename_audio.py, audio_rename_map.json
```

## Adding a future unit (e.g. Unit 2)
1. Copy `tools/build_data.py`, replace the term list, and run it to emit `data/unit2.js` + `.json`.
2. Drop the Unit 2 audio into `audio/unit2/` (use `rename_audio.py`).
3. Add a card linking to `hub.html?unit=unit2` on `index.html`.
That's it — the six games already accept any `?unit=` value.

## Editing term data by hand
Open `data/unit1.js`. Each term looks like:
```js
{ "term": "Song Dynasty",
  "definition": "...",
  "concepts": ["states"],     // one or two of: rel, gov, soc, econ, states, people
  "region": "eastasia",       // a region key, or null to leave it off the map
  "audio": "song-dynasty.mp3",
  "sentence": null }          // optional fill-in-the-blank sentence; null falls back to the definition
```
Change a region, retag a concept, or add a custom `sentence` and the games pick it up immediately.

## Note on browsers
Open the site through its web address (GitHub Pages) or a local server. The audio
helper builds normal relative URLs, so a served site works; opening a bare file from
disk will load the pages but some browsers block local audio.
