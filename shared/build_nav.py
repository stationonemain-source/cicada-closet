"""Render the shared nav for a page. links = [(hash, label, sheet_note)]"""
import pathlib
here = pathlib.Path(__file__).parent


def render(links, root='', home='#top'):
    html = (here / 'nav.html').read_text(encoding='utf-8')
    top = '\n'.join(f'    <a href="{h}">{l}</a>' for h, l, _ in links)
    sheet = '\n'.join(f'    <a href="{h}">{l}<small>{n}</small></a>' for h, l, n in links)
    return (html.replace('{{ROOT}}', root).replace('{{HOME}}', home)
                .replace('{{LINKS}}', top).replace('{{SHEET_LINKS}}', sheet))


def css():
    return (here / 'nav.css').read_text(encoding='utf-8')


def js():
    return (here / 'nav.js').read_text(encoding='utf-8')
