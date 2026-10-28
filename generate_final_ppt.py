import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Colors matching the template
C_DARK_BG = RGBColor(11, 25, 44)      # Deep Navy #0B192C
C_LIGHT_BG = RGBColor(248, 249, 250)  # Off White #F8F9FA
C_CARD_BG = RGBColor(255, 255, 255)   # Pure White
C_BORDER = RGBColor(222, 226, 230)    # Light Gray
C_TEXT_DARK = RGBColor(33, 37, 41)    # Dark Charcoal #212529
C_TEXT_MUTED = RGBColor(108, 117, 125)# Muted Gray #6C757D
C_BLUE = RGBColor(13, 110, 253)       # Accent Blue #0D6EFD
C_TEAL = RGBColor(20, 184, 166)       # Teal #14B8A6
C_RED = RGBColor(220, 53, 69)         # Danger Red
C_GREEN = RGBColor(25, 135, 84)       # Success Green
C_HEADER_BG = RGBColor(15, 34, 64)    # Table Header Dark Navy

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, slide_num_str):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p0 = tf.paragraphs[0]
    p0.text = "BCSE308L / BCSE308P • COMPUTER NETWORKS • FINAL COURSE PROJECT REVIEW"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_DARK
    p1.space_before = Pt(4)

    num_box = slide.shapes.add_textbox(Inches(12.0), Inches(7.0), Inches(0.8), Inches(0.3))
    np = num_box.text_frame.paragraphs[0]
    np.text = slide_num_str
    np.font.size = Pt(10)
    np.font.color.rgb = C_TEXT_MUTED
    np.alignment = PP_ALIGN.RIGHT

def create_card(slide, left, top, width, height, title, body_text_list, border_color=C_BORDER, header_color=C_BLUE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    tf.margin_bottom = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = header_color
    p.space_after = Pt(8)
    
    for item in body_text_list:
        p_item = tf.add_paragraph()
        p_item.text = item
        p_item.font.size = Pt(10.5)
        p_item.font.color.rgb = C_TEXT_DARK
        p_item.space_after = Pt(4)
    return card

def create_table(slide, left, top, width, height, headers, rows, col_widths=None):
    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    table = table_shape.table
    
    if col_widths and len(col_widths) == num_cols:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w
            
    # Headers
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.LEFT
        
    # Rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if r_idx % 2 == 1:
                cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
            else:
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            p.alignment = PP_ALIGN.LEFT

# ==========================================
# SLIDE 1: Title Slide (Updated with All 3 Students)
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, C_DARK_BG)

right_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.5), 0, Inches(4.833), prs.slide_height)
right_box.fill.solid()
right_box.fill.fore_color.rgb = RGBColor(15, 34, 64)
right_box.line.fill.background()

tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(7.5), Inches(5.8))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "BCSE308L / BCSE308P • COMPUTER NETWORKS"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_TEAL

p = tf.add_paragraph()
p.text = "FINAL COURSE\nPROJECT REVIEW"
p.font.size = Pt(34)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)
p.space_before = Pt(6)
p.space_after = Pt(14)

p = tf.add_paragraph()
p.text = "Adaptive SDN Framework and AI-Driven Digital Twin for Hospital Campus Network Failure Prediction"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = RGBColor(147, 197, 253)
p.space_after = Pt(18)

meta_items = [
    "Team Members (Sorted on Register Number):",
    "  • Kumar Aditya Raghuwanshi (24BCE0464)",
    "  • Parth Kashyap (24BCE2030)",
    "  • Prakrash Pandey (24BCE2849)",
    "",
    "Faculty Mentor: DR. YOGANAND S., Assistant Professor Senior Grade-2",
    "Centre for Artificial Intelligence and Research (CFAIR), SCOPE",
    "Review Date: October 2026"
]
for item in meta_items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(2)

# ==========================================
# SLIDE 2: Project Snapshot
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, C_LIGHT_BG)
add_header(s2, "Project snapshot", "02")

create_card(s2, Inches(0.8), Inches(1.5), Inches(3.7), Inches(2.8), "Problem", [
    "• Enterprise campus networks suffer from sudden outages caused by silent failures (uplink congestion, switch degradation, broadcast loops).",
    "• Traditional monitoring (SNMP/Syslog) is purely reactive: alarms trigger only after packet drop and clinical/academic disruptions occur.",
    "• Manual troubleshooting results in long Mean Time to Repair (MTTR > 10 mins)."
], header_color=C_RED)

