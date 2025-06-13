import unittest
from typing import Any

from src.tms_io.sources.mock_input_source import MockInputSource


class TestMockInputSource(unittest.TestCase):
    def setUp(self) -> None:
        """Setup test MockInputSource
        """
        self.source = MockInputSource(
            params={
                "output": [
                    "Fake data #1",
                    "Fake data #2",
                ]
            }
        )

    def test_initialization(self) -> None:
        """Test that MockInputSource initializes with empty log and no callback"""
        self.assertEqual(self.source.log, [])
        self.assertIsNone(self.source.callback)

    def test_read_without_callback(self) -> None:
        """Test that read method adds data to log without callback"""
        self.source.read()
        self.assertEqual(self.source.log, ["Fake data #1"])

        self.source.read()
        self.assertEqual(self.source.log, ["Fake data #1", "Fake data #2"])

    def test_read_with_callback(self) -> None:
        """Test that read method triggers callback with correct data"""
        callback_data = []

        def test_callback(data: Any) -> None:
            callback_data.append(data)

        self.source.register_callback(test_callback)
        self.source.read()
        self.source.read()

        self.assertEqual(callback_data, ["Fake data #1", "Fake data #2"])
        self.assertEqual(self.source.log, ["Fake data #1", "Fake data #2"])

    def test_initialize_and_shutdown(self) -> None:
        """Test initialize and shutdown methods (even though they're empty)"""
        self.source.initialize()  # Should not raise any exception
        self.source.shutdown()  # Should not raise any exception
