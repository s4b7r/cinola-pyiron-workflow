# README

## Setup

1. Clone this repository.
2. Make sure all git submodules are correctly loaded (recursively).
3. See READMEs of submodules.
4. Install Python requirements: The last tested environment is in `requirements-freeze.txt`.
5. See `magnetic_monte_carlo-multishell.ipynb`.

## Citation & Attribution

If you use this software for an academic publication, please give proper attribution: This can be done by citing the code directly by the original author's full name (Simon Bekemeier) and its original GitHub URL: https://github.com/s4b7r/cinola-pyiron-workflow

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