create_card(s2, Inches(4.8), Inches(1.5), Inches(3.7), Inches(2.8), "Solution", [
    "• A 4-layer Closed-Loop Digital Twin integrating spatio-temporal deep learning with Software-Defined Networking (SDN).",
    "• Hybrid Predictor (FTS-LSTM + MPNN) continuously ingests 5-metric telemetry across a 30-node topology to predict failures 15-30s in advance.",
    "• Autonomous SDN remediation injects OpenFlow rules without human delay."
], header_color=C_BLUE)

create_card(s2, Inches(8.8), Inches(1.5), Inches(3.7), Inches(2.8), "Outcome", [
    "• 94.6% multi-class failure prediction accuracy achieved under extreme 98:2 class imbalance using Focal Loss (gamma=2.0).",
    "• Sub-second recovery: Automated SDN flow rerouting & port isolation executes in 320ms, cutting MTTR by ~95%.",
    "• Real-time interactive NOC web dashboard with live telemetry inspection."
], header_color=C_GREEN)

tb = s2.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(11.7), Inches(0.4))
tb.text_frame.paragraphs[0].text = "At-a-glance"
tb.text_frame.paragraphs[0].font.size = Pt(14)
tb.text_frame.paragraphs[0].font.bold = True
tb.text_frame.paragraphs[0].font.color.rgb = C_TEXT_DARK

create_card(s2, Inches(0.8), Inches(4.9), Inches(5.6), Inches(0.9), "Target Metrics", [
    "Prediction Lead Time: 15-30s | MTTR: < 500ms | F1-Score: 0.91 | Packet Loss: < 0.05%"
])
create_card(s2, Inches(6.9), Inches(4.9), Inches(5.6), Inches(0.9), "Environment", [
    "PyTorch Geometric, OpenFlow 1.3 / SDN REST, Cytoscape.js (fcose), Flask Backend"
])
create_card(s2, Inches(0.8), Inches(6.0), Inches(5.6), Inches(0.9), "Project Status", [
    "Fully Implemented, Integrated End-to-End, Validated with Live Fault Injection Testbed"
])
create_card(s2, Inches(6.9), Inches(6.0), Inches(5.6), Inches(0.9), "Key Contribution", [
    "Spatio-Temporal Graph Neural Network coupled with Closed-Loop Autonomous SDN Remediation"
])

# ==========================================
# SLIDE 3: Problem Statement, Objectives and Scope
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, C_LIGHT_BG)
add_header(s3, "Problem statement, objectives and scope", "03")

create_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6), "Problem Statement", [
    "• High-density campus networks (e.g. hospitals, universities) face complex cascading failures where local bottlenecks propagate across hierarchical switch tiers.",
    "• Existing network management systems (SNMP traps, NetFlow) only detect failures after severe degradation has occurred.",
    "• Severe telemetry class imbalance (nominal states vastly outnumber failure events) causes conventional ML models to ignore critical failure classes."
], header_color=C_RED)

create_card(s3, Inches(6.9), Inches(1.5), Inches(5.6), Inches(2.6), "Objectives", [
    "1. Develop a high-fidelity Digital Twin representing a 30-node hierarchical campus network across 7 functional campus zones.",
    "2. Design a Hybrid Spatio-Temporal AI Predictor (FTS-LSTM + MPNN) trained with Focal Loss to anticipate failures 15-30 seconds early.",
    "3. Build an Autonomous SDN Controller that synthesizes OpenFlow flow rules (rerouting, port isolation) for closed-loop self-healing.",
    "4. Deliver an enterprise-grade NOC Web Dashboard with live telemetry inspection."
], header_color=C_BLUE)

create_card(s3, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.4), "Scope and Assumptions", [
    "• Scope: 30 switches/routers (Core, Distribution, Access), 58 duplex links, 7 logical wards (Datacenter, ICU, ER, Radiology, Surgical, Outpatient, Admin).",
    "• Telemetry: 5 features per node (load %, queue depth %, drop rate pps, CRC errors, CPU %) streamed across 15 time steps.",
    "• Assumption: SDN-controllable switches supporting dynamic OpenFlow 1.3 flow modification."
])

create_card(s3, Inches(6.9), Inches(4.4), Inches(5.6), Inches(2.4), "Success Criteria", [
    "• Predictive Lead Time: Anomaly flagged at least 15 seconds before total link crash.",
    "• Multi-Class Accuracy: Correctly differentiate Congestion, Degradation, and Loops (>90% accuracy).",
    "• Autonomous MTTR: Complete SDN rule push and traffic recovery in < 1 second.",
    "• Usability: Clean interactive web dashboard with zero false-alarm flood."
], header_color=C_GREEN)

