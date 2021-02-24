import os
import unittest
from tests import patch, Mock

import argparse
from url_debugger.cli import CLI

class TestCLI(unittest.TestCase):
    
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(command="blah"), autospec=True)
    @patch('argparse.ArgumentParser.print_help', return_value="Help", autospec=True)
    def test_invalid_command_prints_help(self, mock_args, mock_help):
        with self.assertRaises(SystemExit) as fail:
            cli = CLI()
        self.assertEqual(fail.exception.code, 1)
        mock_help.assert_called_once()