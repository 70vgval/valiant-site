# Valiant Australia

A tribute website celebrating Chrysler Australia's legendary Valiant — from the R Series of 1962 to the final CM of 1981.

**Hey Charger!**

## Pages

| Page | Description |
|------|-------------|
| [Home](index.html) | Hero banner in classic "Hey Charger!" style |
| [Model Timeline](timeline.html) | Interactive timeline from RV1 → CM |
| [Charger Performance](charger.html) | E38/E49/E55 spotlight |
| [Marketing Archive](archive.html) | Recreated period-style advertisements |
| [Engine Tech](engines.html) | Slant-6, Hemi-6, Fireball V8 |
| [Gallery](gallery.html) | High-contrast retro photo layout |
| [Production History](production.html) | Tonsley Park & Lonsdale foundry |
| [Owner Stories](stories.html) | Community submissions |

## Branding

- **Primary colours:** `#FF6A00` (Vitamin C), `#F2C200` (Mustard), `#0A0A0A` (Black)
- **Headings:** League Gothic, Anton
- **Body:** Roboto

## Image pipeline

Stylized timeline illustrations are generated from Wikimedia Commons photographs:

```bash
python3 scripts/fetch_and_stylize.py
```

Source photos are saved to `assets/source/`, stylized PNGs to `assets/models/`, and licence metadata to `assets/attributions.json`.

## Running Locally

No build step required — open `index.html` in a browser, or serve with any static file server:

```bash
python3 -m http.server 8080
```

Then visit [http://localhost:8080](http://localhost:8080).

## Disclaimer

This is an enthusiast tribute site. Not affiliated with Stellantis or Chrysler LLC.