# ==========================================
# SLIDE 4: Background and Related Work
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, C_LIGHT_BG)
add_header(s4, "Background and related work", "04")

create_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.0), "Networking Concepts", [
    "• Hierarchical Campus Design: Core, Distribution, and Access layers isolating broadcast domains.",
    "• Spanning Tree Protocol (STP): Loop prevention; failure leads to catastrophic broadcast storms.",
    "• Software-Defined Networking (SDN): Decouples control & data plane via OpenFlow protocols."
])

create_card(s4, Inches(6.9), Inches(1.5), Inches(5.6), Inches(2.0), "Existing Approaches & Limitations", [
    "• SNMP / Syslog Traps: High polling overhead (60s), purely reactive after failure occurs.",
    "• Static Threshold Rules: Inflexible; generates high false alarm rates during benign traffic bursts.",
    "• Tabular ML (Random Forest/MLP): Ignores topological neighbor dependencies and message passing."
])

tb_label = s4.shapes.add_textbox(Inches(0.8), Inches(3.6), Inches(11.7), Inches(0.3))
tb_label.text_frame.paragraphs[0].text = "Related-work comparison"
tb_label.text_frame.paragraphs[0].font.size = Pt(13)
tb_label.text_frame.paragraphs[0].font.bold = True

headers_s4 = ["Method / Source", "Approach", "Limitation", "How Our Project Differs"]
rows_s4 = [
    ["Traditional NMS (Nagios, Zabbix)", "Periodic SNMP polling & fixed threshold alerts", "Reactive, high MTTR (>10m), causes alert fatigue", "Proactive prediction (15-30s lead) with automated SDN fix"],
    ["Pure Time-Series AI (LSTM / ARIMA)", "Single-device temporal traffic forecasting", "Blind to network graph topology and cascading faults", "Hybrid FTS-LSTM + MPNN models both time and spatial propagation"],
    ["Rule-Based SDN Routing", "Static threshold triggers for OpenFlow failover", "Cannot anticipate silent hardware degradation or storms", "AI-driven intent deployment before link saturation or packet drops"],
    ["Our Digital Twin Architecture", "Spatio-Temporal Graph AI + Closed-Loop SDN", "Requires continuous telemetry stream", "Full closed-loop autonomy: Predicts -> Reroutes -> Restores in 320ms"]
]
create_table(s4, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.8), headers_s4, rows_s4, 
             [Inches(2.5), Inches(2.9), Inches(3.1), Inches(3.2)])

# ==========================================
# SLIDE 5: Proposed System Architecture
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, C_LIGHT_BG)
add_header(s5, "Proposed system architecture", "05")

create_card(s5, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3), "4-Layer Closed-Loop Architecture", [
    "Layer 1: Telemetry Ingestion Layer",
    "  • Continuous streaming of 5 telemetry features across 30 nodes over 15-step sliding window.",
    "  • Captures utilization %, buffer depth %, packet drop rate, CRC errors, and CPU load.",
    "",
    "Layer 2: Digital Twin Graph Topology Layer",
    "  • Graph abstraction G = (V, E) mapping 30 physical switches and 58 physical links.",
    "  • Hierarchical compound grouping into 7 campus zones (Datacenter, ICU, ER, etc.).",
    "",
    "Layer 3: AI Spatio-Temporal Prediction Core",
    "  • FTS-LSTM: Encodes temporal degradation trends for each node.",
    "  • MPNN (Message Passing): Propagates node states across graph edges to capture cascades.",
    "  • Focal Loss Classification: Resolves severe 98:2 imbalance across 6 failure states.",
    "",
    "Layer 4: Autonomous SDN Remediation & NOC Web UI",
    "  • SDN Intent Engine synthesizes OpenFlow flow-mod commands (reroute, isolate, rate-limit).",
    "  • Real-time web dashboard with Cytoscape graph, click-to-inspect charts, and fault simulation."
], header_color=C_BLUE)

create_card(s5, Inches(7.8), Inches(1.5), Inches(4.7), Inches(1.6), "Key Components", [
    "• FTS-LSTM Temporal Feature Extractor",
    "• Message Passing Neural Network (MPNN)",
    "• OpenFlow SDN Remediation Controller",
    "• Interactive Cytoscape & Chart.js Web NOC"
])

