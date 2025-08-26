# HIDE - Hidden Dynamics Engine

**HIDE** is a domain-agnostic, strategy-driven framework for detecting hidden, anomalous behaviors in complex systems. It leverages a modular architecture to apply specialized, state-of-the-art machine learning models to different problem domains, all orchestrated through simple configuration files.

This project demonstrates a professional-grade AI/ML workflow, separating model training from prediction and packaging the application for reproducible, cross-platform execution.

---

## Table of Contents

1.  [Architectural Vision](#architectural-vision)
2.  [Implemented Domain Strategies](#implemented-domain-strategies)
3.  [Project Structure](#project-structure)
4.  [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Data Setup](#data-setup)
5.  [How to Run (Local Execution)](#how-to-run-local-execution)
    -   [Step 1: Setup Virtual Environment](#step-1-setup-virtual-environment)
    -   [Step 2: Install Dependencies](#step-2-install-dependencies)
    -   [Step 3: Train a Model](#step-3-train-a-model)
    -   [Step 4: Run Prediction](#step-4-run-prediction)
6.  [How to Run (Docker Execution)](#how-to-run-docker-execution)
    -   [Step 1: Build the Docker Image](#step-1-build-the-docker-image)
    -   [Step 2: Run Training or Prediction via Docker](#step-2-run-training-or-prediction-via-docker)

---

## Architectural Vision

The HIDE framework is built on a **Strategy Pattern**. The core pipeline is a lightweight, domain-agnostic orchestrator. All complex, domain-specific logic is encapsulated within self-contained "strategy" modules. This design provides maximum flexibility and scalability.

-   **Core Engine (`src/hide/core/`):** A generic system that handles loading configurations, routing data, and executing the main pipeline steps. It knows *what* to do, but not *how*.
-   **Strategies (`src/hide/strategies/`):** These modules define *how* to analyze a specific domain. Each strategy implements a complete workflow: custom feature engineering, execution of a specialized ML model, and generation of human-readable explanations.
-   **Configuration (`adapters/`):** Simple YAML files define the parameters for each domain, allowing users to control the analysis without changing any Python code.
-   **Train/Predict Separation:** The framework follows a professional MLOps workflow.
    -   `train.py`: An offline script to train a model for a specific domain and save the resulting artifact (e.g., a `.joblib` or `.pth` file) to the `/models` directory.
    -   `score.py`: A script designed for on-demand prediction. It loads a pre-trained model and scores new, unseen data, simulating a production API endpoint.

---

## Implemented Domain Strategies

HIDE comes with four fully implemented, advanced strategies:

### 1. Dark Pools: Unsupervised Learning + SHAP
-   **Objective:** Identify anomalous trading venues from aggregate FINRA ATS data.
-   **Model:** An **Isolation Forest** is used to detect statistical outliers in a multi-dimensional feature space (`total_shares`, `avg_trade_size`, `hybrid_score`).
-   **Explainability:** **SHAP (SHapley Additive exPlanations)** is used to explain *why* a venue was flagged, identifying the specific feature that contributed most to its anomaly score.

### 2. Energy Theft: Time-Series Analysis with FFT
-   **Objective:** Detect anomalous household power consumption patterns indicative of non-technical loss.
-   **Model:** A **Fast Fourier Transform (FFT)** based anomaly detector. It learns the dominant periodic (seasonal, daily) patterns in the energy signal and flags days where the consumption deviates significantly from this learned "normal rhythm."

### 3. Blockchain AML: Graph Neural Network (GraphSAGE)
-   **Objective:** Classify "unknown" transactions in the Elliptic Bitcoin dataset as potentially illicit.
-   **Model:** A **GraphSAGE (Graph Sample and Aggregate)** network, a type of Graph Neural Network (GNN). It learns features from a transaction's local neighborhood in the graph to predict its class, effectively learning the patterns of illicit fund flows.

### 4. Supply Chain: Sequential Anomaly Detection with LSTM
-   **Objective:** Identify "ghost" or anomalous shipping carriers from real-world freight data.
-   **Model:** A **Recurrent Neural Network (RNN) based LSTM Autoencoder**. It treats each carrier's monthly shipping history as a sequence. The model learns the patterns of normal logistical behavior, and carriers whose historical sequences cannot be accurately reconstructed are flagged as anomalies.

---

## Project Directory

/hide_framework/
|
|-- adapters/                 # Domain configuration files (YAMLs)
|   |-- dark_pools.yaml
|   |-- energy_theft.yaml
|   |-- blockchain_aml.yaml
|   `-- supply_chain.yaml
|
|-- data/                     # Local datasets (as fallbacks or primary sources)
|   |-- finra_quarterly/
|   |   `-- (FINRA .xlsx files go here)
|   |-- energy/
|   |   `-- household_power_consumption.txt
|   `-- elliptic/
|       |-- elliptic_txs_classes.csv
|       |-- elliptic_txs_edgelist.csv
|       `-- elliptic_txs_features.csv
|
|-- models/                   # OUTPUT: Saved/trained model artifacts (.joblib, .pth)
|
|-- notebooks/                # For exploratory data analysis and research
|
|-- reports/                  # OUTPUT: Generated HTML reports
|
|-- src/
|   `-- hide/
|       |-- \__init__.py
|       |
|       |-- core/             # Core, domain-agnostic framework components
|       |   |-- __init__.py
|       |   |-- adapters.py   # Loads YAML configs
|       |   |-- ingestion.py  # Master data ingestion router
|       |   |-- pipeline.py   # Generic, strategy-driven pipeline orchestrator
|       |   `-- reporting.py  # Generic HTML report generator
|       |
|       `-- strategies/       # All domain-specific logic is encapsulated here
|           |-- __init__.py
|           |-- base_strategy.py  # The "interface" for all strategies
|           |
|           |-- dark_pools/
|           |   |-- __init__.py
|           |   `-- strategy.py   # Implements Unsupervised model + SHAP
|           |
|           |-- energy_theft/
|           |   |-- __init__.py
|           |   `-- strategy.py   # Implements FFT time-series analysis
|           |
|           |-- blockchain_aml/
|           |   |-- __init__.py
|           |   `-- strategy.py   # Implements GraphSAGE GNN model
|           |
|           `-- supply_chain/
|               |-- __init__.py
|               `-- strategy.py   # Implements LSTM Autoencoder model
|
|-- tests/                    # Unit and integration tests
|
|-- README.md                 # The main project documentation
|-- requirements.txt          # All Python package dependencies
|-- Dockerfile                # For creating a reproducible containerized environment
|-- train.py                  # **NEW:** Command-line script to train models
`-- score.py                  # **NEW:** Command-line script to run predictions

---

## Getting Started

### Prerequisites

-   Python 3.9+
-   Docker (Recommended for easiest setup)

### Data Setup

-   **Dark Pools:** Place your `finra-ats-*-nms.xlsx` files inside a `data/finra_quarterly/` folder.
-   **Energy Theft:** The framework will attempt to download this data automatically. As a fallback, place `household_power_consumption.txt` inside `data/energy/`.
-   **Blockchain AML:** **Manual download required.**
    1.  Download from [Kaggle: Elliptic Data Set](https://www.kaggle.com/datasets/ellipticco/elliptic-data-set).
    2.  Create a folder: `data/elliptic/`.
    3.  Place the three CSV files inside it.
-   **Supply Chain:** The framework will attempt to download this data automatically. As a fallback, place `Port_Freight_Profiles.csv` inside `data/supply_chain/`.

---

## How to Run (Local Execution)

### Step 1: Setup Virtual Environment

```powershell
# Create the environment
python -m venv venv
# Activate it (Windows)
.\venv\Scripts\Activate.ps1
# On macOS/Linux: source venv/bin/activate
