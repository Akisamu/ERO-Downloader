# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ERO-Downloader downloads hentai doujinshi from nhentai.com and eromanga-show.com, converts them to PDF, and provides a Gradio web UI. Terminal and GUI entry points share the same `modules/` backend.

## Commands

```bash
# Terminal mode (edit URLs in main.py first)
python main.py

# Web UI (Gradio on http://127.0.0.1:7860, LAN at http://<local-ip>:7860)
python app.py

# PowerShell shortcut (after one-time PATH setup)
ero
```

`cmd.bat` provides a menu to choose between terminal and web mode.

## Architecture

```
main.py          — terminal entry point, three input modes (A/B/C)
app.py           — Gradio Web UI, preview server on port 7861
modules/
  nhentai.py     — nhentai.com scraper (JSON-LD parsing) + image downloader
  eromanga.py    — eromanga-show.com scraper (Next.js RSC parsing) + downloader
  Utils.py       — shared: image compression, history CRUD, thumbnails
  ptf/
    i2p.py       — I2P class: PIL images → PDF, JPEG compression, Ghostscript
    ptf.py       — legacy CLI converter (images from disk)
    test.py      — legacy download test
```

### Data flow

1. `scrape_info(url)` → dict with `name`, `final` (pages), `id`/`article_id`, format/cdn
2. `get_images(info/url)` → concurrent downloads → list of `PIL.Image`
3. `I2P(images, pdf_name, image_quality, max_dimension)` → PDF
4. `record_history(...)` → `outputs/.history/info` (JSON Lines)
5. Thumbnails saved to `outputs/.history/thumbnails/` with uuid-based unique filenames

### Key design decisions

- **`I2P.output_dir`** is the canonical output path (`outputs/`). History and thumbnail functions use it.
- **`_sanitize_filename`** strips non-printable chars (including `\xa0`) from filenames — Windows compatibility.
- **History records** use JSON Lines (`.history/info`), newest-first. Each record has a `thumb` field with the unique thumbnail filename.
- **Concurrent downloads** use `ThreadPoolExecutor` (3 workers) with exponential backoff retry.
- **Format fallback**: when an image 404s in the primary format, the downloader tries `webp → jpg → jpeg → png`.
- **Gradio cross-tab sync**: History tab components are created first in code (so download tabs can reference them), then CSS `flex order` moves History to the end visually.
- **PDF preview**: a separate `HTTPServer` on port 7861 serves PDFs with `Content-Disposition: inline` so browsers open them rather than downloading. Links use the LAN IP auto-detected via socket.

### Submodule

`modules/ptf` is a separate git repo (`Picture-to-PDF`). Commit changes there first, then update the main repo's submodule reference.
