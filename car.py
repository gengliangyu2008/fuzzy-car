import math

from planecoord import Line2D, LineSeg2D


class Car(object):
    def __init__(self, pos, angle, radius, wall_points):
        """The car controlled by fuzzy system.

        Args:
            pos (tuple): (x, y) position of the car.
            angle (float): the angle of the car in degree and always in
                [0, 360).
            radius (int): the size (radius) of the car.
            wall_points (list): a list with all the edge points of the map.
        """

        self.pos = pos
        self.angle = angle % 360
        self.radius = radius
        self.wheel_angle = 0
        self.walls = []
        for idx in range(len(wall_points) - 1):
            self.walls.append(
                LineSeg2D(wall_points[idx], wall_points[idx + 1]))

    def move(self):
        pass

    def dist_radar(self, direction, get_intersection=False):
        if direction == 'front':
            degree = self.angle
        elif direction == 'left':
            degree = (self.angle + 30) % 360
        else:
            degree = (self.angle - 30) % 360
        radar = Line2D(self.pos, (self.pos[0] + math.cos(math.radians(degree)),
                                  self.pos[1] + math.sin(math.radians(degree))))
        intersections = []
        for wall in self.walls:
            inter = wall.intersection(radar)
            if inter is not None:
                if (degree == 0 and inter[0] > 0
                        or degree == 180 and inter[0] < 0
                        or 0 < degree < 180 and inter[1] > 0
                        or 180 < degree < 360 and inter[1] < 0):
                    intersections.append(inter)
        if get_intersection:
            return min(intersections, key=lambda item: dist(self.pos, item))
        return min(dist(self.pos, i) for i in intersections)


def dist(pt0, pt1):
    """Return the distance between pt0 and pt1."""
    return math.sqrt(sum(map(lambda a, b: (a - b)**2, pt0, pt1)))
