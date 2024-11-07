from brick import Brick


class FallingBrick(Brick):
    def __init__(self, x, y, width, height, screen, color):
        super().__init__(x, y, width, height, screen, color)

        # Velocity
        self.vx = 0
        self.vy = 0

        # Acceleration
        self.ax = 0
        self.ay = 0

        # Mass
        self.mass = 1

        # Forces
        self.forces = []

        self.gravity = -0.001

    def add_force(self, fx: float, fy: float) -> None:
        """Add a force vector (fx, fy) to the object"""
        self.forces.append((fx, fy))

    def update(self, delta_time: float) -> None:
        # Reset acceleration
        self.ax = 0
        self.ay = 0

        # Add gravity
        self.ay -= self.gravity

        # Sum up all forces and convert to acceleration (F = ma)
        for fx, fy in self.forces:
            self.ax += fx / self.mass
            self.ay += fy / self.mass

        # Clear forces for next frame
        self.forces.clear()

        # Update velocity (v = v0 + at)
        self.vx += self.ax * delta_time
        self.vy += self.ay * delta_time

        # Update position (x = x0 + vt)
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
