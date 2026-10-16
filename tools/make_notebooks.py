"""Write and execute the completed teaching notebook; create a runnable practice book."""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"


def md(value: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": value.strip().splitlines(True)}


def code(value: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": value.strip().splitlines(True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": f"{sys.version_info.major}.{sys.version_info.minor}"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def save(name: str, cells: list[dict], *, execute: bool = False) -> None:
    if execute:
        namespace: dict = {}
        count = 0
        previous = Path.cwd()
        os.chdir(OUT)
        try:
            for cell in cells:
                if cell["cell_type"] != "code":
                    continue
                count += 1
                script = "".join(cell["source"])
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(compile(script, f"{name}:cell-{count}", "exec"), namespace)
                cell["execution_count"] = count
                if output.getvalue():
                    cell["outputs"] = [{
                        "output_type": "stream", "name": "stdout", "text": output.getvalue().splitlines(True)
                    }]
        finally:
            os.chdir(previous)
    (OUT / name).write_text(json.dumps(notebook(cells), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {name} ({len(cells)} cells, executed={execute})")


complete = [
    md("""# Regular expressions: follow along

This notebook accompanies the slides. Run it from `notebooks/` with `../data/talks_sample.csv` available. Predict each result before running the next cell. The slides also contain the outputs."""),
    code(r'''import re
from pathlib import Path
import pandas as pd

print("Ready to explore regex")'''),
    md("""## Recall last week's work

If income is missing more often for older respondents, observed age predicts missingness. That is evidence against MCAR, but does not establish MAR over MNAR. When a cleaning rule changes, preserve raw data and record which pipeline version produced each output."""),
    md("""## Search or fullmatch?

Predict what happens if the five-digit pattern looks inside a labeled string versus checking the entire field."""),
    code(r'''print("Search:", re.search(r"\d{5}", "ZIP: 84043").group())
print("Whole labeled field:", re.fullmatch(r"\d{5}", "ZIP: 84043"))
print("Whole ZIP field:", re.fullmatch(r"\d{5}", "84043").group())'''),
    md("""## ZIP codes

`\\d{5}` means five digits. An optional `-` followed by four digits admits ZIP+4. A word boundary prevents the pattern from beginning in the middle of a word."""),
    code(r'''zip_pattern = r"\b\d{5}(?:-\d{4})?\b"
examples = ["84043", "84043-4820", "ID84043X", "8404"]
for value in examples:
    hit = re.search(zip_pattern, value)
    print(f"{value:12} -> {hit.group() if hit else None}")
print("Whole-field check:", bool(re.fullmatch(zip_pattern, "ZIP: 84043")))'''),
    md("""## Four whiteboard patterns

Pause here. Groups A–D first write a **short pattern only** for their assigned whole-field problem. Explain the rejected example. After the board discussion, run the four patterns below and compare their results."""),
    code(r'''board_patterns = {
    "A ZIP": (r"\d{5}(?:-\d{4})?", ["84043", "84043-4820", "84043-482"]),
    "B phone": (r"\d{3}[-.]\d{3}[-.]\d{4}", ["801-555-0142", "801.555.0142", "8015550142"]),
    "C email": (r"[A-Za-z0-9]+@byu\.edu", ["tom@byu.edu", "tom7@byu.edu", "tom@byuXedu"]),
    "D citation": (r"(?:John|Alma) \d+:\d+", ["John 8:31", "Alma 34:32", "Mosiah 3:19"]),
}
for group, (pattern, cases) in board_patterns.items():
    print(group, [bool(re.fullmatch(pattern, value)) for value in cases])'''),
    md("""## Phone numbers

The area code can be followed by punctuation, or can be surrounded by literal parentheses. `(?:A|B)` groups alternatives without capturing an output column."""),
    code(r'''phone_pattern = r"(?:\(\d{3}\)\s*|\d{3}[-. ])\d{3}[-. ]\d{4}"
numbers = ["801-555-0142", "(801) 555-0142", "801.555.0142", "8015550142"]
for value in numbers:
    print(f"{value:16} -> {bool(re.fullmatch(phone_pattern, value))}")'''),
    md("""## Email addresses

Here we are extracting common email shapes from unstructured text. This short pattern is not intended to validate all legitimate email addresses."""),
    code(r'''email_pattern = r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"
line = "Write first.last+class@byu.edu or help@example.org."
print(re.findall(email_pattern, line))'''),
    md("""## Two real talks

These are a small sample from the course dataset. Inspect the original strings before writing a rule. In particular, the space between a number and `Nephi` is not always an ordinary ASCII space."""),
    code(r'''talks = pd.read_csv(Path("../data/talks_sample.csv"))
print(talks[["talk_name", "speaker", "conference"]].to_string(index=False))
first = re.search(r"1\s+Nephi\s+\d+:\d+", talks.loc[0, "text"])
print("Raw citation:", repr(first.group()))'''),
    md("""## Begin with a single book

What information does this pattern lose from `John 8:31–32`?"""),
    code(r'''print(re.findall(r"John\s+\d+:\d+", talks.loc[0, "text"]))'''),
    md("""## Capture the parts

The group names become column names. `\\s+` also matches a nonbreaking space. `[-–]` accepts the two range separators we want to handle today."""),
    code(r'''citation_pattern = (
    r"\b(?P<book>Doctrine\s+and\s+Covenants|D&C|[1-3]\s+Nephi|John|Alma|Mosiah)"
    r"\s+(?P<chapter>\d{1,3}):(?P<verse_start>\d{1,3})"
    r"(?:[-–](?P<verse_end>\d{1,3}))?\b"
)
print("One reference:", re.search(citation_pattern, "Alma 34:32–33").groupdict())
matches = talks["text"].str.extractall(citation_pattern)
citations = matches.reset_index().rename(
    columns={"level_0": "talk_row", "match": "citation_number"}
)
citations.insert(0, "talk_name", talks.loc[citations["talk_row"], "talk_name"].to_numpy())
print(citations[["talk_name", "book", "chapter", "verse_start", "verse_end"]].to_string(index=False))'''),
    md("""## Three pandas operations

`.str.contains()` answers whether a talk contains a chosen pattern. `.str.extract()` returns only the first captured match. `.str.extractall()` supplies one row per match, which is what we need when a talk mentions several references."""),
    code(r'''has_john = talks["text"].str.contains(r"\bJohn\s+\d+:\d+", regex=True)
first_john = talks["text"].str.extract(r"\b(John\s+\d+:\d+)")[0]
print(pd.DataFrame({"talk_name": talks["talk_name"], "has_john": has_john, "first_john": first_john}).to_string(index=False))'''),
    md("""## Normalize without deleting the source

The raw `text` and the extracted `book` fields remain in the data. The standardized book name goes into a separate field."""),
    code(r'''citations["book_clean"] = (
    citations["book"]
    .str.replace("\u00a0", " ", regex=False)
    .replace({"D&C": "Doctrine and Covenants"})
)
print(citations.groupby("talk_name").size().to_string())
print(citations.loc[citations["book"] == "D&C", ["book", "book_clean"]].to_string(index=False))'''),
    md("""## Greedy matching

Two sets of parentheses give `.*` a chance to match far more than one reference."""),
    code(r'''sentence = "(John 8:31) and (Alma 7:12)"
print("Greedy:", re.findall(r"\(.*\)", sentence))
print("Lazy:  ", re.findall(r"\(.*?\)", sentence))'''),
    md("""## Check what the pattern misses

The observed counts are counts produced by this particular pattern. A good next step is to inspect uncaptured references and expand the book list in the independent practice notebook."""),
    code(r'''expected = {"Now Is the Time": 7, "The Sacrament Can Help Us Become Holy": 6}
observed = citations.groupby("talk_name").size().to_dict()
assert observed == expected, (observed, expected)
print("Observed counts match the inspected examples:", observed)'''),
]


practice = [
    md("""# Regex practice: predict, test, revise

Run from `notebooks/`. During the whiteboard activity, solve your assigned problem on paper **before** running code. Then use the cells to test your pattern. Later, work with a partner on the citation challenge. These four problems check *whole fields*."""),
    code(r'''import re
from pathlib import Path
import pandas as pd'''),
    md("""## Group A: ZIP codes

Write a pattern for five digits with an optional four-digit extension. Explain why the rejected value fails."""),
    code(r'''zip_pattern = r""  # TODO: write your group A pattern
zip_cases = {
    "84043": True,
    "84043-4820": True,
    "84043-482": False,
}
for value, expected in zip_cases.items():
    observed = bool(re.fullmatch(zip_pattern, value))
    print(f"{value:12} expected={expected!s:5} observed={observed}")'''),
    md("""## Group B: phone numbers

Allow a hyphen or dot as each separator. Does your rule also allow mixed separators?"""),
    code(r'''phone_pattern = r""  # TODO: write your group B pattern
phone_cases = {
    "801-555-0142": True,
    "801.555.0142": True,
    "8015550142": False,
}
for value, expected in phone_cases.items():
    observed = bool(re.fullmatch(phone_pattern, value))
    print(f"{value:17} expected={expected!s:5} observed={observed}")'''),
    md("""## Group C: a narrow campus email

Allow letters and numbers in the username and require the literal domain `byu.edu`. A real email pattern would need more tests."""),
    code(r'''email_pattern = r""  # TODO: write your group C pattern
email_cases = {"tom@byu.edu": True, "tom7@byu.edu": True, "tom@byuXedu": False}
for value, expected in email_cases.items():
    print(f"{value:16} expected={expected!s:5} observed={bool(re.fullmatch(email_pattern, value))}")'''),
    md("""## Group D: a two-book citation

Allow only John and Alma with an ordinary space, a chapter, a colon, and a verse. We will stress the rule with actual text next."""),
    code(r'''simple_citation = r""  # TODO: write your group D pattern
citation_cases = {"John 8:31": True, "Alma 34:32": True, "Mosiah 3:19": False}
for value, expected in citation_cases.items():
    print(f"{value:14} expected={expected!s:5} observed={bool(re.fullmatch(simple_citation, value))}")'''),
    md("""## Think, pair, share: an assistant's citation pattern

Predict the matches. Find a missed reference and a misleading partial match. With a partner, revise the specification before changing the code. Each pair should propose one new test case that could expose another failure."""),
    code(r'''suggested = r"[A-Za-z]+ \d+:\d+"
cases = [
    "John 8:31–32",
    "1\u00a0Nephi 8:27",
    "D&C 19:16",
    "Doctrine and Covenants 121:35",
    "Alma 7:12",
]
for value in cases:
    print(repr(value), "->", re.findall(suggested, value))'''),
    md("""## Try your improved rule on actual talks

The two records include numbered books, verse ranges with an en dash, and both long and abbreviated forms of Doctrine and Covenants. Begin with the working `John` pattern and extend it. Use named groups for `book`, `chapter`, `verse_start`, and optional `verse_end`."""),
    code(r'''talks = pd.read_csv(Path("../data/talks_sample.csv"))
print(talks[["talk_name", "conference"]].to_string(index=False))
pattern = r"(?P<book>John)\s+(?P<chapter>\d+):(?P<verse_start>\d+)"  # TODO
found = talks["text"].str.extractall(pattern)
print(found.head(10).to_string())
print("Matches by talk:", found.groupby(level=0).size().to_dict())'''),
    md("""## Evaluate and normalize

After revising the pattern, inspect a few original spans. Decide which values require normalization in a *new* column, keeping the raw text. The completed walkthrough demonstrates one approach if you become stuck."""),
    code(r'''# Explore your new results here. For example:
for talk_row, row in talks.iterrows():
    spans = list(re.finditer(pattern, row["text"]))
    print(row["talk_name"], "matches:", len(spans))
    print([m.group() for m in spans[:4]])'''),
    md("""### Reflection

What does your pattern still miss? What would be a false match? Which part of the work belongs in a subsequent standardization step rather than inside the regex?"""),
]


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    save("regex_follow_along.ipynb", complete, execute=True)
    save("regex_practice.ipynb", practice)
