import glob
from cnki2bibtex.cnki2bib import get_bib_file_content_string
from cnki2bibtex.misc.configure import set_id_format
import os
import unittest


class IntegrationTest(unittest.TestCase):
    all_net = glob.glob("./tests/assets/*.net")

    def _test_bib_net_pair(self, bib, net):
        self.max_diff = 1000000
        with open(bib, "r", encoding="utf-8") as b,\
                open(net, "r", encoding="utf-8") as n:
            self.assertEqual(b.read(),
                             get_bib_file_content_string(n.read()))

    def _test_format(self, format_):
        set_id_format(format_)
        for net in self.all_net:
            dir_, file_ = os.path.split(net)
            bib_dir = os.path.join(dir_, format_)
            bib_file = os.path.splitext(file_)[0] + ".bib"
            self._test_bib_net_pair(
                os.path.join(bib_dir, bib_file),
                net
            )

    def test_nameyear(self):
        self._test_format("nameyear")

    def test_title(self):
        self._test_format("title")
