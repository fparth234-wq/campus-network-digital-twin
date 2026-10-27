from flask import Flask, render_template, jsonify, request
import torch
import os
import random
from models.hybrid_predictor import HybridSpatioTemporalPredictor

app = Flask(__name__)

DATASET_PATH = "data/campus_dataset.pt"
network_data = None
model = None

def init_system():
    global network_data, model
    if os.path.exists(DATASET_PATH):
        network_data = torch.load(DATASET_PATH, weights_only=False)
        num_raw_features = network_data.x.size(2)
        model = HybridSpatioTemporalPredictor(num_raw_features=num_raw_features, num_classes=6)
        model.eval()

init_system()

WARD_MAPPING = {
    0: "datacenter", 1: "datacenter",
    2: "er", 3: "icu", 4: "radiology", 5: "outpatient", 6: "surgical", 7: "admin"
}

WARD_NAMES = {
    "datacenter": "Main Datacenter",
    "er": "Emergency Department",
    "icu": "Intensive Care Unit",
    "radiology": "Radiology & Imaging",
    "outpatient": "Outpatient Clinic",
    "surgical": "Surgical Wing",
    "admin": "Admin & Billing"
}

FAULT_DETAILS = {
    1: {
        "name": "Uplink Congestion", 
        "desc": "Bandwidth saturation detected on switch uplink. Clinical applications may experience latency.", 
        "fix": "Recommended Action: Deploy traffic shaping. Reroute non-clinical data to backup route to relieve pressure."
    },
    2: {
        "name": "Hardware Degradation", 
        "desc": "High packet drop rate and CRC errors detected on switch port.", 
        "fix": "Recommended Action: Administratively shut down degraded port and shift sessions to redundant path."
    },
    3: {
        "name": "Broadcast Storm", 
        "desc": "Spanning-Tree Protocol failure detected causing a broadcast storm.", 
        "fix": "Recommended Action: Implement MAC-level port isolation to block rogue traffic."
    }
}

# State tracking
# Default injected faults: 5: Congestion, 15: Hardware, 22: Broadcast Storm
active_injections = {5: 1, 15: 2, 22: 3}
remediated_nodes = set()

def get_node_role(node_id):
    if node_id < 2:
        return "Core Router"
    elif node_id < 8:
        return "Distribution Switch"
    return "Access Switch"

def get_node_ward(node_id):
    if node_id < 2:
        return "datacenter"
    elif node_id < 8:
        return WARD_MAPPING[node_id]
    dist_parent = 2 + (node_id % 6)
    return WARD_MAPPING[dist_parent]

def get_node_neighbors(node_id):
    if network_data is None:
        return []
    edge_index = network_data.edge_index
    neighbors = set()
    for i in range(edge_index.size(1)):
        src = int(edge_index[0, i])
        tgt = int(edge_index[1, i])
        if src == node_id:
            neighbors.add(tgt)
        elif tgt == node_id:
            neighbors.add(src)
    return sorted(list(neighbors))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/network_state")
def get_network_state():
    global network_data, model, remediated_nodes, active_injections
    if network_data is None:
        return jsonify({"error": "No data"})

    edge_index = network_data.edge_index

    nodes = []
    edges = []
    
    # Compound nodes for ward grouping
    for ward_id, ward_name in WARD_NAMES.items():
        nodes.append({"data": {"id": ward_id, "label": ward_name, "is_ward": True}})

    # Topology edges
    for i in range(edge_index.size(1)):
        source = int(edge_index[0, i])
        target = int(edge_index[1, i])
        if source < target:
            edges.append({"data": {"id": f"e{source}-{target}", "source": str(source), "target": str(target)}})

    faults_detected = []
    
    for i in range(network_data.num_nodes):
        role = get_node_role(i)
        parent_ward = get_node_ward(i)
        
        is_remediated = i in remediated_nodes
        fault_id = active_injections.get(i, 0)

        if is_remediated or fault_id == 0:
            status = "Nominal"
            color = "#198754" # Bootstrap Success Green
            border = "#146c43"
            utilization = random.uniform(15.0, 30.0)
        else:
            status = FAULT_DETAILS.get(fault_id, {}).get("name", "Unknown Anomaly")
            color = "#dc3545" # Bootstrap Danger Red
            border = "#b02a37"
            utilization = random.uniform(88.0, 99.0)
            faults_detected.append({
                "node_id": i,
                "role": role,
                "location": WARD_NAMES[parent_ward],
                "fault": status,
                "fault_id": fault_id,
                "description": FAULT_DETAILS[fault_id]["desc"],
                "suggested_fix": FAULT_DETAILS[fault_id]["fix"]
            })

        nodes.append({
            "data": {
                "id": str(i),
                "parent": parent_ward,
                "label": f"Node {i}\n{utilization:.1f}%",
                "role": role,
                "status": status,
                "color": color,
                "border": border
            }
        })

    faults_detected.sort(key=lambda x: x["node_id"])

    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "faults": faults_detected,
        "metrics": {
            "total_nodes": network_data.num_nodes,
            "active_faults": len(faults_detected),
            "remediated": len(remediated_nodes)
        }
    })