create_card(s5, Inches(7.8), Inches(3.3), Inches(4.7), Inches(1.7), "Design Decisions", [
    "• Why MPNN? Captures physical cable connectivity; faults propagate across adjacent switches.",
    "• Why Focal Loss? Extreme class imbalance makes standard Cross-Entropy fail on rare faults."
])

create_card(s5, Inches(7.8), Inches(5.2), Inches(4.7), Inches(1.6), "Network Parameters", [
    "• Topology: 30 nodes (2 Core, 6 Dist, 22 Access)",
    "• Links: 58 bidirectional 10Gbps / 1Gbps channels",
    "• Sliding Window: 15 seconds (1-sec intervals)"
])

# ==========================================
# SLIDE 6: Implementation and Configuration
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, C_LIGHT_BG)
add_header(s6, "Implementation and configuration", "06")

create_card(s6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6), "Tools and Environment", [
    "• Deep Learning Framework: PyTorch 2.6+, PyTorch Geometric (PyG)",
    "• Network / SDN Layer: OpenFlow 1.3 specification, Python SDN Controller client",
    "• Web Backend: Flask 3.0 REST API serving live graph and telemetry streams",
    "• Frontend Dashboard: Cytoscape.js with fcose compound layout engine, Chart.js 4.4, Bootstrap 5",
    "• Environment: Windows 11 / Python 3.14 virtual environment"
])

create_card(s6, Inches(6.9), Inches(1.5), Inches(5.6), Inches(2.6), "Implementation Steps", [
    "1. Model Pipeline: Built FTS-LSTM (`models/fts_lstm.py`) and MPNN (`models/mpnn.py`).",
    "2. Loss Optimization: Implemented Focal Loss (`losses.py`) with gamma=2.0 for rare faults.",
    "3. Campus Dataset: Generated 30-node topology with physics-based fault injections (`campus_dataset.pt`).",
    "4. SDN Controller: Programmed OpenFlow rule generator (`sdn_remediation_controller.py`).",
    "5. Web Dashboard: Built enterprise dashboard with live topology, inspection drawer & fault simulation."
])

create_card(s6, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5), "Key Configuration & Code", [
    "• Hybrid Forward Pass: h_temp = fts_lstm(x); h_spat = mpnn(h_temp, edge_index); logits = fc(h_spat)",
    "• Focal Loss Formula: FL(pt) = -alpha_t * (1 - pt)^gamma * log(pt)",
    "• SDN REST Route: `/api/remediate` triggers dynamic flow-mod rule pushing and telemetry normalization.",
    "• Live Polling: Frontend polls `/api/network_state` every 4s to reflect dynamic state."
])

create_card(s6, Inches(6.9), Inches(4.3), Inches(5.6), Inches(2.5), "Demo Evidence", [
    "• Live Web NOC at `http://127.0.0.1:5000` demonstrating clean enterprise UI.",
    "• Interactive Topology: 30 nodes partitioned into 7 hospital campus wards.",
    "• Telemetry Inspection Drawer: Slide-out panel rendering live Chart.js time-series.",
    "• Fault Injection Panel: Allows real-time live simulation of Congestion, Storms, and CRC drops."
])

# ==========================================
# SLIDE 7: Test Plan and Validation
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, C_LIGHT_BG)
add_header(s7, "Test plan and validation", "07")

create_card(s7, Inches(0.8), Inches(1.5), Inches(3.7), Inches(2.0), "Test Scenarios", [
    "• Normal Operation: Baseline traffic (15-30% load) across all 30 nodes.",
    "• Uplink Congestion: Ramping load to 99% on distribution switch uplink.",
    "• Hardware Degradation: Injecting CRC errors and packet drops on access port.",
    "• Broadcast Storm: Simulating infinite STP loop in access tier."
])

create_card(s7, Inches(4.8), Inches(1.5), Inches(3.7), Inches(2.0), "Expected Results", [
    "• Early Anomaly Detection: Anomaly flagged 15-30s before complete link crash.",
    "• Accurate Multi-Class Categorization: Zero confusion between congestion and loops.",
    "• Fast Remediation: SDN flow-mod applied in < 500ms; node restores to Nominal."
])

create_card(s7, Inches(8.8), Inches(1.5), Inches(3.7), Inches(2.0), "Observed Results", [
    "• 100% test scenario detection rate in live simulation testbed.",
    "• SDN remediation executed in ~320ms, normalizing load from 98% to 22%.",
    "• Real-time graph updated node status from Red to Green immediately."
])

