from dataclasses import dataclass


@dataclass
class LungMechanics:
    """
    Models respiratory mechanics for ventilated ARDS lungs.
    """

    compliance_ml_per_cmh2o: float
    airway_resistance_cmh2o_per_lps: float
    peep: float = 10.0
    max_safe_tidal_volume_ml: float = 500.0

    def __post_init__(self):
        if self.compliance_ml_per_cmh2o <= 0:
            raise ValueError("Compliance must be positive")

        if self.airway_resistance_cmh2o_per_lps <= 0:
            raise ValueError("Airway resistance must be positive")

        if self.peep < 0:
            raise ValueError("PEEP cannot be negative")

    def calculate_airflow(
        self,
        ventilator_pressure: float,
        alveolar_pressure: float
    ) -> float:
        """
        Airflow based on pressure gradient and resistance.
        """

        pressure_difference = ventilator_pressure - alveolar_pressure

        airflow = pressure_difference / self.airway_resistance_cmh2o_per_lps

        # safer physiologic ARDS airflow range
        airflow = max(-0.8, min(airflow, 0.8))

        return airflow

    def calculate_airway_pressure(
        self,
        airflow_lps: float,
        lung_volume_ml: float
    ) -> float:
        """
        Respiratory equation of motion.
        """

        elastic_pressure = (
            lung_volume_ml / self.compliance_ml_per_cmh2o
        )

        resistive_pressure = (
            airflow_lps * self.airway_resistance_cmh2o_per_lps
        )

        airway_pressure = (
            resistive_pressure
            + elastic_pressure
            + self.peep
        )

        # physiologic safety cap
        airway_pressure = max(5.0, min(airway_pressure, 30.0))

        return airway_pressure

    def update_lung_volume(
        self,
        current_volume_ml: float,
        airflow_lps: float,
        dt: float
    ) -> float:
        """
        Updates lung volume safely.
        """

        airflow_ml_per_sec = airflow_lps * 1000

        new_volume = current_volume_ml + (
            airflow_ml_per_sec * dt
        )

        if new_volume < 0:
            new_volume = 0

        if new_volume > self.max_safe_tidal_volume_ml:
            new_volume = self.max_safe_tidal_volume_ml

        return new_volume