from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Patient:
    """
    Represents the physiological state of an ARDS patient.
    """

    patient_id: str
    age: int
    weight_kg: float
    height_cm: float

    spo2: float = 0.88
    pao2: float = 65.0
    paco2: float = 50.0
    respiratory_rate: int = 28
    tidal_volume_ml: float = 450.0

    heart_rate: int = 110
    systolic_bp: int = 110
    diastolic_bp: int = 70

    lung_compliance: float = 25.0
    airway_resistance: float = 12.0

    lung_volume_ml: float = 0.0
    airflow_lps: float = 0.0
    airway_pressure: float = 0.0

    ards_severity: str = "moderate"

    history: Dict[str, List[float]] = field(default_factory=lambda: {
        "time": [],
        "spo2": [],
        "pao2": [],
        "paco2": [],
        "lung_volume_ml": [],
        "airflow_lps": [],
        "airway_pressure": []
    })

    def __post_init__(self):
        self.validate()

    def validate(self):
        """
        Validates physiological realism.
        """

        if not (0.0 <= self.spo2 <= 1.0):
            raise ValueError("SpO2 must be between 0.0 and 1.0")

        if self.pao2 <= 0:
            raise ValueError("PaO2 must be positive")

        if self.paco2 <= 0:
            raise ValueError("PaCO2 must be positive")

        if self.respiratory_rate <= 0:
            raise ValueError("Respiratory rate must be positive")

        if self.tidal_volume_ml <= 0:
            raise ValueError("Tidal volume must be positive")

        if self.lung_compliance <= 0:
            raise ValueError("Lung compliance must be positive")

        if self.airway_resistance <= 0:
            raise ValueError("Airway resistance must be positive")

        if self.ards_severity.lower() not in ["mild", "moderate", "severe"]:
            raise ValueError("ARDS severity must be mild, moderate, or severe")

    def update_state(
        self,
        spo2=None,
        pao2=None,
        paco2=None,
        lung_volume_ml=None,
        airflow_lps=None,
        airway_pressure=None
    ):
        """
        Updates the patient's physiological state during simulation.
        """

        if spo2 is not None:
            self.spo2 = spo2

        if pao2 is not None:
            self.pao2 = pao2

        if paco2 is not None:
            self.paco2 = paco2

        if lung_volume_ml is not None:
            self.lung_volume_ml = lung_volume_ml

        if airflow_lps is not None:
            self.airflow_lps = airflow_lps

        if airway_pressure is not None:
            self.airway_pressure = airway_pressure

        self.validate()

    def record_state(self, time_step: float):
        """
        Stores simulation values for analysis and plotting.
        """

        self.history["time"].append(time_step)
        self.history["spo2"].append(self.spo2)
        self.history["pao2"].append(self.pao2)
        self.history["paco2"].append(self.paco2)
        self.history["lung_volume_ml"].append(self.lung_volume_ml)
        self.history["airflow_lps"].append(self.airflow_lps)
        self.history["airway_pressure"].append(self.airway_pressure)

    def get_state(self):
        """
        Returns the current physiological state.
        """

        return {
            "patient_id": self.patient_id,
            "spo2": self.spo2,
            "pao2": self.pao2,
            "paco2": self.paco2,
            "respiratory_rate": self.respiratory_rate,
            "tidal_volume_ml": self.tidal_volume_ml,
            "lung_compliance": self.lung_compliance,
            "airway_resistance": self.airway_resistance,
            "lung_volume_ml": self.lung_volume_ml,
            "airflow_lps": self.airflow_lps,
            "airway_pressure": self.airway_pressure,
            "ards_severity": self.ards_severity
        }