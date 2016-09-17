"""
Contains classes which serve to provide functionalities that handle calculations
involving coordinate systems.
"""

import sys
from math import atan, pi

from coordinatesystem.component import Point2D
from coordinatesystem.component import Line2D
from coordinatesystem.exceptions import ZeroDistanceError

class EquivalentCoordinate:
    """
    A class handling conversion from a cartesian coordinate system to another
    scaled or rotated equivalent cartesian coordinate system. Two reference points must be
    provided for each coordinate system in order to plot a point from the original
    coordinate to the equivalent coordinate.

    :param origpointref1: First reference point from the original coordinate system.
    :param origpointref2: Second reference point from the original coordinate system.
    :param equipointref1: First reference point from the equivalent coordinate system.
    :param equipointref2: Second reference point from the equivalent coordinate system.
    """

    def __init__(self, origpointref1, origpointref2, equipointref1, equipointref2):
        self.origpointref1 = origpointref1
        self.origpointref2 = origpointref2
        self.equipointref1 = equipointref1
        self.equipointref2 = equipointref2

        try:
            self.__distancescale = equipointref1.get_distance(equipointref2) / origpointref1.get_distance(origpointref2)
        except ZeroDivisionError:
            raise ZeroDistanceError()

        self.__origlineref = Line2D.from_two_points(origpointref1, origpointref2)
        # Get the slope of the line which is perpendicular to the
        # original line reference.
        if(self.__origlineref.slope != 0):
            self.__origperpensloperef = -1 / self.__origlineref.slope
        else:
            self.__origperpensloperef = -1 / sys.float_info.min
        
        self.__equilineref = Line2D.from_two_points(equipointref1, equipointref2)

        self.__is_reflected_horizontally = equipointref1.x > equipointref2.x
        self.__is_reflected_vertically = equipointref1.y > equipointref2.y

    def get_equivalent_point(self, origpoint):
        """
        Gets the point in the equivalent coordinate system correponding
        to a point the the original coordinate system.

        :param origpoint: Point in the original coordinate system.
        :returns: Point in the equivalent coordinate system.
        """
        origdistance = self.origpointref1.get_distance(origpoint)
        origline = Line2D.from_two_points(self.origpointref1, origpoint)

        # Get the equivalent distance.
        equidistance = self.__distancescale * origdistance

        # Get the equivalent angle. Add 180 degrees if the point is 
        # located below the line which is perpendicular to the original line reference.
        anglebetween = origline.get_angle_between(self.__origlineref)
        origperpenline = Line2D.from_point_slope(self.__origperpensloperef, self.origpointref1)
        if(origperpenline.is_above_point(origpoint) != origperpenline.is_above_point(self.origpointref2)):
            anglebetween += pi
        
        equipointrelative = Point2D.from_polar_coordinate(equidistance, anglebetween)
        equipointrelative.rotate(atan(-self.__origlineref.slope))

        # Reflect if references are reflected.
        if(self.__is_reflected_horizontally):
            equipointrelative.x *= -1
        if(self.__is_reflected_vertically):
            equipointrelative.y *= -1

        # Offset the first equivalent point reference.
        equipoint = self.equipointref1
        equipoint.offset(equipointrelative.x, equipointrelative.y)

        return equipoint