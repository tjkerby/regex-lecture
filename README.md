# Regular expressions for data wrangling

This STAT 386 Quarto website contains one slide deck in `slides.qmd`, with generated HTML in `docs/` for GitHub Pages. The deck reviews data pipelines, teaches how regex pieces combine, includes a four-group whiteboard exercise, then continues with three all-group problems on phone numbers, written-out emails, and verse ranges. Students and instructor extend the scripture pattern together and test it against actual conference talks.

To resume after the whiteboard work, start at **slide 25**. Slides 25–34 revisit optional pieces and give every group three short problems. Slides 35–42 build and test the wider citation rule. Allow about three minutes of group work per problem and use the tests after each reveal to guide discussion.

The earlier combined lecture is preserved in `drafts/combined-slides.qmd`. The follow-along and practice notebooks belong to that earlier draft. They are included for development, but the current site does not assign them.

## Preview and rebuild

- Open `docs/index.html` for the current site and `docs/slides.html` for the lecture slides.
- Install [Quarto](https://quarto.org/docs/get-started/), then run `quarto render` from this directory to regenerate `docs/`.
- If working with the draft notebooks, run `uv sync` and `uv run jupyter lab`. From `notebooks/`, they expect `../data/talks_sample.csv`.

Quarto is an application separate from the Python dependencies installed by `uv`. The included HTML preview was built from the Quarto sources with a local fallback because the Quarto executable was unavailable in this environment.

## GitHub Pages

Commit the repository including `docs/`. Under repository Settings → Pages, choose **Deploy from a branch**, the main branch, and **/docs**. The root `.nojekyll` marker carries through to the rendered site.

## Sample data

`data/talks_sample.csv` contains two talks from the supplied cleaned General Conference dataset. The full source CSV is not included. The new slides extend the John/Alma rule to additional book forms, then show partial matches and omissions that still need attention. The complete extraction workflow belongs in the lab.
