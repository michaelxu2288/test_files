"""
Unit tests for can_manager.py utilities using unittest.TestCase style
"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import can_lib.can_manager as can_utils  # noqa: F401 


class TestCanUtils(unittest.TestCase):
    # ------------------------------------------------------------------
    # load_dbc_file
    # ------------------------------------------------------------------
    def test_load_dbc_file_success(self):
        fake_db = MagicMock()
        path = Path("example.dbc")

        with patch(f"{can_utils.__name__}.cantools.database.load_file", return_value=fake_db) as mock_load:
            result = can_utils.load_dbc_file(path)
            self.assertIs(result, fake_db)
            mock_load.assert_called_once_with(path)

    def test_load_dbc_file_failure(self):
        path = Path("missing.dbc")

        with patch(
            f"{can_utils.__name__}.cantools.database.load_file",
            side_effect=ValueError("boom"),
        ):
            with self.assertRaises(ValueError):
                can_utils.load_dbc_file(path)

    
    def test_initialize_can_bus_success(self):
        fake_bus = MagicMock()

        with patch(f"{can_utils.__name__}.can.interface.Bus", return_value=fake_bus) as mock_bus:
            bus = can_utils.initialize_can_bus("socketcan", 1, 250000)
            self.assertIs(bus, fake_bus)
            mock_bus.assert_called_once_with(interface="socketcan", channel=1, bitrate=250000)

    def test_initialize_can_bus_failure(self):
        with patch(
            f"{can_utils.__name__}.can.interface.Bus",
            side_effect=OSError("init fail"),
        ):
            with self.assertRaises(OSError):
                can_utils.initialize_can_bus("socketcan", 1, 250000)

   
    def test_receive_can_messages_decoding(self):
        # prepare fake messages
        good_msg = MagicMock(arbitration_id=0x100, data=b"\x01\x02")
        bad_msg = MagicMock(arbitration_id=0x200, data=b"\x03\x04")

        bus = MagicMock()
        bus.recv.side_effect = [good_msg, bad_msg, None]

        db = MagicMock()
        db.decode_message.side_effect = [{"speed": 88}, ValueError("decode fail")]

        result = can_utils.receive_can_messages(bus, db)

        self.assertEqual(result, {0x100: {"speed": 88}})
        self.assertEqual(db.decode_message.call_count, 2)
        self.assertGreaterEqual(bus.recv.call_count, 3)

    def test_receive_can_messages_empty(self):
        bus = MagicMock()
        bus.recv.return_value = None
        db = MagicMock()

        self.assertEqual(can_utils.receive_can_messages(bus, db), {})

   
    def test_send_message_success(self):
        frame_id = 0x500
        encoded = b"\x10\x20"

        msg_def = MagicMock(frame_id=frame_id)
        msg_def.encode.return_value = encoded

        db = MagicMock()
        db.get_message_by_name.return_value = msg_def

        bus = MagicMock()

        can_utils.send_message(bus, db, "TEST_MSG", {"val": 1})

        db.get_message_by_name.assert_called_once_with("TEST_MSG")
        msg_def.encode.assert_called_once_with({"val": 1})
        bus.send.assert_called_once()

        sent_msg = bus.send.call_args.args[0]
        self.assertEqual(sent_msg.arbitration_id, frame_id)
        self.assertEqual(sent_msg.data, encoded)
        self.assertTrue(sent_msg.is_extended_id)

    def test_send_message_failure(self):
        msg_def = MagicMock()
        msg_def.encode.return_value = b"\x00"

        db = MagicMock()
        db.get_message_by_name.return_value = msg_def

        bus = MagicMock()
        bus.send.side_effect = RuntimeError("bus down")

        with self.assertRaises(RuntimeError):
            can_utils.send_message(bus, db, "FAIL_MSG", {})

   
    def test_print_bus_stats_success(self):
        bus = MagicMock()
        bus.get_stats.return_value = "OK"

        self.assertEqual(can_utils.print_bus_stats(bus), "OK")
        bus.get_stats.assert_called_once()

    def test_print_bus_stats_failure(self):
        bus = MagicMock()
        bus.get_stats.side_effect = ValueError("stats err")

        with self.assertRaises(ValueError):
            can_utils.print_bus_stats(bus)



# if __name__ == "__main__":  # pragma: no cover
#     unittest.main()