"""Test warn_on_duplicate_keys"""
from collections import OrderedDict
import pytest
from createconf.createconf import warn_on_duplicate_keys, DuplicateKeyError

class TestWarnOnDuplicateKeys:
    """
    Test the warn_on_duplicate_keys function in the createconf module.
    """

    def test_duplicates_found(self):
        """
        Test the warn_on_duplicate_keys function with a list of ordered pairs 
        containing duplicate keys.
        It should raise a DuplicateKeyError.
        """
        ordered_pairs = [("key1", "value1"), ("key1", "value2"), ("key2", "value3")]
        with pytest.raises(DuplicateKeyError):
            warn_on_duplicate_keys(ordered_pairs)

    def test_no_duplicates_found(self):
        """
        Test the warn_on_duplicate_keys function with a list of ordered pairs
        without duplicate keys.
        It should return an OrderedDict with the given ordered pairs.
        """
        ordered_pairs = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]
        expected = OrderedDict([("key1", "value1"), ("key2", "value2"), ("key3", "value3")])
        result = warn_on_duplicate_keys(ordered_pairs)
        assert result == expected
