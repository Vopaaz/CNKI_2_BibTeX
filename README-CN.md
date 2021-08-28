# CNKI_2_BibTeX

将中国知网导出的 NoteExpress 文献记录转换成 BibTeX 文献记录。

[![Downloads](https://pepy.tech/badge/cnki2bib)](https://pepy.tech/project/cnki2bib)
![PyPI](https://img.shields.io/pypi/v/cnki2bib)
[![Actions Status](https://github.com/Vopaaz/CNKI_2_BibTeX/workflows/CI/badge.svg)](https://github.com/Vopaaz/CNKI_2_BibTeX/actions)
[![codecov](https://codecov.io/gh/Vopaaz/CNKI_2_BibTeX/branch/master/graph/badge.svg)](https://codecov.io/gh/Vopaaz/CNKI_2_BibTeX)

- [CNKI_2_BibTeX](#cnki2bibtex)
  - [开始](#%e5%bc%80%e5%a7%8b)
    - [环境要求](#%e7%8e%af%e5%a2%83%e8%a6%81%e6%b1%82)
    - [安装](#%e5%ae%89%e8%a3%85)
    - [使用](#%e4%bd%bf%e7%94%a8)
    - [最后...](#%e6%9c%80%e5%90%8e)
  - [Windows 上的骚操作](#windows-%e4%b8%8a%e7%9a%84%e9%aa%9a%e6%93%8d%e4%bd%9c)
  - [在知网上导出 .net 文件](#%e5%9c%a8%e7%9f%a5%e7%bd%91%e4%b8%8a%e5%af%bc%e5%87%ba-net-%e6%96%87%e4%bb%b6)
  - [在知网上将 .net 文件内容复制到剪贴板](#%e5%9c%a8%e7%9f%a5%e7%bd%91%e4%b8%8a%e5%b0%86-net-%e6%96%87%e4%bb%b6%e5%86%85%e5%ae%b9%e5%a4%8d%e5%88%b6%e5%88%b0%e5%89%aa%e8%b4%b4%e6%9d%bf)

## 开始

### 环境要求

- Python3

### 安装

```
pip install cnki2bib
```

### 使用

请确认 `cnki2bib` 被安装到了你的 `PATH` 中。

```
cnki2bib [OPTIONS] [INPUTFILE]
```

参数：

- `INPUTFILE`:
  - 输入要转换的 .net 文件。如果留空，则会尝试读取剪贴板中的内容。

选项：

- `-c, --copy / -nc, --no-copy`
  - 是否将转换结果复制到剪贴板中
  - 默认：`True`

- `-od, --outputDefault / -nod, --no-outputDefault`
  - 是否创建一个默认的输出 .bib 文件
  - 这个文件与输入的 .net 文件同名，并且在它同一个目录下
  - 如果输入使用的是剪贴板，则会创建在当前的工作目录
  - 默认：`True`

- `-o, --outputfile FILENAME`
  - 指定一个输出的 .bib 文件

- `-f, --id-format [title|nameyear]`
  - 选择 BibTeX 条目 ID 的格式
    - 文章标题的前几个单词（或中文字符的拼音）
    - 第一作者的姓名（若是中文则取其拼音）+ 发表年份
  - 默认：`title`
  - 当指定过一次这个选项之后，你的选择会被保存在 `~/.cnki2bib.cfg` 中，之后使用无需再次选择这一选项

- `--help`
  - 显示英文帮助

### 最后...

开始使用 BibTeX 来管理你的文献吧！

## 双击以使用

你可以在 Python/Scripts 文件夹中找到 `cnki2bib.exe` 并且将其设置为打开 .net 文件的默认程序。

之后，当你双击一个 .net 文件，相应的 BibTeX 结果会被复制到你的剪贴板，同时在同一目录下会创建同名 .bib 文件。

如果发生问题。请用命令行来查看错误信息并尽情 issue~

## 在知网上导出 .net 文件

![FxL8Cq.png](https://s2.ax1x.com/2019/01/14/FxL8Cq.png)

## 在知网上将 .net 文件内容复制到剪贴板

![FxL8Cq.png](https://github.com/SNBQT/share-images/blob/master/cnki2bib.png?raw=true)

**你必须允许 Flash 才能看到“复制到剪贴板”按钮。**

复制之后，直接在 console 中使用命令 `cnki2bib`. 相应的 BibTeX 输出会被复制到你的剪贴板，同时在工作目录下会创建一个 `out.bib` 文件。 :smile:
