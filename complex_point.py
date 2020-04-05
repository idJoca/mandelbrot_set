from pygame import Vector2, Surface, Color
from pygame.draw import circle, aaline
from helper import cohenSutherlandClip


class ComplexPoint():
    CONSTANT_COLOR = Color(255, 10, 10)
    POINT_COLOR = Color(200, 200, 200)

    def __init__(self, center: Vector2):
        self.center = center
        self.point = complex(0.0, 0.0)
        self.previous_points = []
        self.constant = complex(1.0, 0.0)
        self.is_calculating = False
        self.overflowed = False

    def from_complex_to_pixels_by_scale(self, point: complex, scale: int):
        return Vector2(point.real * scale + self.center.x, point.imag * scale + self.center.y)

    def is_complex_overflowing(self, position: complex, scale: int):
        x_position = position.real * scale + self.center.x
        y_position = position.imag * scale + self.center.y
        return (x_position > self.center.x * 2 or x_position < 0
                or y_position > self.center.y * 2 or y_position < 0)

    def set_constant(self, position: Vector2, scale: int):
        self.reset()
        scaled_position = (position - self.center) / scale
        self.constant = complex(
            scaled_position.x,
            scaled_position.y
        )

    def set_point(self, position: Vector2, scale: int):
        self.reset()
        scaled_position = (position - self.center) / scale
        self.point = complex(
            scaled_position.x,
            scaled_position.y
        )

    def reset(self):
        self.point = complex(0.0, 0.0)
        self.previous_points = []
        self.is_calculating = False
        self.overflowed = False

    def calculate_point(self, scale: int):
        try:
            if self.overflowed is True:
                self.reset()
            self.previous_points.append(self.point)
            self.point = self.point ** 2 + self.constant
            if self.is_complex_overflowing(self.point, scale):
                # Here we'll calculate the projection of the point
                # onto the side of the screen
                point = self.from_complex_to_pixels_by_scale(
                    self.point, scale)
                previous_point = self.from_complex_to_pixels_by_scale(
                    self.previous_points[len(self.previous_points) - 1], scale)
                projected_line = cohenSutherlandClip(
                    point.x, point.y, previous_point.x, previous_point.y, self.center.x * 2, self.center.y * 2, 0, 0)
                self.previous_points.append(
                    complex(projected_line[0], projected_line[1])
                )
                raise OverflowError()
        except OverflowError as _:
            self.overflowed = True
            self.is_calculating = False

    def draw_constant(self, canvas: Surface, scale: int):
        circle(canvas, ComplexPoint.CONSTANT_COLOR, self.from_complex_to_pixels_by_scale(
            self.constant, scale
        ), 5)

    def draw_previous_point_to_current(self, canvas: Surface, previous_point: complex, next_point: complex, scale: int):
        aaline(canvas, ComplexPoint.POINT_COLOR, self.from_complex_to_pixels_by_scale(
            previous_point, scale
        ), self.from_complex_to_pixels_by_scale(
            next_point, scale
        ))
