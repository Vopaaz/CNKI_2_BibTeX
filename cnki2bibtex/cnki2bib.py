import click
import pyperclip
import logging
import os

from cnki2bibtex.bibtex_entry import BibTeXContentStringFactory
from cnki2bibtex.cnki_entry import CNKIEntryFactory
from cnki2bibtex.misc.configure import set_id_format


def get_bib_file_content_string(cnki_file_content):
    cnki_entries = CNKIEntryFactory().give_all_entries(cnki_file_content)
    return BibTeXContentStringFactory.give_bib_file_content_string(cnki_entries)


def copy_to_clipboard(content):
    pyperclip.copy(content)


@click.command()
@click.argument("inputFile", type=click.Path(exists=True, dir_okay=False), required=False)
@click.option(
    "--copy/--no-copy", "-c/-nc", default=True, help="Whether or not to copy the result to clipboard. Default: True"
)
@click.option(
    "--outputDefault/--no-outputDefault",
    "-od/-nod",
    default=True,
    help="Whether or not to create a default .bib file. It has the same name as the source .net file in its directory. Or if the input source is clipboard, it will be 'out.bib' in current working directory. Default: True",
)
@click.option(
    "--outputfile", "-o", type=click.Path(exists=False, dir_okay=False), help="Create a certain output .bib file"
)
@click.option(
    "--id-format",
    "-f",
    type=click.Choice(["title", "nameyear"]),
    help="Choose the format of the ID. Pinyin of the first words in the title, or pinyin of the first author plus year",
)
@click.option(
    "--append/--no-append",
    "-a/-na",
    default=False,
    help="Whether to append at the end of output file or overwrite it. Default: False (overwrite)",
)
def launch(inputfile, copy, outputdefault, outputfile, id_format, append):
    """Converting a NoteExpress Entry .net file exported by CNKI to BibTeX .bib file.

\b
Arguments:

    INPUTFILE: Optional. The input .net file to be converted. If left empty, the contents in the clipboard will be used."""

    if id_format:
        set_id_format(id_format)
        click.echo(f"Id format set to {id_format}")

    if not copy and not outputdefault and not outputfile and not id_format:
        return

    if inputfile != None:
        if os.path.splitext(inputfile)[1] != ".net":
            logging.warning("The input file may not be a NoteExpress Entries file.")

        try:
            with open(inputfile, "r", encoding="utf-8") as f:
                cnki_file_content = f.read()
        except:
            click.echo("Failed to open the file. Please check input path.")
    else:
        click.echo("Read the NoteExpress Entry content from the clipboard.")
        cnki_file_content = pyperclip.paste()

    try:
        bib_file_string = get_bib_file_content_string(cnki_file_content)
    except Exception as e:
        click.echo("Failed to phrase the NoteExpress Entry content.")
        click.echo("Error message:\n" + str(e))

    if copy:
        try:
            copy_to_clipboard(bib_file_string)
            click.echo("BibTeX entries copied to clipboard.")
        except Exception as e:
            click.echo("Failed to copy to the clipboard.")
            click.echo("Error message:\n" + str(e))

    if outputdefault:
        try:
            target_path = (os.path.splitext(inputfile)[0] if inputfile else "out") + ".bib"
            with open(target_path, "a" if append else "w", encoding="utf-8") as f:
                f.write(bib_file_string)

            if inputfile:
                click.echo(
                    "File '{}' is created at the same directory as the source file.".format(
                        os.path.basename(target_path)
                    )
                )
            else:
                click.echo("File 'out.bib' is created at current directory.")
        except Exception as e:
            click.echo("Failed to write the default output .bib file.")
            click.echo("Error message:\n" + str(e))

    if outputfile:
        try:
            with open(outputfile, "a" if append else "w", encoding="utf-8") as f:
                f.write(bib_file_string)

            click.echo("The output file is created.")
        except Exception as e:
            click.echo("Failed to create a .bib file at the path you choose.")
            click.echo("Error message:\n" + str(e))


if __name__ == "__main__":
    # The parameter is specified by CLI argument and managed by Click
    launch()  # pylint: disable=no-value-for-parameter
