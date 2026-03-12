import re


def translate_md_table(txt: str) -> str:
    """Replace Markdown tables with key: value pairs."""

    txt = re.sub(r"(\|.+\n)+", table_to_text, txt)
    return txt


def table_to_text(match):
    """Md table → key: value lines. Header and separator rows are skipped."""

    rows = [r.strip() for r in match.group(0).strip().split("\n")]
    sep_idx = next((i for i, r in enumerate(rows) if "---" in r), None)

    skip = set()
    if sep_idx is not None:
        if sep_idx > 0:
            skip.add(sep_idx - 1)   # header before separator
        skip.add(sep_idx)            # separator itself
        # Also skip row after separator if it looks like a column-header row
        # (both cells non-empty, short, no bullets or <br>)
        nxt = sep_idx + 1
        if nxt < len(rows):
            nxt_cells = [c.strip() for c in rows[nxt].strip("|").split("|")]
            nxt_cells = [c for c in nxt_cells if c]
            if (len(nxt_cells) == 2
                    and all(len(c) < 15 and "•" not in c and "<br>" not in c
                            for c in nxt_cells)):
                skip.add(nxt)

    result = []
    for i, row in enumerate(rows):
        cells = [c.strip() for c in row.strip("|").split("|")]
        cells = [c for c in cells if c and c != "---"]
        if not cells or i in skip:
            continue
        if len(cells) == 2:
            key, value = cells[0], cells[1]
            if "•" in value:
                items = [item.strip() for item in value.split("•") if item.strip()]
                result.append(f"{key}:")
                result.extend(items)
            else:
                result.append(f"{key}: {value}")
        elif len(cells) == 1:
            result.append(f"- {cells[0]}")
    return "\n".join(result)
