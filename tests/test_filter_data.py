"""TestFilterData"""
from createconf.createconf import filter_data

class TestFilterData:
    """TestFilterData"""
    def test_filter_data_ignore_keys(self):
        """
        Test the filter_data function with a list of keys to ignore.
        It should return a dictionary with the specified keys removed.
        """
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        ignore = ["key1", "key2"]
        verbose = False
        expected = {"key3": "value3"}

        result = filter_data(data, ignore, verbose)
        assert result == expected

    def test_filter_data_no_ignore_keys(self):
        """
        Test the filter_data function without any keys to ignore.
        It should return the same dictionary as the input data.
        """
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        ignore = []
        verbose = False
        expected = data.copy()

        result = filter_data(data, ignore, verbose)
        assert result == expected

    def test_filter_data_ignore_nonexistent_keys(self):
        """
        Test the filter_data function with keys to ignore that don't exist in the data.
        It should return the same dictionary as the input data.
        """
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        ignore = ["key4", "key5"]
        verbose = False
        expected = data.copy()

        result = filter_data(data, ignore, verbose)
        assert result == expected
