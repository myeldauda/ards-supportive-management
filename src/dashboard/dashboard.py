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
from src.data.dataset_loader import ARDSDataset

# ==================================================
# INITIALIZE SIMULATION
# ==================================================

patient = Patient(
    patient_id="ARDS001",
    age=45,
    weight_kg=70,
    height_cm=175,
)

ards_model = ARDSModel(
    severity="moderate"
)

lung_mechanics = LungMechanics(
    compliance_ml_per_cmh2o=25,
    airway_resistance_cmh2o_per_lps=12,
    peep=10,
)

gas_exchange = GasExchange(
    fio2=0.60,
    shunt_fraction=0.60,
)

ventilator = Ventilator(
    peep=10,
    respiratory_rate=15,
    inspiratory_pressure=20,
)

solver = EulerSolver()

simulation = SimulationEngine(
    patient=patient,
    ards_model=ards_model,
    lung_mechanics=lung_mechanics,
    gas_exchange=gas_exchange,
    ventilator=ventilator,
    solver=solver,
)
# ==================================================
# DATASETS
# ==================================================

mild_dataset = ARDSDataset(
    "data/mild_ards.csv"
)

moderate_dataset = ARDSDataset(
    "data/moderate_ards.csv"
)

severe_dataset = ARDSDataset(
    "data/severe_ards.csv"
)

# ==========================================
# TREND STORAGE
# ==========================================

time_history = []

spo2_history = []

pao2_history = []

compliance_history = []

# ==================================================
# DASH APP
# ==================================================

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
                },
            ),
            html.H1(
                id=card_id,
                style={
                    "color": color,
                    "margin": "0",
                },
            ),
        ],
    )

# ==================================================
# LAYOUT
# ==================================================

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
        "Biomedical Engineering ARDS Supportive Management Simulator",
        style={
            "textAlign": "center",
            "marginBottom": "10px",
        },
    ),

    html.H4(
        "Real-Time Computational Respiratory Monitoring and Ventilator Simulation Platform",
        style={
            "textAlign": "center",
            "color": "#94a3b8",
            "marginBottom": "30px",
        },
    ),

    html.Div(
        id="system-status",
        style={
            "backgroundColor": "#1e293b",
            "padding": "12px",
            "borderRadius": "12px",
            "marginBottom": "20px",
            "textAlign": "center",
            "fontWeight": "bold",
            "fontSize": "18px",
        },
    ),

    html.Label("Classification Mode"),

    dcc.Dropdown(
        id="mode-selector",
        options=[
            {"label": "Manual", "value": "manual"},
            {"label": "Dynamic", "value": "dynamic"},
        ],
       value="dynamic",
        clearable=False,
    ),

        # ==========================================
        # CONTROL PANEL
        # ==========================================

        html.Div(
            style={
                "backgroundColor": "#1e293b",
                "padding": "20px",
                "borderRadius": "16px",
                "marginBottom": "20px",
            },
            children=[

                html.H2("Ventilator Controls"),

                html.Label("Patient Profile"),

                dcc.Dropdown(
                    id="profile-selector",
                    options=[
                        {"label": "Mild ARDS", "value": "mild"},
                        {"label": "Moderate ARDS", "value": "moderate"},
                        {"label": "Severe ARDS", "value": "severe"},
                    ],
                    value="moderate",
                    clearable=False,
                    style={
                        "color": "black",
                        "backgroundColor": "white",
                    },
                ),

                html.Br(),

                html.Label("FiO₂"),

                dcc.Slider(
                    id="fio2-slider",
                    min=0.21,
                    max=1.00,
                    step=0.01,
                    value=0.60,
                    tooltip={"placement": "bottom"},
                ),

                html.Br(),

                html.Label("PEEP (cmH₂O)"),

                dcc.Slider(
                    id="peep-slider",
                    min=5,
                    max=20,
                    step=1,
                    value=10,
                    tooltip={"placement": "bottom"},
                ),
            ],
        ),

        # ==========================================
        # METRIC CARDS
        # ==========================================

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

                metric_card("P/F Ratio", "pf-card", "#06b6d4"),
                metric_card("Compliance", "compliance-card", "#a855f7"),
                metric_card("Driving Pressure", "driving-card", "#f97316"),
                metric_card("ARDS Severity", "severity-card", "#e11d48"),
            ],
        ),

        # ==========================================
        # CLINICAL ALERTS PANEL
        # ==========================================

        html.Div(
            id="alerts-panel",
            style={
                "backgroundColor": "#1e293b",
                "padding": "20px",
                "borderRadius": "16px",
                "marginBottom": "20px",
            },
        ),
