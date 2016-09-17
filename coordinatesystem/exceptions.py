"""
Contains exceptions related to coordinate system handling.
"""

class ZeroDistanceError(Exception):
    """
    Raised when a two points corresponding to a single location
    are involved in a division process. Two points of the same location
    produce zero distance which cannot be used in division.
    """
    def __str__(self):
        return 'two points corresponding to a single location involved in division process'