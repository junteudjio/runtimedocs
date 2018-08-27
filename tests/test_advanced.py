# -*- coding: utf-8 -*-

from .context import runtimedocs

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(runtimedocs.hmm())


if __name__ == '__main__':
    unittest.main()
