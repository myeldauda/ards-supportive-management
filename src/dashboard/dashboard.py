from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np

from src.models.patient import Patient
from src.models.ards_model import ARDSModel
from src.models.lung_mechanics import LungMechanics
from src.models.gas_exchange import GasExchange
from src.models.ventilator import Ventilator
from src.simulation.solver import EulerSolver
from src.simulation.simulation_engine import SimulationEngine


# =========================
# INITIALIZE SIMULATION
# =========================

patient = Patient(
    patient_id="ARDS001",
    age=45,
    weight_kg=70,
    height_cm=175,
)

ards_model = ARDSModel(severity="moderate")

lung_mechanics = LungMechanics(
    compliance_ml_per_cmh2o=25,
    airway_resistance_cmh2o_per_lps=12,
    peep=10
)

gas_exchange = GasExchange(
    fio2=0.6,
    shunt_fraction=0.60
)

ventilator = Ventilator(
    peep=10,
    respiratory_rate=15,
    inspiratory_pressure=20
)

solver = EulerSolver()

simulation = SimulationEngine(
    patient=patient,
    ards_model=ards_model,
    lung_mechanics=lung_mechanics,
    gas_exchange=gas_exchange,
    ventilator=ventilator,
    solver=solver
)


# =========================
# DASH APP
# =========================

app = Dash(__name__)


def metric_card(title, card_id, color):

    return html.Div(
        style={
            "backgroundColor": "#1e293b",
            "padding": "20px",
            "borderRadius": "16px",
            "boxShadow": "0px 4px 12px rgba(0,0,0,0.3)",
        },
        children=[

            html.H3(
                title,
                style={
                    "marginBottom": "10px",
                    "color": "#cbd5e1",
                }
            ),

            html.H1(
                id=card_id,
                style={
                    "color": color,
                    "margin": "0",
                }
            ),

        ]
    )


app.layout = html.Div(

    style={
        "backgroundColor": "#0f172a",
        "minHeight": "100vh",
        "padding": "20px",
        "fontFamily": "Arial",
        "color": "white",
    },

    children=[

        html.H1(
            "ARDS Supportive Management Dashboard",
            style={
                "textAlign": "center",
                "marginBottom": "30px",
            }
        ),

        html.Div(

            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))",
                "gap": "20px",
                "marginBottom": "30px",
            },

            children=[

                metric_card("SpO₂", "spo2-card", "#22c55e"),
                metric_card("PaO₂", "pao2-card", "#3b82f6"),
                metric_card("PaCO₂", "paco2-card", "#f59e0b"),
                metric_card("Airway Pressure", "pressure-card", "#ef4444"),

            ]
        ),

        dcc.Graph(
            id="pressure-waveform"
        ),

        dcc.Interval(
            id="interval-component",
            interval=1000,
            n_intervals=0
        )

    ]
)


# =========================
# LIVE CALLBACK
# =========================

@app.callback(
    [
        Output("spo2-card", "children"),
        Output("pao2-card", "children"),
        Output("paco2-card", "children"),
        Output("pressure-card", "children"),
        Output("pressure-waveform", "figure"),
    ],
    Input("interval-component", "n_intervals")
)
def update_dashboard(n):

    # Run simulation step
    simulation.step(current_time=n, dt=0.2)

    patient_state = patient.get_state()

    spo2 = f"{patient_state['spo2'] * 100:.1f}%"
    pao2 = f"{patient_state['pao2']:.1f} mmHg"
    paco2 = f"{patient_state['paco2']:.1f} mmHg"
    pressure = f"{patient_state['airway_pressure']:.1f} cmH₂O"

    # Generate waveform
    time = np.linspace(0, 6, 200)

    waveform = (
        patient_state["airway_pressure"]
        + 5 * np.sin(2 * np.pi * time / 4)
    )

    figure = go.Figure()

    figure.add_trace(

        go.Scatter(
            x=time,
            y=waveform,
            mode="lines",
            name="Pressure",
        )

    )

    figure.update_layout(
        template="plotly_dark",
        title="Real-Time Airway Pressure Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Pressure (cmH₂O)",
        height=400,
    )

    return (
        spo2,
        pao2,
        paco2,
        pressure,
        figure
    )


if __name__ == "__main__":
    app.run(debug=True)