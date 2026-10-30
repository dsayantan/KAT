# KAT (Krea Assessment Test) preparation site

Static site in `site/` — no build step needed to host it.

## Publish on GitHub Pages
Push this folder, then Settings → Pages → deploy from branch, folder `/site` (or copy `site/` to the repo root).

## Rebuild
`cd src && python3 build.py` regenerates every page. Numeric and puzzle answers come from `gen_numeric.py` / `gen_ps.py`
(computed). Verbal questions are in `verbal.py`, essays in `writing.py`, the official sample in `official.py`.

## Sources and gaps
- Only official material that exists: Krea's sample test (`krea.edu.in/sias/...Sample-Krea-Aptitude-Test-2023-24.pdf`; the 2022 file is identical) and the selection-process page. Not redistributed; linked.
- Krea publishes no syllabus beyond the four section names, no past papers, no key, no marking scheme.
- ASOKA / SNUSAT / BITSAT papers were NOT downloaded; level was calibrated from the Krea sample.
- Test timing is 80 min (as published); question counts (30 MCQs + essay) are our choice. No negative marking.
