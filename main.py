from src.models.patient import Patient
from src.models.ards_model import ARDSModel
from src.models.lung_mechanics import LungMechanics
from src.models.gas_exchange import GasExchange
from src.models.ventilator import Ventilator
from src.simulation.solver import EulerSolver
from src.simulation.simulation_engine import SimulationEngine
patient = Patient(
    patient_id="ARDS001",
    age=54,
    weight_kg=78,
    height_cm=172
)

ards_model = ARDSModel(
    severity="moderate"
)

lung_mechanics = LungMechanics(
    compliance_ml_per_cmh2o=25.0,
    airway_resistance_cmh2o_per_lps=12.0,
    peep=10.0
)

gas_exchange = GasExchange(
    fio2=0.6
)

ventilator = Ventilator(
    fio2=0.6,
    peep=10.0,
    respiratory_rate=20,
    inspiratory_pressure=20.0,
    tidal_volume_target_ml=450.0
)

solver = EulerSolver()
engine = SimulationEngine(
    patient=patient,
    ards_model=ards_model,
    lung_mechanics=lung_mechanics,
    gas_exchange=gas_exchange,
    ventilator=ventilator,
    solver=solver
)

engine.run(duration_sec=60, dt=1.0)

final_state = patient.get_state()

print("=== FINAL PATIENT STATE ===")
print(final_state)