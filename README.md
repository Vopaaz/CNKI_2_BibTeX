# CNKI_2_BibTeX

Converting the NoteExpress (.net) file exported by CNKI (中国知网) to BibTeX (.bib) file.

将中国知网导出的 NoteExpress 文献记录转换成 BibTeX 文献记录。

[![Downloads](https://pepy.tech/badge/cnki2bib)](https://pepy.tech/project/cnki2bib)
[![Downloads](https://pepy.tech/badge/cnki2bib/month)](https://pepy.tech/project/cnki2bib/month)
![GitHub](https://img.shields.io/github/license/vopaaz/cnki_2_bibtex)
![PyPI](https://img.shields.io/pypi/v/cnki2bib)

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [CNKI_2_BibTeX](#cnki2bibtex)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
  - [Using](#using)
  - [Finally...](#finally)
- [Tricky Usage](#tricky-usage)
- [Export NoteExpress .net File on CNKI](#export-noteexpress-net-file-on-cnki)

<!-- /code_chunk_output -->


# Getting Started

## Prerequisites

- Python3

## Installing

```
pip install cnki2bib
```

## Using

Make sure it's in your `PATH`.

```
cnki2bib [OPTIONS] INPUTFILE
```

Options:

-  `-c, --copy / -nc, --no-copy`
    - Whether or not to copy the result to clipboard.
    - Default: `True`

-  `-od, --outputDefault / -nod, --no-outputDefault`
    - Whether or not to create a .bib file with the same name as the .net file in its directory.
    - Default: `True`

-  `-o, --outputfile FILENAME`
    - Create a  certain output .bib file.

-  `-f, --id-format [title|nameyear]`
    - Choose the format of the ID.
      - The first several words (or their pinyin) in the title
      - The first author (or the pinyin) plus year.
    - Default: `title`
    - Once you have assigned a format, your choice will be saved in `~/.cnki2bib.cfg`. It is unnecessary to type this choice since then.

-  `--help`
    - Show this message and exit.


## Finally...

Start using BibTeX to manage the literature references.

# Tricky Usage

You can find `cnki2bib.exe` in your Python/Scripts and set it as the default program to open the .net file.

Then when you double-click a .net file, the corresponding BibTeX Entries will be copied to your clipborad, and a .bib file would be created on the same directory.

Use the console to check for Exception if it does not work as expected.


# Export NoteExpress .net File on CNKI

![FxL8Cq.png](https://s2.ax1x.com/2019/01/14/FxL8Cq.png)


