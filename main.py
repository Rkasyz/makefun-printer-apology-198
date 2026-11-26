"""The Printer Apology — make.fun entry.

Writes a single apology of at most 120 characters, in the voice of an
office printer apologising to the people who keep jamming it, to
``entry.txt`` inside the output directory.

The program is deterministic: it writes the same bytes on every run,
with no time, no randomness and no network access.
"""

import os

ENTRY = (
    "Sorry I jammed. You fed me cheap paper, slammed my tray, "
    "and swore at me. I printed your rage. It was beautiful."
)

# Gate: entry.txt must be UTF-8 text of 1 to 120 characters, not only
# whitespace, on a single line. This line is exactly 112 characters,
# counted by hand, with no trailing newline in the file.
MIN_CHARS = 1
MAX_CHARS = 120


def validate(entry: str) -> None:
    """Fail loudly if the entry ever drifts outside the gate."""
    assert MIN_CHARS <= len(entry) <= MAX_CHARS, (
        f"entry is {len(entry)} chars, gate is {MIN_CHARS}-{MAX_CHARS}"
    )
    assert entry.strip(), "entry must not be only whitespace"
    assert "\n" not in entry and "\r" not in entry, "entry must be one line"


def main() -> None:
    validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Read back and confirm the file holds exactly the validated entry:
    # no trailing newline, no encoding surprise, nothing appended.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == ENTRY, "entry.txt differs from the validated entry"
    validate(written)


if __name__ == "__main__":
    main()
