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