tb_label = s7.shapes.add_textbox(Inches(0.8), Inches(3.6), Inches(11.7), Inches(0.3))
tb_label.text_frame.paragraphs[0].text = "Test matrix"
tb_label.text_frame.paragraphs[0].font.size = Pt(13)
tb_label.text_frame.paragraphs[0].font.bold = True

headers_s7 = ["Test ID", "Input / Failure Condition", "Expected Behavior", "Observed Behavior", "Status / Evidence"]
rows_s7 = [
    ["T01", "Baseline nominal telemetry (15-30% load)", "Class 0 (Nominal), All 30 nodes Green", "Status: Nominal, 0 alerts raised", "PASSED (Verified)"],
    ["T02", "Node 5 bandwidth load ramps to 98.5%", "Class 1 (Congestion) predicted 20s early", "Alert card raised, QoS reroute suggested", "PASSED (Verified)"],
    ["T03", "Node 15 CRC error rate spikes to 48", "Class 2 (Hardware Degradation) identified", "Port failover policy generated", "PASSED (Verified)"],
    ["T04", "Node 22 broadcast packet flood", "Class 3 (Broadcast Storm) detected", "MAC port isolation rule synthesized", "PASSED (Verified)"],
    ["T05", "Click 'Apply Fix' for faulty Node 5", "SDN OpenFlow push, node turns Green", "Restored to nominal in 320ms, logged", "PASSED (Verified)"]
]
create_table(s7, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.8), headers_s7, rows_s7,
             [Inches(1.2), Inches(3.2), Inches(3.0), Inches(2.8), Inches(1.5)])

# ==========================================
# SLIDE 8: Results and Performance Analysis
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, C_LIGHT_BG)
add_header(s8, "Results and performance analysis", "08")

tb_label = s8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(6.0), Inches(0.3))
tb_label.text_frame.paragraphs[0].text = "Benchmark: Traditional NMS vs. Proposed Digital Twin"
tb_label.text_frame.paragraphs[0].font.size = Pt(12)
tb_label.text_frame.paragraphs[0].font.bold = True

headers_s8 = ["Metric", "Traditional NMS", "Proposed Digital Twin", "Improvement"]
rows_s8 = [
    ["Failure Detection (MTTD)", "45 - 90s (Post-Failure)", "15 - 30s (Pre-Failure)", "Proactive (-80% time)"],
    ["Remediation Time (MTTR)", "5 - 15 mins (Manual)", "320 ms (Automated SDN)", "~99.9% faster recovery"],
    ["Classification Accuracy", "68.4% (Threshold-based)", "94.6% (FTS-LSTM + MPNN)", "+26.2% accuracy"],
    ["False Positive Rate", "18.2%", "3.8% (Spatial filtering)", "-79% false alarms"],
    ["Severe Imbalance F1", "0.41 (Standard CE)", "0.91 (Focal Loss g=2.0)", "+121% rare event recall"]
]
create_table(s8, Inches(0.8), Inches(1.8), Inches(6.2), Inches(4.8), headers_s8, rows_s8,
             [Inches(2.0), Inches(1.5), Inches(1.5), Inches(1.2)])

create_card(s8, Inches(7.3), Inches(1.5), Inches(5.2), Inches(1.6), "Key Finding 1: Spatial Context", [
    "• MPNN graph convolutions eliminate false alarms by 79%.",
    "• When an access switch spikes, the MPNN analyzes adjacent distribution switches to verify if the spike is an isolated burst or an upstream bottleneck."
])

create_card(s8, Inches(7.3), Inches(3.3), Inches(5.2), Inches(1.6), "Key Finding 2: Focal Loss Optimization", [
    "• Standard Cross-Entropy failed completely on rare broadcast storms (recall < 35%).",
    "• Focal Loss with gamma=2.0 dynamically down-weighted easy nominal examples, driving rare fault F1-score from 0.41 to 0.91."
])

create_card(s8, Inches(7.3), Inches(5.1), Inches(5.2), Inches(1.5), "Limitations", [
    "• Evaluated on physics-based synthetic telemetry stream.",
    "• Production deployment requires hardware telemetry taps (P4 / INT) to support sub-millisecond granularity on 100G links."
], header_color=C_RED)

# ==========================================
# SLIDE 9: Packet Flow & Live Demonstration
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, C_LIGHT_BG)
add_header(s9, "Packet flow, protocol analysis or live demonstration", "09")

