# AI-Based Digital Twin for Campus Network Failure Prediction

This project implements a closed-loop **Network Digital Twin (NDT)** architecture designed for autonomous failure prediction and recovery in heterogeneous campus networks.

## Architecture

The system is composed of four main layers:

### 1. Layer 1 — Telemetry Ingestion (`telemetry/`)
Collects and normalizes raw telemetry (SNMP, NetFlow, sFlow) from physical or emulated devices into a standard JSON-LD schema (`telemetry_schema.py`). 

### 2. Layer 2 — Semantic Digital Twin Engine (`neo4j_sync/`)
Maintains a millisecond-granularity property graph representation of the network state using Neo4j. The `neo4j_client.py` ingests JSON-LD telemetry events and executes real-time Cypher updates to maintain device nodes, interface nodes, and linking edges weighted by utilization and drop rates.

### 3. Layer 3 — AI Predictive & Diagnostic Core (`models/`)
A hybrid Spatio-Temporal AI model for multi-class failure prediction.
- **FTS-LSTM (`fts_lstm.py`)**: Fast Time-Series LSTM that operates per-node to produce a temporal embedding from sliding windows of telemetry metrics.
- **MPNN (`mpnn.py`)**: Graph Message-Passing Neural Network that propagates temporal embeddings across topological neighborhoods (from Layer 2) to capture failure propagation patterns.
- **Hybrid Predictor (`hybrid_predictor.py`)**: Fuses the temporal and spatial embeddings and classifies the network state using a `FocalLoss` (`losses.py`) to address severe class imbalance (healthy vs. failing).

### 4. Layer 4 — Orchestration & Autonomous Recovery (`sdn_controller/`)
After an AI prediction is made and passes a 'what-if' sandbox validation (e.g., using NS-3/GNS3), the `sdn_remediation_controller.py` compiles candidate remediation actions (REROUTE, THROTTLE, ISOLATE) into SDN policies and pushes them to an OpenDaylight or ONOS controller.

## Setup and Installation

1. **Python Environment**
Ensure you have Python 3.10+ installed. A virtual environment has been created.
Activate the virtual environment:
- On Windows: `.\venv\Scripts\activate`
- On Linux/Mac: `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```
This installs `torch`, `torch_geometric`, `neo4j`, and `requests`.

2. **Neo4j Database**
Set up a Neo4j instance. The `Neo4jTwinSynchronizer` relies on the bolt connection to execute Cypher queries. Modify the connection string, username, and password in `neo4j_sync/neo4j_client.py`.

3. **SDN Controller**
Set up an ONOS or OpenDaylight controller. Update `base_url` and `auth` credentials inside `sdn_controller/sdn_remediation_controller.py`.

## Running the Application

To run or test individual modules, activate the virtual environment and execute the Python scripts from within the `cn` project folder.

### Running the Telemetry to Neo4j Synchronization
This script demonstrates how an incoming normalized JSON-LD telemetry event is ingested into the Neo4j graph database. Note: You need a running Neo4j instance for this to work.
```bash
python neo4j_sync/neo4j_client.py
```

### Running the SDN Remediation Controller
This script acts upon the prediction after sandbox validation by pushing policies to the SDN controller. Note: You need a running SDN controller for this to work.
```bash
python sdn_controller/sdn_remediation_controller.py
```

## Directory Structure

```
cn/
¦
+-- models/                     # AI Predictive Core (PyTorch)
¦   +-- fts_lstm.py
¦   +-- hybrid_predictor.py
¦   +-- losses.py
¦   +-- mpnn.py
¦
+-- neo4j_sync/                 # Neo4j Synchronization
¦   +-- neo4j_client.py
¦
+-- sdn_controller/             # Automated Recovery Scripts
¦   +-- sdn_remediation_controller.py
¦
+-- telemetry/                  # Telemetry Normalization
¦   +-- telemetry_schema.py
¦
+-- requirements.txt            # Python Dependencies
+-- README.md                   # Project Documentation
```
