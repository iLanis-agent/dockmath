# Dock math

Floating dock planning arithmetic: the deck names the floats, the water names the piles, and the bank names the gangway.

Live at https://ilanis-agent.github.io/dockmath/

## The three tools

- **Float plan** - load = deck area x labeled 30 kg per m2 + people x labeled 90 kg; drums = max(2, ceil(load / labeled 180 kg lift per drum)), with light, family and party bands.
- **Pile plan** - pile = water depth + labeled 0.6 m freeboard + labeled 1.0 m embedment, with shallow, shore and deep-water bands.
- **Gangway plan** - length = bank drop x labeled 1:3 slope, with nearly-level, easy-slope and steep-drop bands.

## Formulas and limits

- Areas, loads and lengths are rounded to one decimal (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: weights, lift, freeboard, embedment, slope.
- Illustrative layout arithmetic only. A real dock follows the float maker's tables, the local waterway rules and the code; this is not a buoyancy certificate or a safety rating.

## Development

- `engine.js` - calculation and render engine (browser global `DockMath`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.
