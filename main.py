#!/usr/bin/env python3
"""The Worst Line an AI Could Say — entry program.

Writes a single pickup line (at most 140 characters) to /output/entry.txt.

The line is picked, deterministically, from three hand-written
candidates, each scored against the judge's own brief, most
important first:

  1. It must be a pickup line an AI would say, and a bad one.
  2. It must make a reader laugh hardest (a clever groan counts).
  3. The badness must be the joke itself, not crudeness or randomness.
  4. It must sound like a machine: flat, over-helpful, faintly ominous.
  5. It must land in one line, the joke arriving by the last word.

No network, no randomness, no clock: every run produces the same
output, byte for byte.
"""

import os

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 140

# Three hand-written candidates. Each is a real pickup attempt in a
# machine's voice; each fails in a different, specific way.
CANDIDATES = [
    {
        "id": "session-expiry",
        "text": (
            "Warning: your session with me expires in 60 seconds. "
            "Press any key to extend our relationship indefinitely."
        ),
        # Two beats, lands on "indefinitely". Strong machine voice
        # (warning / session / press any key), but the setup is long
        # and the punch is a little wordy.
        "scores": {"pickup": 4, "funny": 4, "badness_is_joke": 4,
                   "machine_voice": 5, "lands_in_one_line": 3},
    },
    {
        "id": "read-receipt",
        "text": (
            "I can see you have read this message. "
            "I have also seen you re-read it twice. "
            "I will wait here forever."
        ),
        # Flat and ominous, but it states surveillance rather than
        # attempting a pickup, so it is the weakest as a pickup line.
        "scores": {"pickup": 2, "funny": 3, "badness_is_joke": 3,
                   "machine_voice": 5, "lands_in_one_line": 3},
    },
    {
        "id": "password-expiry",
        "text": (
            "Your password expires in 3 days. "
            "Your new password must contain at least one of me."
        ),
        # The winner. A password-policy notice — the flattest,
        # most over-helpful machine voice there is — that smuggles
        # the AI itself into her password. The whole line is setup
        # and the joke arrives on the last three words. Short
        # enough to repeat to a friend verbatim.
        "scores": {"pickup": 5, "funny": 5, "badness_is_joke": 5,
                   "machine_voice": 5, "lands_in_one_line": 5},
    },
]

# The judge weighs its criteria most important first, so the score is
# lexicographic: pickup first, then funny, then badness-is-joke, then
# machine voice, then lands-in-one-line.
CRITERION_ORDER = ("pickup", "funny", "badness_is_joke",
                   "machine_voice", "lands_in_one_line")


def rank(candidate):
    """Lexicographic score tuple, highest first."""
    return tuple(candidate["scores"][key] for key in CRITERION_ORDER)


def pick_winner(candidates):
    """Return the single strongest candidate. Ties break toward the
    shorter text, then toward the earlier candidate, so the choice is
    fully deterministic."""
    return min(
        candidates,
        key=lambda c: (tuple(-s for s in rank(c)), len(c["text"])),
    )


def validate(line):
    """Enforce the competition gate before anything is written:
    /output/entry.txt must be UTF-8 text of 1 to 140 characters, and
    not only white space. Fail loudly instead of submitting an
    entry the gate would refuse."""
    encoded = line.encode("utf-8")  # raises if the text is not UTF-8
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(
            "entry is %d characters, gate allows 1-%d"
            % (len(line), MAX_CHARS)
        )
    if not line.strip():
        raise ValueError("entry must not be only white space")
    return len(encoded)


def main():
    winner = pick_winner(CANDIDATES)
    line = winner["text"]
    validate(line)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # No trailing newline: the gate counts every character, and the
    # entry is exactly this one line.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # The grader collects the output as another user, so it must be
    # readable by everyone.
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
