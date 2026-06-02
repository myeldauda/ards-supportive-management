class EulerSolver:
    """
    Simple Euler numerical integration solver.
    """

    @staticmethod
    def integrate(
        current_value: float,
        rate_of_change: float,
        dt: float
    ) -> float:
        """
        Euler integration step.

        x(t+dt) = x(t) + dt * dx/dt
        """

        return current_value + (dt * rate_of_change)