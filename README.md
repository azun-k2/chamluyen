# Chăm Luyện

Practice and tests for Vietnamese primary-school children, with a buddy who reads every question aloud.

This repository holds the app's public website (English at the root, Vietnamese in `vi/`; served by GitHub Pages at <https://azun-k2.github.io/chamluyen/>) and, as GitHub releases, the **downloadable voice packs** the app fetches after installation. The packs are content only (pre-recorded voice clips); the app sends nothing about the child.

Voices are generated with VieNeu-TTS v3 Turbo (Apache-2.0) and VoxCPM2 (Apache-2.0). No real person's voice is cloned.

Icons are regenerated from the app with `../_tools/make-site-icons.py` run in `../ChamLuyen`.
The store badges and the "More apps" grid are written by `../_tools/site-family.py apply`.
