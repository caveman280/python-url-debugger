import io
import os
import sys
import pytest
import unittest
from tests import patch, Mock, mock_open

import argparse
import requests
import requests_mock
from url_debugger.cli import CLI, FetchUrl
from url_debugger.exceptions import *


class TestCLI(unittest.TestCase):

    @patch.object(sys, "argv", ["/", "fetch"])
    @patch('argparse.ArgumentParser.print_help', return_value="Help", autospec=True)
    def test_no_commands_prints_help(self, mock_help):
        with self.assertRaises(SystemExit) as fail:
            cli = CLI()
        self.assertEqual(fail.exception.code, 1)
        mock_help.assert_called_once()

    @patch.object(sys, "argv", ["/", "fetch", "--fake"])
    @patch('argparse.ArgumentParser.print_help', return_value="Help", autospec=True)
    def test_invalid_command_prints_help(self, mock_help):
        with self.assertRaises(SystemExit) as fail:
            cli = CLI()
        self.assertEqual(fail.exception.code, 1)
        mock_help.assert_called_once()

    @patch.object(sys, "argv", ["/", "fetch", "-u", "bad://address"])
    @patch('requests.get', autospec=True)
    def test_bad_address_returns_error(self, mock_get):

        cli = CLI()
        self.assertEqual(len(cli.urls), 1)

        self.assertTrue(cli.urls[0]._has_critical_error)

        first_url = cli.urls[0].as_dict()
        self.assertTrue("errors", first_url.keys())
        self.assertEqual(str(InvalidUrl()), first_url["errors"][0])

        assert not mock_get.called, "A get request should not be called with an invalid URL"

    @patch.object(sys, "argv", ["/", "fetch", "-u", "https://not.exists.google.com"])
    @requests_mock.Mocker()
    def test_fake_address_returns_error(self, mock_get):
        cli = CLI()

        self.assertEqual(len(cli.urls), 1)

        first_url = cli.urls[0].as_dict()
        self.assertTrue("errors", first_url.keys())
        self.assertIn("No mock address:", first_url["errors"][0])

    @patch.object(sys, "argv", ["/", "fetch", "-u", "https://www.google.com"])
    @requests_mock.Mocker()
    def test_valid_domain(self, mock_get):
        mock_get.register_uri("GET", "https://www.google.com")

        #mock_peer_name.return_value = "1.1.1.1", "443"

        cli = CLI()

        self.assertEqual(len(cli.urls), 1)

        first_url = cli.urls[0].as_dict()
        # make sure there's no errors
        self.assertNotIn("errors", first_url.keys())

        self.assertEqual(200, first_url["response_code"])

    @patch.object(sys, "argv", ["/", "fetch", "-f", "/some/file"])
    @requests_mock.Mocker()
    def test_can_read_from_files(self, mock_get):
        mock_file = mock_open(read_data='https://www.google.com\nbad://address')
        
        mock_get.register_uri("GET", "https://www.google.com")
        #mock_peer_name.return_value = "1.1.1.1", "443"

        with patch('builtins.open', return_value=mock_file('some-filename')):
            cli = CLI()

        self.assertEqual(len(cli.urls), 2)

        first_url = cli.urls[0].as_dict()
        # make sure there's no errors
        self.assertNotIn("errors", first_url.keys())
        self.assertEqual(200, first_url["response_code"])

        second_url = cli.urls[1].as_dict()
        # make sure there's no errors
        self.assertIn("errors", second_url.keys())
        self.assertEqual(str(InvalidUrl()), second_url["errors"][0])