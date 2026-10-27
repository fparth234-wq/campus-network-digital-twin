# Single Physical Building Network & Digital Twin Map

This map illustrates how the physical network hardware within a **single physical building** connects to the 4-layer AI Digital Twin architecture.

```mermaid
flowchart TB
    %% Styling
    classDef physical fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef virtual fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef ai fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef sdn fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000

    subgraph PhysicalBuilding [🏢 1 Physical Building]
        direction TB
        
        subgraph ServerRoom [Basement: Main Server Room]
            Core1[Core Switch 1]:::physical
            Core2[Core Switch 2]:::physical
            Core1 --- Core
        end

        subgraph Floor1 [Floor 1: Admin & Distribution]
            Dist1[Distribution Switch 1]:::physical
            Dist2[Distribution Switch 2]:::physical
            Core1 --- Dist1
            Core2 --- Dist2
        end

        subgraph Floor2 [Floor 2: Classrooms (Access Layer)]
            Acc1[Access Switch 1]:::physical
            AP1((Wi-Fi AP)):::physical
            IoT1[[Smart Thermostat]]:::physical
            Dist1 --- Acc1
            Acc1 --- AP1
            Acc1 --- IoT1
        end

        subgraph Floor3 [Floor 3: Labs (Access Layer)]
            Acc2[Access Switch 2]:::physical
            PC1[Lab Workstations]:::physical
            Dist2 --- Acc2
            Acc2 --- PC1
        end
    end

    subgraph DigitalTwin [☁️ Digital Twin Ecosystem]
        direction TB
        
        L1[Layer 1: Telemetry Ingestion\nKafka / Logstash]:::virtual
        L2[(Layer 2: Neo4j Graph Twin\nReal-time Network State)]:::virtual
        L3{{Layer 3: AI Predictive Core\nFTS-LSTM + MPNN}}:::ai
        L4[Layer 4: SDN Controller\nONOS / OpenDaylight]:::sdn
        Sandbox[NS-3 / GNS3\nValidation Sandbox]:::virtual

        L1 == JSON-LD ==> L2
        L2 == Graph Topology\n& Metrics ==> L3
        L3 == "Predicts: Congestion on Floor 2" ==> Sandbox
        Sandbox == "Validation Passed" ==> L4
    end

    %% Connections between Physical and Virtual
    Acc1 -. "SNMP / NetFlow" .-> L1
    Acc2 -. "SNMP / NetFlow" .-> L1
    Core1 -. "sFlow / CPU Metrics" .-> L1
    
    %% Remediation Action
    L4 -. "OpenFlow Policy (e.g. Reroute/Throttle)" .-> Dist1
    L4 -. "Isolate Port" .-> Acc1

```

### How to Read This Map:
1. **Upward Data Flow (Observation)**: The physical switches and routers on the various floors continuously stream telemetry data (SNMP, NetFlow, drop rates) up to **Layer 1** of the Digital Twin.
2. **Virtualization & Prediction**: The telemetry is injected into the **Neo4j Graph (Layer 2)**, creating a live virtual replica of the building. The **AI Core (Layer 3)** continuously analyzes this graph. If a classroom on Floor 2 starts causing a broadcast storm, the AI detects the pattern.
3. **Downward Control Flow (Action)**: The AI proposes a fix, tests it in the **Sandbox**, and sends it to the **SDN Controller (Layer 4)**. The SDN controller then shoots a command directly down to the Floor 1 Distribution switch to throttle or reroute the traffic, saving the network before humans even notice the issue!
