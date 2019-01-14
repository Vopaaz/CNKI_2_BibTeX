import click
import pyperclip
import logging
import os

from .BibTexEntries import BibTeXContentStringFactory
from .cnkiNetEntries import CNKINetEntryFactory


def getBibFileContentString(cnkiNetFileContent):
    cnkiNetEntries = CNKINetEntryFactory.giveAllEntries(cnkiNetFileContent)
    return BibTeXContentStringFactory.giveBibFileContentString(cnkiNetEntries)


def copyToClipBoard(content):
    pyperclip.copy(content)


@click.command()
@click.argument("inputFile", type=click.Path(exists=True, dir_okay=False))
@click.option("--copy/--no-copy", "-c/-nc", default=True,help="Whether or not to copy the result to clipboard.")
@click.option("--outputDefault/--no-outputDefault", "-od/-nod", default=True,help="Whether or not to create a file at the default position.")
@click.option("--outputfile", "-o", type=click.File('w', encoding="utf8"),help="The path to a certain output file.")
def launch(inputfile, copy, outputdefault, outputfile):
    '''Converting a NoteExpress Entry .net file exported by CNKI to BibTeX .bib file.'''

    if not copy and not outputdefault and not outputfile:
        click.echo("Why are you calling me ???")
        return

    if os.path.splitext(inputfile)[1] != ".net":
        logging.warning(
            "The input file may not be a NoteExpress Entries file.")

    try:
        with open(inputfile, 'r', encoding="utf8") as f:
            cnkiNetFileContent = f.read()
    except:
        click.echo("Failed to open the file. Please check input path.")

    try:
        bibFileString = getBibFileContentString(cnkiNetFileContent)
    except Exception as e:
        click.echo("Failed to phrase the NoteExpress Entry content.")
        click.echo("Error message:\n" + str(e))

    if copy:
        try:
            copyToClipBoard(bibFileString)
            click.echo("BibTeX entries copied to clipboard.")
        except Exception as e:
            click.echo("Failed to copy to the clipboard.")
            click.echo("Error message:\n" + str(e))

    if outputdefault:
        try:
            targetPath = os.path.splitext(inputfile)[0] + ".bib"
            with open(targetPath, "w", encoding="utf8") as f:
                f.write(bibFileString)
            click.echo(
                "File '{}' is created at the same directory as the source file.".format(os.path.basename(targetPath)))
        except Exception as e:
            click.echo(
                "Failed to write a .bib file at the same directory as the source file.")
            click.echo("Error message:\n" + str(e))

    if outputfile:
        try:
            outputfile.write(bibFileString)
            click.echo("The output file is created.")
        except Exception as e:
            click.echo(
                "Failed to create a .bib file at the path you choose.")
            click.echo("Error message:\n" + str(e))


if __name__ == "__main__":
    launch()
