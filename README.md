# CINOLA pyiron Workflow

## Setup

1. Clone this repository.
2. Make sure all git submodules are correctly loaded (recursively).
3. See READMEs of submodules.
4. Install Python requirements: The last tested environment is in `requirements-freeze.txt`.
5. See `magnetic_monte_carlo-multishell.ipynb`.

## Citation & Attribution

If you use this software for an academic publication, please give proper attribution: This can be done by citing the code directly by the original author's full name (Simon Bekemeier) and its original GitHub URL: https://github.com/s4b7r/cinola-pyiron-workflow

## Notes on Workflow Development and Publication

We would also like to develop this workflow and document its development as a case study for the development and publication of scientific (software) workflows. Our aim is to document the steps we took, beginning with the publication of a "minimum viable workflow" (see [Minimum Viable Product](https://en.wikipedia.org/wiki/Minimum_viable_product)), then continuously improving and documenting how it iteratively develops into something better and better, that gets more useable as a workflow step-by-step. With that, we hope to reduce the barrier to publish (scientific) workflows for people and projects, who are just starting with workflow development. Because a very simple workflow with rough edges is a lot better than a polished workflow, that is never shared with the community because it is "not yet ready".

For this workflow we considered the following checklist to have a minimum viable workflow:

- Setup instructions (Just try to help your user. Can be simple, don't need to be sophisticated. There are still some rough edges and manual setup steps in this workflow as well.)
- Probably a README, like this one.
- For setup instructions of Python environments you can use a [`requirements.txt`](https://pip.pypa.io/en/stable/user_guide/#requirements-files) file.
- "UX-friendly" Python notebook (UX = user experience): convey clearly which cells are for input or output and which ones are "just to execute"
- Add a [`meta.json`](https://workflows.material-digital.de/info//) for the [PMD Workflow Store](https://workflows.material-digital.de/)
- If you care about proper software sharing, [choose a license](https://choosealicense.com/) and add a `LICENSE` file.
- If you care about citing, add a hint on that in your readme and/or add a [`CREDENTIALS.cff`](https://citation-file-format.github.io/) file.

## Ipython Notebooks in Git

Remeber to put the following filter into the repo's config:

```
[filter "nbstrip_full"]
        clean = "\"jq\" --indent 1 \
                '(.cells[] | select(has(\"outputs\")) | .outputs) = []  \
                | (.cells[] | select(has(\"execution_count\")) | .execution_count) = null  \
                | .metadata = {\"language_info\": {\"name\": \"python\", \"pygments_lexer\": \"ipython3\"}} \
                | .cells[].metadata = {} \
                '"
        smudge = cat
        required = true
```

And also

```
*.ipynb filter=nbstrip_full
```

into `.gitattributes`.

Install [jq](https://stedolan.github.io/jq/) somewhere into `PATH`, if necessary.
