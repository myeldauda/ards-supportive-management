from src.models.patient import Patient
from src.models.ards_model import ARDSModel
from src.models.lung_mechanics import LungMechanics
from src.models.gas_exchange import GasExchange
from src.models.ventilator import Ventilator
from src.simulation.solver import EulerSolver


class SimulationEngine:
    """
    Coordinates ARDS physiological simulation.
    """

    def __init__(
        self,
        patient: Patient,
        ards_model: ARDSModel,
        lung_mechanics: LungMechanics,
        gas_exchange: GasExchange,
        ventilator: Ventilator,
        solver: EulerSolver
    ):
        self.patient = patient
        self.ards_model = ards_model
        self.lung_mechanics = lung_mechanics
        self.gas_exchange = gas_exchange
        self.ventilator = ventilator
        self.solver = solver

    def step(self, current_time: float, dt: float):

        # ==========================================
        # VENTILATOR PHASE
        # ==========================================

        ventilator_pressure = (
            self.ventilator.get_ventilator_pressure(
                current_time
            )
        )

        alveolar_pressure = (
            self.patient.lung_volume_ml
            / self.lung_mechanics.compliance_ml_per_cmh2o
        )

        airflow = (
            self.lung_mechanics.calculate_airflow(
                ventilator_pressure=ventilator_pressure,
                alveolar_pressure=alveolar_pressure
            )
        )

        # ==========================================
        # INSPIRATION / EXPIRATION
        # ==========================================

        if self.ventilator.is_inspiration_phase(current_time):

            new_lung_volume = (
                self.lung_mechanics.update_lung_volume(
                    current_volume_ml=self.patient.lung_volume_ml,
                    airflow_lps=airflow,
                    dt=dt
                )
            )

        else:

            # passive expiration
            expiratory_flow = 0.35

            new_lung_volume = max(
                self.patient.lung_volume_ml
                - expiratory_flow * 1000 * dt,
                0.0
            )

            airflow = -expiratory_flow

        # ==========================================
        # AIRWAY PRESSURE
        # ==========================================

        airway_pressure = (
            self.lung_mechanics.calculate_airway_pressure(
                airflow_lps=airflow,
                lung_volume_ml=new_lung_volume
            )
        )

        # ==========================================
        # GAS EXCHANGE
        # ==========================================

        alveolar_oxygen = (
            self.gas_exchange.calculate_alveolar_oxygen(
                paco2=self.patient.paco2
            )
        )

        oxygen_efficiency = (
            self.ards_model.get_oxygen_transfer_efficiency()
        )

        arterial_oxygen = (
            self.gas_exchange.calculate_arterial_oxygen(
                alveolar_oxygen=alveolar_oxygen,
                oxygen_transfer_efficiency=oxygen_efficiency
            )
        )

        spo2 = (
            self.gas_exchange.calculate_spo2(
                pao2=arterial_oxygen
            )
        )

        # ==========================================
        # CO2 DYNAMICS
        # ==========================================

        alveolar_ventilation = max(
            airflow * 60,
            0
        )

        new_paco2 = (
            self.gas_exchange.update_paco2(
                current_paco2=self.patient.paco2,
                alveolar_ventilation=alveolar_ventilation,
                dt=dt
            )
        )

        # ==========================================
        # UPDATE PATIENT
        # ==========================================

        self.patient.update_state(
            spo2=spo2,
            pao2=arterial_oxygen,
            paco2=new_paco2,
            lung_volume_ml=new_lung_volume,
            airflow_lps=airflow,
            airway_pressure=airway_pressure
        )

        self.patient.record_state(current_time)

    def run(
        self,
        duration_sec: float,
        dt: float = 0.2
    ):

        current_time = 0.0

        while current_time <= duration_sec:

            self.step(
                current_time=current_time,
                dt=dt
            )

            current_time += dt