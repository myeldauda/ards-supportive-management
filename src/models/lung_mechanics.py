from dataclasses import dataclass


@dataclass
class LungMechanics:
    """
    Models respiratory mechanics for ventilated ARDS lungs.
    """

    compliance_ml_per_cmh2o: float
    airway_resistance_cmh2o_per_lps: float
    peep: float = 10.0

    def __post_init__(self):
        """
        Validate parameters.
        """

        if self.compliance_ml_per_cmh2o <= 0:
            raise ValueError(
                "Compliance must be positive."
            )

        if self.airway_resistance_cmh2o_per_lps <= 0:
            raise ValueError(
                "Airway resistance must be positive."
            )

        if self.peep < 0:
            raise ValueError(
                "PEEP cannot be negative."
            )

    # ==================================================
    # AIRFLOW
    # ==================================================

    def calculate_airflow(
        self,
        ventilator_pressure: float,
        alveolar_pressure: float
    ) -> float:
        """
        Calculates airflow using Ohm's law of respiration.

        Flow = ΔP / Resistance
        """

        pressure_gradient = (
            ventilator_pressure
            - alveolar_pressure
        )

        airflow = (
            pressure_gradient
            / self.airway_resistance_cmh2o_per_lps
        )

        # Physiological limits
        airflow = max(
            -2.0,
            min(
                airflow,
                2.0
            )
        )

        return airflow

    # ==================================================
    # AIRWAY PRESSURE
    # ==================================================

    def calculate_airway_pressure(
        self,
        airflow_lps: float,
        lung_volume_ml: float
    ) -> float:
        """
        Calculates airway pressure.

        Paw = PEEP + Resistive + Elastic
        """

        elastic_pressure = (
            lung_volume_ml
            / self.compliance_ml_per_cmh2o
        )

        resistive_pressure = (
            airflow_lps
            * self.airway_resistance_cmh2o_per_lps
        )

        airway_pressure = (
            self.peep
            + elastic_pressure
            + resistive_pressure
        )

        # Safety limits
        airway_pressure = max(
            0.0,
            min(
                airway_pressure,
                60.0
            )
        )

        return airway_pressure

    # ==================================================
    # LUNG VOLUME
    # ==================================================

    def update_lung_volume(
        self,
        current_volume_ml: float,
        airflow_lps: float,
        dt: float
    ) -> float:
        """
        Updates lung volume from airflow.
        """

        airflow_ml_per_sec = (
            airflow_lps
            * 1000
        )

        new_volume = (
            current_volume_ml
            + airflow_ml_per_sec * dt
        )

        # Prevent negative volume
        new_volume = max(
            0.0,
            new_volume
        )

        # Prevent overdistension
        new_volume = min(
            new_volume,
            1000.0
        )

        return new_volume

    # ==================================================
    # ALVEOLAR PRESSURE
    # ==================================================

    def calculate_alveolar_pressure(
        self,
        lung_volume_ml: float
    ) -> float:
        """
        Calculates alveolar pressure from lung volume.
        """

        alveolar_pressure = (
            self.peep
            + (
                lung_volume_ml
                / self.compliance_ml_per_cmh2o
            )
        )

        return alveolar_pressure