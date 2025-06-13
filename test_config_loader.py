import json

import tempfile
import unittest
from pathlib import Path

# Import the class under test
from src.config.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """Unit‑tests for the ConfigLoader helper class."""

    def setUp(self):
        """Create a temporary directory that test‑cases can use."""
        self.tempdir = tempfile.TemporaryDirectory()
        self.cfg_file_path = Path(self.tempdir.name) / "config.json"

    def tearDown(self):
        """Clean up any temporary resources created during the test run."""
        self.tempdir.cleanup()

    # ------------------------------------------------------------------
    # Positive path
    # ------------------------------------------------------------------
    def test_load_config_success(self):
        """Config file exists → JSON is parsed and values are retrievable."""
        payload = {"foo": "bar", "answer": 42}
        self.cfg_file_path.write_text(json.dumps(payload))

        loader = ConfigLoader(str(self.cfg_file_path))

        self.assertEqual(loader.get_config("foo"), "bar")
        self.assertEqual(loader.get_config("answer"), 42)

    # ------------------------------------------------------------------
    # Negative path
    # ------------------------------------------------------------------
    def test_load_config_file_not_found(self):
        """Non‑existent path should raise FileNotFoundError in constructor."""
        with self.assertRaises(FileNotFoundError):
            ConfigLoader(str(Path(self.tempdir.name) / "does_not_exist.json"))

    # ------------------------------------------------------------------
    # Default value behaviour
    # ------------------------------------------------------------------
    def test_get_config_returns_default_when_key_missing(self):
        """If a key is missing, get_config should return the provided default."""
        self.cfg_file_path.write_text("{}")  # empty JSON object
        loader = ConfigLoader(str(self.cfg_file_path))

        self.assertIsNone(loader.get_config("nonexistent"))  # implicit default
        self.assertEqual(loader.get_config("nonexistent", default=123), 123)


# if __name__ == "__main__":  # pragma: no cover
#     unittest.main()
