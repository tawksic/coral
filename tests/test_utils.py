from unittest.mock import patch, mock_open
from app.utils import get_version


class TestUtils:
    @patch('builtins.open', mock_open(read_data='[project]\nversion = "1.2.3"'))
    @patch('tomllib.load')
    def test_get_version_success(self, mock_tomllib_load):
        mock_tomllib_load.return_value = {"project": {"version": "1.2.3"}}

        version = get_version()
        assert version == "1.2.3"

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_version_file_not_found(self, mock_open):
        version = get_version()
        assert version == "unknown"

    @patch('builtins.open', mock_open(read_data='invalid toml'))
    @patch('tomllib.load', side_effect=KeyError)
    def test_get_version_parse_error(self, mock_tomllib_load):
        version = get_version()
        assert version == "unknown"
