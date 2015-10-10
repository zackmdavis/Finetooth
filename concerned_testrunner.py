import unittest

from django.test.runner import DiscoverRunner


class ConcernedTestLoader(unittest.TestLoader):
    testMethodPrefix = "concerning"


class ConcernedTestRunner(DiscoverRunner):
    test_loader = ConcernedTestLoader()
