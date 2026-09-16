"""Assemble tier2/index.html from the film engine template + shared tier1 sections.
Usage: python build.py <FRAME_COUNT> <SEAM_HEX>
"""
import sys, pathlib
here = pathlib.Path(__file__).parent
FRAMES = int(sys.argv[1]); SEAM = sys.argv[2]
style = (here/'_style.css').read_text(encoding='utf-8')
after = (here/'_after.html').read_text(encoding='utf-8')
footer = (here/'_footer.html').read_text(encoding='utf-8')
dialog = (here/'_dialog.html').read_text(encoding='utf-8')
tpl = (here/'_engine.html').read_text(encoding='utf-8')
out = (tpl.replace('/*SHARED_STYLE*/', style)
          .replace('<!--AFTER-->', after)
          .replace('<!--FOOTER-->', footer)
          .replace('<!--DIALOG-->', dialog)
          .replace('__FRAME_COUNT__', str(FRAMES))
          .replace('__SEAM__', '#'+SEAM.lstrip('#')))
(here/'index.html').write_text(out, encoding='utf-8')
print('wrote index.html', FRAMES, 'frames, seam', SEAM)
