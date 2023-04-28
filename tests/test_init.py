# test_init.py
from importlib_metadata import version as get_version
from createconf import DIST_NAME, __version__

def test_version_retrieval():
    try:
        expected_version = get_version(DIST_NAME)
    except Exception:
        expected_version = "unknown"

    assert __version__ == expected_version, f"Expected version: {expected_version}, but got: {__version__}"
