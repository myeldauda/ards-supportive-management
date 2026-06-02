# ARDS Supportive Management Simulation System

## Overview

This project presents a web-based physiological simulation and monitoring framework for Acute Respiratory Distress Syndrome (ARDS) supportive management.

The system integrates mathematical modeling, ventilator-lung interaction simulation, gas exchange analysis, and real-time physiological monitoring through an interactive web dashboard.

The framework is intended for research, educational, and simulation purposes and is not designed for direct clinical use.

---

## Research Objectives

### Objective 1

Design and implement an object-oriented mathematical simulation engine that models the dynamic physiological effects of ARDS and ventilator support.

### Objective 2

Develop and integrate an interactive real-time graphical software dashboard for physiological monitoring.

### Objective 3

Simulate a web-based monitoring system for remote assessment of ventilator efficiency in ARDS supportive management.

### Objective 4

Evaluate the efficiency and accuracy of oxygen delivery systems and ICU monitoring devices used for ARDS supportive care.

---

## Features

* Object-oriented physiological simulation engine
* ARDS severity modeling
* Lung mechanics simulation
* Gas exchange modeling
* Ventilator interaction simulation
* Real-time physiological monitoring
* Dynamic pressure waveform visualization
* Browser-based dashboard
* Smartphone-compatible architecture
* Modular and extensible design

---

## Project Structure

ards_supportive_management/

├── src/

│ ├── models/

│ ├── simulation/

│ └── dashboard/

├── data/

├── outputs/

├── tests/

├── main.py

├── run_dashboard.py

├── requirements.txt

└── README.md

---

## Installation

Create a virtual environment:

python -m venv .venv

Activate the environment:

Windows PowerShell:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

---

## Running the Simulation

Run the physiological simulation engine:

python main.py

---

## Running the Dashboard

Launch the dashboard:

python run_dashboard.py

Open:

http://127.0.0.1:8050

in a web browser.

---

## Technologies Used

* Python
* Dash
* Plotly
* NumPy
* Object-Oriented Programming (OOP)

---

## Disclaimer

This software is intended solely for academic, educational, and research purposes. It must not be used for clinical diagnosis, treatment planning, or direct patient care.