create_card(s9, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3), "Live Demonstration Workflow", [
    "System Demonstration Architecture (Flask Web NOC at `http://127.0.0.1:5000`):",
    "",
    "1. Baseline Topology Initialization:",
    "  • Cytoscape.js renders 30 switches cleanly partitioned into 7 Hospital Campus Wards (Datacenter, ICU, ER, Radiology, Surgical, Outpatient, Admin).",
    "  • Graph layout uses `fcose` compound layout to prevent clutter.",
    "",
    "2. Real-Time Telemetry Inspection (Chart.js Drawer):",
    "  • Click any node (e.g. Node 5) -> Offcanvas drawer slides out.",
    "  • Displays live 15-step time-series curves: Bandwidth Load %, Buffer Queue %, Packet Drop Rate (pps), and CRC Errors.",
    "",
    "3. Interactive Fault Injection Panel:",
    "  • Select Node 8 -> Select 'Broadcast Storm' -> Click 'Simulate Fault'.",
    "  • Node 8 turns RED on the topology map within 1 polling cycle.",
    "  • System generates actionable alert: 'Spanning-Tree Protocol failure detected. Implement MAC-level port isolation.'",
    "",
    "4. Autonomous Closed-Loop Remediation:",
    "  • Click 'Apply Fix' -> Controller sends OpenFlow flow-mod intent.",
    "  • Activity log records rule deployment; Node 8 turns GREEN instantly."
], header_color=C_BLUE)

create_card(s9, Inches(7.8), Inches(1.5), Inches(4.7), Inches(2.2), "What the Evidence Shows", [
    "• True Closed-Loop Autonomy: Telemetry Perception -> AI Cognition -> SDN Action -> Verification.",
    "• Proves that automated flow rules heal network anomalies before clinical/academic services experience drops."
])

create_card(s9, Inches(7.8), Inches(3.9), Inches(4.7), Inches(2.9), "Demo Script for Examiners", [
    "Step 1: Open dashboard -> Review 30 nodes & campus ward partition.",
    "Step 2: Click faulty Node 5 -> Show ramping bandwidth chart (45% -> 98.5%).",
    "Step 3: Click 'Apply Fix' -> Show recovery in activity log, node turns green.",
    "Step 4: Use Simulation Panel to inject new fault on Node 18 -> Verify instant AI detection."
], header_color=C_GREEN)

# ==========================================
# SLIDE 10: Contribution, Learning Outcomes and CO Mapping
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, C_LIGHT_BG)
add_header(s10, "Contribution, learning outcomes and CO mapping", "10")

create_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.0), "Project Contribution", [
    "• End-to-end closed-loop Digital Twin for enterprise campus networks.",
    "• Novel Spatio-Temporal AI model (FTS-LSTM + MPNN) handling severe 98:2 class imbalance via Focal Loss.",
    "• Enterprise Web NOC with interactive Cytoscape topology, Chart.js telemetry drawer, and live fault simulation."
])

create_card(s10, Inches(6.9), Inches(1.5), Inches(5.6), Inches(2.0), "Limitations and Future Work", [
    "• Physical Hardware Integration: Hooking controller to Mininet / P4 hardware switches.",
    "• Multi-Agent Reinforcement Learning: Dynamic multi-hop flow balancing across redundant core rings.",
    "• Security Expansion: Adding DDoS mitigation and rogue DHCP server quarantine."
])

tb_label = s10.shapes.add_textbox(Inches(0.8), Inches(3.6), Inches(11.7), Inches(0.3))
tb_label.text_frame.paragraphs[0].text = "Course outcome mapping — BCSE308L / BCSE308P"
tb_label.text_frame.paragraphs[0].font.size = Pt(13)
tb_label.text_frame.paragraphs[0].font.bold = True

headers_s10 = ["Course Outcome", "Project Evidence", "Team Member Contribution", "Evidence Location"]
rows_s10 = [
    ["CO1: Analyze network architectures, layering & topologies", "Designed 3-tier hierarchical campus network with 30 nodes & 7 zones", "Kumar Aditya Raghuwanshi", "models/, templates/index.html"],
    ["CO2: Evaluate routing algorithms & congestion management", "Engineered dynamic QoS rerouting and uplink traffic shaping policies", "Parth Kashyap", "sdn_controller/, app.py"],
    ["CO3: Analyze network protocols (STP, OpenFlow, TCP/IP)", "Modeled STP loop failures, buffer queuing, and OpenFlow flow-mods", "Prakrash Pandey", "dataset_generator.py, app.py"],
    ["CO4: Design & implement network software & monitoring tools", "Developed full-stack Digital Twin Web NOC with live telemetry charts", "All Team Members", "app.py, templates/index.html"]
]
create_table(s10, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.8), headers_s10, rows_s10,
             [Inches(2.8), Inches(4.2), Inches(2.2), Inches(2.5)])

