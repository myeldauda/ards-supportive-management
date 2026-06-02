from dataclasses import dataclass


@dataclass
class GasExchange:
    """
    Models oxygen and carbon dioxide exchange in ARDS physiology.
    """

    fio2: float = 0.6
    atmospheric_pressure: float = 760.0
    water_vapor_pressure: float = 47.0
    respiratory_quotient: float = 0.8
    shunt_fraction: float = 0.60   # Moderate ARDS default

    def __post_init__(self):
        if not (0.21 <= self.fio2 <= 1.0):
            raise ValueError("FiO2 must be between 0.21 and 1.0")

        if not (0.0 <= self.shunt_fraction <= 0.8):
            raise ValueError("Shunt fraction must be between 0.0 and 0.8")

    def calculate_alveolar_oxygen(self, paco2: float) -> float:
        """
        Alveolar gas equation.
        """

        return (
            self.fio2
            * (self.atmospheric_pressure - self.water_vapor_pressure)
            - (paco2 / self.respiratory_quotient)
        )

    def calculate_arterial_oxygen(
        self,
        alveolar_oxygen: float,
        oxygen_transfer_efficiency: float
    ) -> float:
        """
        ARDS-adjusted arterial oxygen.
        """

        arterial_oxygen = (
            alveolar_oxygen
            * oxygen_transfer_efficiency
            * (1 - self.shunt_fraction)
        )

        return max(40.0, min(arterial_oxygen, 95.0))

    def calculate_spo2(self, pao2: float) -> float:
        """
        Hemoglobin oxygen dissociation approximation.
        """

        p50 = 26.6
        hill_coefficient = 2.7

        spo2 = (
            pao2 ** hill_coefficient
        ) / (
            (pao2 ** hill_coefficient)
            + (p50 ** hill_coefficient)
        )

        return max(0.5, min(spo2, 0.99))

    def update_paco2(
        self,
        current_paco2: float,
        alveolar_ventilation: float,
        dt: float
    ) -> float:
        """
        CO2 dynamics.
        """

        co2_production = 0.12
        elimination_factor = 0.003

        new_paco2 = current_paco2 + dt * (
            co2_production - (elimination_factor * alveolar_ventilation)
        )

        return max(35.0, min(new_paco2, 80.0))