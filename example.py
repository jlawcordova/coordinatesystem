"""
Example Code
============

This is a sample code showing the usage and applications
of the coordinate system library.
"""

import math

from coordinatesystem.component import Point2D
from coordinatesystem.component import Line2D
from coordinatesystem.utility import EquivalentCoordinate

# Point2D handling
point1 = Point2D()
point2 = Point2D(1, 1)

slope = point1.get_slope(point2)
print("Slope of the two points: " + str(slope))

point3 = Point2D.from_polar_coordinate(1, math.pi/4)
print("Point with a polar coordinate:" + str(point3))

# Line handling
l1 = Line2D()
print("Example line: " + str(l1))
print("Is line above first point?: " + str(l1.is_above_point(point1)))
print("Is first point on line?: " + str(l1.includes_point(point1)))

#Equivalent Coordinate
original1 = Point2D(865377, 113203)
equivalent1 = Point2D(418.8, 411.8)
original2 = Point2D(864100.1, 112931.6)
equivalent2 = Point2D(-854.2, 143.3)

sampleoriginal = Point2D(864533.8, 112912.8)
converter = EquivalentCoordinate(original1, original2, equivalent1, equivalent2)
print("Equivalent point: " + str(converter.get_equivalent_point(sampleoriginal)))