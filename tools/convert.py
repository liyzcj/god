"""Convert Markdown to WikiText"""

import re
import argparse
from typing import Text


TITLE_PATTERN =  re.compile(r"^(#{1,5})(\ .*)$", flags=re.MULTILINE)
def title(m):
    prefix = m.group(1).replace('#', '!')
    return prefix + m.group(2)


LINK_PATTERN = re.compile(r"""([^!]|^)\[(?P<text>.+?)\]\((?P<url>[^ ]+)(?: "(?P<title>.+)")?\)""", flags=re.MULTILINE)
def link(m):
    return f"{m.group(1)}[[{m.group('text')}|{m.group('url')}]]"


IMAGE_PATTERN = re.compile(r"""\!\[(?P<text>.+?)\]\((?P<url>[^ ]+)(?: "(?P<title>.+)")?\)""", flags=re.MULTILINE)
IMAGE_PATTERN2 = re.compile(r'''<img[^>]+src="(?P<url>[^">]+)".*\/>''', flags=re.MULTILINE)
def image(m):
    return f"[img[{m.group('url')}]]"

BORD_PATTERN = re.compile(r"""\*\*(?P<text>.*?)\*\*""", flags=re.MULTILINE)
def bord(m):
    return f"''{m.group('text')}''"


LIST_PATTERN = re.compile(r"^- ", flags=re.MULTILINE)
list_r = "* "


NUM_LIST_PAT = re.compile(r"^[1-9]\.", flags=re.MULTILINE)
num_list_r = "#"


CODE_PATTERN = re.compile(r"""\n```(?P<scheme>\w*)\n(?P<code>(\n|.)*?)\n```\n""")
def code(m):
    if not m.group('scheme'):
        scheme = 'bash'
    else:
        scheme = m.group('scheme')
    return f"""\n```{scheme}\n{m.group('code')}\n```\n"""


def _get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", help="The input Markdown file.", required=True)
    return parser.parse_args()


def convert(mdtext: Text):
    repl_patterns = {TITLE_PATTERN: title,
                     LINK_PATTERN: link,
                     IMAGE_PATTERN: image,
                     IMAGE_PATTERN2: image,
                     BORD_PATTERN: bord,
                     LIST_PATTERN: list_r,
                     NUM_LIST_PAT: num_list_r,
                     CODE_PATTERN: code,
                     }
    wikitext = mdtext
    for pat, repl in repl_patterns.items():
        wikitext = re.sub(pat, repl, wikitext)
    return wikitext


if __name__ == "__main__":
    args = _get_args()
    with open(args.input) as md_f:
        mdtext = md_f.read()
    wikitext = convert(mdtext)
    with open('./converted.tid', 'w') as f:
        f.write(wikitext)
