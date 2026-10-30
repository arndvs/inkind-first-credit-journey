"""Renders the library outside Braze.

Braze resolves {{content_blocks.${name}}} on its servers and runs tags that plain
Liquid doesn't have. This harness inlines each Content Block from blocks/ by file
name and swaps the Braze-only syntax for fixture data:

  custom_attribute.${x}          -> x               (profile fields from the fixture)
  context.${x}                   -> entry.x         (Canvas context)
  ${user_id}, unsubscribe URL    -> fixture values
  preference_center.${name}      -> fixture value
  catalog_items restaurants {id} -> items = catalog[id]   (unknown ID -> empty list, as in Braze)
  connected_content ... :save x  -> removed; the fixture supplies recs
  abort_message("reason")        -> raises Abort(reason)
"""
import re
from pathlib import Path
from liquid import Environment

LIQUID_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = LIQUID_DIR.parent
BLOCKS = {p.stem: p.read_text().rstrip("\n") for p in sorted((LIQUID_DIR / "blocks").glob("*/*.liquid"))}
BLOCK_LAYER = {p.stem: p.parent.name for p in (LIQUID_DIR / "blocks").glob("*/*.liquid")}


class Abort(Exception):
    pass


def _abort(reason):
    raise Abort(reason)


_env = Environment()
_env.add_filter("abort", _abort)


def inline_blocks(src, blocks=BLOCKS, depth=0):
    if depth > 10:
        raise RuntimeError("Content Blocks nested more than 10 deep")

    def replace(match):
        name = match.group(1)
        if name not in blocks:
            raise KeyError(f"no Content Block named {name}")
        return inline_blocks(blocks[name], blocks, depth + 1)

    return re.sub(r"\{\{content_blocks\.\$\{(\w+)\}\}\}", replace, src)


def to_plain_liquid(src, blocks=BLOCKS):
    src = inline_blocks(src, blocks)
    src = re.sub(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", "", src, flags=re.S)
    src = re.sub(r"custom_attribute\.\$\{(\w+)\}", r"\1", src)
    src = re.sub(r"\bcontext\.\$\{(\w+)\}", r"entry.\1", src)
    src = src.replace("${user_id}", "user_id").replace("${set_user_to_unsubscribed_url}", "unsubscribe_url")
    src = re.sub(r"\{\{preference_center\.\$\{\w+\}\}\}", "{{ preferences_url }}", src)
    src = re.sub(r'\{%-?\s*abort_message\("([^"]*)"\)\s*-?%\}', r'{{ "\1" | abort }}', src)
    src = re.sub(r"\{%-?\s*catalog_items restaurants \{\{ saved_id \}\}\s*-?%\}",
                 "{%- assign items = catalog[saved_id] -%}", src)
    src = re.sub(r"\{%-?\s*connected_content [^%]*-?%\}", "", src)
    return src


def render(src, context, blocks=BLOCKS):
    """Render Liquid source. Returns the output, or raises Abort(reason)."""
    try:
        return _env.from_string(to_plain_liquid(src, blocks)).render(**context)
    except Abort:
        raise
    except Exception as error:
        cause = error.__cause__ or error.__context__
        if isinstance(cause, Abort):
            raise cause from None
        raise


def render_or_abort(src, context, blocks=BLOCKS):
    """Like render, but returns 'ABORT: reason' instead of raising."""
    try:
        return render(src, context, blocks)
    except Abort as abort:
        return f"ABORT: {abort}"


def message(name):
    return (LIQUID_DIR / "messages" / name).read_text()


def single_file_message():
    return (REPO_DIR / "03-message.liquid").read_text()