@app.route("/api/node_metrics/<int:node_id>")
def get_node_metrics(node_id):
    global network_data, active_injections, remediated_nodes
    if network_data is None or node_id >= network_data.num_nodes:
        return jsonify({"error": "Invalid node ID"}), 404

    role = get_node_role(node_id)
    parent_ward = get_node_ward(node_id)
    neighbors = get_node_neighbors(node_id)
    
    is_remediated = node_id in remediated_nodes
    fault_id = active_injections.get(node_id, 0)
    
    # 15 time steps: T-14 to T-0
    time_labels = [f"T-{14 - i}" if i < 14 else "Now" for i in range(15)]
    
    if not is_remediated and fault_id != 0:
        status = FAULT_DETAILS[fault_id]["name"]
        if fault_id == 1: # Congestion: load & queue ramps up
            utilization = [round(x, 1) for x in torch.linspace(45, 98.5, 15).tolist()]
            queue_depth = [round(x, 1) for x in torch.linspace(20, 94.0, 15).tolist()]
            drop_rate = [round(random.uniform(0, 2), 1) if i < 10 else round(random.uniform(15, 45), 1) for i in range(15)]
            errors = [0] * 12 + [1, 2, 3]
        elif fault_id == 2: # Hardware degradation: CRC errors & drops climb
            utilization = [round(random.uniform(25, 45), 1) for _ in range(15)]
            queue_depth = [round(random.uniform(15, 30), 1) for _ in range(15)]
            drop_rate = [round(x, 1) for x in torch.linspace(1, 85, 15).tolist()]
            errors = [int(x) for x in torch.linspace(0, 48, 15).tolist()]
        else: # Broadcast storm: utilization pinned at max, massive drops
            utilization = [round(random.uniform(96, 99.8), 1) for _ in range(15)]
            queue_depth = [round(random.uniform(85, 98), 1) for _ in range(15)]
            drop_rate = [round(x, 1) for x in torch.linspace(10, 120, 15).tolist()]
            errors = [round(random.uniform(5, 15), 1) for _ in range(15)]
    else:
        status = "Nominal"
        utilization = [round(random.uniform(18, 28), 1) for _ in range(15)]
        queue_depth = [round(random.uniform(5, 18), 1) for _ in range(15)]
        drop_rate = [0.0] * 15
        errors = [0] * 15

    return jsonify({
        "node_id": node_id,
        "role": role,
        "location": WARD_NAMES[parent_ward],
        "status": status,
        "is_faulty": (not is_remediated and fault_id != 0),
        "fault_id": fault_id if (not is_remediated) else 0,
        "suggested_fix": FAULT_DETAILS.get(fault_id, {}).get("fix", "") if (not is_remediated and fault_id != 0) else "",
        "neighbors": neighbors,
        "time_labels": time_labels,
        "utilization": utilization,
        "queue_depth": queue_depth,
        "drop_rate": drop_rate,
        "errors": errors
    })

@app.route("/api/inject_fault", methods=["POST"])
def inject_fault():
    global active_injections, remediated_nodes
    data = request.json or {}
    node_id = int(data.get("node_id", 0))
    fault_type = int(data.get("fault_type", 1))

    # Clear from remediated if it was fixed earlier
    if node_id in remediated_nodes:
        remediated_nodes.remove(node_id)

    if fault_type in FAULT_DETAILS:
        active_injections[node_id] = fault_type
        fault_name = FAULT_DETAILS[fault_type]["name"]
        return jsonify({"success": True, "message": f"Injected {fault_name} into Node {node_id}."})
    else:
        # 0 or invalid means reset to nominal
        active_injections.pop(node_id, None)
        remediated_nodes.add(node_id)
        return jsonify({"success": True, "message": f"Node {node_id} set to Nominal."})

@app.route("/api/reset_network", methods=["POST"])
def reset_network():
    global active_injections, remediated_nodes
    active_injections = {5: 1, 15: 2, 22: 3}
    remediated_nodes.clear()
    return jsonify({"success": True, "message": "Network reset to baseline simulation state."})

@app.route("/api/remediate", methods=["POST"])
def remediate():
    data = request.json or {}
    node_id = int(data.get("node_id", 0))
    remediated_nodes.add(node_id)
    active_injections.pop(node_id, None)
    return jsonify({"success": True, "message": f"Fix applied successfully on Node {node_id}."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
