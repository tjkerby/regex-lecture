# Regular expressions for data wrangling

This STAT 386 Quarto website contains the **Day 1 slide deck** in `slides.qmd`, with generated HTML in `docs/` for GitHub Pages. Day 1 reviews data pipelines, teaches how regex pieces combine, and ends with a four-group whiteboard exercise.

The earlier combined lecture is preserved in `drafts/combined-slides.qmd` for the Day 2 revision. The follow-along and practice notebooks still belong to that earlier combined draft. They are included for development, but the Day 1 website does not assign them.

## Preview and rebuild

- Open `docs/index.html` for the current site and `docs/slides.html` for the Day 1 slides.
- Install [Quarto](https://quarto.org/docs/get-started/), then run `quarto render` from this directory to regenerate `docs/`.
- If working with the draft notebooks, run `uv sync` and `uv run jupyter lab`. From `notebooks/`, they expect `../data/talks_sample.csv`.

Quarto is an application separate from the Python dependencies installed by `uv`. The included HTML preview was built from the Quarto sources with a local fallback because the Quarto executable was unavailable in this environment.

## GitHub Pages

Commit the repository including `docs/`. Under repository Settings → Pages, choose **Deploy from a branch**, the main branch, and **/docs**. The root `.nojekyll` marker carries through to the rendered site.

## Sample data

`data/talks_sample.csv` contains two talks from the supplied cleaned General Conference dataset. The full source CSV is not included. The Day 1 deck only uses a few citation forms as a bridge to Day 2; it does not teach the full extraction workflow.
