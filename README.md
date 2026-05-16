# CrowdLuma Stadium Choreo

Open-source static web app to design supporter-tribune choreographies.

The goal: turn a stadium stand into a pixel matrix. Each seat can either display a phone color or receive instructions for flags, clothes, cards, ponchos or other approved visual props.

## Principles

- 100% static: HTML/CSS/JavaScript only.
- Free hosting: GitHub Pages, Cloudflare Pages, Netlify, Vercel static.
- Open source: MIT license.
- Privacy-first: no backend, no account, no tracking by default.
- Works offline after page load for simple scenarios.
- Designed for clubs to enter their stand data, images, colors and timing.

## MVP features

- Define stand size: rows × seats.
- Upload an image/logo.
- Convert the image into a pixel grid using a limited color palette.
- Generate seat IDs like `R12-C34`.
- Open a direct supporter view from URL parameters: `?stand=Tribune%20Nord&block=A&row=12&seat=34`.
- Export a CSV registry of all seats and their unique URLs for QR code production.
- Generate QR codes per seat with the optional open-source Python tool.
- Show a supporter view by seat.
- Show a director/regie preview.
- Export choreography JSON.
- Import choreography JSON.

## Intended modes

1. **Phone pixel mode** — the phone screen displays the color.
2. **Instruction mode** — the phone tells the supporter which flag/card/color to show.
3. **Hybrid mode** — phone color + next action instruction.

## Deployment on GitHub Pages

1. Put these files in a GitHub repository.
2. Go to **Settings → Pages**.
3. Select branch `main`, folder `/` or `/docs`.
4. Open the generated GitHub Pages URL.

No server required.


## Admin console included in MVP1

`admin.html` is the first administration interface. It is still 100% static and free to host on GitHub Pages.

The club/admin can:

- enter stand, block, rows and seats;
- choose phone/instruction/hybrid mode;
- upload a photo or logo;
- upload a video and extract multiple frames;
- convert visual media into a low-resolution stand grid;
- preview each frame;
- export a `show.json` file;
- publish/import that JSON in the supporter/regie web app.

MVP1 deliberately has no backend login or database. Everything is processed in the browser. For a later production version, admin persistence can be added through GitHub commits/API, Supabase/Firebase, or a small private backend.

## Unique QR codes per seat

Each seat can have its own URL:

```text
https://club.github.io/stadium-choreo-web/?stand=Tribune%20Nord&block=A&row=12&seat=34
```

When a supporter scans the QR code on their seat, the app opens directly on the right stand/block/row/seat.

### Browser-only registry

Inside the web app, set the public GitHub Pages URL, then click:

```text
Exporter CSV sièges + URLs QR
```

This produces `seat-qr-urls.csv`, which can be sent to a print/QR workflow.

### Optional QR image generator

Install the small open-source dependency in a local venv:

```bash
cd modules/operations/stadium-choreo-web
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/generate_seat_qr.py \
  --base-url https://club.github.io/stadium-choreo-web/ \
  --stand "Tribune Nord" --block A --rows 50 --cols 50 \
  --out dist/tribune-nord-a
```

Outputs:

- `seat-registry.csv`
- `qrs/*.png`
- `print-sheet.html`

## Safety notes

- Avoid aggressive flashing/stroboscopic effects.
- Provide a photosensitivity warning.
- Use human stewards/capos for live coordination.
- Do not use pyrotechnics or hazardous props without formal authorization.
- Validate all stadium/security requirements before live use.

## Roadmap

- Multi-frame animations.
- Time/BPM sequencing.
- QR code per seat.
- CSV/PDF export per row.
- Seat map with unavailable seats and aisles.
- Regie console with start/pause/next.
- Offline preloaded show mode.
