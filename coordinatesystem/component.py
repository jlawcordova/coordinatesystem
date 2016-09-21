"""
Contains necessary classes involved in various coordinate system calculations.
"""

import sys
from math import cos, sin, atan, pow, sqrt

class Point2D:
    """
    Represents a point in a 2-dimensional plane.
    
    :param xCoordinate: X-coordinate of the point.
    :param yCoordinate: Y-coordinate of the point. 
    """

    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%f, %f)' % (self.x, self.y)
    
    @classmethod
    def from_polar_coordinate(cls, magnitude, angle):
        """
        Creates a point in a 2-dimensional plane 
        from a given polar coordinate.

        :param magnitude: Magnitude of the polar coodinate.
        :param angle: Angle of the polar coordinate.

        :returns: Point2D object.
        """
        x = magnitude * cos(angle)
        y = magnitude * sin(angle)
        point2d = cls(x, y)
        
        return point2d

    def rotate(self, angle):
        """
        Rotates the point by an angle in radians.

        :param angle: Angle in radians.
        """
        cosang = cos(angle)
        sinang = sin(angle)
        temp = self.x
        self.x = (self.x * cosang) + (self.y * sinang)
        self.y = (-temp * sinang) + (self.y * cosang)

    def offset(self, xoffset, yoffset):
        """
        Offsets the point by an x and y displacement.
        
        :param xoffset: Offset in the x-axis.
        :param yoffset: Offset in the y-axis
        """
        self.x += xoffset
        self.y += yoffset

    def get_distance(self, point):
        """
        Gets the distance from the point and another point.

        :param point: Point to calculate the distance with.
        :returns: Distance between the two points.
        """
        xdistance = self.x - point.x
        ydistance = self.y - point.y

        distance = sqrt(pow(xdistance, 2) + pow(ydistance, 2))

        return distance

    def get_slope(self, point):
        """
        Gets the slope of the line formed from the point
        and another point.

        :param point: Point to calculate the slope with.
        :returns: Slope of the line formed from the two points.
        """
        xdistance = self.x - point.x
        ydistance = self.y - point.y

        if xdistance != 0:
            slope = ydistance/xdistance
        else:
            # Avoid a divide by zero error. Use the smallest possible float instead.
            slope = ydistance/sys.float_info.min
        
        return slope

class Line2D:
    """
    Represents an infinite-lengthed line in a 2-dimensional plane.

    :param slope: Slope of the line.
    :param yintercept: Y-intercept of the line.
    """

    def __init__(self, slope = 1.0, yintercept = 0.0):
        self.slope = slope
        self.yintercept = yintercept

    def __str__(self):
        return 'y = %2fx + %f' % (self.slope, self.yintercept)
    
    @classmethod
    def from_two_points(cls, point1, point2):
        """
        Creates an infinite-lengthed line in a 2-dimensional plane given
        two points on the line.

        :param point1: First point on the line.
        :param point2: Second point on the line.
        :returns: Line2D object.
        """
        slope = point1.get_slope(point2)
        # Since the equation of a line in slope-intercept form is y = mx - m(x1) + (y1),
        # where - m(x1) + (y1) is the y-intercept.
        yintercept = (-(slope * point1.x) + point1.y)

        line2d = cls(slope, yintercept)

        return line2d

    @classmethod
    def from_point_slope(cls, slope, point):
        """
        Creates an infinite-lengthed line in a 2-dimensional plane given
        a point on the line and the line's slope.

        :param slope: Slope of the line.
        :param point: Point on the line.
        :returns: Line2D object.
        """
        # Since the equation of a line in slope-intercept form is y = mx - m(x1) + (y1),
        # where - m(x1) + (y1) is the y-intercept.
        yintercept = (-(slope * point.x) + point.y)

        line2d = cls(slope, yintercept)

        return line2d

    def includes_point(self, point):
        """
        Determines if a point is on or included in the line.

        :param point: Point to be determine if on the line.
        :returns: Boolean stating if the point is on the line.
        """
        # Given a value x-coordinate, determine the corresponding y-coordinate
        # on the line (y = mx + b).
        liney = (self.slope * point.x) - self.yintercept

        return (liney == point.y)

    def is_above_point(self, point):
        """
        Determines if the line is above a given point.

        .. note::
            If the line is vertical with a positive infinite slope, 
            the result of this function will be true if the point is on
            the left side of the line.

        :param point: Point to determine the position with.
        :returns: Boolean stating if the line is above the given point.
        """
        # Given a value x-coordinate, determine the corresponding y-coordinate
        # on the line (y = mx + b).
        liney = (self.slope * point.x) - self.yintercept

        return (liney > point.y)

    def get_angle_between(self, line):
        """
        Gets the angle between the line and another line.

        :param line: Line used to calculate the angle in between.
        :returns: Angle in between the two line in radians.
        """
        angle = atan((self.slope - line.slope) / (1 + (self.slope * line.slope)))

        return angle 