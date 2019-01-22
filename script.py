import click
import logging
import json

from typing import Dict

logging.getLogger().setLevel(logging.DEBUG)

# TODO: Should we have a --file option instead of piping?

def check_metadata(parsed_json: Dict[str, str]) -> bool:
    """
    Check the JSON metadata to determine if a suppress
    output flag has been set.
    """
    metadata = parsed_json["metadata"]
    suppress_output = False
    if "git" in metadata:
        if "suppress_outputs" in metadata["git"]:
            if metadata["git"]["suppress_outputs"]:
                suppress_output = True

    return suppress_output

def determine_version(parsed_json: Dict[str, str]) -> int:
    """
    Check the iPython version used to write the notebook.
    """
    version = int(parsed_json["nbformat"]) - 1
    logging.debug("Notebook created by version {0}".format(version))
    return version

def strip_output(cell):
    """
    Remove the prompt number and output fields from a notebook cell.
    """
    if "outputs" in cell:
        cell["outputs"] = []
    if "prompt_number" in cell:
        del cell["prompt_number"]

@click.command()
@click.option('--suppress', is_flag=True, help='Ignore notebook metadata and suppress output')
def cli(suppress):
    # Read the notebook from stdin (or eventually, file)
    with click.open_file('-') as f:
        json_text = f.read()
        json_parsed = json.loads(json_text)

        # Check metadata for suppress_output flag
        suppress_output = check_metadata(json_parsed)

        if not suppress_output and not suppress:
            # Just write notebook back to stdout
            logging.debug("Not suppressing output.")
            with click.open_file('-', 'w') as fout:
                fout.write(json_text)
            exit()

        logging.debug("Suppressing output.")

        # Strip output at level depending on version
        if determine_version(json_parsed) == 2:
            for sheet in json_parsed["worksheets"]:
                for cell in sheet["cells"]:
                    strip_output(cell)
        else:
            for cell in json_parsed["cells"]:
                strip_output(cell)

        with click.open_file('-', 'w') as fout:
            json.dump(json_parsed, fout, sort_keys=True, indent=1, separators=(",", ": "))
