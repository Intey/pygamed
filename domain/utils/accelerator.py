

class Accelerator:
    """Control speed function"""

    def __init__(self, max_accel, init_accel, accel_in_dt):
        self.max_accel = max_accel
        self.min_accel = init_accel
        self.speed = init_accel
        self.accel_in_dt = accel_in_dt

    def accelerate(self):
        """
        Increment speed
        """
        if self.speed < self.max_accel:
            self.speed += self.accel_in_dt
        if self.speed > self.max_accel:
            self.speed = self.max_accel

    def reset(self):
        """
        reset speed
        """
        self.speed = self.min_accel