# ==========================================
# ICU DEVICE EVALUATION
# ==========================================

html.Div(
    style={
        "backgroundColor": "#1e293b",
        "padding": "20px",
        "borderRadius": "16px",
        "marginBottom": "20px",
    },
    children=[

        html.H2("ICU Device Evaluation"),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns":
                    "repeat(auto-fit, minmax(220px, 1fr))",
                "gap": "20px",
            },
            children=[

                metric_card(
                    "Pulse Oximeter Accuracy",
                    "accuracy-card",
                    "#22c55e",
                ),

                metric_card(
                    "Oxygen Supply Reliability",
                    "reliability-card",
                    "#3b82f6",
                ),

                metric_card(
                    "Alarm Response Time",
                    "alarm-card",
                    "#f59e0b",
                ),

                metric_card(
                    "Monitor Stability Index",
                    "stability-card",
                    "#a855f7",
                ),
            ],
        ),
    ],
),
        dcc.Graph(
            id="pressure-waveform"
        ),

        dcc.Interval(
            id="interval-component",
            interval=1000,
            n_intervals=0,
        ),
    ],
)


# ==================================================
# LIVE CALLBACK
# ==================================================

@app.callback(
    [
        Output("spo2-card", "children"),
        Output("pao2-card", "children"),
        Output("paco2-card", "children"),
        Output("pressure-card", "children"),

        Output("pf-card", "children"),
        Output("compliance-card", "children"),
        Output("driving-card", "children"),
    Output("severity-card", "children"),

    Output("system-status", "children"),

    Output("alerts-panel", "children"),
        Output("accuracy-card", "children"),
        Output("reliability-card", "children"),
        Output("alarm-card", "children"),
        Output("stability-card", "children"),
    Output("pressure-waveform", "figure"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("profile-selector", "value"),
        Input("mode-selector", "value"),
        Input("fio2-slider", "value"),
        Input("peep-slider", "value"),
    ],
)
def update_dashboard(
    n,
    profile,
    mode,
    fio2,
    peep,
):

    # Apply settings

    ards_model.severity = profile

    gas_exchange.fio2 = fio2

    lung_mechanics.peep = peep
    ventilator.peep = peep

    # Run simulation

    simulation.step(
        current_time=n,
        dt=0.2,
    )

    patient_state = patient.get_state()

    # ==========================================
    # DATASET-DRIVEN PATIENT STATE
    # ==========================================

    profile = profile.lower()
    # ==========================================
    # DYNAMIC MODE
    # ==========================================

    if mode == "dynamic":

        pf_ratio_estimate = (
            patient_state["pao2"] / fio2
        )

        if pf_ratio_estimate > 200:

            profile = "mild"

        elif pf_ratio_estimate > 100:

            profile = "moderate"

        else:
            profile = "severe"

    # ==========================================
    # DATASET SELECTION
    # ==========================================

    if profile == "mild":

        current_dataset = mild_dataset

    elif profile == "moderate":

        current_dataset = moderate_dataset

    else:

        current_dataset = severe_dataset

    row = current_dataset.get_current_row()

    patient_state["pao2"] = row["pao2"]

    patient_state["paco2"] = row["paco2"]

    patient_state["spo2"] = (
        row["spo2"] / 100
    )

    lung_mechanics.compliance_ml_per_cmh2o = (
        row["compliance"]
    )

    compliance = row["compliance"]

    lung_mechanics.compliance_ml_per_cmh2o = (
        row["compliance"]
    )
    spo2 = f"{patient_state['spo2'] * 100:.1f}%"
    pao2 = f"{patient_state['pao2']:.1f} mmHg"
    paco2 = f"{patient_state['paco2']:.1f} mmHg"
    pressure = f"{patient_state['airway_pressure']:.1f} cmH₂O"

    # ==========================================
    # CLINICAL METRICS
    # ==========================================

    pf_ratio = patient_state["pao2"] / fio2
    # ==========================================
    # DYNAMIC SEVERITY SCORING
    # ==========================================

    severity_score = (
        0.4 * (100 - (patient_state["spo2"] * 100))
        +
        0.3 * patient_state["paco2"]
        +
        0.3 * max(
            0,
            60 - compliance
        )
    )
    compliance = row["compliance"]

    driving_pressure = (
        ventilator.inspiratory_pressure
    )

    if severity_score < 25:

        severity_text = "Mild"

    elif severity_score < 50:

        severity_text = "Moderate"

    else:

        severity_text = "Severe"
    if mode == "dynamic":

        if severity_score < 25:
            profile = "mild"

        elif severity_score < 50:
            profile = "moderate"

        else:
            profile = "severe"
    pf_ratio_text = f"{pf_ratio:.0f}"
    compliance_text = f"{compliance:.1f} mL/cmH₂O"
    driving_text = f"{driving_pressure:.1f} cmH₂O"
     # ==========================================
    # CLINICAL ALERTS
    # ==========================================

    alerts = []

    if pf_ratio < 100:
        severity_text = "Severe"
        alerts.append("🔴 Severe ARDS")

    elif pf_ratio < 200:
        severity_text = "Moderate"
        alerts.append("🟠 Moderate ARDS")

    else:
        severity_text = "Mild"
        alerts.append("🟢 Mild ARDS")

    if patient_state["paco2"] > 45:
        alerts.append(
            f"⚠ Hypercapnia (PaCO₂ = {patient_state['paco2']:.1f} mmHg)"
        )

    if driving_pressure > 15:
        alerts.append(
            f"⚠ High Driving Pressure ({driving_pressure:.1f} cmH₂O)"
        )

    alerts_panel = html.Div(
        [
            html.H3("Clinical Alerts"),
            html.Hr(),
            *[
                html.Div(
                    alert,
                    style={
                        "fontSize": "20px",
                        "marginBottom": "6px",
                    },
                )
                for alert in alerts
            ]
        ]
    )


    # ==========================================
    # OBJECTIVE 4A
    # REALISTIC PRESSURE CONTROL WAVEFORM
    # ==========================================

    time = np.linspace(
        0,
        12,
        600
    )

    cycle_duration = (
        60 / ventilator.respiratory_rate
    )

    inspiration_time = (
        ventilator.inspiration_time_sec
    )

    peep_level = (
        ventilator.peep
    )

    pip_level = (
        ventilator.peep
        + (
            ventilator.tidal_volume_target_ml
            / max(
                lung_mechanics.compliance_ml_per_cmh2o,
                1,
            )
        )
    )

    waveform = []

    tau = max(
        lung_mechanics.compliance_ml_per_cmh2o
        * 0.03,
        0.15,
    )

    for t in time:

        cycle_time = (
            t % cycle_duration
        )

        if cycle_time <= inspiration_time:

            rise_time = (
                inspiration_time * 0.25
            )

            # Smooth pressure rise
            if cycle_time <= rise_time:

                pressure = (
                    peep_level
                    +
                    (
                        pip_level
                        - peep_level
                    )
                    *
                    (
                        1
                        -
                        np.exp(
                            -4
                            * cycle_time
                            / max(
                                rise_time,
                                0.01
                            )
                        )
                    )
                )

            # Plateau phase
            else:

                plateau_fraction = (
                    cycle_time
                    - rise_time
                ) / max(
                    inspiration_time
                    - rise_time,
                    0.01
                )

                pressure = (
    pip_level
    -
    (
        0.4
        * plateau_fraction
    )
)

        else:

            exp_time = (
                cycle_time
                - inspiration_time
            )

            pressure = (
                peep_level
                +
                (
                    pip_level
                    - peep_level
                )
                *
                np.exp(
                    -exp_time
                    / tau
                )
            )

        waveform.append(
            pressure
        )

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=time,
            y=waveform,
            mode="lines",
            line=dict(
                width=3
            ),
            name="Airway Pressure",
        )
    )

    figure.update_layout(
        template="plotly_dark",
        title="Realistic Pressure-Controlled Ventilator Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Pressure (cmH₂O)",
        height=450,
        yaxis=dict(
            range=[
                peep_level - 2,
                pip_level + 5,
            ]
        ),
    )

    if "Mild" in severity_text:

        severity_display = "🟢 Mild ARDS"

    elif "Moderate" in severity_text:

        severity_display = "🟠 Moderate ARDS"

    else:

        severity_display = "🔴 Severe ARDS"

    status_text = (
        f"🟢 System Online | "
        f"Mode: {mode.title()} | "
        f"Severity: {severity_display}"
    )

    accuracy = f"{patient_state['spo2'] * 100:.1f}%"

    reliability = "99.1%"

    alarm_time = "1.2 s"

    stability = "96.8%"

    return (
            spo2,
            pao2,
            paco2,
            pressure,

            pf_ratio_text,
            compliance_text,
            driving_text,
            severity_text,

            status_text,

            alerts_panel,

            accuracy,
            reliability,
            alarm_time,
            stability,

            figure,
        )