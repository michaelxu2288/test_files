
import dataclasses
import unittest
from unittest.mock import patch

import src.config.utils as utils 

from src.config.utils import loadCurve

class TestLoadCurve(unittest.TestCase):
    """Unit-tests for utils.loadCurve()."""

    def test_basic_conversion(self):
        """Given a list of dicts, loadCurve should return a Curve2D
        instance whose .points list contains Point2D instances with the
        same coordinates"""
        sample = [{"x": 0.0, "y": 1.0},
                  {"x": 2.5, "y": 3.3}]

 
        with patch.object(utils, "tms") as mock_tms:
            @dataclasses.dataclass
            class Point2D:
                x: float
                y: float

            @dataclasses.dataclass
            class Curve2D:
                points: list["Point2D"]

            mock_tms.Point2D = Point2D
            mock_tms.Curve2D = Curve2D

            curve = utils.loadCurve(sample)

            expected_points = [Point2D(x=0.0, y=1.0),
                               Point2D(x=2.5, y=3.3)]

            self.assertIsInstance(curve, Curve2D)
            self.assertEqual(curve.points, expected_points)

    def test_empty_input(self):
        """An empty list should return a Curve2D with an empty points list."""
        with patch.object(utils, "tms") as mock_tms:
            @dataclasses.dataclass
            class Point2D:
                x: float
                y: float

            @dataclasses.dataclass
            class Curve2D:
                points: list["Point2D"]

            mock_tms.Point2D = Point2D
            mock_tms.Curve2D = Curve2D

            curve = utils.loadCurve([])
            self.assertEqual(curve.points, [])


# if __name__ == "__main__":
#     unittest.main()
