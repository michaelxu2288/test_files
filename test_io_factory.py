import unittest

from src.tms_io.io_factory import InputSourceFactory, OutputSinkFactory
from src.tms_io.sinks.mock_output_sink import MockOutputSink
from src.tms_io.sources.mock_input_source import MockInputSource


class TestInputSourceFactory(unittest.TestCase):

    def test_create_mock_input_source(self) -> None:
        """Test creation of MockInputSource through factory
        """
        source = InputSourceFactory.create("MockInputSource", {})

        self.assertIsInstance(source, MockInputSource)
        self.assertEqual(source.log, [])
        self.assertIsNone(source.callback)

    def test_invalid_source_type(self) -> None:
        """Test that factory raises error for invalid source type
        """
        with self.assertRaises(ValueError):
            InputSourceFactory.create("invalid_type", {})


class TestOutputSinkFactory(unittest.TestCase):
    def test_invalid_sink_type(self) -> None:
        """Test that factory raises error for invalid sink type
        """
        with self.assertRaises(ValueError):
            OutputSinkFactory.create("invalid_type", {})

    def test_create_mock_output_sink(self) -> None:
        """Test creation of MockOutputSink through factory
        """
        sink = OutputSinkFactory.create("MockOutputSink", {})

        self.assertIsInstance(sink, MockOutputSink)
        self.assertEqual(sink.log, [])
        self.assertFalse(sink.initialized)
