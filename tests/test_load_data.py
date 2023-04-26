"""TestLoadData"""
import json
from unittest.mock import patch, mock_open
import pytest
from createconf.createconf import load_data, DuplicateKeyError

class TestLoadData:
    """TestLoadData"""
    def test_load_data_from_file(self):
        """
        Test the load_data function when loading data from a file.
        It should return a dictionary containing the data from the file.
        """
        test_data = '{"key1": "value1", "key2": "value2"}'
        test_dict = json.loads(test_data)

        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=test_data)):
                result = load_data("test_file.json", strict=False)
                assert result == test_dict

    def test_load_data_from_string(self):
        """
        Test the load_data function when loading data from a string.
        It should return a dictionary containing the data from the string.
        """
        test_data = '{"key1": "value1", "key2": "value2"}'
        test_dict = json.loads(test_data)

        with patch("os.path.exists", return_value=False):
            result = load_data(test_data, strict=False)
            assert result == test_dict

    def test_load_data_with_duplicate_keys(self):
        """
        Test the load_data function when loading data with duplicate keys and strict mode disabled.
        It should return a dictionary with the last value of the duplicate keys.
        """
        test_data = '{"key1": "value1", "key1": "value2"}'
        test_dict = {"key1": "value2"}

        with patch("os.path.exists", return_value=False):
            result = load_data(test_data, strict=False)
            assert result == test_dict

    def test_load_data_with_duplicate_keys_strict(self):
        """
        Test the load_data function when loading data with duplicate keys and strict mode enabled.
        It should raise a DuplicateKeyError.
        """
        test_data = '{"key1": "value1", "key1": "value2"}'

        with patch("os.path.exists", return_value=False):
            with pytest.raises(DuplicateKeyError):
                load_data(test_data, strict=True)
