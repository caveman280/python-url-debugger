import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../url_debugger/"))  # noqa


try:
    from unittest.mock import patch, Mock, call, mock_open  # noqa
except ImportError:
    from mock import patch, Mock, call, mock_open  # noqa