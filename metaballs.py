import matplotlib.animation as animation  # type: ignore
import matplotlib.pyplot as plt

"""Metaballs from video https://www.youtube.com/watch?v=6oMZb3yP_H8"""


class MetaBall:
    def __init__(self, R: float, x0: float, y0: float, vx: float, vy: float):
        self.sample_time: float = 0.0
        self.R = R
        self.x0 = x0
        self.y0 = y0
        self.vx = vx
        self.vy = vy

    def check_boundary(self):
        expected_x = self.x0 + self.vx * self.sample_time
        expected_y = self.y0 + self.vy * self.sample_time
        if expected_x - self.R < 0 or expected_x + self.R > 1:
            self.vx = -1 * self.vx
        if expected_y - self.R < 0 or expected_y + self.R > 1:
            self.vy = -1 * self.vy

    def update(self, sample_time: float):
        self.sample_time = sample_time
        self.check_boundary()
        self.x0 += self.vx * sample_time
        self.y0 += self.vy * sample_time

    def draw(self):
        return plt.Circle((self.x0, self.y0), self.R, fill=False)  # type: ignore


class Frame:
    def __init__(self, metaballs: list[MetaBall]):
        self.metaballs = metaballs
        self.total_time: float = 0.0
        self.framenum: int = 0

    def draw_circles(self, ax):  # type: ignore
        ax.clear()
        circles = [metaball.draw() for metaball in self.metaballs]
        for circle in circles:
            ax.add_artist(circle)
        plt.title(f"Frame {self.framenum} Time {self.total_time}")

    # TODO Marching squares for contours
    def draw_contours(self, ax):
        ax.clear()

    def update(self, framenum: int, sample_time: float, ax):
        self.framenum = framenum
        self.total_time += sample_time
        for metaball in self.metaballs:
            metaball.update(sample_time)
        self.draw_circles(ax)


if __name__ == "__main__":
    # Initialize frame
    fig, ax = plt.subplots()
    ax.set_aspect(1)  # type: ignore
    sample_time = 0.1

    # Initialize objects in frame
    mb1 = MetaBall(0.05, 0.1, 0.1, -0.05, 0.1)
    mb2 = MetaBall(0.1, 0.5, 0.5, 0.05, 0.15)
    mb3 = MetaBall(0.22, 0.4, 0.4, -0.25, 0.1)
    mb4 = MetaBall(0.17, 0.3, 0.7, 0.55, 0.32)
    frame = Frame([mb1, mb2, mb3, mb4])

    # Play animation
    anim = animation.FuncAnimation(
        fig, frame.update, fargs=(sample_time, ax), interval=sample_time * 1000
    )
    plt.show()
