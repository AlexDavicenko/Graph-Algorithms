from typing import List
from pygame import Vector2


def get_line_points(x1, y1, x2, y2, width) -> List[Vector2]:
    start = Vector2(x1, y1)
    end = Vector2(x2, y2)

    line_vector = start - end

    angle = line_vector.angle_to(Vector2(0, -1))

    points = [
        Vector2(-width/2, 0),
        Vector2(width/2, 0),
        Vector2(width/2, line_vector.length()),
        Vector2(-width/2, line_vector.length())
    ]
    for p in range(len(points)):
        points[p].rotate_ip(-angle)
        points[p] += start
    return points


def get_arrow_points(x1, y1, x2, y2, size, d=0.75) -> List[Vector2]:

    start = Vector2(x1, y1)

    end = Vector2(x1 + d * (x2 - x1), y1 + d * (y2 - y1))

    arrow_vector = start - end
    angle = arrow_vector.angle_to(Vector2(0, -1))

    points = [
        Vector2(0, size / 4),  # Center
        Vector2(size / 4, -size / 4),  # Bottom right
        Vector2(-size / 4, -size / 4),  # Bottom left
    ]

    # Rotate and translate the head into place
    translation = Vector2(0, arrow_vector.length() - (size / 4)).rotate(-angle)
    for p in range(len(points)):
        points[p].rotate_ip(-angle)
        points[p] += translation
        points[p] += start

    return points

