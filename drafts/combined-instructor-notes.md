# Instructor notes: regex lecture

## Main idea

Students should be able to **describe a set of strings**, predict what a regex will actually match, and revise their specification when real text surprises them. The named-group pattern is a worked application of those ideas, not a syntax students need to recreate from memory today.

## Suggested 50-minute route

| Minutes | Slides and student work |
|:--|:--|
| 0–6 | **Review from last week:** Give 1 minute silent thought and 1 minute paired explanation on the age/missing-income question. Debrief: association with observed age weighs against MCAR but does not identify MAR over MNAR. Ask what to preserve when the cleaning rule changes; show the answer before moving on. |
| 6–15 | **Construct the model:** Explain regex as a set of strings. Have students predict search versus fullmatch; show the result, then read literals, digit classes, repetitions, escaped punctuation, and groups. Ask about `84043-482` before revealing the output. |
| 15–27 | **Whiteboard groups:** Assign A–D. For more than four groups, repeat assignments and compare different solutions; with fewer groups, combine C and D or assign one group two. Give 5 minutes to write and test mentally, then ~7 minutes for a representative from each group to write the short regex and explain the rejected example. Use the solution slides only after their reasoning. |
| 27–33 | **Transition to actual text:** Compare the tiny group D rule to four real citation forms. Pairs identify the broken assumptions. Show the two-talk sample and `repr()` of the nonbreaking space. Run the simple John matcher and discuss the missing range. |
| 33–41 | **Think, pair, share:** Have students predict actual substrings from the tempting assistant pattern, then explain one partial and one missed match. Debrief before showing the complete sample-specific pattern. Ask them to predict the four captured fields of `Alma 34:32–33`. |
| 41–48 | **Move from regex to data:** Compare contains, extract, and extractall. Show five rows and why `verse_end` can be missing. Preserve raw text while normalizing an extracted book name. |
| 48–50 | **Exit question:** Explain the optional range and give a plausible missed citation with a test. |

There are more slides than need full narration. The greedy/lazy pair is an extension if time permits; the practice notebook also covers it. Prioritize the review, board explanations, and citation debrief.

## Whiteboard facilitation

Keep the previous pattern-pieces slide visible while groups work. Ask students to put the **pattern only** on the board, without `r""`; they can add the Python raw string notation when testing it in the notebook.

| Group | Example answer for `re.fullmatch` | Probe after the explanation |
|:--|:--|:--|
| A | `\d{5}(?:-\d{4})?` | Does it validate that a ZIP actually exists? |
| B | `\d{3}[-.]\d{3}[-.]\d{4}` | It permits mixed separators. Is that okay for your specification? |
| C | `[A-Za-z0-9]+@byu\.edu` | What happens to `first.last@byu.edu`? Why is the dot escaped? |
| D | `(?:John|Alma) \d+:\d+` | What happens with `1 Nephi 8:27` and `John 8:31–32`? |

Accept equivalent short patterns if they fit the examples and the student's stated scope. A string that passes the three listed cases may still be too broad. Ask every group for a fresh counterexample.

## Follow-along and practice

The slides contain code **and its outputs**; do not require live notebook switching to reveal answers. The completed follow-along runs the same patterns and table extraction. The practice notebook lets students first attempt one assigned board problem and later work through real citation failures with a partner.

The two records came from the supplied `talks_final.csv`. The citation pattern recognizes only `Doctrine and Covenants`, `D&C`, numbered Nephi, John, Alma, and Mosiah. It finds **7** target matches in *Now Is the Time* and **6** in *The Sacrament Can Help Us Become Holy*. These are counts under this pattern, not all possible citations. The source includes nonbreaking spaces and en dashes. Keep the talk text unchanged; normalize into a separate field.

## Bridge to scraping

Once students obtain a talk page, separate finding the relevant HTML element, extracting the talk text, and running a tested regex on that text. A more comprehensive scripture parser can be an extension with test cases and a recorded processing version.
