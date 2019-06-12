#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Init tests"""

from unittest.mock import MagicMock
from flask import Flask

import flaskr.__init__
import unittest


class TestInit(unittest.TestCase):
    def test_create_app(self) -> None:
        self.assertIsInstance(flaskr.__init__.create_app(), Flask)

    def test_create_app_with_config(self) -> None:
        self.assertIsInstance(flaskr.__init__.create_app(MagicMock()), Flask)


if __name__ == '__main__':
    unittest.main()
