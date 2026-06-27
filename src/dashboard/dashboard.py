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
# ==================================================
# CLINICAL ALERT MODEL
# ==================================================

class ClinicalAlert:

    def __init__(
        self,
        severity,
        title,
        value,
        explanation,
        recommendation,
        color,
        icon,
    ):

        self.severity = severity

        self.title = title

        self.value = value

        self.explanation = explanation

        self.recommendation = recommendation

        self.color = color

        self.icon = icon

def metric_card(title, card_id, color):
    return html.Div(
        style={
            "backgroundColor": "#f8fafc",
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
# ALERT CARD RENDERER
# ==================================================

def render_alert(alert):

    return html.Div(

        style={
            "backgroundColor": alert.color,
            "padding": "15px",
            "borderRadius": "12px",
            "marginBottom": "10px",
        },

        children=[

            html.H4(
                f"{alert.icon} {alert.title}",
                style={
                    "marginBottom": "8px",
                },
            ),

            html.Div(
                alert.value,
                style={
                    "fontWeight": "bold",
                    "fontSize": "18px",
                    "marginBottom": "8px",
                },
            ),

            html.P(
                alert.explanation
            ),

            html.Div(
                f"Recommendation: {alert.recommendation}",
                style={
                    "fontWeight": "bold",
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
        "ARDS Supportive Management Simulator",
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

html.Div(
    [
        html.Span("FiO₂"),

        html.Span(
            id="fio2-display",
            children="0.60",
            style={
                "float": "right",
                "backgroundColor": "#ffffff",
                "color": "#16a34a",
                "padding": "4px 12px",
                "borderRadius": "8px",
                "fontWeight": "bold",
                "fontSize": "18px",
                "minWidth": "70px",
                "textAlign": "center",
                "display": "inline-block",
            },
        ),
    ]
),

dcc.Slider(
    id="fio2-slider",
    min=0.21,
    max=1.00,
    step=0.01,
    value=0.60,
  marks={
    0.21: {
        "label": "0.21",
        "style": {"color": "#f8fafc", "fontWeight": "bold"},
    },
    0.40: {
        "label": "0.40",
        "style": {"color": "#f8fafc", "fontWeight": "bold"},
    },
    0.60: {
        "label": "0.60",
        "style": {"color": "#f8fafc", "fontWeight": "bold"},
    },
    0.80: {
        "label": "0.80",
        "style": {"color": "#f8fafc", "fontWeight": "bold"},
    },
    1.00: {
        "label": "1.00",
        "style": {"color": "#f8fafc", "fontWeight": "bold"},
    },
}
),
html.Br(),

html.Div(
    [
        html.Span("PEEP (cmH₂O)"),

        html.Span(
            id="peep-display",
            children="10",
            style={
                "backgroundColor": "#ffffff",
                "color": "#3b82f6",
                "padding": "4px 12px",
                "borderRadius": "8px",
                "fontWeight": "bold",
                "fontSize": "18px",
                "minWidth": "70px",
                "textAlign": "center",
            },
        ),
    ],
    style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
    },
),

dcc.Slider(
    id="peep-slider",
    min=5,
    max=20,
    step=1,
    value=10,
),

html.Br(),

html.Div(
    [
        html.Span("Tidal Volume (mL)"),

        html.Span(
            id="tv-display",
            children="420",
            style={
                "backgroundColor": "#ffffff",
                "color": "#f59e0b",
                "padding": "4px 12px",
                "borderRadius": "8px",
                "fontWeight": "bold",
                "fontSize": "18px",
                "minWidth": "70px",
                "textAlign": "center",
            },
        ),
    ],
    style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
    },
),

dcc.Slider(
    id="tv-slider",
    min=250,
    max=700,
    step=10,
    value=420,
),

html.Br(),

html.Div(
    [
        html.Span("Plateau Pressure (cmH₂O)"),

        html.Span(
            id="plateau-display",
            children="25",
            style={
                "float": "right",
                "backgroundColor": "#ffffff",
                "color": "#ef4444",
                "padding": "4px 12px",
                "borderRadius": "8px",
                "fontWeight": "bold",
                "fontSize": "18px",
                "minWidth": "70px",
                "textAlign": "center",
                "display": "inline-block",
            },
        ),
    ]
),

dcc.Slider(
    id="plateau-slider",
    min=10,
    max=40,
    step=1,
    value=25,
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
                        "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))",
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
        # ==========================================
        # REMOTE ICU SESSION
        # ==========================================

        html.Div(
            style={
                "backgroundColor": "#1e293b",
                "padding": "20px",
                "borderRadius": "16px",
                "marginBottom": "20px",
            },
            children=[

                html.H2("Remote ICU Session"),

                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns":
                            "repeat(auto-fit, minmax(220px, 1fr))",
                        "gap": "20px",
                    },
                    children=[

                        metric_card(
                            "Session ID",
                            "session-card",
                            "#22c55e",
                        ),

                        metric_card(
                            "Connected Users",
                            "users-card",
                            "#3b82f6",
                        ),

                        metric_card(
                            "Last Sync Time",
                            "sync-card",
                            "#f59e0b",
                        ),

                        metric_card(
                            "Network Status",
                            "network-card",
                            "#a855f7",
                        ),

                        metric_card(
                            "Monitoring Status",
                            "monitor-card",
                            "#06b6d4",
                        ),

                        metric_card(
                            "Hospital Node",
                            "hospital-card",
                            "#e11d48",
                        ),
                    ],
                ),
            ],
        ),
# ==========================================
# OBJECTIVE 4B
# FLOW-TIME WAVEFORM
# ==========================================

dcc.Graph(
    id="flow-waveform"
),

# ==========================================
# OBJECTIVE 4C
# VOLUME-TIME WAVEFORM
# ==========================================

dcc.Graph(
    id="volume-waveform"
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
Output("session-card", "children"),
Output("users-card", "children"),
Output("sync-card", "children"),
Output("network-card", "children"),
Output("monitor-card", "children"),
Output("hospital-card", "children"),

Output("fio2-display", "children"),
Output("peep-display", "children"),
Output("tv-display", "children"),
Output("plateau-display", "children"),

Output("pressure-waveform", "figure"),
    Output("flow-waveform", "figure"),
    Output("volume-waveform", "figure"),
    ],
   [
    Input("interval-component", "n_intervals"),
    Input("profile-selector", "value"),
    Input("mode-selector", "value"),
    Input("fio2-slider", "value"),
    Input("peep-slider", "value"),

    Input("tv-slider", "value"),
    Input("plateau-slider", "value"),
],
)
def update_dashboard(
    n,
    profile,
    mode,
    fio2,
    peep,
    tidal_volume,
    plateau_pressure,
):

    # Apply settings

    ards_model.severity = profile

    gas_exchange.fio2 = fio2

    lung_mechanics.peep = peep
    ventilator.peep = peep

    ventilator.tidal_volume_target_ml = (
        tidal_volume
    )

    # Remove this for now
    # patient_state["plateau_pressure"] = (
    #     plateau_pressure
    # )

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

    base_paco2 = row["paco2"]
# Ventilation effect

    tv_effect = (
    (420 - tidal_volume) / 10
)
    patient_state["paco2"] = max(
    25,
    base_paco2 + tv_effect
)
    patient_state["spo2"] = (
        row["spo2"] / 100
    )
    print(
    f"BASE={base_paco2} "
    f"TV={tidal_volume} "
    f"EFFECT={tv_effect} "
    f"PACO2={patient_state['paco2']}"
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

    driving_pressure = plateau_pressure - peep

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

            ClinicalAlert(

                severity="warning",
                title="Hypercapnia",
                value=f"PaCO₂ = {patient_state['paco2']:.1f} mmHg",
                explanation="Carbon dioxide retention detected.",
                recommendation="Review respiratory rate and minute ventilation.",
                color="#92400e",
                icon="⚠",
            )
        )
    print("CURRENT DRIVING PRESSURE =", driving_pressure)
    if driving_pressure > 15:

     alerts.append(

        ClinicalAlert(

            severity="warning",

            title="High Driving Pressure",

            value=f"{driving_pressure:.1f} cmH₂O",

            explanation=(
                "Driving pressure exceeds the "
                "recommended lung-protective threshold."
            ),

            recommendation=(
                "Reduce tidal volume or improve "
                "lung recruitment."
            ),

            color="#7c2d12",

            icon="⚠",
        )
    )
    alerts_panel = html.Div(
    [
        html.H3("Clinical Alerts"),
        html.Hr(),

        *[
            render_alert(alert)
            if isinstance(alert, ClinicalAlert)
            else html.Div(
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
    # ==========================================
    # OBJECTIVE 4B
    # FLOW-TIME WAVEFORM
    # ==========================================

    flow_waveform = []

    peak_insp_flow = 0.8
    peak_exp_flow = -1.0

    for t in time:

        cycle_time = t % cycle_duration

        if cycle_time <= inspiration_time:

            flow = (
                peak_insp_flow
                * np.exp(
                    -2 * cycle_time
                    / max(inspiration_time, 0.1)
                )
            )

        else:

            exp_time = (
                cycle_time
                - inspiration_time
            )

            flow = (
                peak_exp_flow
                * np.exp(
                    -exp_time
                    / tau
                )
            )

        flow_waveform.append(flow)

    flow_figure = go.Figure()

    flow_figure.add_trace(
        go.Scatter(
            x=time,
            y=flow_waveform,
            mode="lines",
            line=dict(width=3),
            name="Airway Flow",
        )
    )

    flow_figure.update_layout(
        template="plotly_dark",
        title="Flow-Time Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Flow (L/s)",
        height=450,
    )
        # ==========================================
    # OBJECTIVE 4C
    # VOLUME-TIME WAVEFORM
    # ==========================================

    volume_waveform = []

    tidal_volume_l = (
        ventilator.tidal_volume_target_ml
        / 1000
    )

    for t in time:

        cycle_time = (
            t % cycle_duration
        )

        if cycle_time <= inspiration_time:

            volume = (
                tidal_volume_l
                * (
                    cycle_time
                    / inspiration_time
                )
            )

        else:

            exp_fraction = (
                cycle_time
                - inspiration_time
            ) / max(
                cycle_duration
                - inspiration_time,
                0.01,
            )

            volume = (
                tidal_volume_l
                * np.exp(
                    -4 * exp_fraction
                )
            )

        volume_waveform.append(volume)

    volume_figure = go.Figure()

    volume_figure.add_trace(
        go.Scatter(
            x=time,
            y=volume_waveform,
            mode="lines",
            line=dict(width=3),
            name="Volume",
        )
    )

    volume_figure.update_layout(
        template="plotly_dark",
        title="Volume-Time Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Volume (L)",
        height=450,
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
    session_id = "ICU-001"

    connected_users = "3"

    last_sync = f"{n}s"

    network_status = "Online"

    monitoring_status = "Active"

    hospital_node = "FTH Gombe"

    fio2_display = f"{fio2:.2f}"
    peep_display = f"{peep}"
    tv_display = f"{tidal_volume}"
    plateau_display = f"{plateau_pressure}"

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
session_id,
connected_users,
last_sync,
network_status,
monitoring_status,
hospital_node,

fio2_display,
peep_display,
tv_display,
plateau_display,

figure,
flow_figure,
volume_figure,
)