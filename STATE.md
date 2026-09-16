# The Cicada Closet — site build STATE (read first)

Built 2026-09-16 from Plan A "The Keyhole". Client: Jenna Feezel, @jens.art / @thecicadacloset, 755 S Jenkins Ave, Norman OK. NOT yet sent to her.

## PUBLIC (GitHub Pages, all noindex)
- Plan A tier 1 (Keyhole one-pager): https://stationonemain-source.github.io/cicada-closet/
- Plan A tier 2 (scroll-film, 480p draft): https://stationonemain-source.github.io/cicada-closet/film/
- Plan B tier 1 (Field Guide): https://stationonemain-source.github.io/cicada-closet/field-guide/
- Plan C tier 1 (Healed + healing dial): https://stationonemain-source.github.io/cicada-closet/healed/
- Repo stationonemain-source/cicada-closet (public). main = workspace, pages = site/ split.
- Redeploy: python planB/build.py; python planC/build.py; python tier2/build.py 301 997656;
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
  Built from tier2/_engine.html + tier1 pieces by `python tier2/build.py 301 997656`. Frames ship as tier2/sheets (31 sprite sheets, 10 frames each, fetched as blobs).
- Plans artifact: https://claude.ai/artifact/74yuWLcSaouPQVo4Q3KRms

## Film (film/)
keys/key01.png = Nano Banana Pro keyframe from her logo. clips/ch1..ch5.mp4 chained last-frame→start-image, all junctions SSIM ≥ 0.91.
Prompts ch1..ch5.txt. chain.sh / assemble.sh are bash ports (skill scripts are zsh). Master 601 frames → 301 extracted at 864px.
MASTER at 1080p NOT run yet (≈275 credits). Re-run: bash chain.sh chN <start> chN.txt <prev-last> 1080p --image <refs>.

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
