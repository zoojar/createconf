"""TestDeepMerge"""
from createconf.createconf import deep_merge

class TestDeepMerge:
    """TestDeepMerge"""
    def test_non_overlapping_keys(self):
        """
        Test the deep_merge function with non-overlapping keys.
        It should return a merged dictionary containing all keys and values.
        """
        dict1 = {"key1": "value1"}
        dict2 = {"key2": "value2"}
        expected = {"key1": "value1", "key2": "value2"}
        assert deep_merge(dict1, dict2) == expected

    def test_overlapping_keys(self):
        """
        Test the deep_merge function with overlapping keys.
        It should return a merged dictionary with the overlapping keys' values combined.
        """
        dict1 = {"key1": {"key2": "value2"}, "key3": "value3"}
        dict2 = {"key1": {"key4": "value4"}}
        expected = {"key1": {"key2": "value2", "key4": "value4"}, "key3": "value3"}
        assert deep_merge(dict1, dict2) == expected

    def test_nested_dictionaries(self):
        """
        Test the deep_merge function with nested dictionaries.
        It should return a merged dictionary with the nested keys' values combined.
        """
        dict1 = {"key1": {"key2": {"key3": "value3"}}}
        dict2 = {"key1": {"key2": {"key4": "value4"}}}
        expected = {"key1": {"key2": {"key3": "value3", "key4": "value4"}}}
        assert deep_merge(dict1, dict2) == expected
