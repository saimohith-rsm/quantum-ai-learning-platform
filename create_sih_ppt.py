"""
Generates the official SIH 2026 Presentation PowerPoint (.pptx)
strictly formatted according to Smart India Hackathon guidelines.
"""
import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen format
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette
    BG_COLOR = RGBColor(10, 15, 30)        # Deep Navy / Space
    CARD_BG = RGBColor(20, 28, 55)         # Card Navy
    CYAN = RGBColor(6, 182, 212)           # Quantum Cyan
    GREEN = RGBColor(16, 185, 129)         # Success Green
    WHITE = RGBColor(255, 255, 255)        # Pure White
    LIGHT_GRAY = RGBColor(203, 213, 225)   # Slate 300
    MUTED = RGBColor(148, 163, 184)        # Slate 400
    GOLD = RGBColor(245, 158, 11)          # Amber / Gold

    def apply_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background() # no line

    def add_header(slide, title_text, category_text="Smart India Hackathon 2026 | Problem #26140"):
        # Header banner
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_sub = tf.paragraphs[0]
        p_sub.text = category_text.upper()
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = CYAN
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s1)
    
    # Title Box
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(3.0))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GOLD
    
    p = tf.add_paragraph()
    p.text = "QuantumAI: Interactive Quantum Algorithm Learning Platform"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "Democratizing Quantum Computing Education with Interactive 3D Visualizations, Real-Time Tensor Simulation, and an Embedded AI Tutor"
    p.font.size = Pt(15)
    p.font.color.rgb = LIGHT_GRAY

    # Details Box (Grid)
    detail_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.2))
    detail_box.fill.solid()
    detail_box.fill.fore_color.rgb = CARD_BG
    detail_box.line.color.rgb = CYAN
    detail_box.line.width = Pt(1.5)
    
    dtf = detail_box.text_frame
    dtf.word_wrap = True
    dtf.margin_left = Inches(0.4)
    dtf.margin_top = Inches(0.25)
    
    fields = [
        ("Problem Statement ID:", "26140", "Theme:", "Smart Education"),
        ("Problem Statement Title:", "AI-Based Interactive Quantum Algorithm Learning Platform", "Category:", "Software"),
        ("Team Name:", "Human X (Team ID: TEAM-186)", "Target Audience:", "Higher Education, Schools, STEM Researchers")
    ]
    for i, (l1, v1, l2, v2) in enumerate(fields):
        p = dtf.paragraphs[0] if i == 0 else dtf.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{l1:<26} "
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = CYAN
        
        run2 = p.add_run()
        run2.text = f"{v1:<50} "
        run2.font.bold = False
        run2.font.size = Pt(12)
        run2.font.color.rgb = WHITE
        
        run3 = p.add_run()
        run3.text = f"{l2:<18} "
        run3.font.bold = True
        run3.font.size = Pt(12)
        run3.font.color.rgb = GOLD
        
        run4 = p.add_run()
        run4.text = f"{v2}\n"
        run4.font.bold = False
        run4.font.size = Pt(12)
        run4.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 2: Problem Description & Proposed Solution
    # =========================================================================
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s2)
    add_header(s2, "Idea & Proposed Solution Overview")

    # Left Box: The Problem
    b1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    b1.fill.solid()
    b1.fill.fore_color.rgb = CARD_BG
    b1.line.color.rgb = RGBColor(239, 68, 68) # Red alert border
    b1.line.width = Pt(1)
    
    tf1 = b1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.3)
    tf1.margin_top = Inches(0.3)
    
    p = tf1.paragraphs[0]
    p.text = "🚨 The Problem & Bottlenecks"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(248, 113, 113)
    p.space_after = Pt(14)
    
    points1 = [
        "High Mathematical Barrier: Quantum concepts (superposition, phase kickback, entanglement) are taught through heavy linear algebra and matrices, deterring 80%+ of STEM students.",
        "Lack of Intuitive Visual Tools: Existing simulators either lack dynamic 3D visualizations or only show final probabilistic histograms without step-by-step gate evolution.",
        "Absence of Intelligent Guidance: When circuits fail or algorithms yield wrong states, students receive no automated diagnostics or Socratic hints.",
        "National Skill Gap: India's National Quantum Mission (NQM) requires 10,000+ quantum researchers, but universities lack accessible, zero-cost quantum lab infrastructure."
    ]
    for pt in points1:
        p = tf1.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = LIGHT_GRAY
        p.space_after = Pt(10)

    # Right Box: The Solution
    b2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    b2.fill.solid()
    b2.fill.fore_color.rgb = CARD_BG
    b2.line.color.rgb = GREEN
    b2.line.width = Pt(1)
    
    tf2 = b2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.3)
    tf2.margin_top = Inches(0.3)
    
    p = tf2.paragraphs[0]
    p.text = "💡 Our Proposed Solution: QuantumAI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_after = Pt(14)
    
    points2 = [
        "Multi-Qubit Visual Timeline: Drag-and-drop circuit canvas with a step scrubber that reveals exact statevector evolution at each gate instant.",
        "Interactive 3D Bloch Sphere: Orbiting Three.js Bloch sphere mapping qubit state vectors, phase shifts, and state trajectories in real-time.",
        "AI Quantum Tutor & Bug Detective: Intelligent AI engine explaining quantum mechanics, diagnosing circuit bugs, and offering tiered Socratic hints.",
        "Challenge Arena with Automated Fidelity Grading: Practice algorithmic quests (Bell States, Grover's Oracle, Teleportation) with instant test grading.",
        "Direct Qiskit & OpenQASM 2.0 Export: Bridges visual learning to industry code, generating runnable IBM Qiskit 1.0+ Python scripts."
    ]
    for pt in points2:
        p = tf2.add_paragraph()
        p.text = "✔ " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: Technical Architecture & Core Modules
    # =========================================================================
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s3)
    add_header(s3, "Technical Architecture & Implementation Flow")

    cards = [
        ("1. Frontend Tier", "React 18 + Vite + Tailwind CSS", [
            "Timeline Canvas: Visual gate placement grid with instant reactive updates",
            "3D Bloch Sphere: Three.js WebGL visualization with spherical coordinates (θ, φ)",
            "Statevector Inspector: Complex amplitude bars, phase color wheels & histograms",
            "Gamification UI: XP counter, tiered badge unlock modal, and guided lesson player"
        ], CYAN),
        ("2. Quantum Engine", "Python 3.12 + NumPy Tensor Math", [
            "Exact Simulation: Kronecker tensor product statevector evolution over 2^n space",
            "Supported Gates: H, X, Y, Z, S, T, Phase, RX, RY, RZ, CNOT, CZ, SWAP, Toffoli (CCX)",
            "Bloch Vector Mapping: Reduced density matrices & partial trace per qubit",
            "Monte Carlo Sampling: Configurable shot simulation (100–8192 shots)"
        ], GREEN),
        ("3. AI Tutor & Persistence", "FastAPI + SQLite + SQLAlchemy", [
            "AI Tutor Engine: Context-aware circuit graph parser, bug detection & explanation",
            "Automated Grader: Quantum state fidelity inner product computation |⟨ψ_target|ψ⟩|²",
            "SQLite Persistence: Users, saved circuits, learning progress, and challenge logs",
            "100% Offline Ready: Runs completely local without third-party API dependencies"
        ], GOLD)
    ]
    
    for i, (title, subtitle, bullets, color) in enumerate(cards):
        x = Inches(0.8 + i * 4.0)
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.7), Inches(5.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = color
        c.line.width = Pt(1.5)
        
        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.25)
        ctf.margin_top = Inches(0.25)
        
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        
        p = ctf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(11)
        p.font.color.rgb = MUTED
        p.space_after = Pt(12)
        
        for b in bullets:
            p = ctf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(11)
            p.font.color.rgb = LIGHT_GRAY
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 4: Innovation & Comparative Advantage
    # =========================================================================
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s4)
    add_header(s4, "Innovation & Competitive Benchmarking")

    # Table comparing features
    rows = 6
    cols = 5
    table_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.0))
    table = table_shape.table
    
    headers = ["Features / Capabilities", "IBM Quantum Composer", "Quirk Simulator", "Brilliant / Blackbird", "Our QuantumAI Platform"]
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 75)
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = CYAN if col_idx == 4 else WHITE
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    matrix = [
        ("Interactive 3D Bloch Sphere", "Static / Separate", "Basic 2D display", "Pre-rendered / Static", "⭐ Fully Interactive 3D (Three.js)"),
        ("Embedded AI Tutor & Bug Detector", "❌ None", "❌ None", "Limited hints", "⭐ Full Circuit Explainer & Diagnostics"),
        ("Automated Challenge Fidelity Grader", "❌ None", "❌ None", "Multiple Choice Only", "⭐ Exact Quantum Fidelity Testing"),
        ("100% Offline / Zero-Cost Deployment", "Requires Cloud / Account", "Client-side only", "Paid Subscription", "⭐ 100% Free & Fully Local Offline"),
        ("Export to Real IBM Qiskit 1.0+ Code", "Yes (Qiskit)", "OpenQASM only", "Proprietary", "⭐ Runnable Python Qiskit & QASM")
    ]
    for row_idx, row_data in enumerate(matrix, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(18, 25, 48) if row_idx % 2 == 0 else RGBColor(14, 20, 40)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = GREEN if col_idx == 4 else (RGBColor(248, 113, 113) if "❌" in text else LIGHT_GRAY)
            p.font.bold = (col_idx == 4)
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Footer note on innovation
    fbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.1))
    fbox.fill.solid()
    fbox.fill.fore_color.rgb = CARD_BG
    fbox.line.color.rgb = GOLD
    ftf = fbox.text_frame
    ftf.margin_left = Inches(0.3)
    p = ftf.paragraphs[0]
    p.text = "🔑 Key Innovation Highlight:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p = ftf.add_paragraph()
    p.text = "Unlike static text-heavy courses, QuantumAI uses an active-recall pedagogical loop: Students build visual circuits, inspect real-time 3D Bloch evolution, receive AI Socratic diagnosis on errors, and validate solutions with automated state fidelity grading."
    p.font.size = Pt(11)
    p.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 5: Feasibility, Testing & Viability
    # =========================================================================
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s5)
    add_header(s5, "Feasibility, Testing & Deployment Viability")

    points_data = [
        ("✔ 100% Operational Prototype", "Complete end-to-end working system already built, containerized, and passing 22/22 unit and integration tests with pytest.", CYAN),
        ("✔ Zero Cloud & Hardware Cost", "No expensive IBM QPU cloud fees or paid LLM APIs required for core operation. Runs comfortably on any standard college student laptop.", GREEN),
        ("✔ High Performance & Scalability", "FastAPI backend handles tensor evaluations in milliseconds. Vite frontend renders 60 FPS 3D Bloch spheres via WebGL hardware acceleration.", GOLD),
        ("✔ Plug-and-Play Launch", "One-click deployment script (start_all.bat / tasks.json in VS Code) ensures effortless setup for professors and students.", WHITE)
    ]
    
    for i, (head, desc, color) in enumerate(points_data):
        y = Inches(1.6 + i * 1.35)
        bx = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.15))
        bx.fill.solid()
        bx.fill.fore_color.rgb = CARD_BG
        bx.line.color.rgb = color
        bx.line.width = Pt(1)
        
        btf = bx.text_frame
        btf.margin_left = Inches(0.3)
        btf.margin_top = Inches(0.18)
        
        p = btf.paragraphs[0]
        p.text = head
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        
        p = btf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = LIGHT_GRAY

    # =========================================================================
    # SLIDE 6: National Impact, Social Relevance & Future Roadmap
    # =========================================================================
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s6)
    add_header(s6, "Impact, National Relevance & Future Roadmap")

    # Left box: National relevance
    b_imp = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    b_imp.fill.solid()
    b_imp.fill.fore_color.rgb = CARD_BG
    b_imp.line.color.rgb = CYAN
    b_imp.line.width = Pt(1)
    
    itf = b_imp.text_frame
    itf.word_wrap = True
    itf.margin_left = Inches(0.3)
    itf.margin_top = Inches(0.3)
    
    p = itf.paragraphs[0]
    p.text = "🇮🇳 Alignment with National Quantum Mission (NQM)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.space_after = Pt(12)
    
    impact_bullets = [
        "Workforce Readiness: Directly supports India's NQM mandate to train 10,000+ quantum researchers and developers across Tier-1, 2, and 3 universities.",
        "Bridging Education Inequality: Requires only a web browser, allowing government colleges and rural institutions to teach cutting-edge quantum science with zero licensing fees.",
        "Industry Bridge: Exports production-grade IBM Qiskit Python code, making learners immediately employable in quantum research labs.",
        "Interactive STEM Pedagogy: Implements NEP 2020 experiential learning guidelines through gamified problem-solving quests."
    ]
    for b in impact_bullets:
        p = itf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_after = Pt(8)

    # Right box: Future Roadmap
    b_road = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    b_road.fill.solid()
    b_road.fill.fore_color.rgb = CARD_BG
    b_road.line.color.rgb = GOLD
    b_road.line.width = Pt(1)
    
    rtf = b_road.text_frame
    rtf.word_wrap = True
    rtf.margin_left = Inches(0.3)
    rtf.margin_top = Inches(0.3)
    
    p = rtf.paragraphs[0]
    p.text = "🗺️ Development Roadmap"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(12)
    
    roadmap = [
        ("Phase 1: Working Prototype (COMPLETED)", "Visual circuit timeline, exact statevector engine, 3D Bloch sphere, AI tutor & 22 unit tests."),
        ("Phase 2: Real Hardware & Cloud Execution", "Direct API integration with IBM Quantum cloud and AWS Braket to dispatch circuits to real physical superconducting QPUs."),
        ("Phase 3: Multi-Language Vernacular Support", "Expanding curriculum & AI Tutor to support Hindi, Tamil, Telugu, and other regional Indian languages."),
        ("Phase 4: Advanced Quantum Algorithms", "Interactive modules for Quantum Approximate Optimization (QAOA), Variational Quantum Eigensolver (VQE), and Quantum Machine Learning (QML).")
    ]
    for phase, pdesc in roadmap:
        p = rtf.add_paragraph()
        r1 = p.add_run()
        r1.text = phase + "\n"
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = GREEN if "COMPLETED" in phase else GOLD
        
        r2 = p.add_run()
        r2.text = pdesc
        r2.font.size = Pt(11)
        r2.font.color.rgb = LIGHT_GRAY
        p.space_after = Pt(8)

    output_path = r"C:\Users\rvnsm\OneDrive\Desktop\sihh\SIH_2026_QuantumAI_Presentation.pptx"
    prs.save(output_path)
    
    # Also copy directly to Desktop
    desktop_path = r"C:\Users\rvnsm\OneDrive\Desktop\SIH_2026_QuantumAI_Presentation.pptx"
    shutil.copy2(output_path, desktop_path)
    print(f"Presentation saved to {output_path} and {desktop_path}")

if __name__ == "__main__":
    create_presentation()