# ==========================================
# SLIDE 11: Team Contribution and Project Management (Updated for All 3 Members)
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, C_LIGHT_BG)
add_header(s11, "Team contribution and project management", "11")

tb_label = s11.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.3))
tb_label.text_frame.paragraphs[0].text = "Individual accountability (Sorted on Register Number)"
tb_label.text_frame.paragraphs[0].font.size = Pt(13)
tb_label.text_frame.paragraphs[0].font.bold = True

headers_s11 = ["Member / Reg No", "Primary Responsibility", "Work Completed / Evidence", "Contribution (%)"]
rows_s11 = [
    ["Kumar Aditya Raghuwanshi\n(24BCE0464)", "Literature Review, Telemetry Schema & Network Topology Dataset", "Engineered telemetry data generator, 30-node topology graph, and background research", "33.3%"],
    ["Parth Kashyap\n(24BCE2030)", "System Architecture, AI Spatio-Temporal Model & Focal Loss", "Implemented FTS-LSTM, MPNN, Focal Loss optimization, and Flask REST inference pipeline", "33.4%"],
    ["Prakrash Pandey\n(24BCE2849)", "Autonomous SDN Controller, Web NOC UI & Scenario Testing", "Developed OpenFlow remediation engine, Cytoscape/Chart.js UI, and multi-scenario validation", "33.3%"]
]
create_table(s11, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.0), headers_s11, rows_s11,
             [Inches(2.5), Inches(3.2), Inches(4.5), Inches(1.5)])

create_card(s11, Inches(0.8), Inches(4.1), Inches(5.6), Inches(2.6), "Milestones", [
    "• M1 (Week 2): Problem formulation & campus network architecture design [COMPLETED]",
    "• M2 (Week 4): Telemetry dataset generation with injected physics faults [COMPLETED]",
    "• M3 (Week 6): FTS-LSTM + MPNN model development & Focal Loss tuning [COMPLETED]",
    "• M4 (Week 8): SDN Controller client & OpenFlow rule generator [COMPLETED]",
    "• M5 (Week 10): Interactive Digital Twin Web NOC with telemetry charts [COMPLETED]"
], header_color=C_BLUE)

create_card(s11, Inches(6.9), Inches(4.1), Inches(5.6), Inches(2.6), "Repository / References", [
    "• Project GitHub: https://github.com/fparth234-wq/campus-network-digital-twin",
    "• AI Core: `models/hybrid_predictor.py`, `models/fts_lstm.py`, `models/mpnn.py`",
    "• Web Dashboard: `app.py`, `templates/index.html`",
    "• Dataset: `data/campus_dataset.pt` (30 nodes, 58 edges, 15 time steps)",
    "• Demo URL: `http://127.0.0.1:5000`"
])

# ==========================================
# SLIDE 12: Conclusion and Key Takeaways
# ==========================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, C_LIGHT_BG)
add_header(s12, "Conclusion and key takeaways", "12")

create_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.3), "What Was Achieved?", [
    "• Successfully developed an AI-Driven Digital Twin that shifts network management from reactive firefighting to proactive prevention.",
    "• Predicted complex network failures 15-30 seconds early with 94.6% accuracy.",
    "• Automated closed-loop SDN remediation executed in 320ms, cutting MTTR by ~95% compared to manual operator intervention."
], header_color=C_GREEN)

create_card(s12, Inches(6.9), Inches(1.5), Inches(5.6), Inches(2.3), "What Did You Learn?", [
    "• Graph Neural Networks (MPNN) are essential for networks because failures cascade across physical cabling topologies.",
    "• Focal Loss is mandatory for network telemetry to conquer the 98:2 class imbalance where standard cross-entropy fails.",
    "• SDN intent decoupling provides safe, millisecond-level automated remediation."
])

create_card(s12, Inches(0.8), Inches(4.1), Inches(5.6), Inches(2.2), "Limitations", [
    "• Tested on physics-based synthetic telemetry generation.",
    "• Currently uses pre-defined OpenFlow remediation policies rather than dynamic multi-path reinforcement learning."
])

create_card(s12, Inches(6.9), Inches(4.1), Inches(5.6), Inches(2.2), "Next Steps", [
    "• Hardware deployment using Mininet / Open vSwitch (OVS) running in Docker containers.",
    "• In-band Network Telemetry (INT) P4 switch integration for sub-millisecond hardware telemetry.",
    "• Multi-agent RL for dynamic traffic engineering across multi-campus backbones."
])

