import unittest

from src.tms_io.sinks.mock_output_sink import MockOutputSink


class TestMockOutputSink(unittest.TestCase):
    def setUp(self) -> None:
        """Setup test MockOutputSink
        """
        self.sink = MockOutputSink({})

    def test_initialization(self) -> None:
        """Test that MockOutputSink initializes with empty log and not initialized"""
        self.assertEqual(self.sink.log, [])
        self.assertFalse(self.sink.initialized)

    def test_write_after_initialize(self) -> None:
        """Test that write method adds data to log after initialization"""
        self.sink.initialize()
        self.sink.write("Test data 1")
        self.assertEqual(self.sink.log, ["Test data 1"])

        self.sink.write("Test data 2")
        self.assertEqual(self.sink.log, ["Test data 1", "Test data 2"])

    def test_write_without_initialize(self) -> None:
        """Test that write method raises error if sink not initialized"""
        with self.assertRaises(RuntimeError):
            self.sink.write("Test data")

    def test_initialize_and_shutdown(self) -> None:
        """Test initialize and shutdown methods affect initialized state"""
        self.assertFalse(self.sink.initialized)

        self.sink.initialize()
        self.assertTrue(self.sink.initialized)

        self.sink.shutdown()
        self.assertFalse(self.sink.initialized)
