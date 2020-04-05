from BaseCanvas import BaseCanvas
from axis import Axis
from complex_point import ComplexPoint
from pygame.event import Event
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, Vector2


class Main(BaseCanvas):

    def init_hook(self):
        self.axis = Axis(self.screen_size)
        self.complexPoint = ComplexPoint(self.screen_size / 2)
        self.scale = 10

    def setup_hook(self):
        pass

    def loop_hook(self):
        self.axis.draw(self.canvas)
        self.axis.draw_unit_circle(self.canvas, self.scale)

        # If the screen if resized
        self.axis.center = self.screen_size / 2
        self.axis.screen_size = self.screen_size
        self.complexPoint.center = self.screen_size / 2

        if self.complexPoint.is_calculating is True:
            self.complexPoint.calculate_point(self.scale)
        self.complexPoint.draw_constant(self.canvas, self.scale)
        if len(self.complexPoint.previous_points) > 1:
            for i in range(1, len(self.complexPoint.previous_points)):
                self.complexPoint.draw_previous_point_to_current(
                    self.canvas, self.complexPoint.previous_points[i - 1],
                    self.complexPoint.previous_points[i], self.scale)
        elif len(self.complexPoint.previous_points) == 1:
            self.complexPoint.draw_previous_point_to_current(
                self.canvas, self.complexPoint.previous_points[0],
                self.complexPoint.point, self.scale)

    def handle_events_hook(self, event: Event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scale += 2
            elif event.button == 5:
                self.scale = (self.scale - 2 ) if self.scale > 2 else 1
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.complexPoint.set_point(Vector2(event.pos), self.scale)
                self.complexPoint.is_calculating = True
            elif event.button == 3:
                self.complexPoint.set_constant(Vector2(event.pos), self.scale)


if __name__ == "__main__":
    main = Main()
    main.loop()
