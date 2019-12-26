from setuptools import setup, find_packages

with open(r'README.md',"r",encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='cnki2bib',
    version='0.2.6',
    author='Vopaaz',
    author_email="liyifan945@163.com",
    url="https://github.com/Vopaaz/CNKI_2_BibTeX",
    description='Converting the NoteExpress file (.net) exported by CNKI to BibTeX file (.bib)',
    long_description = long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click','jieba','pyperclip','pypinyin'
    ],
    entry_points='''
        [console_scripts]
        cnki2bib=cnki2bibtex.cnki2bib:launch
    ''',
)