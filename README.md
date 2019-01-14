# CNKI_2_BibTeX
Converting the NoteExpress (.net) file exported by CNKI (中国知网) to BibTeX (.bib) file.  将中国知网导出的 NoteExpress 文献记录转换成 BibTeX 文献记录。

# Getting Started

## Prerequisites

- Python3

## Installing

```
pip install cnki2bib
```

## Using

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

-  `--help`
    - Show this message and exit.

