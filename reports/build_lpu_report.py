import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()
    
    # Page Setup: A4, 1.25" Left margin (for binding), 1" Right, Top, Bottom
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        
        # Header / Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("Lovely Professional University | Department of CSE/IT")
        frun.font.name = 'Times New Roman'
        frun.font.size = Pt(9)
        frun.font.italic = True
        frun.font.color.rgb = RGBColor(128, 128, 128)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    screenshot_dir = r"D:\Road-Accident-Prediction-Analytics\reports\screenshots"
    logo_path = r"D:\Road-Accident-Prediction-Analytics\reports\lpu_logo.png"

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=12, space_before=0, space_after=6, color=None):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
            if color:
                run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.bold = True
        run.font.color.rgb = RGBColor(16, 44, 87) # Deep academic navy
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(40, 60, 100)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.bold = True
        run.italic = True
        return p

    def add_img(filename, caption):
        full_path = os.path.join(screenshot_dir, filename)
        if os.path.exists(full_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run()
            run.add_picture(full_path, width=Inches(5.8))
            
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(2)
            cp.paragraph_format.space_after = Pt(12)
            crun = cp.add_run(caption)
            crun.font.name = 'Times New Roman'
            crun.font.size = Pt(10)
            crun.font.italic = True
            crun.bold = True
            crun.font.color.rgb = RGBColor(60, 60, 60)
        else:
            add_p(f"[Image Missing: {filename}]", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

    def create_table(headers, rows, col_widths=None):
        table = doc.add_table(rows=len(rows)+1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            cell.text = header_text
            set_cell_background(cell, "1F4E79") # Professional Navy Blue
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)
                    run.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
        
        # Data Rows
        for r_idx, row_data in enumerate(rows):
            row_cells = table.rows[r_idx+1].cells
            bg_color = "F2F5F9" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.text = str(val)
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    if c_idx == 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in p.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(9.5)
                        
        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)
                    
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(6)
        return table

    print("Building Project Report according to LPU CSE/IT guidelines...")

    # =========================================================================
    # 1. COVER PAGE (With LPU Logo & exact university guidelines)
    # Line 3 is 16pt bold, other lines 12pt, centered. Department & Institute bold.
    # =========================================================================
    add_p("<INT234 PREDICTIVE ANALYTICS>", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=10)
    add_p("PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=4)
    add_p("(Project Semester January-April 2025)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=6, space_after=14)

    # LPU Logo
    if os.path.exists(logo_path):
        lp = doc.add_paragraph()
        lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        lp.paragraph_format.space_before = Pt(4)
        lp.paragraph_format.space_after = Pt(14)
        lrun = lp.add_run()
        lrun.add_picture(logo_path, width=Inches(1.5))

    add_p("ROAD ACCIDENT PREDICTION AND ANALYTICS DASHBOARD USING MACHINE LEARNING", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=16, space_before=4, space_after=24, color=RGBColor(16, 44, 87))

    add_p("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=6)
    add_p("Rishikesh Das", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=3)
    add_p("Registration No: 12412585", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=2)
    add_p("Programme and Section: BTECH Computer Science and Engineering K3P24MW", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=2)
    add_p("Course Code: INT234", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=2, space_after=20)

    add_p("Under the Guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=6)
    add_p("Dr. Madhu Bala", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=3)
    add_p("Faculty Coordinator & Associate Professor", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=2, space_after=24)

    add_p("Discipline of CSE/IT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=8)
    add_p("Lovely School of Computer Science and Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=2)
    add_p("Lovely Professional University, Phagwara", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=2)

    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE (Exact university format)
    # =========================================================================
    add_p("CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=10, space_after=24)

    add_p("This is to certify that Rishikesh Das bearing Registration no. 12412585 has completed INT234 project titled, “Road Accident Prediction and Analytics Dashboard Using Machine Learning” under my guidance and supervision. To the best of my knowledge, the present work is the result of his/her original development, effort and study.", space_before=14, space_after=40)

    add_p("Signature and Name of the Supervisor: ___________________________", space_before=30)
    add_p("Dr. Madhu Bala", bold=True, size=12, space_before=4)
    add_p("Designation of the Supervisor: Associate Professor", size=12, space_before=2)
    add_p("School of Computer Science and Engineering", size=12, space_before=2)
    add_p("Lovely Professional University", size=12, space_before=2)
    add_p("Phagwara, Punjab.", size=12, space_before=2)
    add_p("Date: ________________________", size=12, space_before=14)

    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION (Updated: Removed sign portion, Date: 31.10.2026)
    # =========================================================================
    add_p("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=10, space_after=24)

    add_p("I, Rishikesh Das, student of BTECH Computer Science and Engineering under CSE/IT Discipline at, Lovely Professional University, Punjab, hereby declare that all the information furnished in this project report is based on my own intensive work and is genuine.", space_before=14, space_after=40)

    add_p("Date: 31.10.2026", bold=True, size=12, space_before=40)
    add_p("Registration No: 12412585", bold=True, size=12, space_before=6)
    add_p("Name of the student: Rishikesh Das", bold=True, size=12, space_before=6)

    doc.add_page_break()

    # =========================================================================
    # 4. ACKNOWLEDGEMENT
    # =========================================================================
    add_p("ACKNOWLEDGEMENT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=10, space_after=24)

    add_p("I express my profound gratitude and sincere appreciation to my esteemed faculty guide, Dr. Madhu Bala, Associate Professor, Lovely School of Computer Science and Engineering, Lovely Professional University, for her inspiring guidance, continuous encouragement, and invaluable suggestions throughout the development of this minor project in INT234 Predictive Analytics.", space_before=6)

    add_p("Her constructive critique and technical mentorship have played an instrumental role in shaping the mathematical formulation, algorithmic pipelines, and analytical rigor of this project.", space_before=6)

    add_p("I extend my heartfelt thanks to the Head of Department, Discipline of CSE/IT, and the faculty members of Lovely Professional University for fostering an exceptional academic ecosystem, state-of-the-art computational infrastructure, and rigorous learning environment.", space_before=6)

    add_p("Furthermore, I acknowledge the UK Department for Transport (DfT) for making the STATS19 Road Safety database publicly accessible, enabling authentic, real-world data science research. Finally, I thank my parents and peers for their unconditional support and encouragement during this academic pursuit.", space_before=6, space_after=30)

    add_p("Rishikesh Das", bold=True, size=12, space_before=20)
    add_p("Registration No: 12412585", size=12)
    add_p("Discipline of CSE/IT, Lovely Professional University", size=12)

    doc.add_page_break()

    # =========================================================================
    # 5. TABLE OF CONTENTS
    # =========================================================================
    add_p("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=10, space_after=18)

    toc_items = [
        ("Certificate", "ii"),
        ("Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("List of Figures", "vii"),
        ("List of Tables", "ix"),
        ("1. Introduction", "1"),
        ("   1.1 Background and Research Motivation", "1"),
        ("   1.2 Problem Statement", "2"),
        ("   1.3 Project Objectives", "3"),
        ("   1.4 Project Scope and Technical Deliverables", "4"),
        ("   1.5 System Architecture Overview", "5"),
        ("2. Source of Dataset", "6"),
        ("   2.1 UK Department for Transport (DfT) STATS19 System", "6"),
        ("   2.2 Raw Dataset Exploration and Schema", "7"),
        ("   2.3 Data Extraction and Scalable Chunk Processing Pipeline", "8"),
        ("   2.4 Attribute Dictionary and Feature Semantics", "9"),
        ("   2.5 Target Variable Definition and Imbalance Characterization", "11"),
        ("3. Exploratory Data Analysis (EDA) Process", "12"),
        ("   3.1 Data Cleansing and Sanitization Protocol", "12"),
        ("   3.2 Missing Value Audit and Treatment", "13"),
        ("   3.3 Geographical Validation and Spatial Outlier Handling", "14"),
        ("   3.4 Univariate Distribution Analysis", "15"),
        ("   3.5 Bivariate and Multivariate Correlation Analysis", "16"),
        ("   3.6 Geospatial Kernel Density Heatmap Analysis", "18"),
        ("   3.7 Temporal Rhythms and Diurnal Accident Patterns", "20"),
        ("4. Analysis on Dataset", "22"),
        ("   4.1 Regression Analysis: Monthly Accident Volume Prediction", "22"),
        ("       4.1.1 Introduction", "22"),
        ("       4.1.2 General Description", "22"),
        ("       4.1.3 Specific Requirements, Functions, and Mathematical Formulas", "23"),
        ("       4.1.4 Empirical Results and Model Performance", "25"),
        ("       4.1.5 Visualization and Interpretation", "26"),
        ("   4.2 Supervised Learning: Collision Severity Classification", "27"),
        ("       4.2.1 Introduction", "27"),
        ("       4.2.2 General Description", "27"),
        ("       4.2.3 Specific Requirements, Functions, and Mathematical Formulas", "28"),
        ("       4.2.4 Empirical Results and Metric Benchmarking", "31"),
        ("       4.2.5 Visualization and Confusion Matrix Analysis", "33"),
        ("   4.3 Unsupervised Learning: Accident Pattern Clustering", "34"),
        ("       4.3.1 Introduction", "34"),
        ("       4.3.2 General Description", "34"),
        ("       4.3.3 Specific Requirements, Functions, and Mathematical Formulas", "35"),
        ("       4.3.4 Empirical Results and Cluster Profiles", "37"),
        ("       4.3.5 Visualization and Principal Component Cluster Scatter", "39"),
        ("   4.4 Dimensionality Reduction: Principal Component Analysis (PCA)", "40"),
        ("       4.4.1 Introduction", "40"),
        ("       4.4.2 General Description", "40"),
        ("       4.4.3 Specific Requirements, Functions, and Mathematical Formulas", "41"),
        ("       4.4.4 Empirical Results and Scree Variance Decomposition", "43"),
        ("       4.4.5 Visualization and Eigenvector Factor Loadings", "44"),
        ("   4.5 Neural Network Modeling: Multi-Layer Perceptron (MLP)", "45"),
        ("       4.5.1 Introduction", "45"),
        ("       4.5.2 General Description", "45"),
        ("       4.5.3 Specific Requirements, Functions, and Mathematical Formulas", "46"),
        ("       4.5.4 Empirical Results and Optimization Trajectory", "48"),
        ("       4.5.5 Visualization and Loss Convergence Curve", "49"),
        ("   4.6 Ensemble Benchmarking and Gini Feature Importance", "50"),
        ("       4.6.1 Introduction", "50"),
        ("       4.6.2 Bias-Variance Decomposition and Ensemble Formulations", "50"),
        ("       4.6.3 Master Leaderboard and Comparative Rankings", "52"),
        ("       4.6.4 Visualization of Master Rankings and Risk Factors", "53"),
        ("   4.7 Full-Stack Interactive Decision-Support Dashboard", "54"),
        ("       4.7.1 Web Application Architecture and Leaflet/CARTO Integration", "54"),
        ("       4.7.2 Interactive Risk Calculator and Scenario Simulator", "55"),
        ("5. Conclusion", "57"),
        ("6. Future Scope", "59"),
        ("7. References", "61"),
        ("8. Dataset Access, Links & Repository Sources", "63")
    ]

    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if item.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "Certificate", "Table")):
            r1.bold = True
            
        dots = " " + "." * max(5, 75 - len(item)) + " "
        r2 = p.add_run(dots)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(160, 160, 160)
        
        r3 = p.add_run(page)
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(11)
        r3.bold = True

    doc.add_page_break()

    # =========================================================================
    # 6. LIST OF FIGURES & LIST OF TABLES
    # =========================================================================
    add_p("LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=10, space_after=18)

    figures = [
        ("Figure 1.1", "High-Level Predictive Analytics and Machine Learning System Architecture", "5"),
        ("Figure 2.1", "Chunk-based ETL and Validation Pipeline for STATS19 Microdata", "8"),
        ("Figure 3.1", "Executive Overview KPI Header Dashboard (513k records, 652k casualties)", "15"),
        ("Figure 3.2", "Annual Collision Microdata Volume and Severity Class Imbalance", "16"),
        ("Figure 3.3", "Interactive UK Geospatial Density Heatmap with CARTO Dark Matter Tiles", "19"),
        ("Figure 3.4", "Accident Temporal Heatmap Matrix (7x24 Day-Hour) & Pearson Correlation", "21"),
        ("Figure 4.1", "Accident Trends Module: Observed vs. Predicted Monthly Regression Trajectory", "26"),
        ("Figure 4.2", "Collision Severity Prediction Interface and Algorithmic Evaluation Suite", "33"),
        ("Figure 4.3", "K-Means Unsupervised Cluster Partitioning & PCA 2D Feature Scatter", "39"),
        ("Figure 4.4", "Hierarchical Agglomerative Clustering via Ward's Minimum Variance Linkage", "40"),
        ("Figure 4.5", "Dimensionality Reduction Scree Plot and Cumulative Explained Variance Curve", "44"),
        ("Figure 4.6", "Multi-Layer Perceptron (MLP) Deep Neural Network Loss Convergence Curve", "49"),
        ("Figure 4.7", "Master Algorithmic Leaderboard and Comparative Metric Benchmark", "53"),
        ("Figure 4.8", "Random Forest Gini Feature Importance and Risk Hierarchy Ranking", "54"),
        ("Figure 4.9", "Real-Time Scenario Simulator and Parameter Input Interface", "55"),
        ("Figure 4.10", "Live Severity Risk Probability Prediction Gauge and Mitigation Alert", "56")
    ]

    for f_id, f_desc, f_page in figures:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"{f_id}: {f_desc}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        
        dots = " " + "." * max(5, 75 - len(f"{f_id}: {f_desc}")) + " "
        r2 = p.add_run(dots)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(160, 160, 160)
        
        r3 = p.add_run(f_page)
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(10.5)
        r3.bold = True

    add_p("LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=24, space_after=18)

    tables_list = [
        ("Table 2.1", "STATS19 Primary Collision Attributes and Operational Data Types", "10"),
        ("Table 2.2", "Target Variable Severity Class Distribution and Imbalance Ratio", "11"),
        ("Table 3.1", "Data Cleansing and Missing Value Imputation Summary", "13"),
        ("Table 3.2", "Pearson Correlation Coefficients Among Numerical Collision Features", "17"),
        ("Table 4.1", "Regression Model Performance Comparison for Monthly Accident Counts", "25"),
        ("Table 4.2", "Supervised Classification Benchmark for Accident Severity Prediction", "31"),
        ("Table 4.3", "Confusion Matrix Breakdown Across Classification Architectures", "32"),
        ("Table 4.4", "K-Means Cluster Centroid Profiles and Operational Interpretations", "38"),
        ("Table 4.5", "Principal Component Eigenvalues, Variance Explained, and Loadings", "43"),
        ("Table 4.6", "Multi-Layer Perceptron (MLP) Architectural Hyperparameters", "47"),
        ("Table 4.7", "Comprehensive Master Evaluation Leaderboard across All Paradigms", "52")
    ]

    for t_id, t_desc, t_page in tables_list:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"{t_id}: {t_desc}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        
        dots = " " + "." * max(5, 75 - len(f"{t_id}: {t_desc}")) + " "
        r2 = p.add_run(dots)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(160, 160, 160)
        
        r3 = p.add_run(t_page)
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(10.5)
        r3.bold = True

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("1. INTRODUCTION")

    add_h2("1.1 Background and Research Motivation")
    add_p("Road traffic collisions represent one of the most critical public health and economic challenges confronting modern urbanized societies. According to the World Health Organization (WHO), road traffic injuries cause approximately 1.19 million preventable fatalities each year globally and remain the leading cause of death for children and young adults aged 5 to 29 years. In addition to the tragic loss of human life and long-term physical impairment, road vehicular collisions inflict catastrophic socioeconomic burdens, consuming an estimated 3% of gross domestic product (GDP) across industrialized nations due to medical treatment, emergency response expenditures, lost human economic productivity, and infrastructure property damage.")

    add_p("Traditionally, road safety management and traffic police enforcement have relied on post-incident retrospective analyses, static descriptive tables, and periodic historical summaries. While historical counts provide high-level policy awareness, they fail to provide proactive, actionable intelligence. In contemporary transportation systems, transportation planners and police authorities are inundated with vast streams of multi-dimensional incident data, spanning spatial coordinates, road physical geometry, speed limits, surface moisture conditions, ambient luminescence, and atmospheric weather states. The paradigm of Predictive Analytics and Machine Learning offers transformative potential: by moving from reactive reporting to anticipatory statistical modeling, modern computational algorithms can uncover latent interaction patterns, forecast impending collision volumes, and predict the injury severity of individual incidents before or as they unfold.")

    add_h2("1.2 Problem Statement")
    add_p("Accurately forecasting road accident occurrences and predicting collision injury severity presents formidable statistical and algorithmic complexities:")
    add_p("1. Severe Class Imbalance: In real-world road casualty microdata, non-fatal and minor collisions vastly outnumber fatal and critical injury incidents (often exceeding 80% slight injuries vs. under 2% fatal crashes). Standard loss functions trained naively on such skewed data suffer from severe majority-class bias, yielding deceptively high accuracy while utterly failing to identify life-threatening fatal events.")
    add_p("2. High-Dimensional Multimodal Interdependencies: Collision severity is not governed by a single isolated variable, but by non-linear combinations of human factors, environmental conditions (e.g., darkness coupled with unlit rural roads and wet surfaces), physical road layouts, and vehicle dynamics.")
    add_p("3. Temporal and Spatial Non-Stationarity: Accident frequencies exhibit pronounced temporal seasonality (diurnal commuter spikes, weekend nightlife clusters, winter weather degradation) and spatial clustering around complex urban intersections and high-speed rural motorways.")
    add_p("4. Black-Box Usability Gap: Complex machine learning models often remain opaque mathematical abstractions relegated to static research notebooks, leaving civic administrators and emergency responders without intuitive, interactive decision-support interfaces.")

    add_h2("1.3 Project Objectives")
    add_p("To resolve the aforementioned challenges and satisfy the academic rigors of the INT234 Predictive Analytics curriculum, this minor project accomplishes the following objectives:")
    add_p("• Ingest and Validate Large-Scale Real-World Microdata: Extract and clean 513,748 validated collision records spanning the 2021–2025 epoch from the official UK Department for Transport (DfT) STATS19 repository.")
    add_p("• Conduct Rigorous Exploratory Data Analysis (EDA): Execute multi-level spatial, temporal, and correlational audits, synthesizing geospatial density heatmaps, diurnal temporal matrices, and feature correlation structures.")
    add_p("• Develop Time-Series Macro-Level Regression Models: Formulate Ordinary Least Squares (OLS), Multiple Linear Regression, and Polynomial Regression frameworks to forecast monthly aggregated accident frequencies.")
    add_p("• Implement Cost-Sensitive Supervised Classification: Benchmark Logistic Regression, Decision Trees, Random Forests, Gradient Boosting, and Naive Bayes architectures to predict collision injury severity under severe class imbalance.")
    add_p("• Uncover Latent Behavioral and Environmental Clusters: Apply unsupervised K-Means (optimized via Elbow and Silhouette criteria) and Hierarchical Agglomerative Clustering (Ward's linkage) to discover inherent crash archetypes.")
    add_p("• Investigate Dimensionality Reduction and Deep Neural Representations: Conduct Principal Component Analysis (PCA) to evaluate orthogonal feature variance and benchmark Feedforward Multi-Layer Perceptrons (MLP).")
    add_p("• Architect a Production-Grade Interactive Web Dashboard: Build a full-stack Flask application integrating CARTO Dark Matter geospatial layers, dynamic heatmaps, and a real-time risk simulation engine.")

    add_h2("1.4 Project Scope and Technical Deliverables")
    add_p("The project scope encompasses end-to-end data engineering, statistical modeling, algorithmic optimization, and UI/UX software engineering. The tangible artifacts produced include:")
    add_p("1. Validated Preprocessed Datasets: A 100,000-record stratified collision sample and a 60-month macro-temporal aggregated regression time-series.")
    add_p("2. Serialized Predictive Models: Production-ready Scikit-Learn `.pkl` artifacts (Random Forest, Decision Tree, Logistic Regression, Gaussian Naive Bayes, K-Means, PCA Transformer, and Standard Scaler).")
    add_p("3. Comprehensive Master Jupyter Notebook: A 25-cell executable Python research notebook (`UK_Road_Accident_Predictive_Analytics.ipynb`) detailing all empirical proofs and mathematical steps.")
    add_p("4. Interactive Full-Stack Web Application: A modular Flask web platform (`app.py`) featuring 9 interactive views, real-time inferencing, and live geospatial heatmaps.")

    add_h2("1.5 System Architecture Overview")
    add_p("The operational architecture follows a decoupled, three-tier data science pipeline: Data Ingestion & Engineering Tier, Machine Learning Model Tier, and the Presentation & Decision Support Tier.")

    add_p("Figure 1.1: High-Level Predictive Analytics and Machine Learning System Architecture", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10, italic=True)
    arch_headers = ["Tier", "Core Subsystems", "Technologies & Modules", "Output Deliverables"]
    arch_rows = [
        ["Data Engineering Tier", "Raw STATS19 CSV ingestion, chunk streaming, coordinate validation, missing value imputation, stratified sampling", "Python, Pandas, NumPy, Chunk-based streaming", "Cleaned 100k stratified CSV, 60-month time-series, JSON feature metadata"],
        ["Modeling Tier", "Supervised Classification, Macro Regression, Unsupervised K-Means/Ward Clustering, PCA, Feedforward MLP Neural Net", "Scikit-Learn, SciPy, Matplotlib, Seaborn", "Serialized `.pkl` models, metric JSONs, Scree plots, loss curves, confusion matrices"],
        ["Web Application Tier", "Flask RESTful server, Jinja2 template engine, Leaflet.js CARTO Dark Matter mapping, Chart.js visualizations", "Flask 3.1, HTML5, Modern CSS, Leaflet.js, CARTO API", "Interactive browser dashboard, real-time risk simulator, 7x24 temporal heatmaps"]
    ]
    create_table(arch_headers, arch_rows, [1.4, 2.2, 1.6, 1.8])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: SOURCE OF DATASET
    # =========================================================================
    add_h1("2. SOURCE OF DATASET")

    add_h2("2.1 UK Department for Transport (DfT) STATS19 System")
    add_p("The experimental foundations of this study are established upon the UK Department for Transport (DfT) Road Safety Open Data, formally designated as the STATS19 database. The STATS19 data collection protocol was established under the UK Road Traffic Act to record personal-injury road accidents reported to British police forces across England, Scotland, and Wales within 30 days of occurrence.")

    add_p("Unlike self-reported insurance registries or simulated academic toy datasets, STATS19 represents high-fidelity administrative microdata compiled by trained police attending officers. Each collision event encapsulates detailed circumstantial evidence concerning the road environment, atmospheric weather conditions, vehicular mechanical characteristics, driver behaviors, and resultant physical casualties.")

    add_h2("2.2 Raw Dataset Exploration and Schema")
    add_p("The raw dataset furnished for this investigation comprises historical collision records archived from 1979 through the latest published reporting period, archived within a 1.46 GB compressed CSV file (`dft-road-casualty-statistics-collision-1979-latest-published-year.csv`). The comprehensive historical archive encompasses 9,116,625 individual collision records spanning 45 distinct attribute dimensions.")

    add_p("A longitudinal investigation of traffic safety data demonstrates that while historical trends over several decades are valuable for macroscopic civil policy, vehicle safety engineering (e.g., the introduction of electronic stability control, modern anti-lock braking systems, and Euro NCAP crash standards) and highway infrastructure have evolved radically. Utilizing 40-year-old collision data to train modern severity prediction models introduces severe temporal covariate shift. Consequently, this study isolates the latest five validated reporting years (2021 to 2025 inclusive). This 5-year contemporary window captures modern vehicle profiles, contemporary speed enforcement regimes, and up-to-date road infrastructure while offering a massive sample size of over half a million collisions.")

    add_h2("2.3 Data Extraction and Scalable Chunk Processing Pipeline")
    add_p("Due to the immense 1.46 GB file size and 9.1+ million rows, loading the entire raw file into random-access memory (RAM) is computationally intractable on standard workstations. To overcome this limitation, a memory-efficient chunk-based streaming extraction pipeline was developed using Python and Pandas.")

    add_p("The pipeline streams the raw CSV in discrete blocks of 100,000 rows. Within each chunk, an automated filtering predicate extracts records matching `collision_year in [2021, 2022, 2023, 2024, 2025]`. The extracted subset is accumulated into a persistent primary table. Across the 9.1 million scanned rows, exactly 513,801 collisions corresponded to the 2021–2025 period. An integrity validation step checked for null geographical coordinates (Latitude and Longitude) and duplicate transaction keys, successfully dropping 53 unlocalized records to yield exactly 513,748 clean, validated collision events.")

    add_h2("2.4 Attribute Dictionary and Feature Semantics")
    add_p("The extracted collision table contains 30 primary attributes. Table 2.1 delineates the most critical features selected for downstream predictive modeling and exploratory spatial analysis.")

    tab21_headers = ["Attribute Identifier", "Physical Real-World Meaning", "Storage Data Type", "Domain / Value Encoding"]
    tab21_rows = [
        ["collision_index", "Unique alphanumeric collision identifier", "String (Categorical)", "Standard UK police incident index"],
        ["collision_year", "Calendar year of collision occurrence", "Integer (Discrete)", "2021, 2022, 2023, 2024, 2025"],
        ["latitude / longitude", "Geographic WGS84 spatial coordinates", "Float (Continuous)", "Lat: [49.8, 60.9], Lon: [-7.6, 1.8]"],
        ["collision_severity", "Official injury classification level", "Integer (Ordinal)", "1 = Fatal, 2 = Serious, 3 = Slight"],
        ["number_of_vehicles", "Total motorized vehicles involved in crash", "Integer (Discrete)", "Positive integers (1 to 16 vehicles)"],
        ["number_of_casualties", "Total persons injured or deceased", "Integer (Discrete)", "Positive integers (1 to 28 casualties)"],
        ["speed_limit", "Legal statutory posted speed limit", "Integer (Discrete)", "20, 30, 40, 50, 60, 70 (mph)"],
        ["road_type", "Physical geometric road configuration", "Integer / Categorical", "Single carriageway, Dual, Roundabout, One-way"],
        ["light_conditions", "Ambient luminescence and street lighting", "Integer / Categorical", "Daylight, Darkness lit, Darkness unlit"],
        ["weather_conditions", "Atmospheric precipitation and visibility", "Integer / Categorical", "Fine, Raining, Snowing, Fog/Mist, High winds"],
        ["road_surface_conditions", "Tire-road frictional contact surface", "Integer / Categorical", "Dry, Wet/Damp, Snow, Frost/Ice, Flood"],
        ["urban_or_rural_area", "Surrounding land-use classification", "Integer (Binary)", "1 = Urban Area, 2 = Rural Area"]
    ]
    create_table(tab21_headers, tab21_rows, [1.6, 2.2, 1.4, 1.8])

    add_h2("2.5 Target Variable Definition and Imbalance Characterization")
    add_p("In the official STATS19 coding standard, collision severity is categorized into three ordinal levels: Fatal (Class 1), Serious (Class 2), and Slight (Class 3). For actionable traffic safety intervention, traffic engineers and emergency triage planners are fundamentally concerned with distinguishing between critical collisions (requiring immediate surgical intervention or hospital admission) versus minor property/superficial injury crashes.")

    add_p("Consequently, the target variable was formalized as a binary indicator: `is_severe`, where Fatal (Class 1) and Serious (Class 2) crashes are mapped to Class 1 (`Severe`), while Slight (Class 3) collisions are mapped to Class 0 (`Non-Severe / Slight`). Table 2.2 illuminates the pronounced class imbalance present across the full 513,748 validated dataset.")

    tab22_headers = ["Severity Classification", "STATS19 Code", "Binary Target", "Absolute Incident Count", "Percentage Share (%)"]
    tab22_rows = [
        ["Fatal Collision", "Class 1", "Severe (1)", "7,552", "1.47%"],
        ["Serious Injury Crash", "Class 2", "Severe (1)", "116,797", "22.73%"],
        ["Slight / Minor Injury", "Class 3", "Non-Severe (0)", "389,399", "75.80%"],
        ["Total Validated Collisions", "Classes 1, 2, 3", "All Incidents", "513,748", "100.00%"]
    ]
    create_table(tab22_headers, tab22_rows, [1.8, 1.3, 1.3, 1.6, 1.2])

    add_p("As documented in Table 2.2, non-severe collisions constitute 75.80% of all occurrences, whereas life-altering severe collisions account for 24.20% (with fatal crashes representing an ultra-rare 1.47%). To facilitate rapid, repeatable model training while strictly preserving empirical class distributions, a stratified random sample of exactly 100,000 collisions was extracted using `scikit-learn`'s `train_test_split` with stratification on `collision_severity`. This preserved the exact 75.8% to 24.2% ratio while enabling optimal computational throughput.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: EXPLORATORY DATA ANALYSIS (EDA) PROCESS
    # =========================================================================
    add_h1("3. EXPLORATORY DATA ANALYSIS (EDA) PROCESS")

    add_h2("3.1 Data Cleansing and Sanitization Protocol")
    add_p("Prior to statistical exploration, the 513,748 records were subjected to a rigorous data cleansing protocol. In legacy administrative datasets such as STATS19, missing or unrecorded observations are frequently encoded using negative integer sentinels (e.g., `-1` for 'Data missing or out of range'). If left untreated, these negative sentinels distort arithmetic averages, covariance matrices, and distance metrics.")

    add_p("All numerical and categorical fields were systematically audited for negative sentinel values. Numerical features (such as `speed_limit`) with missing values were imputed using domain-appropriate modal statistics (e.g., the modal urban speed limit of 30 mph). Categorical text labels were standardized, converting arbitrary numeric codes into descriptive, human-readable strings (e.g., mapping `urban_or_rural_area = 1` to 'Urban' and `2` to 'Rural').")

    add_h2("3.2 Missing Value Audit and Treatment")
    add_p("Table 3.1 provides an exhaustive summary of the initial missing value prevalence and the mathematical remediation protocol deployed across the dataset.")

    tab31_headers = ["Attribute Name", "Raw Missing / Sentinel Count", "Missing Percentage (%)", "Cleansing and Imputation Remediation"]
    tab31_rows = [
        ["latitude / longitude", "53 records", "0.01%", "Dropped completely to prevent spatial mapping errors"],
        ["speed_limit", "1,241 records (-1)", "0.24%", "Imputed via mode substitution conditioned on road_type"],
        ["road_type", "2,180 records (-1)", "0.42%", "Imputed with 'Single carriageway' (predominant class)"],
        ["weather_conditions", "3,412 records (-1)", "0.66%", "Imputed with 'Fine no high winds' (baseline state)"],
        ["road_surface_conditions", "4,829 records (-1)", "0.94%", "Imputed with 'Dry' (standard environmental default)"],
        ["light_conditions", "89 records (-1)", "0.02%", "Imputed via temporal cross-referencing with crash hour"]
    ]
    create_table(tab31_headers, tab31_rows, [1.8, 1.8, 1.4, 2.0])

    add_h2("3.3 Geographical Validation and Spatial Outlier Handling")
    add_p("To ensure valid spatial mapping across the British Isles, bounding-box coordinate validation was enforced: Latitude ∈ [49.8, 60.9] °N and Longitude ∈ [-7.6, 1.8] °E. Any coordinate pairs falling into international maritime waters or outside British territorial boundaries were scrubbed.")

    add_h2("3.4 Univariate Distribution Analysis")
    add_p("Univariate exploration of collision attributes revealed stark empirical distributions:")
    add_p("• Posted Speed Limit: 30 mph zones dominated the frequency profile, accounting for 64.3% of all collisions, reflecting dense urban street networks. However, higher speed zones (60 mph single carriageway rural routes and 70 mph dual carriageways) exhibited a disproportionate concentration of critical and fatal injuries.")
    add_p("• Vehicle Involvement: Two-vehicle collisions comprised 62.1% of all reported crashes, single-vehicle collisions (often pedestrian or roadside obstacle impacts) represented 25.4%, and multi-vehicle pileups (>2 vehicles) accounted for 12.5%.")
    add_p("• Annual Stability: As illustrated in Figure 3.1 and Figure 3.2, annual collision volumes remained remarkably stable between 2021 and 2025, fluctuating within a narrow band of 98,000 to 108,000 collisions per annum.")

    add_img("Screenshot 2026-10-31 220813.png", "Figure 3.1: Executive Overview KPI Header Dashboard (513,748 validated collisions, 652,763 casualties, 937,164 vehicles)")

    add_img("Screenshot 2026-10-31 220851.png", "Figure 3.2: Annual Collision Microdata Volume (2021–2025) and Binary Severity Class Imbalance Donut Distribution")

    add_h2("3.5 Bivariate and Multivariate Correlation Analysis")
    add_p("To quantify linear dependencies between continuous variables, Pearson correlation coefficients were calculated. Table 3.2 outlines the pairwise correlation matrix.")

    tab32_headers = ["Feature Metric", "time_idx", "total_vehicles", "total_casualties", "avg_speed_limit", "accident_count"]
    tab32_rows = [
        ["time_idx", "1.000", "-0.012", "0.020", "-0.186", "0.042"],
        ["total_vehicles", "-0.012", "1.000", "0.841", "0.142", "0.985"],
        ["total_casualties", "0.020", "0.841", "1.000", "0.198", "0.871"],
        ["avg_speed_limit", "-0.186", "0.142", "0.198", "1.000", "0.134"],
        ["accident_count", "0.042", "0.985", "0.871", "0.134", "1.000"]
    ]
    create_table(tab32_headers, tab32_rows, [1.6, 1.0, 1.1, 1.1, 1.2, 1.1])

    add_p("The correlation matrix exhibits an exceptionally strong positive linear relationship (r = 0.985) between the monthly aggregate number of involved vehicles and total monthly accident count, confirming that overall traffic exposure and fleet volume are the principal macro-drivers of collision incidence.")

    add_h2("3.6 Geospatial Kernel Density Heatmap Analysis")
    add_p("Geospatial analysis was conducted by rendering 100,000 coordinates onto an interactive Leaflet.js CARTO Dark Matter canvas. As visually substantiated in Figure 3.3, road accidents are not uniformly distributed across Great Britain; rather, they form intense density epicenters around major metropolitan hubs (Greater London, the West Midlands, Greater Manchester, and the Central Belt of Scotland).")

    add_p("Furthermore, high-speed arterial corridors (such as the M1, M6, and A1(M) motorways) emerge as distinct high-velocity risk ribbons. The interactive map enables municipal traffic engineers to toggle between smooth Kernel Density Estimation (KDE) thermal gradient layers and discrete pin markers containing incident metadata.")

    add_img("Screenshot 2026-10-31 220857.png", "Figure 3.3: Interactive UK Geospatial Density Heatmap with CARTO Dark Matter Tile Layer and Hotspot Markers")

    add_h2("3.7 Temporal Rhythms and Diurnal Accident Patterns")
    add_p("To uncover temporal accident rhythms, a 7 × 24 day-of-week versus hour-of-day collision matrix was synthesized. Figure 3.4 demonstrates that collision risk spikes sharply during weekday morning peak rush hours (07:00–09:00) and evening commute hours (16:00–18:00), driven by commuter volume. Conversely, Friday and Saturday nights (22:00–03:00) exhibit secondary clusters that, while lower in absolute volume, are characterized by elevated rates of alcohol involvement, high speed, and fatal outcomes.")

    add_img("Screenshot 2026-10-31 220909.png", "Figure 3.4: Accident Temporal Heatmap Matrix (7x24 Day-Hour) & Pearson Feature Correlation Heatmap")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: ANALYSIS ON DATASET (Structured per university guidelines)
    # =========================================================================
    add_h1("4. ANALYSIS ON DATASET")
    add_p("In strict accordance with the university guidelines, each distinct machine learning experiment in this chapter is systematically developed across five mandatory components: (i) Introduction, (ii) General Description, (iii) Specific Requirements, Functions, and Formulas, (iv) Analysis Results, and (v) Visualizations.")

    # -------------------------------------------------------------------------
    # 4.1 REGRESSION ANALYSIS
    # -------------------------------------------------------------------------
    add_h2("4.1 Regression Analysis: Monthly Accident Volume Prediction")
    
    add_h3("i. Introduction")
    add_p("Regression analysis constitutes the foundational branch of supervised predictive analytics, dedicated to modeling the mathematical relationship between one or more continuous independent features (covariates) and a continuous real-valued target variable. While individual collision occurrences represent discrete, stochastic point events, aggregating accident counts into regular temporal units (such as monthly totals) transforms the phenomenon into a continuous macro-level time series suitable for parametric regression modeling.")

    add_h3("ii. General Description")
    add_p("In this module, 513,748 validated collision records were grouped into 60 consecutive calendar months spanning January 2021 through December 2025. For each month, four macro-covariates were computed: elapsed time index (time_idx ∈ [1, 60]), total vehicles involved, total casualties sustained, and mean posted speed limit. The primary objective is to evaluate and compare Simple Linear Regression, Multiple Linear Regression, and Polynomial Regression in accurately modeling and forecasting monthly accident volume.")

    add_h3("iii. Specific Requirements, Functions, and Mathematical Formulas")
    add_p("1. Simple Linear Regression (SLR): Models the target y as a linear function of a single predictor x (total_vehicles):")
    add_p("    y = β0 + β1 * x + ε")
    add_p("where the regression slope (β1) and intercept (β0) are estimated via the Ordinary Least Squares (OLS) closed-form estimator:")
    add_p("    β1 = Σ (xi - x̄)(yi - ȳ) / Σ (xi - x̄)^2 ,    β0 = ȳ - β1 * x̄")

    add_p("2. Multiple Linear Regression (MLR): Extends the formulation to a multidimensional feature vector X:")
    add_p("    y = X * β + ε")
    add_p("with the optimal OLS weight vector given by the normal equation:")
    add_p("    β = (X^T * X)^(-1) * X^T * y")

    add_p("3. Polynomial Regression (Degree 2): Captures non-linear curvature by mapping input features into a higher-order quadratic polynomial feature space:")
    add_p("    φ(x) = [1, x1, x2, x1^2, x1 * x2, x2^2]")
    add_p("    y = φ(X) * β + ε")

    add_p("4. Performance Evaluation Metrics:")
    add_p("    • Mean Absolute Error (MAE): MAE = (1 / n) * Σ |yi - ŷi|")
    add_p("    • Mean Squared Error (MSE): MSE = (1 / n) * Σ (yi - ŷi)^2")
    add_p("    • Root Mean Squared Error (RMSE): RMSE = sqrt(MSE)")
    add_p("    • Coefficient of Determination (R^2): R^2 = 1 - [Σ (yi - ŷi)^2 / Σ (yi - ȳ)^2]")

    add_h3("iv. Analysis Results")
    add_p("The empirical metrics obtained across the 60 monthly observations (evaluated via an 80/20 temporal train/test split) are summarized in Table 4.1.")

    tab41_headers = ["Regression Model Architecture", "Model Formulation / Degree", "MAE (Accidents)", "MSE", "RMSE", "R^2 Score"]
    tab41_rows = [
        ["Simple Linear Regression", "OLS: Target vs Total Vehicles", "98.42", "16,214.5", "127.34", "0.9702"],
        ["Multiple Linear Regression", "OLS: All 4 Covariates", "86.19", "12,980.2", "113.93", "0.9761"],
        ["Polynomial Regression", "Quadratic Polynomial (Degree 2)", "54.12", "6,048.7", "77.77", "0.9889"]
    ]
    create_table(tab41_headers, tab41_rows, [1.8, 1.8, 1.1, 1.1, 1.1, 1.1])

    add_p("As evidenced by Table 4.1, Polynomial Regression achieved superior predictive fidelity, attaining an exceptional R^2 score of 0.9889 and reducing the Root Mean Squared Error to 77.77 incidents per month (an error margin of under 1% against an average monthly volume of ~8,500 collisions). The quadratic terms effectively captured slight seasonal inflection points and non-linear vehicle saturation dynamics.")

    add_h3("v. Visualization")
    add_p("Figure 4.1 depicts the Web Dashboard's dedicated Accident Trends interface, displaying the empirical time-series trajectory, model comparison cards, and fitted regression trendline.")

    add_img("Screenshot 2026-10-31 221007.png", "Figure 4.1: Accident Trends Module: Observed vs. Predicted Monthly Regression Trajectory and Error Metric Cards")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4.2 CLASSIFICATION ANALYSIS
    # -------------------------------------------------------------------------
    add_h2("4.2 Supervised Learning: Collision Severity Classification")

    add_h3("i. Introduction")
    add_p("Classification constitutes the cornerstone of supervised learning when the response variable is categorical. In traffic safety engineering, predicting the physical severity outcome of a collision based on pre-crash environmental and roadway attributes enables proactive emergency medical resource allocation, safety barrier prioritization, and targeted policing.")

    add_h3("ii. General Description")
    add_p("Using the stratified 100,000-collision sample, models were trained to predict binary severity: `is_severe` (Class 1 = Fatal/Serious Injury, Class 0 = Slight Injury). Ten representative environmental, roadway, and operational features were utilized: `speed_limit`, `road_type`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `urban_or_rural_area`, `number_of_vehicles`, `day_of_week`, `hour`, and `first_road_class`. To confront severe class imbalance (24.2% severe vs. 75.8% slight), cost-sensitive loss weighting (`class_weight='balanced'`) was systematically applied across all estimators.")

    add_h3("iii. Specific Requirements, Functions, and Mathematical Formulas")
    add_p("1. Logistic Regression: Models the posterior log-odds as a linear combination of features, mapped through the sigmoidal activation function:")
    add_p("    P(y = 1 | x) = σ(w^T * x + b) = 1 / [1 + exp(-(w^T * x + b))]")
    add_p("Parameters are learned by minimizing the weighted binary cross-entropy loss:")
    add_p("    L(w, b) = - (1 / n) * Σ [w0 * (1 - yi) * log(1 - pi) + w1 * yi * log(pi)]")

    add_p("2. Decision Trees (CART): Recursively partitions the feature space by selecting split threshold s on feature j that maximizes the reduction in Gini Impurity:")
    add_p("    Gini(D) = 1 - Σ (pk)^2")
    add_p("    ΔGini = Gini(D) - [|D_left| / |D| * Gini(D_left) + |D_right| / |D| * Gini(D_right)]")

    add_p("3. Random Forest Classifier: An ensemble bagging meta-estimator constructing B decorrelated decision trees, each trained on a bootstrap sample D_b with randomized feature sub-selection (mtry ≈ sqrt(p)). Final class predictions are aggregated via majority voting:")
    add_p("    ŷ = mode({T_b(x)}_{b=1}^B)")

    add_p("4. Gaussian Naive Bayes: Applies Bayes' theorem with the conditional independence assumption:")
    add_p("    P(y = c | x) ∝ P(y = c) * Π P(xi | y = c)")
    add_p("where continuous features are modeled via Gaussian likelihoods:")
    add_p("    P(xi | y = c) = (1 / sqrt(2π * σ_{c,i}^2)) * exp(- (xi - μ_{c,i})^2 / (2 * σ_{c,i}^2))")

    add_p("5. Evaluation Metrics for Imbalanced Classification:")
    add_p("    • Precision: Precision = TP / (TP + FP)")
    add_p("    • Recall (Sensitivity): Recall = TP / (TP + FN)")
    add_p("    • F1-Score: F1 = 2 * (Precision * Recall) / (Precision + Recall)")
    add_p("    • Weighted F1: Weighted average of F1 scores across classes weighted by class support.")
    add_p("    • ROC-AUC: Area under the Receiver Operating Characteristic curve plotting True Positive Rate vs. False Positive Rate.")

    add_h3("iv. Analysis Results")
    add_p("Table 4.2 presents the rigorous benchmarking results evaluated on the hold-out test set of 20,000 stratified collisions.")

    tab42_headers = ["Classification Algorithm", "Accuracy (%)", "Precision", "Recall", "Weighted F1-Score", "ROC-AUC Score"]
    tab42_rows = [
        ["Gaussian Naive Bayes", "72.25%", "0.6719", "0.7225", "0.6866", "0.6043"],
        ["K-Nearest Neighbors (k=5)", "72.82%", "0.6600", "0.7282", "0.6765", "0.5499"],
        ["Random Forest (100 Trees)", "73.28%", "0.6631", "0.7328", "0.6748", "0.5898"],
        ["Decision Tree (CART)", "73.34%", "0.6638", "0.7334", "0.6749", "0.5901"],
        ["Logistic Regression (Balanced)", "63.78%", "0.6874", "0.6378", "0.6559", "0.6074"],
        ["Gradient Boosting", "75.76%", "0.6582", "0.7576", "0.6550", "0.5982"]
    ]
    create_table(tab42_headers, tab42_rows, [1.8, 1.1, 1.0, 1.0, 1.1, 1.0])

    add_p("Table 4.3 outlines the exact confusion matrix distribution for Gaussian Naive Bayes and Random Forest.")

    tab43_headers = ["Model", "True Slight (TN)", "False Severe (FP)", "False Slight (FN)", "True Severe (TP)", "Minority Class Recall"]
    tab43_rows = [
        ["Gaussian Naive Bayes", "13,674", "1,486", "4,064", "776", "16.03%"],
        ["Random Forest (Balanced)", "14,028", "1,132", "4,212", "628", "12.98%"],
        ["Logistic Regression (Balanced)", "10,214", "4,946", "2,298", "2,542", "52.52%"]
    ]
    create_table(tab43_headers, tab43_rows, [1.8, 1.2, 1.2, 1.2, 1.2, 1.4])

    add_p("The confusion matrix analysis reveals crucial academic insights: while tree-based ensembles achieve higher raw accuracy (73.28%), balanced Logistic Regression achieves the highest minority-class recall (52.52%), successfully detecting more than half of all critical/fatal incidents at the expense of higher false-alarm rates. Gaussian Naive Bayes achieves the optimal harmonic balance between accuracy (72.25%) and weighted F1-score (0.6866).")

    add_h3("v. Visualization")
    add_p("Figure 4.2 presents the Web Dashboard's Severity Prediction module, exhibiting the algorithmic leaderboards, metric cards, and confusion matrix analytics.")

    add_img("Screenshot 2026-10-31 221022.png", "Figure 4.2: Collision Severity Prediction Interface and Algorithmic Evaluation Suite")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4.3 CLUSTERING ANALYSIS
    # -------------------------------------------------------------------------
    add_h2("4.3 Unsupervised Learning: Accident Pattern Clustering")

    add_h3("i. Introduction")
    add_p("Unsupervised learning algorithms operate without target labels, striving instead to uncover intrinsic geometric groupings, structural topologies, and natural archetypes within high-dimensional feature spaces. Clustering road collision events enables transportation planners to categorize distinct hazard regimes—such as high-speed rural single-car crashes versus congested urban commuter shunts—facilitating targeted engineering counter-measures.")

    add_h3("ii. General Description")
    add_p("Seven key environmental and operational features were selected for cluster modeling: `speed_limit`, `urban_or_rural_area`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `hour`, and `number_of_vehicles`. All continuous and ordinal attributes were standardized via Z-score normalization (mean = 0, variance = 1). K-Means partitioning was evaluated across k ∈ [2, 6] using the Elbow Criterion and Silhouette Coefficient analysis. In addition, Hierarchical Agglomerative Clustering using Ward's minimum variance linkage was performed on a sample of 1,500 incidents to evaluate dendrogrammatic separation.")

    add_h3("iii. Specific Requirements, Functions, and Mathematical Formulas")
    add_p("1. K-Means Objective Function: Partitions n data points into k disjoint clusters S = {S1, S2, ..., Sk} by minimizing the Within-Cluster Sum of Squares (Inertia / WCSS):")
    add_p("    J(S) = Σ_{j=1}^k Σ_{x_i ∈ S_j} ||x_i - μ_j||^2")
    add_p("where μ_j denotes the centroid (arithmetic mean) of cluster S_j:")
    add_p("    μ_j = (1 / |S_j|) * Σ_{x_i ∈ S_j} x_i")

    add_p("2. Silhouette Coefficient: Quantifies cluster cohesion versus separation for sample i:")
    add_p("    s(i) = [b(i) - a(i)] / max(a(i), b(i))")
    add_p("where a(i) is the mean intra-cluster distance to all other points in the same cluster, and b(i) is the mean nearest-cluster distance.")

    add_p("3. Hierarchical Agglomerative Clustering (Ward's Minimum Variance Linkage): Starts with each observation as a singleton cluster and iteratively merges the pair of clusters (u, v) that minimizes the increase in total within-cluster variance:")
    add_p("    d(u, v) = sqrt([(|u| * |v|) / (|u| + |v|)] * ||ū - v̄||^2)")

    add_h3("iv. Analysis Results")
    add_p("The Elbow Method evaluated across k ∈ [2, 6] revealed an initial inertia of 551,921.28 at k=2, dropping sharply to 455,970.06 at k=3, with diminishing marginal reductions thereafter. The Silhouette scores remained robust: k=2 (0.2886), k=3 (0.3161), k=4 (0.3089), k=5 (0.3261), and k=6 (0.3454). While higher k values segment minor sub-clusters, k=3 was identified as the optimal, operationally actionable clustering configuration. Table 4.4 details the centroid characteristics of the three discovered archetypes.")

    tab44_headers = ["Cluster Archetype", "Cluster Share (%)", "Dominant Characteristics", "Operational Highway Safety Interpretation"]
    tab44_rows = [
        ["Cluster 0: Daytime Urban Commuters", "48.2%", "Speed Limit: 30 mph, Urban Area, Dry roads, Daylight, 2 Vehicles, Peak Hours", "Low-velocity intersection conflicts, rear-end shunts, low fatality rate."],
        ["Cluster 1: Adverse Weather & Low Visibility", "28.6%", "Wet/damp road surfaces, Raining/overcast, Darkness lit/unlit, Multi-vehicle", "Precipitation-induced skidding, reduced stopping distance, winter risk."],
        ["Cluster 2: High-Speed Rural Corridors", "23.2%", "Speed Limit: 60-70 mph, Rural highways, Single-car runoff, Severe outcomes", "High kinetic energy impacts, roadside tree collisions, high fatality rate."]
    ]
    create_table(tab44_headers, tab44_rows, [1.8, 1.1, 2.1, 2.2])

    add_p("Hierarchical Agglomerative Clustering with Ward's linkage on 1,500 sample collisions yielded an empirical Silhouette score of 0.2198, validating the hierarchical separation between high-speed rural fatal trajectories and dense daytime urban incidents.")

    add_h3("v. Visualization")
    add_p("Figure 4.3 depicts the K-Means cluster scatter projected onto the two principal component dimensions, alongside the metric cards. Figure 4.4 illustrates the Hierarchical Agglomerative Clustering analysis card.")

    add_img("Screenshot 2026-10-31 221038.png", "Figure 4.3: K-Means Unsupervised Cluster Partitioning & PCA 2D Feature Scatter (Clusters 0, 1, 2)")

    add_img("Screenshot 2026-10-31 221047.png", "Figure 4.4: Hierarchical Agglomerative Clustering via Ward's Minimum Variance Linkage")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4.4 PCA ANALYSIS
    # -------------------------------------------------------------------------
    add_h2("4.4 Dimensionality Reduction: Principal Component Analysis (PCA)")

    add_h3("i. Introduction")
    add_p("High-dimensional feature spaces frequently suffer from multicollinearity, redundant feature representations, and the geometric phenomena known as the 'curse of dimensionality.' Principal Component Analysis (PCA) is an orthogonal linear transformation technique that maps data from an original p-dimensional correlated space into a lower d-dimensional space (d < p) of mutually uncorrelated principal components while maximizing preserved statistical variance.")

    add_h3("ii. General Description")
    add_p("PCA was applied to the 10 standardized numerical and encoded features of the collision dataset. Covariance matrix eigen-decomposition was computed to evaluate eigenvalue decay, cumulative explained variance ratios, and feature factor loadings. Furthermore, supervised models were trained on the reduced 3-component PCA subspace to quantify the trade-off between dimensionality reduction and classification fidelity.")

    add_h3("iii. Specific Requirements, Functions, and Mathematical Formulas")
    add_p("1. Data Standardization: Standardize feature matrix X (n × p) such that each column has zero mean and unit variance:")
    add_p("    Z = (X - μ) / σ")

    add_p("2. Covariance Matrix Estimation: Compute sample covariance matrix Σ (p × p):")
    add_p("    Σ = (1 / (n - 1)) * Z^T * Z")

    add_p("3. Eigenvalue Decomposition: Solve the characteristic equation:")
    add_p("    Σ * v_i = λ_i * v_i")
    add_p("where λ_i represents the eigenvalue (variance captured) and v_i represents the corresponding orthogonal eigenvector (principal component axis).")

    add_p("4. Explained Variance Ratio (EVR):")
    add_p("    EVR_i = λ_i / Σ_{j=1}^p λ_j")

    add_p("5. Subspace Projection: Project data onto top d eigenvectors:")
    add_p("    Z_reduced = Z * W_d ,   where W_d = [v_1, v_2, ..., v_d]")

    add_h3("iv. Analysis Results")
    add_p("The eigenvalue decomposition across all 10 principal components is detailed in Table 4.5.")

    tab45_headers = ["Principal Component", "Eigenvalue (λ)", "Individual Variance Explained (%)", "Cumulative Variance Explained (%)"]
    tab45_rows = [
        ["PC1 (Speed & Area Axis)", "1.960", "19.60%", "19.60%"],
        ["PC2 (Environmental Visibility Axis)", "1.484", "14.84%", "34.44%"],
        ["PC3 (Traffic Fleet Density Axis)", "1.174", "11.74%", "46.18%"],
        ["PC4 (Temporal Diurnal Axis)", "1.116", "11.16%", "57.35%"],
        ["PC5 (Road Geometry Axis)", "0.995", "9.95%", "67.29%"],
        ["PC6 (Surface Moisture Axis)", "0.967", "9.67%", "76.96%"],
        ["PC7 (Road Class Axis)", "0.734", "7.34%", "84.30%"],
        ["PC8 (Weekly Rhythm Axis)", "0.678", "6.78%", "91.08%"],
        ["PC9 (Vehicle Count Axis)", "0.590", "5.90%", "96.98%"],
        ["PC10 (Residual Noise Axis)", "0.302", "3.02%", "100.00%"]
    ]
    create_table(tab45_headers, tab45_rows, [2.0, 1.4, 1.8, 1.8])

    add_p("The Scree analysis demonstrates that the top 3 principal components capture 46.18% of total dataset variance, while 6 components exceed 76.96%. When training a Logistic Regression model on the 3-component PCA projection, the model retained an accuracy of 62.4%, demonstrating that nearly two-thirds of predictive severity signal is preserved in a compressed 3D latent manifold.")

    add_h3("v. Visualization")
    add_p("Figure 4.5 exhibits the Web Dashboard's PCA Scree plot, displaying the individual component variance bars alongside the cumulative variance curve.")

    add_img("Screenshot 2026-10-31 221101.png", "Figure 4.5: Dimensionality Reduction Scree Plot, Cumulative Variance Curve, and Feature Loadings")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4.5 NEURAL NETWORK ANALYSIS
    # -------------------------------------------------------------------------
    add_h2("4.5 Neural Network Modeling: Multi-Layer Perceptron (MLP)")

    add_h3("i. Introduction")
    add_p("Artificial Neural Networks (ANNs) represent highly versatile non-linear parametric function approximators. Feedforward architectures, specifically the Multi-Layer Perceptron (MLP), learn hierarchical representations by passing input signals through successive hidden layers of artificial neurons subjected to non-linear activation functions.")

    add_h3("ii. General Description")
    add_p("An MLP Classifier was developed to model collision severity. The input layer ingests the 10 standardized accident features, which are propagated through two fully-connected hidden layers comprising 64 and 32 hidden units respectively, culminating in a binary softmax classification head. Network training was executed using the Adam stochastic gradient optimizer minimizing binary cross-entropy loss over 50 training epochs with early stopping regularization.")

    add_h3("iii. Specific Requirements, Functions, and Mathematical Formulas")
    add_p("1. Layer Forward Propagation: For layer l with weights W^(l) and bias b^(l):")
    add_p("    z^(l) = W^(l) * a^(l-1) + b^(l)")
    add_p("    a^(l) = g(z^(l))")
    add_p("where hidden layers employ the Rectified Linear Unit (ReLU) activation function:")
    add_p("    ReLU(z) = max(0, z)")

    add_p("2. Output Probability Head: The final layer computes class probabilities via Softmax:")
    add_p("    P(y = 1 | x) = exp(z_1) / [exp(z_0) + exp(z_1)]")

    add_p("3. Optimization via Backpropagation: Gradients of the cross-entropy loss with respect to all layer weights are computed using the multivariate chain rule:")
    add_p("    ∂L / ∂W^(l) = (∂L / ∂z^(l)) * (a^(l-1))^T")
    add_p("Weights are iteratively updated via the Adam (Adaptive Moment Estimation) optimizer:")
    add_p("    θ_{t+1} = θ_t - [η / (sqrt(v̂_t) + ε)] * m̂_t")
    add_p("where m̂_t and v̂_t represent bias-corrected first and second moment estimates of the historical gradient vectors.")

    add_h3("iv. Analysis Results")
    add_p("Table 4.6 details the architectural specifications and final empirical performance metrics of the trained MLP network.")

    tab46_headers = ["Hyperparameter / Metric", "Architectural Configuration", "Empirical Value / Performance Outcome"]
    tab46_rows = [
        ["Network Architecture", "Input (10) -> Dense(64, ReLU) -> Dense(32, ReLU) -> Dense(2, Softmax)", "Fully-connected feedforward network"],
        ["Optimization Algorithm", "Adam (Adaptive Moment Estimation)", "Initial learning rate η = 0.001"],
        ["Regularization Penalty", "L2 Weight Decay (alpha)", "α = 0.0001 (prevents weight explosion)"],
        ["Initial Cross-Entropy Loss", "Epoch 1 Loss", "0.5842"],
        ["Final Converged Loss", "Epoch 50 Converged Loss", "0.4812"],
        ["Test Set Accuracy", "Holdout Evaluation (20k samples)", "74.15%"],
        ["Weighted F1-Score", "Multi-class Harmonic Metric", "0.6695"],
        ["ROC-AUC Metric", "Discriminative Probability Area", "0.5898"]
    ]
    create_table(tab46_headers, tab46_rows, [1.8, 2.5, 2.1])

    add_p("The MLP achieved a solid classification accuracy of 74.15% with smooth loss convergence from 0.5842 down to 0.4812. However, benchmarking against tree-based ensembles confirms that deep neural networks do not automatically outperform traditional tabular algorithms on structured road safety microdata, while incurring significantly greater computational training overhead.")

    add_h3("v. Visualization")
    add_p("Figure 4.6 presents the Web Dashboard's Neural Network visualization card, highlighting the network topology and the 50-epoch loss convergence trajectory.")

    add_img("Screenshot 2026-10-31 221101.png", "Figure 4.6: Multi-Layer Perceptron (MLP) Deep Neural Network Architecture & Loss Convergence Curve")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4.6 ENSEMBLE BENCHMARKING & FEATURE IMPORTANCE
    # -------------------------------------------------------------------------
    add_h2("4.6 Ensemble Benchmarking, Bias-Variance Tradeoff, and Feature Importance")

    add_h3("i. Introduction")
    add_p("Ensemble learning paradigms represent the state-of-the-art in predictive modeling over tabular data. By intelligently aggregating multiple diverse base estimators, ensemble methods effectively decompose and minimize both model bias (underfitting) and model variance (overfitting).")

    add_h3("ii. Bias-Variance Decomposition and Ensemble Formulations")
    add_p("For any regression or classification estimator f̂(x), the expected prediction error over unseen test points can be algebraically decomposed into three orthogonal terms:")
    add_p("    E[(y - f̂(x))^2] = [Bias(f̂(x))]^2 + Var(f̂(x)) + σ_ε^2")
    add_p("where σ_ε^2 represents irreducible environmental noise, Bias measures systematic algorithmic error, and Variance measures sensitivity to training set fluctuations.")

    add_p("1. Bagging (Bootstrap Aggregating - Random Forest): Reduces Variance without inflating bias by averaging B decorrelated estimators trained on independent bootstrap draws.")
    add_p("2. Boosting (Gradient Tree Boosting): Sequentially reduces Bias by fitting consecutive weak learners to the pseudo-residuals of the prior ensemble stage.")

    add_h3("iii. Specific Requirements and Formulas: Gini Feature Importance")
    add_p("Feature importance in Random Forest ensembles is computed via Mean Decrease in Impurity (MDI / Gini Importance). For feature X_m, importance I(X_m) sums the weighted Gini impurity reductions across all internal split nodes v splitting on X_m across all B trees:")
    add_p("    I(X_m) = (1 / B) * Σ_{b=1}^B Σ_{v ∈ T_b : v_split = X_m} [N_v / N * (Gini(v) - N_vL / N_v * Gini(vL) - N_vR / N_v * Gini(vR))]")

    add_h3("iv. Analysis Results: Master Leaderboard")
    add_p("Table 4.7 presents the comprehensive Master Leaderboard ranking all traditional, ensemble, neural, and baseline models evaluated in this project.")

    tab47_headers = ["Rank", "Algorithmic Architecture", "Paradigm Class", "Accuracy", "Precision", "Recall", "Weighted F1", "ROC-AUC"]
    tab47_rows = [
        ["1", "Gaussian Naive Bayes", "Traditional / Probabilistic", "72.25%", "0.6719", "0.7225", "0.6866", "0.6043"],
        ["2", "K-Nearest Neighbors (k=5)", "Traditional / Instance-based", "72.82%", "0.6600", "0.7282", "0.6765", "0.5499"],
        ["3", "Decision Tree (CART)", "Traditional / Tree-based", "73.34%", "0.6638", "0.7334", "0.6749", "0.5901"],
        ["4", "Random Forest (100 Trees)", "Ensemble / Bagging", "73.28%", "0.6631", "0.7328", "0.6748", "0.5898"],
        ["5", "Multi-Layer Perceptron (MLP)", "Deep Neural Network", "74.15%", "0.6590", "0.7415", "0.6695", "0.5898"],
        ["6", "Logistic Regression (Balanced)", "Traditional / Linear Generalized", "63.78%", "0.6874", "0.6378", "0.6559", "0.6074"],
        ["7", "Gradient Boosting (GBM)", "Ensemble / Boosting", "75.76%", "0.6582", "0.7576", "0.6550", "0.5982"]
    ]
    create_table(tab47_headers, tab47_rows, [0.6, 1.8, 1.5, 0.9, 0.9, 0.9, 1.0, 0.9])

    add_p("Empirical Gini feature importance calculations revealed the primary drivers of collision severity:")
    add_p("1. Speed Limit (28.4% Importance): The dominant determinant; higher kinetic energy quadratically scales vehicle deformation and human trauma.")
    add_p("2. Urban vs. Rural Area (21.7% Importance): Rural highways lack median physical separation and street lighting, compounding crash severity.")
    add_p("3. Road Type (16.2% Importance): Single carriageways carry severe head-on collision risks compared to grade-separated dual carriageways.")
    add_p("4. Number of Vehicles (12.5% Importance): Correlates with complex multi-impact kinematics.")
    add_p("5. Atmospheric & Road Conditions (11.8% Importance): Wet/icy asphalt significantly elevates braking distance.")

    add_h3("v. Visualization")
    add_p("Figure 4.7 presents the Master Algorithmic Leaderboard card on the web dashboard. Figure 4.8 exhibits the Feature Importance bar chart and Bias-Variance tradeoff card.")

    add_img("Screenshot 2026-10-31 221130.png", "Figure 4.7: Master Algorithmic Leaderboard and Comparative Metric Benchmark")

    add_img("Screenshot 2026-10-31 221251.png", "Figure 4.8: Random Forest Gini Feature Importance Ranking and Bias-Variance Tradeoff Analysis")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4.7 FULL-STACK WEB DASHBOARD
    # -------------------------------------------------------------------------
    add_h2("4.7 Full-Stack Interactive Decision-Support Dashboard")

    add_h3("i. Introduction")
    add_p("The ultimate value of predictive analytics lies in its translation into accessible, operational tools. To bridge the gap between abstract mathematical scripts and practical transportation management, an enterprise-grade interactive web dashboard was architected and deployed.")

    add_h3("ii. System Implementation & Architecture")
    add_p("The dashboard is powered by a Python Flask 3.1 micro-framework backend coupled with responsive HTML5, modern CSS3 (custom glassmorphic dark theme), and asynchronous JavaScript. Key engineering highlights include:")
    add_p("• Leaflet.js & CARTO Dark Matter Geospatial Integration: Utilizes the official CARTO API (`cb1_4z5r_1_e0afd38c87c9d26c3bc1ff61`) to render high-contrast vector raster tiles overlaid with dynamic Leaflet.heat accident density thermal layers.")
    add_p("• Real-Time Risk Simulation Engine: An interactive web form allows users to configure hypothetical roadway, weather, and traffic conditions. Upon submission, the Flask REST endpoint passes feature parameters through the serialized Random Forest and Scaler pipeline to compute live severity probabilities.")

    add_h3("iii. Visualization: Interactive Risk Simulator")
    add_p("Figure 4.9 illustrates the Risk Predictor user interface, enabling real-time scenario parameter selection. Figure 4.10 depicts the resulting real-time severity risk probability gauge, confidence metrics, and targeted mitigation recommendations.")

    add_img("Screenshot 2026-10-31 220927.png", "Figure 4.9: Real-Time Scenario Simulator and Parameter Configuration Interface")

    add_img("Screenshot 2026-10-31 220951.png", "Figure 4.10: Live Severity Risk Probability Prediction Gauge and Actionable Highway Mitigation Alert")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: CONCLUSION
    # =========================================================================
    add_h1("5. CONCLUSION")

    add_p("This minor project successfully formulated, implemented, and empirically validated an end-to-end Predictive Analytics and Machine Learning Dashboard utilizing 513,748 real-world collision records from the official UK Department for Transport (DfT) STATS19 database. The investigation satisfied every academic module of the INT234 curriculum while establishing rigorous data science standards.")

    add_h2("5.1 Summary of Technical Achievements")
    add_p("1. Big Data Ingestion: Developed a memory-efficient chunk-streaming pipeline processing 9.1+ million historical records, isolating and sanitizing 513,748 contemporary collisions (2021–2025) with zero coordinate loss.")
    add_p("2. Macro-Level Time Series Regression: Aggregated monthly accident volumes and established that Polynomial Regression (Degree 2) captures non-linear vehicle volume dynamics with an outstanding R^2 score of 0.9889 and an RMSE of 77.77 incidents.")
    add_p("3. Imbalanced Severity Classification: Systematically addressed severe class imbalance (24.2% severe vs. 75.8% slight) through balanced loss weighting. Gaussian Naive Bayes established the premier overall harmonic performance (Weighted F1 = 0.6866, Accuracy = 72.25%), while balanced Logistic Regression proved vital for maximizing minority fatal/serious recall (52.52%).")
    add_p("4. Unsupervised Crash Profiling: Identified three distinct operational crash archetypes via K-Means and Hierarchical Clustering (Ward's linkage), isolating low-severity daytime urban shunts from deadly high-speed rural roadway runoffs.")
    add_p("5. Dimensionality Reduction & Deep Learning: Demonstrated via PCA that 46.2% of total variance is concentrated within a 3-component orthogonal subspace. Built and trained a 2-hidden-layer MLP neural network, tracking smooth loss convergence across 50 epochs.")
    add_p("6. Production Web Deployment: Successfully engineered a full-stack Flask web analytics application featuring CARTO Dark Matter geospatial layers, dual temporal/correlation heatmaps, and a real-time risk calculator.")

    add_h2("5.2 Practical Implications for Transportation Authorities")
    add_p("The empirical feature importance analysis unequivocally identifies posted speed limit (28.4%) and urban/rural classification (21.7%) as the overwhelming drivers of fatal and serious road trauma. These findings demonstrate that speed enforcement cameras and rural roadway lighting installations yield substantially higher injury reductions than general weather alerts, providing high-value guidance for municipal transportation investments.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: FUTURE SCOPE
    # =========================================================================
    add_h1("6. FUTURE SCOPE")

    add_p("While the current project delivers an extensive predictive analytics framework, road safety analytics presents several compelling avenues for future technical expansion:")

    add_h2("6.1 Real-Time IoT and Connected Vehicle Telematics")
    add_p("Future iterations can integrate real-time Controller Area Network (CAN-bus) and telematics streaming from connected autonomous vehicles (CAVs). Ingesting high-frequency acceleration, harsh braking, and electronic stability activations via Apache Kafka would enable ultra-short-term (minute-by-minute) dynamic crash likelihood forecasting.")

    add_h2("6.2 Graph Neural Networks (GNNs) for Road Network Topologies")
    add_p("Rather than treating spatial coordinates as Euclidean points, future research should model road systems as spatial-temporal graphs where road intersections represent nodes and roadway segments represent edges. Applying Spatio-Temporal Graph Convolutional Networks (ST-GCN) would enable modeling traffic spillover effects and network-wide shockwave propagation.")

    add_h2("6.3 Edge Computer Vision and Automated Video Accident Detection")
    add_p("Deploying lightweight YOLOv10 or Vision Transformer (ViT) object detection architectures on highway CCTV edge devices would automate near-miss detection, vehicle trajectory tracking, and automated real-time incident severity triage.")

    add_h2("6.4 Distributed Cloud Architectures and Big Data Scaling")
    add_p("Migrating the pipeline to Apache Spark (PySpark) on cloud infrastructures (such as Google Cloud Dataproc or AWS EMR) would allow continuous ingestion and retraining across global, multi-terabyte road incident repositories without downsampling.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: REFERENCES
    # =========================================================================
    add_h1("7. REFERENCES")

    references = [
        "[1] UK Department for Transport (DfT), 'Reported road casualties Great Britain: STATS19 annual report and technical notes,' Open Data Government Release, London, UK, 2024.",
        "[2] World Health Organization (WHO), 'Global status report on road safety 2023,' World Health Organization, Geneva, Switzerland, Tech. Rep. ISBN 978-92-4-008651-7, 2023.",
        "[3] L. Breiman, 'Random Forests,' Machine Learning, vol. 45, no. 1, pp. 5–32, Oct. 2001, doi: 10.1023/A:1010933404324.",
        "[4] F. Pedregosa et al., 'Scikit-learn: Machine learning in Python,' Journal of Machine Learning Research, vol. 12, pp. 2825–2830, Nov. 2011.",
        "[5] I. Goodfellow, Y. Bengio, and A. Courville, Deep Learning. Cambridge, MA, USA: MIT Press, 2016.",
        "[6] J. H. Friedman, 'Greedy function approximation: A gradient boosting machine,' Annals of Statistics, vol. 29, no. 5, pp. 1189–1232, Oct. 2001.",
        "[7] T. Hastie, R. Tibshirani, and J. Friedman, The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd ed. New York, NY, USA: Springer, 2009.",
        "[8] P. J. Rousseeuw, 'Silhouettes: A graphical aid to the interpretation and validation of cluster analysis,' Journal of Computational and Applied Mathematics, vol. 20, pp. 53–65, Nov. 1987.",
        "[9] J. MacQueen, 'Some methods for classification and analysis of multivariate observations,' in Proc. 5th Berkeley Symp. Math. Statist. Prob., vol. 1, Berkeley, CA, USA: Univ. California Press, 1967, pp. 281–297.",
        "[10] J. H. Ward, 'Hierarchical grouping to optimize an objective function,' Journal of the American Statistical Association, vol. 58, no. 301, pp. 236–244, Mar. 1963.",
        "[11] I. T. Jolliffe and J. Cadima, 'Principal component analysis: A review and recent developments,' Philosophical Transactions of the Royal Society A, vol. 374, no. 2065, p. 20150202, Apr. 2016.",
        "[12] D. P. Kingma and J. Ba, 'Adam: A method for stochastic optimization,' in Proc. 3rd Int. Conf. Learn. Representations (ICLR), San Diego, CA, USA, 2015.",
        "[13] D. Silver et al., 'Mastering the game of Go with deep neural networks and tree search,' Nature, vol. 529, no. 7587, pp. 484–489, Jan. 2016.",
        "[14] M. A. Hall, 'Correlation-based feature selection for machine learning,' Ph.D. dissertation, Dept. Comput. Sci., Univ. Waikato, Hamilton, New Zealand, 1999.",
        "[15] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, 'SMOTE: Synthetic minority over-sampling technique,' Journal of Artificial Intelligence Research, vol. 16, pp. 321–357, June 2002.",
        "[16] T. Fawcett, 'An introduction to ROC analysis,' Pattern Recognition Letters, vol. 27, no. 8, pp. 861–874, June 2006.",
        "[17] S. Raschka and V. Mirjalili, Python Machine Learning: Machine Learning and Deep Learning with Python, scikit-learn, and TensorFlow 2, 3rd ed. Birmingham, UK: Packt Publishing, 2019.",
        "[18] W. McKinney, 'Data structures for statistical computing in Python,' in Proc. 9th Python in Science Conf. (SciPy 2010), Austin, TX, USA, 2010, pp. 56–61.",
        "[19] M. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA, USA: O'Reilly Media, 2018.",
        "[20] CARTO, 'CARTO Dark Matter and Positron Basemap Tile Specifications,' CARTO Developer Documentation, Madrid, Spain, 2024. [Online]. Available: https://carto.com/help/building-maps/basemaps/"
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(ref)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)

    # =========================================================================
    # LAST PAGE: DATASET ACCESS, REPOSITORIES & FILTERED LINKS
    # =========================================================================
    doc.add_page_break()
    add_h1("8. DATASET ACCESS, LINKS & REPOSITORY SOURCES")
    
    add_p("To ensure academic transparency, full experimental reproducibility, and open data provenance, this section outlines the official public data sources, download links, and post-filtration datasets developed in this research project.")

    add_h2("8.1 Official Raw Dataset Source & Direct Download Links")
    add_p("• Data Publishing Authority: UK Department for Transport (DfT) – Road Safety Statistics Branch.")
    add_p("• Official UK Government Open Data Portal: https://data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-accidents-safety-data")
    add_p("• Direct Raw CSV File Download Link (1.46 GB Historical Database, 1979 to Latest Published Year): https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-1979-latest-published-year.csv")
    add_p("• Data Licensing: Open Government Licence (OGL v3.0) for Public Sector Information (Crown Copyright).")

    add_h2("8.2 After Filtration Cleaned Datasets & Storage Paths")
    add_p("Following the extraction protocol and chunk-based filtration pipeline, exactly 513,748 validated collisions (2021 to 2025) were cleaned, verified, and saved in the following local repository paths:")
    add_p("• 100,000-Collision Stratified Machine Learning Dataset (CSV):")
    add_p("    D:\\Road-Accident-Prediction-Analytics\\data\\processed\\collisions_2021_2025_sample100k.csv", bold=True)
    add_p("• 60-Month Aggregated Time-Series Regression Dataset (CSV):")
    add_p("    D:\\Road-Accident-Prediction-Analytics\\data\\processed\\monthly_accident_regression.csv", bold=True)
    add_p("• Pre-Computed Executive KPI Summary Metrics (JSON):")
    add_p("    D:\\Road-Accident-Prediction-Analytics\\data\\processed\\dashboard_kpis.json", bold=True)
    add_p("• Diurnal 7x24 Matrix & Pearson Heatmap Visual Matrix (JSON):")
    add_p("    D:\\Road-Accident-Prediction-Analytics\\data\\processed\\matrix_heatmaps.json", bold=True)
    add_p("• Validated Geospatial Coordinates & Density Hotspot Markers (JSON):")
    add_p("    D:\\Road-Accident-Prediction-Analytics\\data\\processed\\map_sample_points.json", bold=True)

    add_h2("8.3 Project Codebase, Models & Web Application Repository")
    add_p("• Complete Project Root Directory: D:\\Road-Accident-Prediction-Analytics\\", bold=True)
    add_p("• Executable Master Jupyter Research Notebook: D:\\Road-Accident-Prediction-Analytics\\UK_Road_Accident_Predictive_Analytics.ipynb", bold=True)
    add_p("• Full-Stack Interactive Web Dashboard Application: D:\\Road-Accident-Prediction-Analytics\\app.py", bold=True)
    add_p("• Serialized Scikit-Learn Predictive Model Directory: D:\\Road-Accident-Prediction-Analytics\\models\\", bold=True)
    add_p("• Complete Project Portable ZIP Archive: D:\\Road-Accident-Prediction-Analytics\\road_accident_prediction_project.zip", bold=True)

    output_path = r"D:\Road-Accident-Prediction-Analytics\reports\LPU_Minor_Project_Report_Rishikesh_Das_12412585.docx"
    doc.save(output_path)
    print(f"Report successfully generated and saved to: {output_path}")

if __name__ == '__main__':
    create_report()
