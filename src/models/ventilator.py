from dataclasses import dataclass


@dataclass
class Ventilator:
    """
    Models mechanical ventilator behavior.
    """

    fio2: float = 0.6
    peep: float = 10.0
    respiratory_rate: int = 20
    inspiratory_pressure: float = 20.0
    tidal_volume_target_ml: float = 450.0
    inspiration_time_sec: float = 1.0

    def __post_init__(self):
        """
        Validates ventilator settings.
        """

        if not (0.21 <= self.fio2 <= 1.0):
            raise ValueError("FiO2 must be between 0.21 and 1.0")

        if self.peep < 0:
            raise ValueError("PEEP cannot be negative")

        if self.respiratory_rate <= 0:
            raise ValueError("Respiratory rate must be positive")

        if self.inspiratory_pressure <= 0:
            raise ValueError("Inspiratory pressure must be positive")

        if self.tidal_volume_target_ml <= 0:
            raise ValueError("Tidal volume target must be positive")

        if self.inspiration_time_sec <= 0:
            raise ValueError("Inspiration time must be positive")

    def get_breath_cycle_duration(self) -> float:
        """
        Returns total duration of one breath cycle in seconds.
        """

        return 60.0 / self.respiratory_rate

    def is_inspiration_phase(self, current_time: float) -> bool:
        """
        Determines whether the ventilator is in inspiration phase.
        """

        cycle_duration = self.get_breath_cycle_duration()
        time_in_cycle = current_time % cycle_duration

        return time_in_cycle <= self.inspiration_time_sec

    def get_ventilator_pressure(self, current_time: float) -> float:
        """
        Returns ventilator pressure at the current simulation time.
        """

        if self.is_inspiration_phase(current_time):
            return self.inspiratory_pressure + self.peep

        return self.peep