# AI-Based Digital Twin for Campus Network Failure Prediction and Autonomous Recovery

This implementation plan outlines the steps to build and deploy a closed-loop Network Digital Twin (NDT) architecture, as specified in the provided research paper. The system integrates millisecond-granularity graph synchronization, a hybrid spatio-temporal AI predictive core, a "what-if" pre-deployment emulation stage, and SDN-based autonomous recovery.

## User Review Required

- **SDN Controller Choice**: The implementation assumes ONOS or OpenDaylight. We should finalize which one to use for the initial deployment.
- **Emulation Environment**: The plan incorporates NS-3 and GNS3 for what-if simulation. We need to confirm if Mininet alone could suffice for an MVP, or if we must proceed with the full NS-3/GNS3 suite from the start.
- **Hardware/Cloud Resources**: Building the testbed requires significant resources. We need to allocate servers for the Neo4j clustered database, GPU resources for PyTorch model training/inference, and compute for the simulated networks.

## Open Questions

- What specific campus network topology should we start with for the baseline testbed?
- Are there pre-existing datasets for the initial training of the FTS-LSTM and MPNN models, or do we need to generate synthetic data from day one?
- Do we have strict compliance requirements for the federated learning setup, or can we start with a centralized training approach for the pilot?

## Proposed Implementation Phases

### Phase 1: Infrastructure and Layer 1 Setup (Telemetry Ingestion)
This phase focuses on setting up the underlying physical/emulated network and the telemetry ingestion pipelines.

1. **Deploy Testbed Environment**:
   - Set up Mininet for data-plane emulation.
   - Integrate GNS3 for device-OS-level emulation.
   - Configure the network topology: 2 core switches, 6 distribution switches, 24 access switches, and simulated endpoints (wired, wireless, IoT).
2. **Setup SDN Controller**:
   - Deploy ONOS (or OpenDaylight) controller.
   - Connect the emulated switches to the controller using OpenFlow/NETCONF.
3. **Implement Telemetry Collectors**:
   - Configure SNMP polling for interface counters, CPU, and memory metrics.
   - Enable NetFlow v9 / IPFIX on distribution and core switches.
   - Deploy sFlow samplers for high line-rate monitoring.
   - Implement collectors to aggregate these streams into a central message bus (e.g., Kafka).

### Phase 2: Layer 2 - Semantic Digital Twin Engine (Neo4j)
This phase builds the real-time graph representation of the network.

1. **Deploy Neo4j Database**:
   - Set up a Neo4j instance optimized for high-throughput write operations.
2. **Develop Telemetry Normalizer**:
   - Build a microservice to consume raw telemetry from the message bus.
   - Transform diverse formats (SNMP, NetFlow) into normalized JSON-LD events using the schema defined in the research (`@context: https://ndt.campus-net.org/schema/v1`).
3. **Implement Real-time Graph Synchronizer**:
   - Write ingestion scripts utilizing Neo4j Cypher to perform real-time `MERGE` and `SET` operations.
   - Ensure node (devices), interface, and link properties (utilization, drop rates) are updated.
   - Log immutable `TelemetryEvent` nodes for temporal replay.
   - **Optimization**: Tune database and queries to achieve the ≤ 50 ms synchronization latency bound.

### Phase 3: Layer 3 - AI Predictive & Diagnostic Core
This phase involves developing and training the hybrid Spatio-Temporal model.

1. **Develop FTS-LSTM Component**:
   - Implement the Fast Time-Series LSTM in PyTorch.
   - Train on historical telemetry to generate per-node temporal embeddings.
2. **Develop MPNN / GFT Component**:
   - Implement the Message Passing Neural Network using PyTorch Geometric (`TopoMPNNLayer`).
   - Define spectral pre-processing using Graph Fourier Transform.
3. **Build the Joint Classification Head**:
   - Combine temporal and spatial embeddings into a multi-class classifier.
   - Implement the Focal Loss function to handle class imbalance (healthy vs. various failure modes).
4. **Integration & Semi-Distributed Inference**:
   - Set up the inference pipeline to query k-hop neighborhoods directly from Neo4j.
   - Expose an API to serve predicted fault classes and confidence scores.

### Phase 4: Layer 4 - Orchestration and Autonomous Recovery
This phase closes the loop by acting on predictions after sandbox validation.

1. **Develop Intent Parser**:
   - Create a service that translates AI predictions (e.g., "link congestion") into candidate remediation intents (e.g., `REROUTE`, `THROTTLE`, `ISOLATE`).
2. **Implement "What-If" Sandbox Validation**:
   - Integrate NS-3/GNS3.
   - Write automation scripts to spin up a sandbox reflecting the *current* twin state.
   - Replay the candidate action in the sandbox and evaluate QoS/SLA feasibility (latency, throughput).
3. **Develop SDN Remediation Controller**:
   - Implement the `SDNController` Python client to interface with ONOS/OpenDaylight.
   - Connect the validation engine to the controller so that only validated actions are pushed to the live network.
   - Implement a fallback mechanism to alert operators for rejected/low-confidence actions.

## Verification Plan

### Automated Tests
- `pytest` for all Python modules (Normalizer, Model components, SDN Controller).
- Unit tests for Neo4j Cypher queries using a mock database to verify graph structure integrity.
- Automated pipeline to inject faults into Mininet and verify the end-to-end detection response time.

### Manual Verification
- Run the **Baseline** test (no NDT) vs. **Full closed-loop** test to measure MTTR reduction.
- Verify that synchronization latency remains ≤ 50ms under heavy simulated traffic load.
- Validate that the AI model correctly identifies failure modes with >99% detection accuracy on a held-out test set.
- Review Grafana dashboards for system health and ML metrics.
