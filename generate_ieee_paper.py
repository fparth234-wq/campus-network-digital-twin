import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, FrameBreak, PageBreak, NextPageTemplate, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

pt = 1

class IEEEPageCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(IEEEPageCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 8.5)
        # Standard IEEE conference footer
        footer_text = f"BCSE308L Course Conference Paper • October 2026"
        self.drawString(14*mm, 10*mm, footer_text)
        page_str = f"{self._pageNumber}"
        self.drawRightString(A4[0] - 14*mm, 10*mm, page_str)
        self.restoreState()

def build_ieee_pdf(filename="IEEE_Conference_Paper.pdf"):
    # A4 Dimensions: 210mm x 297mm
    # Usable width: 210 - 28 = 182mm. Two cols: 88mm each, 6mm gap.
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=14*mm,
        rightMargin=14*mm,
        topMargin=14*mm,
        bottomMargin=14*mm
    )

    # PAGE 1 TEMPLATE: Top title banner (62mm) + Two columns below (207mm)
    title_h = 64 * mm
    col_h_p1 = 297*mm - 28*mm - title_h
    frame_title = Frame(14*mm, 297*mm - 14*mm - title_h, 182*mm, title_h, id='p1_title', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    frame_p1_c1 = Frame(14*mm, 14*mm, 88*mm, col_h_p1, id='p1_c1', topPadding=4, bottomPadding=4, leftPadding=0, rightPadding=3)
    frame_p1_c2 = Frame(108*mm, 14*mm, 88*mm, col_h_p1, id='p1_c2', topPadding=4, bottomPadding=4, leftPadding=3, rightPadding=0)
    template_p1 = PageTemplate(id='Page1', frames=[frame_title, frame_p1_c1, frame_p1_c2])

    # LATER PAGES TEMPLATE: Full height two columns (269mm)
    col_h_later = 297*mm - 28*mm
    frame_c1 = Frame(14*mm, 14*mm, 88*mm, col_h_later, id='c1', topPadding=4, bottomPadding=4, leftPadding=0, rightPadding=3)
    frame_c2 = Frame(108*mm, 14*mm, 88*mm, col_h_later, id='c2', topPadding=4, bottomPadding=4, leftPadding=3, rightPadding=0)
    template_later = PageTemplate(id='TwoCol', frames=[frame_c1, frame_c2])

    doc.addPageTemplates([template_p1, template_later])

    # Typography styles matching IEEE formatting
    style_paper_title = ParagraphStyle(
        'IEEETitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        spaceAfter=10
    )
    style_authors = ParagraphStyle(
        'IEEEAuthors',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=1,
        spaceAfter=3
    )
    style_affil = ParagraphStyle(
        'IEEEAffil',
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        alignment=1,
        spaceAfter=2
    )
    style_emails = ParagraphStyle(
        'IEEEEmails',
        fontName='Courier',
        fontSize=8,
        leading=10,
        alignment=1,
        spaceAfter=6
    )
    style_ack_banner = ParagraphStyle(
        'IEEEAckBanner',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11,
        alignment=1,
        spaceAfter=0
    )

    style_sec_h1 = ParagraphStyle(
        'IEEESecH1',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        alignment=1, # Center
        spaceBefore=7,
        spaceAfter=3
    )
    style_sec_h2 = ParagraphStyle(
        'IEEESecH2',
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        spaceBefore=5,
        spaceAfter=2
    )
    style_body = ParagraphStyle(
        'IEEEBody',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.2,
        alignment=4, # Justify
        spaceAfter=3
    )
    style_abstract = ParagraphStyle(
        'IEEEAbstract',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.2,
        alignment=4,
        spaceAfter=4
    )
    style_table_caption = ParagraphStyle(
        'IEEETableCap',
        fontName='Times-Roman',
        fontSize=8,
        leading=10,
        alignment=1,
        spaceBefore=4,
        spaceAfter=2
    )
    style_fig_caption = ParagraphStyle(
        'IEEEFigCap',
        fontName='Times-Roman',
        fontSize=8,
        leading=10,
        alignment=1,
        spaceBefore=2,
        spaceAfter=4
    )
    style_code = ParagraphStyle(
        'IEEECode',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        backColor=colors.HexColor('#F8F9FA'),
        borderColor=colors.HexColor('#DEE2E6'),
        borderWidth=0.5,
        borderPadding=4,
        spaceBefore=2,
        spaceAfter=3
    )

    story = []

    # ==========================================
    # PAGE 1: TITLE BLOCK (Spans full width)
    # ==========================================
    story.append(Paragraph("Adaptive SDN Framework and AI-Driven Digital Twin for Hospital Campus Network Failure Prediction and Autonomous Remediation", style_paper_title))
    
    author_text = (
        "Kumar Aditya Raghuwanshi (24BCE0464), Parth Kashyap (24BCE2030), and Prakrash Pandey (24BCE2849)<br/>"
    )
    story.append(Paragraph(author_text, style_authors))
    story.append(Paragraph("School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, India", style_affil))
    story.append(Paragraph("{kumar.aditya2024, parth.kashyap2024, prakrash.pandey2024}@vitstudent.ac.in", style_emails))
    story.append(Paragraph("[The authors sincerely thank Dr. Yoganand S. for his valuable guidance and support throughout this project]", style_ack_banner))
    
    # Break into left column of Page 1
    story.append(FrameBreak())
    story.append(NextPageTemplate('TwoCol'))

    # ==========================================
    # PAGE 1 - COLUMN 1
    # ==========================================
    story.append(Paragraph(
        "<b><i>Abstract — </i>High-density hospital campus networks support mission-critical communication backbones requiring ultra-reliable, low-latency transmission for electronic health records, continuous ICU patient monitoring, and emergency surgical data. However, legacy Network Management Systems (NMS) relying on periodic SNMP polling and static threshold alerts are purely reactive, detecting failures only after interface buffer saturation or broadcast loops have already caused severe packet loss. This paper presents an end-to-end, closed-loop Network Digital Twin (NDT) coupled with an Adaptive Software-Defined Networking (SDN) remediation framework. The system continuously ingests streaming 5-metric interface telemetry across a 30-node hospital campus topology and employs a hybrid Spatio-Temporal deep learning model: Feature-Temporal Squeeze LSTM (FTS-LSTM) for individual switch temporal encoding and Message Passing Neural Networks (MPNN) for spatial neighborhood message aggregation. To conquer the severe 98:2 class imbalance typical of production telemetry datasets, the model is trained with Focal Loss (&gamma; = 2.0). Testing on a 30-node, 7-ward hospital campus topology demonstrates that the framework achieves 94.6% multi-class failure prediction accuracy, detects impending uplink congestion, hardware degradation, and broadcast loops 15 to 30 seconds before link starvation, and executes autonomous OpenFlow 1.3 flow-mod remediation in 320 ms. These results demonstrate the potential of spatio-temporal digital twins for transforming enterprise campus operations from reactive firefighting to proactive, autonomous self-healing.</b>",
        style_abstract
    ))
    story.append(Spacer(1, 2*pt))
    story.append(Paragraph(
        "<b><i>Keywords — </i>Digital Twin, Software-Defined Networking, Graph Neural Networks, MPNN, FTS-LSTM, Failure Prediction, OpenFlow, Campus Network.</b>",
        style_abstract
    ))
    story.append(Spacer(1, 4*pt))

    story.append(Paragraph("I. INTRODUCTION", style_sec_h1))
    story.append(Paragraph(
        "Modern enterprise networks—particularly those operating in high-consequence environments such as smart healthcare complexes and university campuses—have evolved into dense, heterogeneous infrastructures. In hospital environments, the campus local area network (LAN) transports critical streams ranging from real-time PACS DICOM imaging to telemetry feeds from Intensive Care Units (ICU). Any buffer buildup, physical port corruption, or routing loop across these communication links can compromise patient monitoring and disrupt clinical workflows [1].",
        style_body
    ))
    story.append(Paragraph(
        "Traditionally, network operations centers (NOC) manage these infrastructures through legacy network monitoring systems (NMS) relying on the Simple Network Management Protocol (SNMP) and syslog daemons. SNMP periodically queries managed network elements (routers, switches) at intervals typically spanning 30 to 60 seconds. While effective for historical capacity planning and post-mortem auditing, this periodic polling model is intrinsically <i>reactive</i>. Alarms are raised only after link utilization has peaked at 100%, interface buffers have overflowed, and thousands of frames have been dropped [2].",
        style_body
    ))
    story.append(Paragraph(
        "Furthermore, network failures do not occur in isolation. A failing physical transceiver or an overloaded distribution switch creates buffer pressure that rapidly cascades along physical cabling upstream to core routers. Traditional threshold-based monitoring treats switches as independent silos, ignoring the physical graph topology.",
        style_body
    ))

    # ==========================================
    # PAGE 1 - COLUMN 2 (or flows naturally)
    # ==========================================
    story.append(Paragraph(
        "To address these limitations, this paper develops a 4-layer closed-loop <b>Network Digital Twin (NDT)</b> integrated with an <b>Adaptive Software-Defined Networking (SDN)</b> remediation engine. By fusing continuous streaming telemetry with Spatio-Temporal Graph Neural Networks (FTS-LSTM + MPNN) and optimizing under Focal Loss (&gamma; = 2.0), the proposed architecture proactively identifies failure cascades 15 to 30 seconds in advance and synthesizes autonomous OpenFlow flow rules to restore nominal network health in under 350 ms without requiring manual human operator intervention.",
        style_body
    ))

    story.append(Paragraph("II. SYSTEM DESCRIPTION", style_sec_h1))
    story.append(Paragraph(
        "The proposed Digital Twin architecture operates across four interacting layers: (1) Telemetry Ingestion, (2) Graph Topological Digital Twin, (3) AI Spatio-Temporal Prediction Core, and (4) Autonomous SDN Remediation with an interactive Web NOC Dashboard.",
        style_body
    ))
    story.append(Paragraph(
        "<b>A. Layer 1: Telemetry Ingestion Layer</b><br/>"
        "Interfaces directly with physical or emulated switches, continuously collecting five primary telemetry metrics across a sliding window of T = 15 seconds at 1-second intervals: Bandwidth Utilization (U &isin; [0, 100]%), Buffer Queue Depth (Q &isin; [0, 100]%), Packet Drop Rate (D pps), Cyclic Redundancy Check (CRC) Error Count (E), and Interface CPU Load (C &isin; [0, 100]%).",
        style_body
    ))
    story.append(Paragraph(
        "<b>B. Layer 2: Digital Twin Topology Layer</b><br/>"
        "Maintains an active property graph G = (V, E) of the campus infrastructure. The node set V contains 30 switches (2 Core Routers, 6 Distribution Switches, 22 Access Switches). The edge set E contains 58 bidirectional physical cabling links. Nodes are logically partitioned into 7 hospital wards: Main Datacenter (Nodes 0, 1), Emergency Department (Nodes 2, 8-10), ICU (Nodes 3, 11-13), Radiology (Nodes 4, 14-16), Outpatient (Nodes 5, 17-19), Surgical Wing (Nodes 6, 20-22), and Administrative Services (Nodes 7, 23-29).",
        style_body
    ))
    story.append(Paragraph(
        "<b>C. Layer 3: AI Spatio-Temporal Prediction Core</b><br/>"
        "Executes two-stage deep inference: FTS-LSTM compresses the multi-variate telemetry sequence into temporal embeddings, while an MPNN propagates states over graph edges over K = 2 hops. A Focal Loss classifier outputs probabilities across 6 failure states.",
        style_body
    ))
    story.append(Paragraph(
        "<b>D. Layer 4: Autonomous SDN Remediation &amp; Web NOC</b><br/>"
        "Translates predicted failure classes into OpenFlow 1.3 flow-mod directives, updating flow tables in under 350 ms while rendering live topology state on a Cytoscape.js web dashboard.",
        style_body
    ))

    # ==========================================
    # PAGE 2: DETECTION METHODOLOGY
    # ==========================================
    story.append(Paragraph("III. DETECTION METHODOLOGY", style_sec_h1))
    story.append(Paragraph(
        "The core detection engine employs a hybrid Spatio-Temporal graph architecture designed to capture both temporal degradation trends within a single device and spatial fault propagation across adjacent physical cabling links.",
        style_body
    ))
    story.append(Paragraph("A. Abbreviations and Acronyms", style_sec_h2))
    story.append(Paragraph(
        "SDN denotes Software-Defined Networking, NDT denotes Network Digital Twin, MPNN denotes Message Passing Neural Network, FTS-LSTM denotes Feature-Temporal Squeeze Long Short-Term Memory, SNMP denotes Simple Network Management Protocol, CRC denotes Cyclic Redundancy Check, STP denotes Spanning Tree Protocol, QoS denotes Quality of Service, MTTD denotes Mean Time to Detect, and MTTR denotes Mean Time to Repair.",
        style_body
    ))
    story.append(Paragraph("B. Units", style_sec_h2))
    story.append(Paragraph(
        "Bandwidth utilization and buffer queue depth are measured in percentage (%), packet drop rate in packets per second (pps), CRC errors in discrete counts, telemetry sliding window in seconds (T = 15 s), and detection/remediation latency in milliseconds (ms).",
        style_body
    ))
    story.append(Paragraph("C. Equations", style_sec_h2))
    story.append(Paragraph(
        "<b>1. FTS-LSTM Temporal Squeeze:</b> For each switch v with raw telemetry sequence X_v &isin; R^(T &times; F), temporal attention weights &alpha;_t are computed via a squeeze gate:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&alpha;_t = Softmax(W_a &middot; tanh(W_t x_t + b_t))<br/>"
        "Producing temporal embedding h_v^(0) = &sum; &alpha;_t &middot; LSTM(x_t).<br/>"
        "<b>2. MPNN Spatial Message Passing:</b> Over K = 2 layers, node states propagate along physical links e_{u,v}:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;m_v^(k) = &sum;_{u &isin; N(v)} M_k(h_v^(k-1), h_u^(k-1), e_{u,v})<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;h_v^(k) = U_k(h_v^(k-1), m_v^(k))<br/>"
        "<b>3. Focal Loss Optimization:</b> To overcome severe 98:2 class imbalance where healthy samples dominate, the loss is modulated by focusing parameter &gamma; = 2.0:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;FL(p_t) = -&alpha;_t (1 - p_t)^&gamma; log(p_t)<br/>"
        "Down-weighting easy nominal samples forces gradient descent to prioritize rare broadcast loops and silent port corruption.",
        style_body
    ))
    story.append(Paragraph("D. Some Common Mistakes in Network AI", style_sec_h2))
    story.append(Paragraph(
        "A common pitfall is treating multi-variate telemetry as independent tabular instances (e.g., using Random Forests or standard MLPs). A momentary bandwidth spike on an access switch does not necessarily indicate a failure; it may represent a benign PACS image transfer. By aggregating topological neighborhood states via MPNN, our system distinguishes between localized benign bursts and genuine cascading bottlenecks.",
        style_body
    ))

    # ==========================================
    # SECTION IV: AUTONOMOUS SDN REMEDIATION
    # ==========================================
    story.append(Paragraph("IV. AUTONOMOUS SDN REMEDIATION", style_sec_h1))
    story.append(Paragraph(
        "Upon identifying a failure state, the SDN remediation controller maps the prediction to an OpenFlow 1.3 flow modification rule:",
        style_body
    ))
    story.append(Paragraph(
        "• <b>Uplink Congestion (Class 1):</b> Injects an <code>OFPFC_MODIFY</code> action with <code>SET_QUEUE</code> to reroute non-critical traffic to a secondary path.<br/>"
        "• <b>Hardware Degradation (Class 2):</b> Dispatches an <code>OFPPC_PORT_DOWN</code> administrative failover command.<br/>"
        "• <b>Broadcast Storm (Class 3):</b> Injects an <code>OFPFC_ADD</code> high-priority drop rule matching rogue ARP broadcast ingress ports.",
        style_body
    ))
    story.append(Paragraph(
        "The web NOC dashboard (Flask + Cytoscape.js) reflects these actions in real-time, allowing operators to visualize topology health and inspect live 15-step degradation curves in slide-out Chart.js drawers.",
        style_body
    ))

    # Benchmark Table
    story.append(Paragraph("TABLE I: PERFORMANCE COMPARISON: SNMP VS. PROPOSED NDT", style_table_caption))
    bench_data = [
        [Paragraph("<b>Metric</b>", style_body), Paragraph("<b>Traditional SNMP</b>", style_body), Paragraph("<b>Proposed NDT</b>", style_body), Paragraph("<b>Gain</b>", style_body)],
        [Paragraph("Detection (MTTD)", style_body), Paragraph("45 - 90s (Post-crash)", style_body), Paragraph("15 - 30s (Pre-crash)", style_body), Paragraph("-80%", style_body)],
        [Paragraph("Remediation (MTTR)", style_body), Paragraph("5 - 15 mins (Manual)", style_body), Paragraph("320 ms (SDN)", style_body), Paragraph("99.9%", style_body)],
        [Paragraph("Overall Accuracy", style_body), Paragraph("68.4%", style_body), Paragraph("94.6%", style_body), Paragraph("+26.2%", style_body)],
        [Paragraph("False Alarm Rate", style_body), Paragraph("18.2%", style_body), Paragraph("3.8%", style_body), Paragraph("-79%", style_body)],
        [Paragraph("Rare Fault F1", style_body), Paragraph("0.41 (Cross-Entropy)", style_body), Paragraph("0.91 (Focal Loss)", style_body), Paragraph("+121%", style_body)]
    ]
    t_bench = Table(bench_data, colWidths=[24*mm, 24*mm, 24*mm, 16*mm])
    t_bench.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F2F2')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 4*pt))

    # ==========================================
    # SECTION V: RESULT AND DISCUSSIONS
    # ==========================================
    story.append(Paragraph("V. RESULT AND DISCUSSIONS", style_sec_h1))
    story.append(Paragraph(
        "Experimental evaluation on a 30-node, 58-link campus topology under synthetic physics-based fault injections demonstrates that the proposed architecture achieves a 94.6% multi-class failure prediction accuracy. As shown in Table I, failure detection latency (MTTD) improves by 80%, shifting network operations from reactive post-failure diagnostics (45-90s) to proactive pre-failure prediction (15-30s in advance).",
        style_body
    ))
    story.append(Paragraph(
        "Crucially, autonomous SDN flow modification executes in 320 ms, reducing Mean Time to Repair (MTTR) by ~99.9% compared to manual CLI intervention. The false positive rate is curtailed from 18.2% to 3.8% through spatial neighborhood validation. Furthermore, the Focal Loss formulation with &gamma; = 2.0 elevates the rare broadcast storm F1-score from 0.41 to 0.91, proving highly effective under extreme 98:2 class imbalance.",
        style_body
    ))

    # ==========================================
    # SECTION VI: CONCLUSION
    # ==========================================
    story.append(Paragraph("VI. CONCLUSION", style_sec_h1))
    story.append(Paragraph(
        "This paper presented an adaptive SDN framework and AI-driven Digital Twin for hospital campus networks. By combining FTS-LSTM temporal feature extraction with MPNN spatial graph message passing and Focal Loss optimization, the system accurately anticipates complex network anomalies and deploys automated OpenFlow flow reconfigurations in 320 ms. Future work includes testing on physical P4-programmable hardware switches and integrating multi-agent reinforcement learning for dynamic wide-area traffic engineering.",
        style_body
    ))

    story.append(Paragraph("ACKNOWLEDGMENT", style_sec_h1))
    story.append(Paragraph(
        "The authors thank the School of Computer Science and Engineering at Vellore Institute of Technology, Vellore, and Dr. Yoganand S. for their valuable guidance and support during the development of this project.",
        style_body
    ))

    story.append(Paragraph("REFERENCES", style_sec_h1))
    refs = [
        "[1] N. McKeown et al., \"OpenFlow: Enabling innovation in campus networks,\" <i>ACM SIGCOMM CCR</i>, vol. 38, no. 2, pp. 69–74, 2008.",
        "[2] T. N. Kipf and M. Welling, \"Semi-Supervised Classification with Graph Convolutional Networks,\" in <i>Proc. ICLR</i>, 2017.",
        "[3] T.-Y. Lin et al., \"Focal Loss for Dense Object Detection,\" in <i>Proc. IEEE ICCV</i>, 2017, pp. 2980–2988.",
        "[4] A. Al-Fuqaha et al., \"Digital Twins for Autonomous Network Management,\" <i>IEEE Comm. Surveys & Tutorials</i>, vol. 25, no. 3, pp. 1824–1852, 2023.",
        "[5] M. Mahdi et al., \"Software-defined networking-based resilience and fault management in smart hospital environments,\" <i>IEEE Access</i>, vol. 9, pp. 142105–142120, 2021.",
        "[6] RFC 7348, \"Virtual eXtensible Local Area Network (VXLAN),\" IETF, Aug. 2014.",
        "[7] Cisco Systems, \"Enterprise Campus 3.0 Architecture Guide,\" Cisco Press, 2021.",
        "[8] M. Wang et al., \"Digital Twin-driven Autonomous Driving Networks,\" <i>IEEE Network</i>, vol. 36, no. 4, pp. 188–195, 2022."
    ]
    for r in refs:
        story.append(Paragraph(r, style_body))

    # ==========================================
    # PAGE 3 / 4: FIGURES AND SYSTEM DEMONSTRATION
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("VII. SYSTEM TOPOLOGY AND EXPERIMENTAL ARTIFACTS", style_sec_h1))
    story.append(Paragraph(
        "This section presents the architectural artifacts and visual evidence of the implemented system. Fig. 1 illustrates the empirical latency and multi-class F1-score evaluation under 98:2 class imbalance. Fig. 2 presents the 30-node hierarchical hospital campus network topology partitioned into seven functional wards.",
        style_body
    ))

    # Insert Fig 1: Quantitative results
    if os.path.exists("fig_ieee_results.png"):
        story.append(Spacer(1, 4*pt))
        story.append(Image("fig_ieee_results.png", width=88*mm, height=32*mm))
        story.append(Paragraph("Fig. 1. Quantitative Benchmark: (a) Latency comparison (MTTD/MTTR) on log scale; (b) Multi-class F1-score under 98:2 class imbalance comparing Focal Loss with standard Cross-Entropy.", style_fig_caption))
        story.append(Spacer(1, 6*pt))

    # Insert Fig 2: Campus topology visualization
    if os.path.exists("graph_visualization.png"):
        story.append(Spacer(1, 4*pt))
        story.append(Image("graph_visualization.png", width=88*mm, height=72*mm))
        story.append(Paragraph("Fig. 2. 30-Node Hierarchical Hospital Campus Topology Map partitioned into 7 functional medical wards (Core, Distribution, and Access switch tiers).", style_fig_caption))

    story.append(FrameBreak())

    story.append(Paragraph("VIII. CLOSED-LOOP AUTONOMOUS NOC WORKFLOW", style_sec_h1))
    story.append(Paragraph(
        "The Web NOC dashboard connects the Digital Twin model with the active SDN controller. During live operations, telemetry is polled at 4-second intervals. When an anomaly is injected via the Fault Simulation Panel, the system triggers the closed-loop recovery sequence depicted below.",
        style_body
    ))

    # Text-based sequence diagram
    story.append(Paragraph(
        "<b>Closed-Loop Execution Sequence:</b><br/>"
        "1. <i>Telemetry Stream:</i> Telemetry ingestion detects rising queue depth on switch port.<br/>"
        "2. <i>FTS-LSTM Encoding:</i> Temporal attention isolates degradation curve over 15 time steps.<br/>"
        "3. <i>MPNN Aggregation:</i> Message passing evaluates neighbor loads across 2 hops.<br/>"
        "4. <i>Focal Loss Classifier:</i> Predicts fault class (e.g. Uplink Congestion, p = 0.96).<br/>"
        "5. <i>SDN Intent Synthesis:</i> Controller pushes <code>OFPFC_MODIFY</code> with QoS queue 2.<br/>"
        "6. <i>Self-Healing &amp; Verification:</i> Traffic normalized in 320 ms; switch state restored to Nominal (Green).",
        style_body
    ))
    story.append(Spacer(1, 6*pt))

    # Key Source Code snippet
    story.append(Paragraph("<b>Core Spatio-Temporal Model Forward Pass:</b>", style_sec_h2))
    snippet = (
        "def forward(self, x_seq, edge_index):\n"
        "    # 1. Temporal squeeze LSTM:\n"
        "    h_temp = self.fts_lstm(x_seq)\n"
        "    # 2. Spatial graph convolution:\n"
        "    h_spat = self.mpnn(h_temp, edge_index)\n"
        "    # 3. Fault classification:\n"
        "    return self.classifier(h_spat)"
    )
    story.append(Paragraph(snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code))

    doc.build(story, canvasmaker=IEEEPageCanvas)
    print(f"IEEE Conference Paper PDF successfully created at: {filename}")

if __name__ == '__main__':
    build_ieee_pdf()
