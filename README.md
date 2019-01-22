# ipynb-strip

Simple CLI to strip output and prompt numbers from an ipython notebook.

## Installation

You can install with `pip`:

`pip install -e .` from within the repo.

## Usage

The utility expects an input from stdin. If you have some notebook `my_notebook.ipynb`, you can do the following:

`cat my_notebook.ipynb | ipynb-strip`

and the processed output will write to stdout.

Whether or not the utility will actually strip any output depends on two things:

1. If the notebook has an entry `"git": { "suppress_outputs": true },` in the metadata.
2. If the `--suppress` flag of the utility is set.

```
Usage: ipynb-strip [OPTIONS]

Options:
  --suppress  Ignore notebook metadata and suppress output
  --help      Show this message and exit.
```

## Thanks

The logic is based on [this](https://pascalbugnion.net/blog/ipython-notebooks-and-git.html) great blog post by [Pascal Bugnion](https://pascalbugnion.net/index.html)!