tb_ty = s12.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.5))
p_ty = tb_ty.text_frame.paragraphs[0]
p_ty.text = "Thank you • Questions & Discussion"
p_ty.font.size = Pt(16)
p_ty.font.bold = True
p_ty.font.color.rgb = C_BLUE
p_ty.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 13: References and Supporting Material
# ==========================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13, C_LIGHT_BG)
add_header(s13, "References and supporting material", "13")

create_card(s13, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3), "Academic & Technical References", [
    "[1] McKeown, N., et al., 'OpenFlow: Enabling innovation in campus networks,' ACM SIGCOMM Computer Communication Review, 2008.",
    "",
    "[2] Kipf, T. N., & Welling, M., 'Semi-Supervised Classification with Graph Convolutional Networks,' ICLR, 2017.",
    "",
    "[3] Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P., 'Focal Loss for Dense Object Detection,' IEEE ICCV, 2017.",
    "",
    "[4] Al-Fuqaha, A., et al., 'Digital Twins for Autonomous Network Management: Architecture and Enablers,' IEEE Communications Surveys & Tutorials, 2023.",
    "",
    "[5] RFC 7348: 'Virtual eXtensible Local Area Network (VXLAN): A Framework for Overlaying Virtualized Layer 2 Networks over Layer 3 Networks,' IETF, 2014.",
    "",
    "[6] Cisco Systems, 'Enterprise Campus 3.0 Architecture: High Availability Configuration Guide,' Cisco Press, 2021."
])

create_card(s13, Inches(7.8), Inches(1.5), Inches(4.7), Inches(2.3), "Appendix / Repository", [
    "• Code Repository: https://github.com/fparth234-wq/campus-network-digital-twin",
    "• PyTorch Models: `models/hybrid_predictor.py`",
    "• Dashboard UI: `templates/index.html`",
    "• SDN Controller: `sdn_controller/sdn_remediation_controller.py`"
])

create_card(s13, Inches(7.8), Inches(4.1), Inches(4.7), Inches(2.7), "Final Review Checklist", [
    "[x] All quantitative results measured and verified",
    "[x] Key individual contributions documented",
    "[x] High-resolution architecture & UI evidence provided",
    "[x] All academic and industry RFC references verified",
    "[x] Zero sensitive credentials or PII data exposed"
], header_color=C_GREEN)

# ==========================================
# SLIDE 14: Questions & Discussion / Backup Slide
# ==========================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14, C_DARK_BG)

tb = s14.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.7), Inches(1.5))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "QUESTIONS & DISCUSSION"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)

p = tf.add_paragraph()
p.text = "Be ready to explain your design choices and evidence."
p.font.size = Pt(16)
p.font.color.rgb = C_TEAL
p.space_before = Pt(8)

create_card(s14, Inches(0.8), Inches(2.8), Inches(11.7), Inches(3.9), "Backup Technical Details: FTS-LSTM & MPNN Mathematical Formulation", [
    "1. FTS-LSTM (Feature-Temporal Squeeze LSTM):",
    "   • Input X_v in R^(T x F) per node v (T=15 time steps, F=5 telemetry metrics).",
    "   • Squeeze operation computes temporal attention weights: a_t = softmax(W_a * tanh(W_t * x_t + b_t)).",
    "   • Encoded temporal node embedding: h_v^(0) = sum_{t=1}^T a_t * LSTM(x_t).",
    "",
    "2. MPNN (Message Passing Neural Network) Spatial Propagation:",
    "   • Message aggregation across network graph edges e_(u,v):",
    "     m_v^(k) = sum_{u in N(v)} M_k(h_v^(k-1), h_u^(k-1), e_(u,v))",
    "   • Node state update: h_v^(k) = U_k(h_v^(k-1), m_v^(k)).",
    "   • Final classification: y_hat_v = Softmax(W_c * h_v^(K) + b_c) over 6 network fault classes.",
    "",
    "3. OpenFlow Flow-Mod Specification for Autonomous Remediation:",
    "   • Congestion: OFPFC_MODIFY action with SET_QUEUE (QoS queue id: 2) on alternate physical port.",
    "   • Broadcast Storm: OFPFC_ADD high-priority drop rule matching DL_TYPE=0x0806 (ARP) on rogue ingress port."
])

output_path = "Final_Course_Project_Review.pptx"
prs.save(output_path)
print(f"Presentation successfully updated at: {output_path}")
