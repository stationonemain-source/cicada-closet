# The Cicada Closet — site build STATE (read first)

## 09-20 CLIENT ROUND 1 (Jenna's 9 edits) — LIVE on both Plan A pages
- Film = chapter 1 ONLY (film/assemble_keyhole.sh, 121 frames): full logo (contain-fit letterboxed on
  #2a1c11, eases to cover by p=0.20 in drawFrame) -> zoom into the keyhole -> black -> site rises out of
  the dark (--seam now #0a0705, landing gradient dark->kraft). NO wings. Wings frames kept in
  tier2/frames_wings_0917_bak. Self-heal in tick: displayed===-1 for >800ms resets bmpCenter (first-load
  black-canvas race seen once in the browser pane).
- Copy is STUDIO-VOICE everywhere outside the artist profile (her exact texts: intro, Artist Walls, bio,
  booking steps 1-2). Nav: Recent Works / The Space / Artists / Booking / Aftercare.
- "Recent Works" gallery is curated via works.json (tier1/ and tier2/, copied+path-rewritten into site/ by
  assemble_site.py). Jenna adds/removes pieces by editing that list + dropping a jpg in assets/ — no code.
- Artists section is a roster: repeat <article class="profile"> to add an artist (photo, role, bio,
  specialty chips, 4-tile folio, IG + booking buttons).
- Aftercare = sheet viewer at assets/aftercare/ (cicada-closet-aftercare.pdf + aftercare-sheet.jpg).
  CURRENTLY A BRANDED PLACEHOLDER (shared/make_aftercare_placeholder.py) — swap in Jenna's real sheet
  (pdf + page-1 jpg, same filenames), rebuild, push.
- User note 09-20 said "The Cicada Lounge" once — treated as a slip, everything stays Cicada Closet.

## 09-20 round-1 fixes (after Circle's review)
- FILM IS THE SITE: root / now redirects to /film/. The quiet one-pager is deprecated, kept at /classic/
  (internal only, never send). Circle: "she doesn't want a quiet one pager".
- Hero text no longer sits on the logo anywhere: film hero beat plays at p .58–.98 (on the black keyhole
  plunge) with a real scrim + heavy text-shadow. ⚠️ `.beat.hero` collides with the page's legacy `.hero`
  CSS (display:grid;min-height:88vh) — `.beat.hero{display:block;min-height:0}` overrides it; keep that.
- Mobile pass done at 375x812: letterboxed logo start looks right, sections stack, overflowX 0.
- tier1 got a `.statement` ink band under its hero (text off the logo) — moot while /classic/ is internal.

## 09-20 ROUND 2b — 3D card on an EVEN desk (BUILT LOCALLY, **NOT DEPLOYED**)
Circle: the flat card "isn't 3d like the other", the background showed "2 tone", and
"i would the whole background to be the same tone or color, texture so the logo sits pretty".
Live is ROLLED BACK to 28a17c2; this work is committed locally and must not be pushed to the
`pages` branch until Circle says so.

- `film/build_wood.py` — measures the plate's low-frequency illumination and divides it out, so
  the whole background is ONE tone and ONE texture (quadrant spread 19 -> 4.0), then grades it to
  a single walnut `TONE=(63,50,42)`. This is what kills the two-tone.
- `film/build_card3d.py` — warps her logo onto the table plane (perspective, 2.4 deg tilt),
  lights it from the upper left like the plate, casts a two-part shadow from the card's own
  silhouette, adds a lit near edge for paper thickness, and defocuses only the far edge.
  **Her artwork is warped, never repainted.** It PRINTS the constants the engine needs.
- Engine constants now `KX=0.5151 KY=0.3840 KW=0.0318 AW=0.7524 AH=0.6682`; `.vig` is hidden
  (its radial gradient was itself a tonal ring). Keep these in step with `film/preview_hero.py`.
- Mobile type tightened so the address fits one line under 480px.

## 09-20 ROUND 2 — new logo, code-driven hero
The hero no longer plays video. `film/logo_new.webp` (her new art-nouveau logo, 1100x1100) is
built by `film/build_hero.py` into:
- `assets/hero-wood.jpg` — the desk, **stationary**, `background:cover` on `.stage .wood`
- `assets/logo-card.webp` — 2800x2800, her artwork at 2200 with 300px shadow padding and a
  baked two-part contact shadow (tight + ambient) on transparency

The engine scales ONLY the card, about the keyhole, on a **viewport-sized canvas**. Constants that
must move together (engine in tier2/index.html AND `film/preview_hero.py`):
`KX=0.4993 KY=0.3950 KW=0.0371 ART=0.7857`, easing `e=p^0.85`, fade `(p-0.62)/0.30`, film `340vh`.

⚠️ **Do not scale the card as a DOM `<img>` transform.** At the end of the push it is ~70,000px
wide; the compositor rasterises a layer that big and the tab dies. The canvas draws only the
visible source slice, so cost is flat.
⚠️ **Single-quoted paths in JS are NOT rewritten by `assemble_site.py`** (it only rewrites `"assets/`
and `url(assets/`). The card path lives in `data-src` on the canvas for that reason — a single-quoted
`card.src = 'assets/...'` 404s on the deployed `/film/` page.
⚠️ The old video frames are no longer deployed (site 25MB → 11MB). They remain in `tier2/frames*`.

**Verify the hero with `python film/preview_hero.py`, not the browser pane.** It mirrors the engine's
maths and writes `film/hero_preview_{phone,desktop}.jpg`. When the pane is hidden, rAF is throttled to
~1 frame/1.5s, screenshots time out and return stale composites — that is the pane, not the page
(confirmed: DOM geometry correct while the capture disagreed).

## 09-20 HERO ROOT CAUSE — historical, superseded by round 2 above
**No source we own shows the whole sheet.** The paper runs off the TOP and the BOTTOM of both
`tier1/assets/hero-logo.jpg` and film frame 1 (measured: bottom row is only 8-9% wood, top row 36%,
sheet bbox touches y=0 and y=h-1). So "the logo sitting on the wood" cannot be cropped out of anything
we have -- it has to be invented. Four attempts, all discarded:
1. CSS background + letterboxed film frame → reads as a photo pasted on wallpaper (two different woods,
   hard rectangle edges, feather halo). This is what Circle caught on the phone.
2. Higgsfield `outpaint` (2 cr) → **REDREW HER LOGO** as generic sans-serif lettering with a different
   cicada. Never shipped. NEVER outpaint her artwork; the model regenerates, it does not preserve.
3. `film/build_plate.py` single-row extrusion → vertical streaking, blown-out row normalisation.
4. Same, 2-D mirrored bands → repeats the sheet like a filmstrip; kraft mode ghosted her logo across
   the field. Script kept as the record of what fails; do not ship its output.

**Shipped instead (honest, zero fabrication):** no background image at all. The film frame's own wood
bleeds edge to edge; where a narrow screen leaves space, the frame's edges fade into `#241811`, sampled
from the photo's own darkest wood (`#b08a64` for `?bg=tan`). One colour, nothing to mismatch.
`sRest = min(sCover, sFit)` keeps her full lettering on screen at every width; zoom lifts it to cover
and the fade disappears. `SHEET_FRAC = 0.795` is the sheet's width as a fraction of the frame.

**THE REAL FIX — ask Jenna for one photo:** the logo print lying on the studio's wood, shot from further
back so the whole sheet and the desk around it are in frame, portrait orientation for phones. Free, real,
permanent, and it retires every workaround above.

## 09-20 hero A/B (Circle's ask: text above the logo at rest, no late pop-in)
- The statement now shows from the start, CENTERED ABOVE the logo, and fades out over the first ~16% of
  scroll. The late "plunge" beat is gone.
- Two variants, one engine flag `?bg=` in /film/: **wood** (default, walnut bg, sheet at 84% resting on the
  desk, cream text) and **tan** (`?bg=tan`, paper-tone bg #9d7d5f, frame's wood bands source-cropped so the
  sheet sits flush, ink text, nav solid, vignette off). Crop releases late (kc after mix .45) so cover-fit
  hides the wood before the crop lets go — do not re-tie it to plain (1-mix), the wood strip flashes.
- Canvas is now alpha:true (background shows through the letterbox), with a #feather inset-shadow that
  fades with zoom. Once Circle/Jenna picks one, hard-code that variant as the default.
- 09-20 later: both hero backgrounds are now REAL TEXTURES made by Nano Banana 2 outpainting the hero shot
  itself (film/wood_raw.png + film/kraft_raw.png are the 2k masters; 3 cr total, balance 31.1):
  assets/hero-wood.jpg (walnut desk, "remove the paper") and assets/hero-kraft.jpg (blank kraft, "remove
  the ink"). Feather colors sampled from the texture edges (#3a2a1e / #bc936f).
- 09-20: Jenna's REAL aftercare sheet arrived (the @jens.art "Tattoo Aftercare / Week 1-3" page) and
  replaced the placeholder at assets/aftercare/ (jpg preview + PDF). Placeholder script kept but obsolete.

Built 2026-09-16 from Plan A "The Keyhole". Client: Jenna Feezel, @jens.art / @thecicadacloset, 755 S Jenkins Ave, Norman OK. NOT yet sent to her.

## PUBLIC (GitHub Pages, all noindex)
- Plan A tier 1 (Keyhole one-pager): https://stationonemain-source.github.io/cicada-closet/
- Plan A tier 2 (scroll-film, 1080p MASTER 09-17): https://stationonemain-source.github.io/cicada-closet/film/
- Plan B tier 1 (Field Guide): https://stationonemain-source.github.io/cicada-closet/field-guide/
- Plan B tier 2 (Living Plates): https://stationonemain-source.github.io/cicada-closet/living-plates/
- Plan C tier 1 (Healed + healing dial): https://stationonemain-source.github.io/cicada-closet/healed/
- Repo stationonemain-source/cicada-closet (public). main = workspace, pages = site/ split.
- Redeploy: python planB/build.py; python planB2/build.py; python planC/build.py; python tier2/build.py 301 997656;
  python shared/assemble_site.py; commit; git branch -D pages; git subtree split --prefix site -b pages; git push -f origin pages

## Shared nav (every page)
shared/nav.css|nav.html|nav.js, rendered by shared/build_nav.py. Pages mark [data-nav-over] (transparent over hero/film)
and [data-nav-dark] (ink bar). Tier1 embeds it directly: after editing shared/*, run python shared/reembed.py.
Verify: node shared/navshots.js <url> <prefix>.

## FACTS — verified sources only (09-16 correction)
The first build invented claims (deposit, "sends design before appointment", "trained as painter first",
"one chair", art-show crowd). All removed. Plate names now come from Jenna's own captions:
stag beetle seraphim (was "moth of eyes"), bluebird (was "sparrow"), pink skies (was "sunset mirror"),
murals for Mira's room (was "cicada studies"). Captions + originals via Instagram embed pages — see ref/posts/hires.txt.
Sources: GBP (5.0, 9 reviews, opens 10am, no phone), flyers (grand opening Sat July 11 2026; gallery wall 100%/no fees),
@jens.art bio (BFA, licensed, owner), highlights names (Booking, Healed, Aftercare, WANNADO, BFA Exhibit).

## Plan C before/after slider — NOT BUILT (no data)
Needs fresh+healed pairs of the same piece. They are in Jenna's Healed story highlight, which needs a login.
Never generate "healed" versions. Ask Jenna for 4–6 pairs.

## Deliverables
- tier1/index.html — quiet premium one-pager (GSAP+Lenis). Artifact: https://claude.ai/artifact/BAHaTRshePYqFcbbB9QnqS
- tier2/index.html — scroll-film (5 Seedance chapters, DRAFT 480p). Artifact: https://claude.ai/artifact/RcYVv3y7AzsSGGeissV1nL
  Built from tier2/_engine.html + tier1 pieces by `python tier2/build.py 301 9c7755`. Frames ship per-file in tier2/frames/hd + sd, fetched coarse-to-fine as blobs, decoded near the playhead (sheets retired; old engine at tier2/_engine.sheets.bak).
- Plans artifact: https://claude.ai/artifact/74yuWLcSaouPQVo4Q3KRms

## Film (film/)
keys/key01.png = Nano Banana Pro keyframe from her logo. clips/ch1..ch5.mp4 chained last-frame→start-image, all junctions SSIM ≥ 0.91.
Prompts ch1..ch5.txt. chain.sh / assemble.sh are bash ports (skill scripts are zsh). Master 601 frames → 301 extracted at 864px.
MASTERED at 1080p 09-17: clips/h1..h5.mp4 (chain.sh ... 1080p), assemble_hd.sh → tier2/frames/{hd,sd} (1600px q3 / 960px q4), engine picks the set by screen size. h5 seam SSIM 0.69 = a 4-level exposure step, matched with GRADE_h5 eq in assemble_hd.sh. Cost 5×55 = 275 (342 → ~168 after h5 bills). Re-run: bash chain.sh chN <start> chN.txt <prev-last> 1080p --image <refs>.

## Higgsfield gotchas (cost a session)
- `--mode fast` returns "Error: Not found" — omit --mode entirely.
- The CLI hangs when its stdout is piped straight into head, or run under `timeout` (background process group). Capture with $(...) and add </dev/null.
- Rapid back-to-back creates stall; space them or use the loop in film/upscale.sh.
- ~1 in 7 jobs fails unbilled; retry the same call.

## Local preview
python -m http.server 4780 --directory C:/Users/Circl/.station/sites/cicada-closet  → /tier1/ and /tier2/
Verify: node ~/.claude/skills/scroll-film-studio/scripts/verify.js shot|jank <url>

## Credits
Start 500.1 → now: main@station.solutions — plus plan, 401.1 credits
Jank (tier2, 1440x900): avg 7.5ms, p95 ~15ms, max ~155ms once per run (1 frame over 50ms).

## Open
- Ask Jenna for full-res originals + logo file + yes on animating her drawings.
- Master the film at 1080p after Circle approves the seams.
- Hosting: GitHub Pages (above). Remove the noindex tag once Jenna approves.

## Plan B tier 2 — The Living Plates (planB2/)
GSAP 3.12.5 + ScrollTrigger + Lenis. Scene 1: cloth book on a walnut desk, cover rotates open (endpaper = her mark
repeated), title page zooms to fill, fades to paper. Scene 2: pinned horizontal run of 7 plates; each draws its frame,
inks in a LINE LAYER, then the real photo opens from the centre. Phones and reduced motion get a vertical run.
Line layers: planB2/extract.py — local-contrast ink extraction from her own photos x Higgsfield
image_background_remover limb mask (4 credits, 401 -> 397). Tuning per piece in TUNE; CLEAR boxes remove strays.
Nothing is redrawn; the page says so. Studio plate = shop photo cropped to the sharp room.
Jank (headless, software GPU): p95 ~9ms, max 78-177ms; traced to GPU raster of newly visible plates. Blend mode and
nav backdrop blur removed on this page because they inflated it. Not yet measured on real hardware.
Gotchas: PIL MinFilter(1) crashes the interpreter (exit 127, no traceback) — guard erode >= 3.

## 09-17 chapter 3 re-take
Circle flagged the flower-to-forearm section as not smooth. Measured: h3 v1 had 6 frame jumps (max step 28 vs median 7)
at 2.5-3.1s. Re-took h3 at 1080p pinned to the same end frame (--end-image clips/h3_v1-last.png) with a gradual-morph
prompt (h3b.txt): max step 8, seam into h4 still 0.91. It has one soft ~8-frame blend from bokeh into the arm.
v1 kept as clips/h3_v1.mp4. Remaining fast moment: end of ch1, the camera lunges into the keyhole (scrub frames 59-60).
Credits after re-take: 46.

## 09-17 short film (Jenna liked the scroll, not the length)
Film = chapter 1 + chapter 2 only: logo -> through the keyhole -> blue luna moth wings -> wings part on golden light.
film/assemble_wings.sh (every frame, 241; hd 1600 q4 22MB, sd 960 q5 11MB), seam #ac7646. Page: .film 480vh, hero beat
only, fade to the golden seam from p .80, .landing overlaps the film by 70vh (transparent -> gold -> kraft) so the site
rises over the wings with no empty screen; nav leaves "over" mode when kraft reaches it. Full 5-chapter version:
tier2/_engine.fullfilm.bak + film/frames_fullfilm_bak + film/assemble_hd.sh (h3 = re-take).
Studio info card redesigned (tier1, synced to film site): ink header with cicada mark, labelled rows with
Directions / Message actions, review as a pull quote on a ticket stub.

## 09-17 polish pass (approved by Circle before push)
shared/polish_0917.py: heading spacing, aftercare cards, studio collage (clean room crop, gallery-wall detail, real
grand-opening poster; chair snapshot + logo tile dropped), artist scale + new line "Painter, licensed tattoo artist,
and the owner behind the keyhole." (our wording, not Jenna's), dark footer. Film handoff gradient eased with extra
stops; phone overlap shortened to 46vh.

## 09-17 dark gap shortened
Circle: too much dark between keyhole and wings. Frames 136-172 (the black stretch) now every 4th frame: 241 -> 214 frames, 42 dark frames -> 13, film 437vh. Full-length frames kept in tier2/frames_wings_full.

## Domain + handover facts (checked 2026-09-18)
- `cicadacloset.com` IS registered: GoDaddy, created 2025-01-13, expires 2027-01-13, GoDaddy default NS, serves
  GoDaddy's parked "/lander" page, no MX. Owner hidden by privacy. The date fits the studio opening, so it may be
  Jenna's and never set up -- ASK HER before buying anything. If hers: connect it. If not: register
  `thecicadacloset.com` (available 09-18) in HER name.
- No analytics on any of the 5 pages. All 5 carry noindex. Hosting is Station's GitHub (stationonemain-source).
- Images are Jenna's own Instagram work (fine to hand over). The film is Higgsfield/Seedance output generated on
  Station's paid account from a Nano Banana keyframe of her logo -- confirm Higgsfield's commercial terms before
  telling her she "owns" the film.
- Quote sent: $750 build, $49.99/mo managed offered then made optional. station.solutions lists storefront sites
  as Premium $500 + $49/mo Care or Custom $1,250 + $49/mo Care; the quote matches neither.
