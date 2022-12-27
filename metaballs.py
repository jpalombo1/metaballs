from dataclasses import dataclass

import matplotlib.animation as animation  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

"""Metaballs from video https://www.youtube.com/watch?v=6oMZb3yP_H8"""

PLOT_SIZE: float = 1
TO_MS: int = 1000


@dataclass
class MetaBall:
    """Metaball object with attributes of radius, x/y start position, x/y velocity."""

    R: float
    x0: float
    y0: float
    vx: float
    vy: float

    def __post_init__(self) -> None:
        """Set sample time to 0."""
        self.sample_time: float = 0.0

    def check_boundary(self) -> None:
        """Check that expected x/y center position minus radius (or edge) does not exceed plot boundaries.

        If so, flip velocity in opposite direction of exceeding dimension so it "bounces" back.
        """
        expected_x = self.x0 + self.vx * self.sample_time
        expected_y = self.y0 + self.vy * self.sample_time
        if expected_x - self.R < 0 or expected_x + self.R > PLOT_SIZE:
            self.vx = -1 * self.vx
        if expected_y - self.R < 0 or expected_y + self.R > PLOT_SIZE:
            self.vy = -1 * self.vy

    def update(self, sample_time: float) -> None:
        """Update the sample time, make sure not out of bounds, then update ball positin based on time and velocity."""
        self.sample_time = sample_time
        self.check_boundary()
        self.x0 += self.vx * sample_time
        self.y0 += self.vy * sample_time

    def draw(self) -> plt.Circle:
        """Draw the circule in matplotlib using center x/y and radius."""
        return plt.Circle((self.x0, self.y0), self.R, fill=False)  # type: ignore


class Frame:
    """Frame that holds all the metaballs."""

    def __init__(self, metaballs: list[MetaBall]) -> None:
        """Gte list of metaball objects in frame, total time."""
        self.metaballs = metaballs
        self.total_time: float = 0.0
        self.framenum: int = 0

    def draw_circles(self, ax) -> None:  # type: ignore
        """Clear axis, get circles for all metabalss and add them to axis for given frame."""
        ax.clear()
        circles = [metaball.draw() for metaball in self.metaballs]
        for circle in circles:
            ax.add_artist(circle)
        plt.title(f"Frame {self.framenum} Time {self.total_time}")

    def draw_contours(self, ax):
        """TODO Marching squares for contours, just clear for now."""
        ax.clear()

    def update(self, framenum: int, sample_time: float, ax) -> None:
        """Update function updates framenum and sample time, makes each metaball update position based on sample time, then draw everything.

        Args:
            framenum (int): The actual number of frame for animation.
            sample_time (float): The sample time that helps determine metaball movement.
            ax (_type_): Axis to draw on.
        """
        self.framenum = framenum
        self.total_time += sample_time
        for metaball in self.metaballs:
            metaball.update(sample_time)
        self.draw_circles(ax)


def main():
    """Main function.

    Initialized frame and metaballs in frame.
    Plays matplotlib animation on figure calling update func each frame with args sample time and axis,
    set interval to sample_time * 1000 for milliseconds.
    """
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
        fig, frame.update, fargs=(sample_time, ax), interval=sample_time * TO_MS
    )
    plt.show()
    print(anim)


if __name__ == "__main__":
    """Main call."""
    main()
