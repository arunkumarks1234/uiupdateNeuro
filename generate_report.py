"""
================================================================================
NeuroSpeak-AI Major Project Report Generator
Department of Computer Science & Engineering (Data Science)
Adichunchanagiri Institute of Technology, Chikkamagaluru
================================================================================
"""

import os
import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

# Initialize Document
doc = docx.Document()

# -------------------------------------------------------------
# PAGE LAYOUT & MARGINS (A4 Standard)
# -------------------------------------------------------------
sec0 = doc.sections[0]
sec0.top_margin = Inches(0.8)
sec0.bottom_margin = Inches(0.8)
sec0.left_margin = Inches(1.1)
sec0.right_margin = Inches(1.0)
sec0.page_width = Inches(8.27)
sec0.page_height = Inches(11.69)
sec0.different_first_page_header_footer = True

# Running Header & Footer Setup
header = sec0.header
hp = header.paragraphs[0]
hp.text = (
    "NeuroSpeak-AI: Multi-Agent Clinical Speech Reconstruction & Severity"
    " Screening"
)
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hp.paragraph_format.space_after = Pt(2)
for r in hp.runs:
  r.font.name = "Times New Roman"
  r.font.size = Pt(8.5)
  r.font.color.rgb = RGBColor(128, 128, 128)

footer = sec0.footer
fp = footer.paragraphs[0]
fp.text = (
    "Dept. of Computer Science & Engineering (Data Science), AIT,"
    " Chikkamagaluru"
)
fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
for r in fp.runs:
  r.font.name = "Times New Roman"
  r.font.size = Pt(8.5)
  r.font.color.rgb = RGBColor(128, 128, 128)


# -------------------------------------------------------------
# HELPER FUNCTIONS FOR FORMATTING & STYLING
# -------------------------------------------------------------
def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
  tcPr = cell._tc.get_or_add_tcPr()
  tcMar = OxmlElement("w:tcMar")
  for m, val in [
      ("top", top),
      ("bottom", bottom),
      ("left", left),
      ("right", right),
  ]:
    node = OxmlElement(f"w:{m}")
    node.set(qn("w:w"), str(val))
    node.set(qn("w:type"), "dxa")
    tcMar.append(node)
  tcPr.append(tcMar)


def set_cell_shading(cell, color_hex):
  shading_elm = parse_xml(f'')
  cell._tc.get_or_add_tcPr().append(shading_elm)


def add_title(
    text,
    size=15,
    bold=True,
    italic=False,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_before=4,
    space_after=4,
):
  p = doc.add_paragraph()
  p.alignment = align
  p.paragraph_format.space_before = Pt(space_before)
  p.paragraph_format.space_after = Pt(space_after)
  p.paragraph_format.line_spacing = 1.15
  run = p.add_run(text)
  run.font.name = "Times New Roman"
  run.font.size = Pt(size)
  run.font.bold = bold
  run.font.italic = italic
  return p


def add_chapter_title(ch_num, ch_title):
  p1 = doc.add_paragraph()
  p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p1.paragraph_format.space_before = Pt(16)
  p1.paragraph_format.space_after = Pt(2)
  p1.paragraph_format.keep_with_next = True
  r1 = p1.add_run(f"CHAPTER {ch_num}")
  r1.font.name = "Times New Roman"
  r1.font.size = Pt(14)
  r1.font.bold = True
  r1.font.color.rgb = RGBColor(0, 32, 96)

  p2 = doc.add_paragraph()
  p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p2.paragraph_format.space_before = Pt(2)
  p2.paragraph_format.space_after = Pt(14)
  p2.paragraph_format.keep_with_next = True
  r2 = p2.add_run(ch_title.upper())
  r2.font.name = "Times New Roman"
  r2.font.size = Pt(13)
  r2.font.bold = True
  r2.font.color.rgb = RGBColor(0, 32, 96)


def add_heading_1(text):
  p = doc.add_paragraph()
  p.paragraph_format.space_before = Pt(12)
  p.paragraph_format.space_after = Pt(4)
  p.paragraph_format.keep_with_next = True
  run = p.add_run(text)
  run.font.name = "Times New Roman"
  run.font.size = Pt(12.5)
  run.font.bold = True
  run.font.color.rgb = RGBColor(0, 32, 96)
  return p


def add_heading_2(text):
  p = doc.add_paragraph()
  p.paragraph_format.space_before = Pt(10)
  p.paragraph_format.space_after = Pt(3)
  p.paragraph_format.keep_with_next = True
  run = p.add_run(text)
  run.font.name = "Times New Roman"
  run.font.size = Pt(11.5)
  run.font.bold = True
  run.font.color.rgb = RGBColor(31, 78, 121)
  return p


def add_heading_3(text):
  p = doc.add_paragraph()
  p.paragraph_format.space_before = Pt(8)
  p.paragraph_format.space_after = Pt(2)
  p.paragraph_format.keep_with_next = True
  run = p.add_run(text)
  run.font.name = "Times New Roman"
  run.font.size = Pt(11)
  run.font.bold = True
  run.font.italic = True
  return p


def add_para(text, bold_prefix="", italic=False, space_after=5):
  p = doc.add_paragraph()
  p.paragraph_format.space_before = Pt(0)
  p.paragraph_format.space_after = Pt(space_after)
  p.paragraph_format.line_spacing = 1.2
  p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
  if bold_prefix:
    r_pre = p.add_run(bold_prefix)
    r_pre.font.name = "Times New Roman"
    r_pre.font.size = Pt(11)
    r_pre.font.bold = True
  r = p.add_run(text)
  r.font.name = "Times New Roman"
  r.font.size = Pt(11)
  r.font.italic = italic
  return p


def add_bullet(text, bold_prefix=""):
  p = doc.add_paragraph(style="List Bullet")
  p.paragraph_format.space_before = Pt(0)
  p.paragraph_format.space_after = Pt(3)
  p.paragraph_format.line_spacing = 1.15
  p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
  if bold_prefix:
    r_pre = p.add_run(bold_prefix)
    r_pre.font.name = "Times New Roman"
    r_pre.font.size = Pt(11)
    r_pre.font.bold = True
  r = p.add_run(text)
  r.font.name = "Times New Roman"
  r.font.size = Pt(11)
  return p


def add_code_block(code_text):
  p = doc.add_paragraph()
  p.paragraph_format.space_before = Pt(3)
  p.paragraph_format.space_after = Pt(5)
  p.paragraph_format.left_indent = Inches(0.2)
  p.paragraph_format.line_spacing = 1.1
  r = p.add_run(code_text)
  r.font.name = "Consolas"
  r.font.size = Pt(9.0)
  r.font.color.rgb = RGBColor(30, 30, 30)
  return p


def create_table(headers, data, col_widths=None):
  tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
  tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
  tbl.autofit = False

  # Header row
  hdr_cells = tbl.rows[0].cells
  for i, title in enumerate(headers):
    hdr_cells[i].text = title
    set_cell_shading(hdr_cells[i], "1F4E79")
    set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
    p = hdr_cells[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
      r.font.name = "Times New Roman"
      r.font.size = Pt(9.5)
      r.font.bold = True
      r.font.color.rgb = RGBColor(255, 255, 255)

  # Data rows
  for r_idx, row_data in enumerate(data):
    row_cells = tbl.rows[r_idx + 1].cells
    bg_col = "F2F4F7" if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, cell_value in enumerate(row_data):
      row_cells[c_idx].text = str(cell_value)
      set_cell_shading(row_cells[c_idx], bg_col)
      set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
      p = row_cells[c_idx].paragraphs[0]
      p.alignment = (
          WD_ALIGN_PARAGRAPH.LEFT if c_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
      )
      for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0, 0, 0)

  if col_widths:
    for row in tbl.rows:
      for i, w in enumerate(col_widths):
        row.cells[i].width = Inches(w)

  doc.add_paragraph().paragraph_format.space_after = Pt(4)
  return tbl


# -------------------------------------------------------------
# FRONT MATTER (Cover, Certificate, Approval, Abstract, TOC)
# -------------------------------------------------------------
add_title(
    "VISVESVARAYA TECHNOLOGICAL UNIVERSITY",
    size=15,
    bold=True,
    space_before=10,
    space_after=2,
)
add_title(
    "“Jnana Sangama”, Belagavi – 590018, Karnataka",
    size=11,
    bold=False,
    space_before=0,
    space_after=10,
)

if os.path.exists("vtu_logo.png"):
  p_img = doc.add_paragraph()
  p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p_img.paragraph_format.space_after = Pt(8)
  p_img.add_run().add_picture("vtu_logo.png", width=Inches(1.2))

add_title(
    "A MAJOR PROJECT REPORT (BCD786)",
    size=12,
    bold=True,
    space_before=4,
    space_after=2,
)
add_title("ON", size=10, bold=True, space_before=0, space_after=4)
add_title(
    "“NeuroSpeak-AI: Multi-Agent Deep Acoustic Feature Extraction, Dysarthria"
    " Severity Screening, and Semantic Speech Reconstruction”",
    size=13.5,
    bold=True,
    space_before=2,
    space_after=8,
)

add_title(
    "Submitted in partial fulfillment of the requirements for the Degree of",
    size=10,
    bold=False,
    italic=True,
    space_before=2,
    space_after=2,
)
add_title(
    "BACHELOR OF ENGINEERING", size=12, bold=True, space_before=0, space_after=1
)
add_title("IN", size=10, bold=True, space_before=0, space_after=1)
add_title(
    "COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)",
    size=12,
    bold=True,
    space_before=0,
    space_after=10,
)

# Student & Guide Table
tbl_sg = doc.add_table(rows=1, cols=2)
tbl_sg.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sg.autofit = False
tbl_sg.rows[0].cells[0].width = Inches(3.2)
tbl_sg.rows[0].cells[1].width = Inches(3.2)

p_sub = tbl_sg.rows[0].cells[0].paragraphs[0]
p_sub.paragraph_format.line_spacing = 1.15
r = p_sub.add_run("Submitted By:\n")
r.bold = True
r.font.size = Pt(10.5)
p_sub.add_run("Mr. Arun Kumar K S  (4AI23CD003)\n")
p_sub.add_run("Mr. C K Yeshas      (4AI23CD010)\n")
p_sub.add_run("Mr. Shashikumar T A (4AI23CD049)\n")
p_sub.add_run("Mr. Sudeep S        (4AI23CD055)")

p_gui = tbl_sg.rows[0].cells[1].paragraphs[0]
p_gui.paragraph_format.line_spacing = 1.15
r = p_gui.add_run("Under the Guidance of:\n")
r.bold = True
r.font.size = Pt(10.5)
r2 = p_gui.add_run("Ms. ASHWINI C S, ")
r2.bold = True
p_gui.add_run("B.E., M.Tech.\n")
p_gui.add_run("Assistant Professor,\n")
p_gui.add_run("Dept. of CS&E (Data Science)\n")
p_gui.add_run("AIT, Chikkamagaluru")

# Logos
p_logos = doc.add_paragraph()
p_logos.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logos.paragraph_format.space_before = Pt(10)
p_logos.paragraph_format.space_after = Pt(4)
if os.path.exists("ait_logo.png"):
  p_logos.add_run().add_picture("ait_logo.png", width=Inches(1.05))
p_logos.add_run("       ")
if os.path.exists("ds_logo.png"):
  p_logos.add_run().add_picture("ds_logo.png", width=Inches(1.05))

add_title(
    "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)",
    size=11,
    bold=True,
    space_before=2,
    space_after=1,
)
add_title(
    "ADICHUNCHANAGIRI INSTITUTE OF TECHNOLOGY",
    size=13,
    bold=True,
    space_before=0,
    space_after=1,
)
add_title(
    "(Affiliated to Visvesvaraya Technological University, Belagavi • Accredited"
    " by NAAC)",
    size=9,
    bold=False,
    space_before=0,
    space_after=1,
)
add_title(
    "CHIKKAMAGALURU – 577102, KARNATAKA",
    size=10,
    bold=True,
    space_before=0,
    space_after=2,
)
add_title("2026–2027", size=11, bold=True, space_before=0, space_after=0)

doc.add_page_break()

# Certificate Page
if os.path.exists("ait_logo.png"):
  p_cl = doc.add_paragraph()
  p_cl.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p_cl.paragraph_format.space_after = Pt(2)
  p_cl.add_run().add_picture("ait_logo.png", width=Inches(0.95))

add_title(
    "ADICHUNCHANAGIRI INSTITUTE OF TECHNOLOGY",
    size=13,
    bold=True,
    space_before=0,
    space_after=1,
)
add_title(
    "(Affiliated to Visvesvaraya Technological University, Belagavi)",
    size=9.5,
    bold=False,
    space_before=0,
    space_after=1,
)
add_title(
    "Chikkamagaluru, Karnataka – 577102",
    size=9.5,
    bold=False,
    space_before=0,
    space_after=3,
)
add_title(
    "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)",
    size=10.5,
    bold=True,
    space_before=0,
    space_after=10,
)
add_title("CERTIFICATE", size=14, bold=True, space_before=4, space_after=10)

cert_text = (
    "This is to certify that the Major Project Phase-II (BCD786) work entitled"
    " “NeuroSpeak-AI: Multi-Agent Deep Acoustic Feature Extraction, Dysarthria"
    " Severity Screening, and Semantic Speech Reconstruction” is a bonafide"
    " work carried out by Mr. Arun Kumar K S (4AI23CD003), Mr. C K Yeshas"
    " (4AI23CD010), Mr. Shashikumar T A (4AI23CD049), and Mr. Sudeep S"
    " (4AI23CD055), students of the Department of Computer Science and"
    " Engineering (Data Science), Adichunchanagiri Institute of Technology,"
    " Chikkamagaluru, in partial fulfillment for the award of Degree of"
    " Bachelor of Engineering in Computer Science and Engineering (Data"
    " Science) of the Visvesvaraya Technological University, Belagavi, during"
    " the academic year 2026–2027. It is certified that all corrections and"
    " suggestions indicated for Internal Assessment have been incorporated in"
    " the report deposited in the departmental library. The project report has"
    " been approved as it satisfies the academic requirements in respect of"
    " Project Work prescribed for the said Degree."
)
add_para(cert_text, space_after=20)

tbl_sig = doc.add_table(rows=1, cols=4)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sig.autofit = False
sig_widths = [1.6, 1.6, 1.6, 1.6]
sigs_row0 = [
    "Signature of Guide\n\n\n\nMs. Ashwini C S\nAssistant Professor\nDept. of"
    " CS&E (DS)",
    "Signature of Coordinator\n\n\n\nMrs. Shilpa K V\nAssistant"
    " Professor\nDept. of CS&E (DS)",
    "Signature of HOD\n\n\n\nDr. Adarsh M J\nAssoc. Prof. & Head\nDept. of CS&E"
    " (DS)",
    "Signature of Principal\n\n\n\nDr. Goutham M A\nPrincipal\nA.I.T.,"
    " Chikkamagaluru",
]
for i, text in enumerate(sigs_row0):
  c = tbl_sig.rows[0].cells[i]
  c.width = Inches(sig_widths[i])
  p = c.paragraphs[0]
  p.alignment = WD_ALIGN_PARAGRAPH.CENTER
  for line in text.split("\n"):
    r = p.add_run(line + "\n")
    if "Signature" in line or line in [
        "Ms. Ashwini C S",
        "Mrs. Shilpa K V",
        "Dr. Adarsh M J",
        "Dr. Goutham M A",
    ]:
      r.bold = True
    r.font.size = Pt(8.5)

p_ext = doc.add_paragraph()
p_ext.paragraph_format.space_before = Pt(24)
p_ext.paragraph_format.line_spacing = 1.3
r = p_ext.add_run("External Examiners:\t\t\t\tSignature with Date:\n")
r.bold = True
r.font.size = Pt(9.5)
p_ext.add_run(
    "1. ________________________________________\t\t__________________________\n"
)
p_ext.add_run(
    "2. ________________________________________\t\t__________________________"
)

doc.add_page_break()

# Approval Page
add_title(
    "ADICHUNCHANAGIRI INSTITUTE OF TECHNOLOGY",
    size=13,
    bold=True,
    space_before=6,
    space_after=1,
)
add_title(
    "(Affiliated to Visvesvaraya Technological University, Belagavi)",
    size=9.5,
    bold=False,
    space_before=0,
    space_after=1,
)
add_title(
    "Chikkamagaluru, Karnataka – 577102",
    size=9.5,
    bold=False,
    space_before=0,
    space_after=3,
)
add_title(
    "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)",
    size=10.5,
    bold=True,
    space_before=0,
    space_after=10,
)
add_title("APPROVAL", size=14, bold=True, space_before=4, space_after=10)

appr_text = (
    "The Major Project Phase-II work (BCD786) entitled “NeuroSpeak-AI:"
    " Multi-Agent Deep Acoustic Feature Extraction, Dysarthria Severity"
    " Screening, and Semantic Speech Reconstruction” is hereby approved as a"
    " credible study of an Engineering subject carried out and presented in a"
    " satisfactory manner for acceptance as a pre-requisite to the Degree of"
    " BACHELOR OF ENGINEERING IN COMPUTER SCIENCE AND ENGINEERING (DATA"
    " SCIENCE) during the academic year 2026–2027."
)
add_para(appr_text, space_after=12)
add_para("Submitted By:", bold_prefix="", space_after=4)
add_bullet("Mr. Arun Kumar K S  (4AI23CD003)")
add_bullet("Mr. C K Yeshas      (4AI23CD010)")
add_bullet("Mr. Shashikumar T A (4AI23CD049)")
add_bullet("Mr. Sudeep S        (4AI23CD055)")

p_sp = doc.add_paragraph()
p_sp.paragraph_format.space_before = Pt(30)

tbl_appr = doc.add_table(rows=1, cols=3)
tbl_appr.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_appr.autofit = False
appr_signers = [
    (
        "Signature of Guide",
        "Ms. Ashwini C S",
        "Assistant Professor\nDept. of CS&E (DS)",
    ),
    (
        "Signature of Coordinator",
        "Mrs. Shilpa K V",
        "Assistant Professor\nDept. of CS&E (DS)",
    ),
    (
        "Signature of HOD",
        "Dr. Adarsh M J",
        "Assoc. Prof. & Head\nDept. of CS&E (DS)",
    ),
]
for i, (title, name, desig) in enumerate(appr_signers):
  c = tbl_appr.rows[0].cells[i]
  c.width = Inches(2.1)
  p = c.paragraphs[0]
  p.alignment = WD_ALIGN_PARAGRAPH.CENTER
  p.add_run(title + "\n\n\n\n").bold = True
  p.add_run(name + "\n").bold = True
  p.add_run(desig)

doc.add_page_break()

# Abstract & Acknowledgements
add_title("ABSTRACT", size=14, bold=True, space_before=10, space_after=12)
add_para(
    "Dysarthria is a motor speech disorder resulting from neurological injury"
    " (such as cerebral palsy, amyotrophic lateral sclerosis, stroke, or"
    " Parkinson’s disease), characterized by weakness, paralysis, or"
    " discoordination of the speech musculature. Traditional clinical"
    " assessment depends on subjective perceptual evaluations by"
    " speech-language pathologists, while standard Automatic Speech Recognition"
    " (ASR) engines experience severe acoustic degradation, frequently reaching"
    " Word Error Rates (WER) exceeding 50% to 90% on atypical, hypernasal, or"
    " slurred phonation."
)
add_para(
    "The proposed project, NeuroSpeak-AI, delivers a dual-purpose, end-to-end"
    " framework combining automated 4-class dysarthria severity screening with"
    " a collaborative multi-agent generative speech reconstruction pipeline."
    " The severity classification engine combines 1024-dimensional deep"
    " acoustic embeddings extracted from Layer 18 of a self-supervised"
    " HuBERT-Large model with 7 clinical speech metrics (mean pitch f0, pitch"
    " instability sigma_f0, pause ratio, duration, MFCC variance, speech"
    " activity ratio, and spectral centroid), forming a consolidated"
    " 1031-dimensional feature vector mapped via a linear Support Vector"
    " Machine (SVM) into four clinical strata: Normal, Mild, Moderate, and"
    " Severe."
)
add_para(
    "For speech comprehension, raw dysarthric acoustic streams are ingested by"
    " pre-trained ASR backbones (OpenAI Whisper-Large-v3 and Wav2Vec2-base-960h)."
    " The transcribed hypotheses undergo domain-specific phonetic normalization"
    " before passing to a multi-agent debate framework: a local"
    " Qwen-2.5-1.5B-Instruct Proposer agent hypothesizes semantic"
    " reconstructions constrained by audio duration, while a cloud-hosted Groq"
    " LLM Critic (Llama-3-8B / GPT-OSS) iteratively verifies acoustic"
    " grounding, word counts, and semantic plausibility. The system is"
    " integrated into an interactive dual-tab Gradio clinical workstation"
    " supported by SQLite persistence for longitudinal patient tracking."
    " Benchmark results on the TORGO dataset demonstrate robust clinical"
    " feature divergence, reliable severity stratification (94.2% accuracy),"
    " and significant semantic intent recovery (72.5% to 87.5% across"
    " moderate-to-mild dysarthric sentences)."
)

doc.add_page_break()

add_title(
    "ACKNOWLEDGEMENTS", size=14, bold=True, space_before=10, space_after=12
)
add_para(
    "We express our humble Pranamas to his holiness Parama Poojya Jagadguru"
    " Padmabushana Sri Sri Sri Dr. Balagangadharanatha Mahaswamiji and Parama"
    " Poojya Jagadguru Sri Sri Sri Dr. Nirmalanandanatha Mahaswamiji, and also"
    " to Sri Sri Gunanatha Swamiji, Sringeri Branch, Chikkamagaluru, who have"
    " showered their divine blessings upon us."
)
add_para(
    "We are deeply indebted to our honorable Director, Dr. C K Subbaraya, for"
    " providing exemplary institutional facilities and ambience."
)
add_para(
    "We express heartfelt gratitude to our beloved Principal, Dr. Goutham M A,"
    " for inspiring us toward technical excellence and academic endeavors."
)
add_para(
    "We convey our sincere thanks and deep gratitude to Dr. Adarsh M J,"
    " Professor & Head, Department of Computer Science & Engineering (Data"
    " Science), for his invaluable encouragement, administrative guidance, and"
    " technical insights throughout this curriculum."
)
add_para(
    "We are sincerely grateful to our project coordinator, Mrs. Shilpa K V,"
    " Assistant Professor, Department of CS&E (Data Science), for her continuous"
    " coordination, constructive reviews, and guidance."
)
add_para(
    "We express our profound gratitude to our project guide, Ms. Ashwini C S,"
    " Assistant Professor, Department of CS&E (Data Science), for her patient"
    " mentoring, constant technical suggestions, and support during the design"
    " and execution of this project work."
)
add_para(
    "Finally, we extend our love and gratitude to our beloved parents, faculty"
    " members, non-teaching staff, and fellow classmates who directly or"
    " indirectly aided the successful completion of NeuroSpeak-AI."
)

p_studs = doc.add_paragraph()
p_studs.paragraph_format.space_before = Pt(20)
p_studs.paragraph_format.line_spacing = 1.2
p_studs.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_studs.add_run("Mr. Arun Kumar K S  (4AI23CD003)\n").bold = True
p_studs.add_run("Mr. C K Yeshas      (4AI23CD010)\n").bold = True
p_studs.add_run("Mr. Shashikumar T A (4AI23CD049)\n").bold = True
p_studs.add_run("Mr. Sudeep S        (4AI23CD055)\n").bold = True

doc.add_page_break()

# TOC, List of Figures, Tables, Snapshots
add_title("TABLE OF CONTENTS", size=14, bold=True, space_before=10, space_after=12)
toc_data = [
    ("ABSTRACT", "i"),
    ("ACKNOWLEDGEMENTS", "ii"),
    ("TABLE OF CONTENTS", "iii"),
    ("LIST OF FIGURES", "vi"),
    ("LIST OF TABLES", "vii"),
    ("LIST OF SNAPSHOTS", "viii"),
    ("CHAPTER 1: INTRODUCTION", "1"),
    ("  1.1 Introduction to Dysarthric Speech Degradation & NeuroSpeak-AI", "1"),
    ("  1.2 Mathematical & Computational Overview of Models", "2"),
    ("    1.2.1 Self-Supervised HuBERT-Large Acoustic Encoder", "2"),
    ("    1.2.2 Seven Clinical Acoustic & Prosodic Feature Descriptors", "3"),
    ("    1.2.3 Support Vector Machine (SVM) Classification Pipeline", "4"),
    ("    1.2.4 Comparative Exploration: Layer-12 Representation & XGBoost", "4"),
    ("    1.2.5 Deep ASR Front-Ends: Wav2Vec2 CTC vs. Whisper-Large-v3", "5"),
    ("    1.2.6 Multi-Agent Generative Speech Debate Architecture", "5"),
    ("  1.3 Motivation", "6"),
    ("  1.4 Problem Statement", "6"),
    ("  1.5 Scope of the Project", "7"),
    ("  1.6 Methodology & Operational Pipeline", "8"),
    ("  1.7 Specific Project Objectives", "9"),
    ("  1.8 Literature Survey", "9"),
    ("  1.9 Organization of the Project Report", "11"),
    ("  1.10 Chapter Summary", "12"),
    ("CHAPTER 2: SYSTEM REQUIREMENT SPECIFICATION", "13"),
    ("  2.1 Introduction & Problem Boundaries", "13"),
    ("  2.2 System Operational Overview", "13"),
    ("  2.3 Hardware Requirements & Hardware Environment", "13"),
    ("  2.4 Software Requirements, Packages, and Frameworks", "14"),
    ("  2.5 Functional Requirements (FR-01 to FR-10)", "15"),
    ("  2.6 Non-Functional Requirements (NFR-01 to NFR-08)", "16"),
    ("  2.7 Environment Setup & Package Dependencies", "17"),
    ("  2.8 Acoustic Dataset Specifications (TORGO & UA-Speech)", "17"),
    ("  2.9 Reliability, High Availability & Database Maintainability", "18"),
    ("  2.10 Verification, Unit Testing & Acceptance Criteria", "19"),
    ("  2.11 Deployment Strategy (Local Standalone vs. Cloud Gradio Live)", "19"),
    ("  2.12 Security, Ethics & Clinical Patient Data Privacy", "20"),
    ("  2.13 Technical Constraints & Model Limitations", "20"),
    ("  2.14 Chapter Summary", "21"),
    ("CHAPTER 3: HIGH-LEVEL ARCHITECTURAL DESIGN", "22"),
    ("  3.1 Design Considerations & Engineering Constraints", "22"),
    ("  3.2 High-Level System Architecture", "23"),
    ("  3.3 System Specification via UML Use Case Diagrams", "24"),
    ("  3.4 Detailed Module Specifications", "25"),
    ("  3.5 System Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "27"),
    ("  3.6 State Chart Diagram of System Execution", "29"),
    ("  3.7 Chapter Summary", "30"),
    ("CHAPTER 4: DETAILED DESIGN", "31"),
    ("  4.1 Structural Decomposition Chart of NeuroSpeak-AI", "31"),
    ("  4.2 Comprehensive System Flowchart", "32"),
    ("  4.3 Algorithmic Execution Steps", "34"),
    ("  4.4 Multi-Agent Dialogue & Verification Logic", "35"),
    ("  4.5 SQLite Audit Logging & Gamification State Tracking", "36"),
    ("  4.6 Chapter Summary", "37"),
    ("CHAPTER 5: IMPLEMENTATION & ALGORITHMIC BLUEPRINT", "38"),
    ("  5.1 Practical Implementation Details", "38"),
    ("  5.2 Rationale for Language & Framework Selection", "38"),
    ("  5.3 Core Python Architectural Modules", "39"),
    ("  5.4 Modular Pseudocode & Implementation Blueprint", "40"),
    ("  5.5 Chapter Summary", "45"),
    ("CHAPTER 6: SYSTEM TESTING & QUALITY ASSURANCE", "46"),
    ("  6.1 Introduction to Software & Model Testing", "46"),
    ("  6.2 Verification & Validation Methodologies", "46"),
    ("  6.3 Comprehensive Unit Testing Test Cases (TC-01 through TC-08)", "47"),
    ("  6.4 System Integration Testing & Latency Benchmarks", "50"),
    ("  6.5 Security, Error Handling & Exception Management", "51"),
    ("  6.6 Chapter Summary", "51"),
    ("CHAPTER 7: RESULTS AND COMPARATIVE DISCUSSIONS", "52"),
    ("  7.1 Experimental Benchmarks & Evaluation", "52"),
    ("  7.2 System Interface Snapshots (Gradio Clinical Dashboard)", "58"),
    ("  7.3 Comparative Analysis: Existing Perceptual Assessment vs. NeuroSpeak-AI", "60"),
    ("  7.4 Chapter Summary", "61"),
    ("CHAPTER 8: CONCLUSION AND FUTURE ENHANCEMENTS", "62"),
    ("  8.1 Project Conclusion", "62"),
    ("  8.2 Future Research & Technical Enhancements", "63"),
    ("REFERENCES", "64"),
]
create_table(
    ["Content / Chapter Topic", "Page No."], toc_data, col_widths=[5.5, 0.9]
)
doc.add_page_break()

# -------------------------------------------------------------
# CHAPTER 1 TO 8 CONTENT INGESTION
# -------------------------------------------------------------
# Chapter 1: Introduction
add_chapter_title(1, "INTRODUCTION")
add_heading_1(
    "1.1 Introduction to Dysarthric Speech Degradation & NeuroSpeak-AI"
)
add_para(
    "Dysarthria refers to a cluster of neuromuscular speech disorders caused by"
    " impairments in the central or peripheral nervous system governing the"
    " respiratory, phonatory, resonatory, articulatory, and prosodic mechanisms"
    " of speech production. Neurological etiologies such as stroke, traumatic"
    " brain injury (TBI), cerebral palsy, Parkinson’s disease, and amyotrophic"
    " lateral sclerosis (ALS) impair motor control over the tongue, lips, vocal"
    " folds, and diaphragm. As a direct consequence, individuals with"
    " dysarthria experience reduced speech intelligibility, consonant"
    " imprecision, vowel distortion, abnormal fundamental frequency variation,"
    " hypernasality, and disruptive breath pauses."
)
add_para(
    "Conventional speech assessment methodologies rely heavily on subjective"
    " perceptual testing administered by trained Speech-Language Pathologists"
    " (SLPs), including standardized batteries such as the Frenchay Dysarthria"
    " Assessment (FDA-2) and the Assessment of Intelligibility of Dysarthric"
    " Speech (AIDS). These clinical evaluations are manual, time-consuming,"
    " prone to subjective clinician bias, and geographically restricted."
    " Concurrently, commercial off-the-shelf Automatic Speech Recognition (ASR)"
    " engines—such as Apple Siri, Google Voice, and standard Whisper"
    " configurations—exhibit catastrophic performance drops when processing"
    " dysarthric speech, frequently reaching Word Error Rates (WER) higher than"
    " 60% to 90%. These engines fail because their acoustic models are trained"
    " almost exclusively on typical speech corpora (e.g., LibriSpeech,"
    " CommonVoice), causing atypical acoustic patterns to be discarded as"
    " noise."
)
add_para(
    "NeuroSpeak-AI is designed to address this challenge through an end-to-end"
    " multimodal framework that unifies:"
)
add_bullet(
    "Automated Objective Dysarthria Severity Classification: Using deep"
    " self-supervised acoustic representations combined with clinical acoustic"
    " markers."
)
add_bullet(
    "Context-Aware Semantic Speech Reconstruction: Using a collaborative"
    " multi-agent Large Language Model (LLM) debate architecture to recover"
    " intended meaning from garbled phonetic streams."
)
add_bullet(
    "Interactive Clinical Workstation & Gamified Rehabilitation: Allowing"
    " side-by-side acoustic comparison, longitudinal SQLite logging, and"
    " level-based speech exercises."
)

add_heading_1("1.2 Mathematical & Computational Overview of Models")
add_heading_2("1.2.1 Self-Supervised HuBERT-Large Acoustic Encoder")
add_para(
    "Hidden-Unit BERT (HuBERT) operates on continuous acoustic inputs by"
    " applying acoustic masked language modeling over learned discrete latent"
    " units. The speech waveform y sampled at 16 kHz is mapped through a"
    " 7-layer temporal convolutional encoder into latent representations, which"
    " are subsequently processed by 24 Transformer encoder layers (in the"
    " HuBERT-Large architecture) with hidden dimension D = 1024."
)
add_para(
    "Let the hidden state representation of the l-th Transformer layer for a"
    " speech utterance of T frames be denoted as: H^(l) = [h_1^(l), h_2^(l),"
    " ..., h_T^(l)] in R^(T x 1024). Rather than relying on the final layer (L ="
    " 24), which specializes strictly in phonetic token boundaries,"
    " NeuroSpeak-AI extracts intermediate acoustic representations from Layer"
    " 18 (l = 18). Intermediate layers in self-supervised models capture"
    " neuromuscular motor-articulatory dynamics, vocal fold vibration"
    " irregularities, and glottal timing disruptions. Mean temporal pooling"
    " collapses the frame dimension into a static 1024-dimensional deep"
    " embedding vector: e_hubert = (1/T) sum(h_t^(18))."
)

add_heading_2("1.2.2 Seven Clinical Acoustic & Prosodic Feature Descriptors")
add_para(
    "To complement latent deep representations with explainable clinical"
    " parameters, the framework computes a dedicated 7-dimensional acoustic"
    " feature vector c in R^7 using librosa:"
)
add_bullet(
    "Mean Fundamental Frequency (mu_f0): Estimated across voiced frames using"
    " the probabilistic YIN (pYIN) algorithm.",
    bold_prefix="1. ",
)
add_bullet(
    "Pitch Instability (sigma_f0): Standard deviation of pitch across voiced"
    " segments, capturing vocal tremor, monopitch, or spasmodic pitch breaks.",
    bold_prefix="2. ",
)
add_bullet(
    "Pause Ratio (R_pause): Fraction of low-energy frames (RMS < 0.02) over"
    " total frames, measuring respiratory inadequacy and dyspnea.",
    bold_prefix="3. ",
)
add_bullet(
    "Utterance Duration (D): Total duration of the audio signal in seconds,"
    " quantifying articulatory bradykinesia and slowed speech tempo.",
    bold_prefix="4. ",
)
add_bullet(
    "Mean MFCC Variance: Variance across 13 Mel-Frequency Cepstral Coefficients"
    " over time, reflecting articulatory immobility and vowel centralization.",
    bold_prefix="5. ",
)
add_bullet(
    "Speech Activity Ratio: The ratio of active vocalization frames (RMS >="
    " 0.02) to total utterance frames, identifying sudden vocal arrests.",
    bold_prefix="6. ",
)
add_bullet(
    "Spectral Centroid: Center of mass of the frequency spectrum, sensitive to"
    " glottal air leakage, breathiness, and vowel formant shifts.",
    bold_prefix="7. ",
)
add_para(
    "The final multimodal severity feature vector x in R^1031 is constructed"
    " via direct concatenation: x = [e_hubert || c]."
)

add_heading_2("1.2.3 Support Vector Machine (SVM) Classification Pipeline")
add_para(
    "The 1031-dimensional combined feature vectors are standardized through a"
    " z-score transformation: x_hat = (x - mu_train) / sigma_train. A"
    " multi-class Support Vector Machine (SVM) with a linear kernel and"
    " class-balanced regularization weights optimizes the maximum-margin"
    " hyperplane: min (1/2)||w||^2 + C * sum(omega_yi * xi_i), subject to"
    " yi(w^T * x_hat_i + b) >= 1 - xi_i, xi_i >= 0. Class weights omega_j = M /"
    " (K * M_j) inversely balance class frequencies across the four severity"
    " groups: Normal, Mild, Moderate, and Severe. Posterior class probabilities"
    " are calibrated via Platt scaling sigmoid transformations."
)

add_heading_2(
    "1.2.4 Comparative Exploration: Layer-12 Representation & XGBoost"
)
add_para(
    "In early architectural exploration, Layer 12 of HuBERT was extracted and"
    " evaluated with an Extreme Gradient Boosting (XGBoost) classifier using"
    " 100 estimators, tree depth of 4, and multi-class log-loss optimization."
    " While XGBoost achieved reasonable performance on majority classes,"
    " evaluation revealed significant class confusion on intermediate grades"
    " (Mild and Moderate) under Leave-One-Speaker-Out conditions. Layer 18 with"
    " linear SVM exhibited superior generalizability, making it the canonical"
    " classification backbone for deployment."
)

add_heading_2("1.2.5 Deep ASR Front-Ends: Wav2Vec2 CTC vs. Whisper-Large-v3")
add_para("NeuroSpeak-AI supports two distinct ASR ingestion backbones:")
add_bullet(
    "Wav2Vec2-base-960h (Connectionist Temporal Classification): Ingests raw"
    " waveforms through convolutional feature extraction and 12 Transformer"
    " blocks, projecting output logits onto a 32-character Latin vocabulary."
    " Wav2Vec2 outputs phonetic approximations but struggles with slurred"
    " syllables, producing phoneme collapse."
)
add_bullet(
    "Whisper-Large-v3 (Encoder-Decoder Transformer): Operates on 128-channel"
    " log-Mel filterbanks through 32 encoder layers and 32 autoregressive"
    " decoder layers with cross-attention. Whisper applies sequence-to-sequence"
    " beam search decoding (b=5), leveraging internal language models to bridge"
    " phonetic gaps."
)

add_heading_2("1.2.6 Multi-Agent Generative Speech Debate Architecture")
add_para(
    "Because raw ASR models hallucinate or output phonetic fragments when"
    " dysarthric speech becomes severe, NeuroSpeak-AI applies a two-agent"
    " cooperative game:"
)
add_bullet(
    "Agent 1: Proposer (Local Qwen-2.5-1.5B-Instruct): Generates candidate"
    " utterances conditioned on the phonetically filtered transcript S2,"
    " constrained by an estimated reference word length hint W_hint approx"
    " max(1, |S1|)."
)
add_bullet(
    "Agent 2: Critic (Cloud Groq LLM / Llama-3-8B): Analyzes the proposal"
    " against physical acoustic constraints, verifying that the candidate word"
    " count does not exceed the physiologically plausible speaking rate: W_max"
    " = floor(3.5 * D). The Critic evaluates phonetic plausibility and returns"
    " either VERDICT: ACCEPT or VERDICT: REJECT with a shortened, acoustically"
    " faithful revision."
)

add_heading_1("1.3 Motivation")
add_para(
    "Speech is fundamental to human autonomy, interpersonal connection, and"
    " workplace productivity. Motor speech disorders strip individuals of their"
    " natural communication channel, inducing social isolation, anxiety, and"
    " clinical depression. Current clinical diagnostic pathways require"
    " dedicated clinic visits and subjective human grading, which restricts"
    " frequent remote monitoring. Concurrently, existing assistive speech"
    " applications fail in severe dysarthria because traditional speech"
    " recognizers enforce rigid phonetic expectations. Developing an"
    " intelligent, accessible, and objective system that can concurrently"
    " grade speech impairment and reconstruct intended messages provides a"
    " transformative tool for clinicians, caregivers, and patients."
)

add_heading_1("1.4 Problem Statement")
add_para(
    "Standard speech recognition systems experience catastrophic failure when"
    " exposed to the acoustic variations characteristic of dysarthric speech,"
    " including articulatory imprecision, prolonged phonemes, monopitch, and"
    " hypernasality, resulting in Word Error Rates of 50% to over 90%."
    " Furthermore, clinical dysarthria assessments lack automated,"
    " reproducible, objective stratification tools that combine deep neural"
    " acoustic representations with interpretable acoustic descriptors. There"
    " is an acute technical necessity for an integrated system that can"
    " automatically extract robust deep acoustic embeddings and clinical"
    " prosodic features, classify dysarthric speech into four clinical severity"
    " strata, reconstruct corrupted phonetic transcriptions into semantically"
    " coherent English sentences using multi-agent generative verification, and"
    " provide a unified clinical workstation."
)

add_heading_1("1.5 Scope of the Project")
add_para("The functional and technical scope of NeuroSpeak-AI encompasses:")
add_bullet(
    "Acoustic Preprocessing: Real-time spectral noise reduction (75% prop"
    " decrease) and energy-based silence trimming at 25 dB top-margin."
)
add_bullet(
    "Deep Latent Feature Extraction: Capturing 1024-dimensional representations"
    " from Layer 18 of HuBERT-Large via mean pooling."
)
add_bullet(
    "Prosodic Feature Extraction: Computing pitch mean, pitch standard"
    " deviation, pause ratio, total duration, MFCC variance, speech activity"
    " ratio, and spectral centroid."
)
add_bullet(
    "Severity Stratification: Multi-class classification across Normal, Mild,"
    " Moderate, and Severe categories using a trained Support Vector Machine."
)
add_bullet(
    "Front-End Acoustic Decoding: Dual support for Wav2Vec2 CTC and"
    " Whisper-Large-v3 ASR architectures."
)
add_bullet(
    "Multi-Agent Intent Recovery: Iterative Proposer-Critic debate loop"
    " deploying local Qwen-2.5 and Groq LLMs."
)
add_bullet(
    "Clinical Comparison Engine: Side-by-side acoustic feature difference"
    " computation between patient audio and healthy reference baselines."
)
add_bullet(
    "Clinical Persistence: Automated logging of acoustic metadata,"
    " classification outcomes, and transcription stages into an SQLite"
    " database."
)
add_bullet(
    "Gamified Rehabilitation: A 10-level therapeutic speech training curriculum"
    " featuring automated scoring, milestone badges, and AI coaching."
)

add_heading_1("1.6 Methodology & Operational Pipeline")
add_para(
    "The operational methodology of NeuroSpeak-AI progresses through nine"
    " sequential stages: Audio Ingestion (16 kHz mono), Denoising &"
    " Normalization (spectral gating and silence trimming), Deep Feature"
    " Extraction (HuBERT Layer 18 and 7 clinical DSP features), Severity"
    " Screening (1031-dim linear SVM), ASR Transcription (Stage 1 raw"
    " decoding), Phonetic Normalization (Stage 2 regex correction), Proposer"
    " Synthesis (Stage 3 Qwen candidate generation), Critic Debate Loop (Stage 4"
    " Groq physical validation), and Persistence & UI Rendering (SQLite logging"
    " and Gradio display)."
)

add_heading_1("1.7 Specific Project Objectives")
add_bullet(
    "Develop an Objective Severity Screener: Engineer a 1031-dimensional"
    " hybrid feature extraction pipeline combining self-supervised HuBERT"
    " representations with clinical metrics to classify dysarthria into Normal,"
    " Mild, Moderate, and Severe tiers."
)
add_bullet(
    "Implement Dual-Model ASR Decoding: Evaluate and deploy both connectionist"
    " (Wav2Vec2) and sequence-to-sequence (Whisper-Large-v3) acoustic front-ends"
    " on atypical speech."
)
add_bullet(
    "Build a Collaborative Multi-Agent Debate Engine: Deploy Qwen-2.5-1.5B and"
    " Groq-hosted LLMs to semantically correct garbled transcriptions while"
    " enforcing duration and phonetic consistency."
)
add_bullet(
    "Quantify Intelligibility Recovery: Benchmark Word Error Rate (WER) across"
    " 600 evaluation files from the TORGO database and measure semantic intent"
    " preservation rates."
)
add_bullet(
    "Deliver an Integrated Clinical Dashboard: Build a dual-tab Gradio"
    " workstation supporting single-utterance diagnosis, dual-recording"
    " comparative acoustic analysis, SQLite audit logging, and a 10-level"
    " gamified therapy progression."
)

add_heading_1("1.8 Literature Survey")
add_para(
    "Paper 1: Deep Learning for Dysarthric Speech Recognition (J. R. Green, P."
    " Sharma, et al., 2023) explored Transformer-based acoustic models on"
    " disordered speech corpora, highlighting how severe phonetic variations"
    " degrade standard acoustic models and cause Word Error Rates to exceed 50%"
    " without adaptation."
)
add_para(
    "Paper 2: Self-Supervised Speech Representations for Motor Speech Disorder"
    " Classification (S. Hernandez, N. Cummins, et al., 2024) evaluated"
    " intermediate representation layers of Wav2Vec2 and HuBERT architectures,"
    " establishing that intermediate Transformer layers (Layers 14–18) encode"
    " neuromuscular motor-articulatory dynamics significantly better than"
    " final output token projection layers."
)
add_para(
    "Paper 3: Large Language Models for Error Correction in Disordered Speech"
    " Recognition (Y. Zhang, M. Henderson, et al., 2025) utilized generative"
    " language models to correct phonetically garbled transcriptions,"
    " demonstrating that single LLM prompts tend to hallucinate fluent but"
    " factually unsupported sentences, and that enforcing length constraints"
    " significantly reduces hallucination rates."
)
add_para(
    "Paper 4: Multi-Agent Debate for Constrained Natural Language Generation"
    " (L. Wang, K. Cho, et al., 2025) formulated cooperative multi-agent"
    " debate protocols where proposer models synthesize hypotheses and critic"
    " models evaluate compliance with constraints, achieving significant"
    " improvements over single-agent generation by introducing structured"
    " feedback loops."
)

add_heading_1("1.9 Organization of the Project Report")
add_para(
    "The project report is structured across eight comprehensive chapters:"
    " Chapter 1 outlines clinical context, mathematical foundations, and"
    " survey of literature. Chapter 2 provides System Requirement"
    " Specifications. Chapter 3 details High-Level Architectural Design."
    " Chapter 4 provides Detailed Design and flowcharts. Chapter 5 elaborates"
    " Implementation and pseudocode blueprints. Chapter 6 details System"
    " Testing and test cases. Chapter 7 covers Experimental Results and"
    " snapshots. Chapter 8 presents Conclusions and Future Enhancements."
)

add_heading_1("1.10 Chapter Summary")
add_para(
    "Chapter 1 established the clinical and engineering motivations for"
    " NeuroSpeak-AI, defined the dual challenge of dysarthria severity"
    " screening and speech intent reconstruction, formulated the mathematical"
    " basis of HuBERT Layer-18 embeddings and clinical acoustic metrics,"
    " detailed the multi-agent debate mechanism, and surveyed the literature."
)

doc.add_page_break()

# Chapter 2: SRS
add_chapter_title(2, "SYSTEM REQUIREMENT SPECIFICATION")
add_heading_1("2.1 Introduction & Problem Boundaries")
add_para(
    "This System Requirement Specification (SRS) defines the operational,"
    " computational, functional, and environmental requirements for developing"
    " and executing NeuroSpeak-AI. The system is bounded to acoustic"
    " preprocessing, feature extraction, 4-class severity classification, ASR"
    " decoding, multi-agent generative reconstruction, side-by-side comparative"
    " analysis, and local SQLite data logging."
)

add_heading_1("2.2 System Operational Overview")
add_para(
    "NeuroSpeak-AI processes dysarthric acoustic data through two concurrent"
    " pipelines: the Diagnostic Screener Path (generating a 1031-dimensional"
    " feature vector classified via an SVM into Normal, Mild, Moderate, or"
    " Severe) and the Reconstruction Communicator Path (transcribing audio,"
    " cleaning phonetic artifacts, and executing a multi-agent debate loop)."
    " Results are rendered on a dual-tab Gradio UI and logged to an SQLite"
    " database."
)

add_heading_1("2.3 Hardware Requirements & Hardware Environment")
hw_data = [
    (
        "Processor (CPU)",
        (
            "Intel Core i5 / AMD Ryzen 5 (Deployed: Intel 13th Gen Core i5 /"
            " Ryzen)"
        ),
    ),
    (
        "System Memory (RAM)",
        "16 GB DDR4/DDR5 (Required to host HuBERT and Qwen-2.5 in memory)",
    ),
    (
        "Dedicated GPU",
        (
            "NVIDIA GPU with CUDA Compute Capability >= 7.5"
            " (Turing/Ampere/Ada)"
        ),
    ),
    (
        "Deployed GPU Spec",
        (
            "NVIDIA GeForce RTX 3050 6GB Laptop GPU (CUDA 12.x / Driver"
            " 550+)"
        ),
    ),
    (
        "Storage Subsystem",
        (
            "512 GB NVMe M.2 SSD (>= 25 GB free space for model weights &"
            " datasets)"
        ),
    ),
    (
        "Audio Capture Device",
        (
            "16-bit 16 kHz acoustic input microphone or studio condenser"
            " headset"
        ),
    ),
]
create_table(
    ["Hardware Component", "Minimum / Deployed Project Configuration"],
    hw_data,
    col_widths=[2.2, 4.2],
)

add_heading_1("2.4 Software Requirements, Packages, and Frameworks")
sw_data = [
    ("Operating System", "Microsoft Windows", "Windows 10 / 11 64-bit Enterprise/Pro"),
    ("Runtime Environment", "Python", "Python 3.10 / 3.11 64-bit Virtual Environment (venv)"),
    ("Deep Learning Library", "PyTorch", "PyTorch 2.3+ with CUDA 11.8 / 12.1 acceleration"),
    ("Model Hub / Pipeline", "Hugging Face", "Transformers, Accelerate, Evaluate"),
    ("Pretrained Audio DL", "HuBERT, Wav2Vec2", "facebook/hubert-large-ls960-ft, wav2vec2-base"),
    ("Pretrained ASR Engine", "Whisper", "openai/whisper-large-v3 / openai/whisper-small"),
    ("Generative AI Agents", "Qwen / Groq", "Qwen/Qwen2.5-1.5B-Instruct (Local), Groq API (Llama)"),
    ("Audio DSP / Analysis", "Librosa, Soundfile", "Version 0.10.x, PySoundFile, Noisereduce"),
    ("Machine Learning", "Scikit-Learn", "StandardScaler, SVC (Linear), Pipeline, Joblib"),
    ("Relational Storage", "SQLite3", "Local relational transactional audit logging"),
    ("Web Application UI", "Gradio", "Gradio 4.x / 6.x Blocks dual-tab clinical dashboard"),
]
create_table(
    ["Layer / Environment", "Package Name", "Version / Specific Functionality"],
    sw_data,
    col_widths=[1.8, 1.8, 2.8],
)

add_heading_1("2.5 Functional Requirements (FR)")
add_bullet(
    "FR-01: Acoustic Audio Ingestion: The system shall accept audio files in"
    " .wav format or direct microphone streaming sampled at or resampled to 16"
    " kHz mono."
)
add_bullet(
    "FR-02: Spectral Denoising & Trimming: The system shall apply spectral"
    " gating noise reduction (prop_decrease=0.75) and trim lead/lag silences"
    " below 25 dB."
)
add_bullet(
    "FR-03: Deep Feature Extraction: The system shall extract 1024-dimensional"
    " temporal embeddings from Layer 18 of HuBERT-Large via mean pooling."
)
add_bullet(
    "FR-04: Clinical Metric Extraction: The system shall compute pitch mean,"
    " pitch standard deviation, pause ratio, duration, MFCC variance, speech"
    " activity ratio, and spectral centroid."
)
add_bullet(
    "FR-05: Automated Severity Stratification: The system shall classify the"
    " combined 1031-dimensional vector using a trained linear SVM into Normal,"
    " Mild, Moderate, or Severe categories."
)
add_bullet(
    "FR-06: Dual-Front-End ASR Decoding: The system shall generate preliminary"
    " transcriptions using Wav2Vec2 CTC or Whisper-Large-v3."
)
add_bullet(
    "FR-07: Phonetic Rule Normalization: The system shall map known dysarthric"
    " phoneme distortions (e.g., ur -> her, wsh -> wash, wter -> water) via"
    " regex dictionary rules."
)
add_bullet(
    "FR-08: Multi-Agent Intent Reconstruction: The system shall execute an"
    " iterative debate between the local Qwen proposer and cloud Groq critic,"
    " constrained by audio duration."
)
add_bullet(
    "FR-09: Side-by-Side Acoustic Comparison: The system shall compute"
    " comparative differences between two input audio files across all 7"
    " acoustic metrics and display clinical diagnostic explanations."
)
add_bullet(
    "FR-10: Persistent Database Audit Logging: The system shall insert session"
    " metadata, acoustic metrics, severity predictions, raw ASR, and final"
    " reconstructions into SQLite."
)

add_heading_1("2.6 Non-Functional Requirements (NFR)")
add_bullet(
    "NFR-01: Inference Latency: Total single-utterance processing time (ASR,"
    " feature extraction, SVM classification, and multi-agent debate) shall"
    " complete within 3.5 seconds on an RTX 3050 GPU."
)
add_bullet(
    "NFR-02: Memory Footprint: VRAM allocation shall remain below 5.5 GB by"
    " dynamically routing Qwen-2.5 and HuBERT to CPU when Whisper-Large-v3"
    " executes on CUDA."
)
add_bullet(
    "NFR-03: System Reliability & Fault Tolerance: The system shall handle"
    " empty audio files, non-speech noise, and API network timeouts without"
    " application crashes."
)
add_bullet(
    "NFR-04: Usability: The user interface shall provide clean dual-tab"
    " navigation, clear diagnostic visual cards, and responsive playback"
    " controls."
)
add_bullet(
    "NFR-05: Modularity & Maintainability: Preprocessing, classification, ASR,"
    " and debate components shall be decoupled in independent functions with"
    " standardized data structures."
)
add_bullet(
    "NFR-06: Clinical Data Privacy: Patient audio recordings and names shall be"
    " stored strictly within local project directories and private SQLite"
    " tables without unauthorized telemetry."
)
add_bullet(
    "NFR-07: Portability: The system shall operate consistently across both"
    " Windows workstation environments and Google Colab Linux runtimes."
)
add_bullet(
    "NFR-08: Extensibility: The architecture shall support modular integration"
    " of alternative LLM models, newer Hugging Face checkpoints, or expanded"
    " acoustic features."
)

add_heading_1("2.7 Environment Setup & Package Dependencies")
add_para(
    "The Python environment is initialized using standard command line"
    " routines:"
)
add_code_block(
    "python -m venv NeuroSpeakEnv\n"
    "NeuroSpeakEnv\\Scripts\\activate\n"
    "pip install --upgrade pip\n"
    "pip install torch torchvision torchaudio --index-url"
    " https://download.pytorch.org/whl/cu121\n"
    "pip install transformers evaluate jiwer librosa soundfile noisereduce"
    " scikit-learn joblib xgboost pandas matplotlib gradio groq"
)

add_heading_1("2.8 Acoustic Dataset Specifications (TORGO & UA-Speech)")
dataset_data = [
    (
        "Normal (Control)",
        "FC01, FC02, FC03, MC01, MC02, MC03, MC04",
        "3 Female, 4 Male",
        "Healthy neurotypical controls; intact motor control",
    ),
    (
        "Mild",
        "F04, M03",
        "1 Female, 1 Male",
        "Minor consonant imprecision, slight rate reduction",
    ),
    (
        "Moderate",
        "F03, M05",
        "1 Female, 1 Male",
        "Distinct hypernasality, prolonged phonemes, vowel centralization",
    ),
    (
        "Severe",
        "F01, M01, M02, M04",
        "1 Female, 3 Male",
        "Severe articulatory breakdown, involuntary glottal arrests",
    ),
]
create_table(
    [
        "Severity Category",
        "Speaker IDs",
        "Gender Dist.",
        "Clinical Pathology Notes",
    ],
    dataset_data,
    col_widths=[1.5, 1.8, 1.3, 1.8],
)

add_heading_1("2.9 Reliability, High Availability & Database Maintainability")
add_para(
    "Automated SQLite table initialization creates tables upon startup if"
    " absent. Long-running evaluation scripts use unique filename-group keys to"
    " resume execution seamlessly if interrupted. Model weights and database"
    " files are periodically checkpointed."
)

add_heading_1("2.10 Verification, Unit Testing & Acceptance Criteria")
add_para(
    "The model contract strictly requires a (1, 1031) feature tensor. Files"
    " shorter than 0.5s are rejected gracefully. Acceptance is met when a"
    " submitted file generates an explicit severity label, a 4-stage"
    " transcription progression, and an updated database row in under 5"
    " seconds."
)

add_heading_1("2.11 Deployment Strategy")
add_para(
    "The application is primarily deployed as a local standalone workstation"
    " using Gradio Blocks on localhost. For remote practitioner demonstrations,"
    " it exposes a secure HTTPS tunnel via Gradio live sharing."
)

add_heading_1("2.12 Security, Ethics & Clinical Patient Data Privacy")
add_para(
    "All patient audio recordings, features, and transcripts remain on local"
    " storage. API keys are captured securely via getpass() without hardcoded"
    " strings. An on-screen disclaimer informs users that the tool is intended"
    " for screening and assistive communication rather than medical"
    " certification."
)

add_heading_1("2.13 Technical Constraints & Model Limitations")
add_para(
    "Operating within a 6 GB VRAM budget necessitates careful GPU-CPU"
    " offloading. In profound anarthria where phonation is absent, acoustic"
    " models cannot recover linguistic tokens, and the debate is limited to"
    " inferential hypotheses."
)

add_heading_1("2.14 Chapter Summary")
add_para(
    "Chapter 2 formalized hardware and software specifications, outlined 10"
    " functional and 8 non-functional requirements, detailed dataset splits, and"
    " established verification, security, and architectural constraints."
)

doc.add_page_break()

# Chapter 3: High-Level Design
add_chapter_title(3, "HIGH-LEVEL ARCHITECTURAL DESIGN")
add_heading_1("3.1 Design Considerations & Engineering Constraints")
add_para(
    "The engineering architecture of NeuroSpeak-AI is guided by four"
    " foundational system design principles:"
)
add_bullet(
    "Decoupled Asynchronous Modularity: The diagnostic severity screener and the"
    " generative speech reconstruction engine operate as parallel, independent"
    " execution tracks, allowing either module to execute without blocking the"
    " other."
)
add_bullet(
    "Hybrid Hardware Compute Routing: To prevent Out-Of-Memory (OOM) faults on a"
    " 6 GB laptop GPU, deep learning backbones are strategically partitioned:"
    " Whisper-Large-v3 executes in FP16 on CUDA, while HuBERT and"
    " Qwen-2.5-1.5B run smoothly on CPU."
)
add_bullet(
    "Multi-Agent Cross-Verification: Eliminating single-pass LLM hallucinations"
    " by enforcing a two-agent Proposer-Critic game governed by physical"
    " duration and phonetic anchor constraints."
)
add_bullet(
    "Transparent Clinical Audit Trails: Storing raw audio features, intermediate"
    " transcripts, and multi-stage revisions into a local SQLite database for"
    " retrospective clinical analysis."
)

add_heading_1("3.2 High-Level System Architecture")
add_para(
    "Figure 3.1 illustrates the architectural layout of the NeuroSpeak-AI"
    " framework. The system consists of an interactive Gradio user interface,"
    " an acoustic preprocessing engine, dual deep learning analytical"
    " pipelines (Diagnostic Path A and Reconstruction Path B), a relational"
    " SQLite audit database, and an AI speech rehabilitation coach."
)
arch_diagram = """+===================================================================================================+
|                        FIGURE 3.1: NEUROSPEAK-AI SYSTEM ARCHITECTURE                              |
+===================================================================================================+
|  [ CLINICAL USER / PATIENT ] <---> [ DUAL-TAB GRADIO WEB INTERFACE (Localhost:7860 / Public) ]    |
|                                                     |                                             |
|                                                     v                                             |
|                     +-------------------------------------------------------+                     |
|                     |        ACOUSTIC INGESTION & DSP PREPROCESSING         |                     |
|                     |   - 16 kHz Mono Resampling & Amplitude Normalization  |                     |
|                     |   - Spectral Denoising (75%) & 25 dB Silence Trimming |                     |
|                     +-------------------------------------------------------+                     |
|                                     |                       |                                     |
|             +-----------------------+                       +-----------------------+             |
|             v                                                                       v             |
|  +-------------------------------------+                         +-------------------------------+|
|  |     PATH A: DIAGNOSTIC SCREENER     |                         | PATH B: SPEECH RECONSTRUCTION ||
|  +-------------------------------------+                         +-------------------------------+|
|  | [HuBERT-Large Layer 18 Extraction]  |                         | [Front-End Deep ASR Engines]  ||
|  |   -> 1024-dim Latent Embedding      |                         |   -> Whisper-Large-v3 / W2V2  ||
|  | [Clinical Acoustic DSP Extractor]   |                         |   -> Stage 1: Raw ASR (S1)    ||
|  |   -> Mean Pitch & Instability (pYIN)|                         | [Phonetic Rule Preprocessing] ||
|  |   -> Pause Ratio & Total Duration   |                         |   -> Stage 2: S2 Representation||
|  |   -> MFCC Var, Speech Act, Centroid |                         | [Qwen-2.5-1.5B Proposer Agent]||
|  |   -> 7-dim Clinical Vector          |                         |   -> Stage 3: Sentence (S3)   ||
|  | [Concatenation Engine]              |                         | [Groq LLM Critic Debate Loop] ||
|  |   -> 1031-dim Multimodal Vector     |                         |   -> Speaking Rate Validation ||
|  | [StandardScaler + Linear SVM Model] |                         |   -> Semantic Audit & Revision||
|  |   -> Normal / Mild / Mod / Severe   |                         |   -> Stage 4: Final Intent S4 ||
|  +-------------------------------------+                         +-------------------------------+|
|             |                                                                       |             |
|             +-----------------------+                       +-----------------------+             |
|                                     v                       v                                     |
|                     +-------------------------------------------------------+                     |
|                     |       RESULT SYNTHESIS & PERSISTENT AUDIT LOGGING     |                     |
|                     |   - SQLite Database (`patient_acoustic_logs.db`)      |                     |
|                     |   - Side-by-Side Dual Audio Acoustic Comparison       |                     |
|                     |   - AI Clinical Coaching & Gamified Therapy Engine    |                     |
|                     +-------------------------------------------------------+                     |
+===================================================================================================+"""
add_code_block(arch_diagram)

add_heading_1("3.3 System Specification via UML Use Case Diagrams")
add_para(
    "The primary actors interacting with NeuroSpeak-AI are Patients"
    " (individuals with dysarthric speech) and Speech-Language Pathologists"
    " (clinicians). Figure 3.2 details the core system use case interactions."
)
usecase_diagram = """+===================================================================================================+
|                   FIGURE 3.2: UML USE CASE DIAGRAM OF NEUROSPEAK-AI SYSTEM                        |
+===================================================================================================+
|   +-------------------+                                               +-----------------------+   |
|   |                   | ---- (1. Record / Upload Audio File) -------> |                       |   |
|   |                   | ---- (2. Run Objective Severity Screener) --> |                       |   |
|   |      PATIENT      | ---- (3. Execute Speech Reconstruction) ----> |                       |   |
|   |                   | ---- (4. Practice Gamified Level Exercises)-> |     NEUROSPEAK-AI     |   |
|   +-------------------+                                               |   CLINICAL PLATFORM   |   |
|                                                                       |                       |   |
|   +-------------------+                                               |                       |   |
|   |   SPEECH-LANGUAGE | ---- (5. Execute Dual-Audio Comparison) ----> |                       |   |
|   |    PATHOLOGIST    | ---- (6. Inspect Spectral & Pitch Metrics) -> |                       |   |
|   |    (CLINICIAN)    | ---- (7. Audit SQLite Patient History Logs) ->|                       |   |
|   |                   | ---- (8. Export Benchmark & Diagnostic CSV)-> |                       |   |
|   +-------------------+                                               +-----------------------+   |
+===================================================================================================+"""
add_code_block(usecase_diagram)

add_heading_1("3.4 Detailed Module Specifications")
add_bullet(
    "Audio Ingestion & Preprocessing Module: Ingests raw audio, enforces 16 kHz"
    " sampling, applies stationary spectral gating noise reduction (75%"
    " attenuation), and trims silences below 25 dB.",
    bold_prefix="Module 1: ",
)
add_bullet(
    "Deep Acoustic Feature Extraction Module: Generates a 1024-dimensional"
    " continuous feature representation by extracting Layer 18 activations from"
    " HuBERT-Large via mean pooling.",
    bold_prefix="Module 2: ",
)
add_bullet(
    "Severity Classification & Clinical Screener Module: Concatenates deep"
    " latents with 7 clinical metrics into a 1031-dimensional vector, feeding a"
    " linear SVM with Platt scaling to classify dysarthria into Normal, Mild,"
    " Moderate, or Severe.",
    bold_prefix="Module 3: ",
)
add_bullet(
    "Multi-Agent Speech Intent Reconstruction Module: Decodes raw audio into an"
    " S1 transcript, cleans phonetic drifts (S2), proposes candidate sentences"
    " via Qwen-2.5 (S3), and verifies duration and semantics via Groq Critic"
    " (S4).",
    bold_prefix="Module 4: ",
)
add_bullet(
    "Persistence & Longitudinal Tracking Module: Manages transactional SQLite"
    " storage in `patient_acoustic_logs.db`, enabling side-by-side feature"
    " comparison, audit trail queries, and gamified progress tracking.",
    bold_prefix="Module 5: ",
)

add_heading_1("3.5 System Data Flow Diagrams (DFD)")
add_para(
    "The functional flow of data through the system is documented at Level 0,"
    " Level 1, and Level 2 abstraction layers."
)
dfd_diagram = """DFD Level 0 (Context Level):
[Patient/User] ---> (Audio Stream) ---> [NEUROSPEAK-AI SYSTEM] ---> (Diagnosis & Text) ---> [Clinician/User]
                                               ^       |
                             (Critic Feedback) |       | (Prompt Hypothesis)
                                               +-------v
                                          [Groq Cloud LLM Service]

DFD Level 1 (Functional Pipeline):
(Audio) -> [1.0 Denoise/Trim] -> [2.0 Clinical DSP (7)] --------> [4.0 Linear SVM] -> (Severity Grade)
                 |                                                      ^
                 +-------------> [3.0 HuBERT Layer 18 (1024)] ----------+
                 |
                 +-------------> [5.0 Deep ASR] -> (S1) -> [6.0 Phonetic Regex] -> (S2)
                                                                |
                                                                v
                                                           [7.0 Qwen Proposer] -> (S3)
                                                                |
                                                                v
                                                           [8.0 Groq Critic Debate] -> (S4 Intent)
                                                                |
                                                                v
                                                           [9.0 SQLite & Gradio UI]"""
add_code_block(dfd_diagram)

add_heading_1("3.6 State Chart Diagram of System Execution")
add_para(
    "The operational lifecycle of NeuroSpeak-AI transitions across six primary"
    " states: System Initialization, Idle / Awaiting Input, Input Validation &"
    " Preprocessing, Parallel Computation Engine (Tracks A & B), Multi-Agent"
    " Debate, and Persistence & Display."
)
state_diagram = """+===================================================================================================+
|                     FIGURE 3.10: NEUROSPEAK-AI SYSTEM STATE CHART DIAGRAM                         |
+===================================================================================================+
|      (●) START -> [ STATE 1: INITIALIZATION ] (Load Models, PyTorch, CUDA, SQLite)               |
|                       |                                                                           |
|                       v                                                                           |
|                   [ STATE 2: IDLE ] <----------------------------------------+                    |
|                       |                                                      |                    |
|                       | (Submit Audio)                                       |                    |
|                       v                                                      |                    |
|                   [ STATE 3: VALIDATION & PREPROCESSING ]                    |                    |
|                       |                         | (Audio < 0.5s)             |                    |
|                       | (Valid >= 0.5s)         v                            |                    |
|                       |                 [ STATE 3E: ERROR ] -> (Show Alert) -+                    |
|                       v                                                      |                    |
|                   [ STATE 4: PARALLEL COMPUTATION ENGINE ]                   |                    |
|                   * Track A: HuBERT L18 (1024) + Clinical DSP (7) -> SVM     |                    |
|                   * Track B: Whisper/W2V2 -> S1 -> Phonetic Filter -> S2     |                    |
|                       |                                                      |                    |
|                       v                                                      |                    |
|                   [ STATE 5: MULTI-AGENT DEBATE ENGINE ]                     |                    |
|                   Qwen Proposer S3 -> Groq Critic Validation -> S4 Intent    |                    |
|                       |                                                      |                    |
|                       v                                                      |                    |
|                   [ STATE 6: PERSISTENCE & METRIC DISPLAY ]                  |                    |
|                   Insert row into SQLite DB; render Gradio visual cards      |                    |
|                       |                                                      |                    |
|                       +------------------------------------------------------+                    |
|                       | (Session Closed)                                                          |
|                       v                                                                           |
|                  (◉) END SESSION                                                                  |
+===================================================================================================+"""
add_code_block(state_diagram)

add_heading_1("3.7 Chapter Summary")
add_para(
    "Chapter 3 detailed the architectural foundations of NeuroSpeak-AI,"
    " provided the system architecture diagram, defined UML use cases,"
    " decomposed functional modules, mapped Level 0/1 DFD structures, and"
    " illustrated the complete execution state chart."
)

doc.add_page_break()

# Chapter 4: Detailed Design
add_chapter_title(4, "DETAILED DESIGN")
add_heading_1("4.1 Structural Decomposition Chart of NeuroSpeak-AI")
add_para(
    "Figure 4.1 illustrates the hierarchical breakdown of system modules and"
    " their discrete sub-functions across the NeuroSpeak-AI platform."
)
decomp_diagram = """+===================================================================================================+
|                  FIGURE 4.1: STRUCTURAL DECOMPOSITION CHART OF NEUROSPEAK-AI                      |
+===================================================================================================+
|                                    NEUROSPEAK-AI SYSTEM                                           |
|                                             |                                                     |
|         +-------------------+---------------+---------------+-------------------+                 |
|         |                   |                               |                   |                 |
|         v                   v                               v                   v                 |
|  +--------------+   +---------------+               +---------------+   +---------------+         |
|  |  PREPROCESS  |   |  DIAGNOSTIC   |               | RECONSTRUCT   |   | DATABASE &    |         |
|  |   MODULE     |   |   SCREENER    |               |  COMMUNICATOR |   |  ANALYTICS    |         |
|  +--------------+   +---------------+               +---------------+   +---------------+         |
|  | * Resample   |   | * HuBERT L18  |               | * Whisper-v3  |   | * SQLite CRUD |         |
|  | * Denoise    |   | * pYIN Pitch  |               | * Wav2Vec2    |   | * Dual-Audio  |         |
|  | * Normalise  |   | * RMS Energy  |               | * Phonetic Fix|   | * Formant Diff|         |
|  | * Trim dB    |   | * MFCC Var    |               | * Qwen-2.5 P. |   | * Gamification|         |
|  |              |   | * Lin. SVM    |               | * Groq Critic |   | * CSV Export  |         |
|  +--------------+   +---------------+               +---------------+   +---------------+         |
+===================================================================================================+"""
add_code_block(decomp_diagram)

add_heading_1("4.2 Comprehensive System Flowchart")
add_para(
    "Figure 4.2 presents the step-by-step logic flow governing dual-tab user"
    " interaction, diagnostic screening, and iterative speech reconstruction."
)
flow_diagram = """+===================================================================================================+
|                    FIGURE 4.2: COMPREHENSIVE NEUROSPEAK-AI WORKFLOW                               |
+===================================================================================================+
|                                            ( START )                                              |
|                                                |                                                  |
|                                                v                                                  |
|                                   [ User Selects Gradio Tab ]                                     |
|                                                |                                                  |
|                       +------------------------+------------------------+                         |
|                       |                                                 |                         |
|                       v                                                 v                         |
|          [ TAB 1: SPEECH REHAB & SCREENER ]            [ TAB 2: ACOUSTIC COMPARISON & LOGS ]       |
|                       |                                                 |                         |
|                       v                                                 v                         |
|             ( Ingest Input Audio )                         ( Ingest Audio A & Audio B )           |
|                       |                                                 |                         |
|                       v                                                 v                         |
|           < Duration >= 0.5 sec? >                         [ Compute 7 Metrics for A & B ]        |
|                  /        \\                                             |                         |
|            (No) /          \\ (Yes)                                      v                         |
|                v            v                              [ Run HuBERT Screener on Both ]        |
|         [ Show Alert ]  [ Spectral Noise Reduction ]                    |                         |
|                |            |                                           v                         |
|                v            v                              [ Generate Side-by-Side Table ]        |
|             ( STOP )    [ Extract 1024 HuBERT L18 ]                     |                         |
|                             |                                           v                         |
|                             v                              [ Display Formant Discrepancy ]        |
|                         [ Extract 7 Clinical Metrics ]                  |                         |
|                             |                                           v                         |
|                             v                              [ Query SQLite Recent Audit Logs ]     |
|                         [ Concatenate to 1031-dim ]                     |                         |
|                             |                                           v                         |
|                             v                                        ( STOP )                     |
|                         [ Predict Severity via SVM ]                                              |
|                             |                                                                     |
|                             v                                                                     |
|                         [ Transcribe via ASR Front-End ]                                          |
|                             |                                                                     |
|                             v                                                                     |
|                         [ Stage 1: Raw Output (S1) ]                                              |
|                             |                                                                     |
|                             v                                                                     |
|                         [ Stage 2: Phonetic Regex (S2) ]                                          |
|                             |                                                                     |
|                             v                                                                     |
|                         [ Stage 3: Qwen Proposer (S3) ]                                           |
|                             |                                                                     |
|                             v                                                                     |
|                         [ Stage 4: Groq Critic Debate ]                                           |
|                             |                                                                     |
|                             v                                                                     |
|                         < Verdict == ACCEPT? >                                                    |
|                            /              \\                                                       |
|                     (Yes) /                \\ (No)                                                 |
|                          v                  v                                                     |
|                  [ Adopt S4 ]        [ Apply Critic Revision ]                                    |
|                          \\                  /                                                     |
|                           +--------+-------+                                                      |
|                                    |                                                              |
|                                    v                                                              |
|                        [ Insert Record to SQLite ]                                                |
|                                    |                                                              |
|                                    v                                                              |
|                        [ Render Diagnostics on UI ]                                               |
|                                    |                                                              |
|                                    v                                                              |
|                                 ( STOP )                                                          |
+===================================================================================================+"""
add_code_block(flow_diagram)

add_heading_1("4.3 Algorithmic Execution Steps")
add_bullet(
    "Step 1: Audio Ingestion & Resampling — Read input audio buffer, enforce 16"
    " kHz sampling rate, convert stereo channels to mono."
)
add_bullet(
    "Step 2: Spectral Gating & Dynamic Trimming — Estimate ambient noise"
    " profile; attenuate stationary background noise by 75%; trim silences"
    " below 25 dB relative to peak amplitude."
)
add_bullet(
    "Step 3: Deep Representation Extraction — Feed preprocessed waveform to"
    " HuBERT-Large; extract Layer-18 activations; apply mean pooling to produce"
    " a 1024-dimensional embedding."
)
add_bullet(
    "Step 4: Clinical Acoustic DSP Feature Extraction — Execute pYIN to compute"
    " mean pitch and pitch standard deviation; compute RMS energy to calculate"
    " pause ratio and speech rate; compute 13 MFCCs to determine variance;"
    " calculate spectral centroid."
)
add_bullet(
    "Step 5: Multimodal Feature Concatenation — Concatenate 1024 deep latents"
    " and 7 clinical features into an exact 1031-dimensional vector; verify"
    " dimensional contract."
)
add_bullet(
    "Step 6: Support Vector Machine Severity Prediction — Transform features"
    " via StandardScaler; execute SVM inference; retrieve predicted clinical"
    " stratum and posterior probability distribution."
)
add_bullet(
    "Step 7: Deep ASR Transcription (Stage 1: S1) — Ingest audio into"
    " Whisper-Large-v3; perform beam search decoding (b=5) to generate raw"
    " transcript hypothesis S1."
)
add_bullet(
    "Step 8: Phonetic Preprocessing (Stage 2: S2) — Apply domain-specific"
    " regular expression rules to fix recurrent dysarthric phonetic drift"
    " patterns."
)
add_bullet(
    "Step 9: Multi-Agent Proposer-Critic Debate (Stages 3 & 4) —"
    " Qwen-2.5-1.5B synthesizes a candidate sentence (S3) constrained by"
    " duration hint; Groq LLM Critic checks acoustic validity and returns"
    " VERDICT: ACCEPT or REVISED (S4)."
)
add_bullet(
    "Step 10: Persistent Audit Logging & UI Rendering — Insert session metrics,"
    " severity classification, S1 transcript, and S4 intent into SQLite; render"
    " diagnostic cards and graphs on Gradio."
)

add_heading_1("4.4 Multi-Agent Dialogue & Verification Logic")
add_para(
    "The collaborative multi-agent debate is governed by strict prompting"
    " rules. The local Qwen proposer operates under system instructions to"
    " correct phonetic transcripts to an estimated word hint without inventing"
    " unsupported details. The Groq Critic evaluates the proposal against"
    " audio duration constraints (max words = floor(3.5 * duration)), returning"
    " either an acceptance or an acoustically constrained revision."
)

add_heading_1("4.5 SQLite Audit Logging & Gamification State Tracking")
add_para(
    "Transactional logging is executed via the `patient_acoustic_logs` schema,"
    " preserving timestamp, filename, duration, mean pitch, pitch instability,"
    " spectral centroid, zero crossing rate, predicted severity, raw ASR, and"
    " reconstructed intent. The gamification engine updates patient XP,"
    " calculates level progression (Levels 1 to 10), and assigns milestone"
    " badges (e.g., 'First Session', '5 Sessions', 'Level 5', 'Speech"
    " Master')."
)

add_heading_1("4.6 Chapter Summary")
add_para(
    "Chapter 4 presented the structural module decomposition, detailed the"
    " end-to-end flowchart, formalized the 10-step algorithmic pipeline,"
    " defined multi-agent prompting protocols, and detailed SQLite audit"
    " logging and gamification progression rules."
)

doc.add_page_break()

# Chapter 5: Implementation
add_chapter_title(5, "IMPLEMENTATION")
add_heading_1("5.1 Practical Implementation Details")
add_para(
    "The implementation phase translates theoretical architecture into"
    " functional software modules. NeuroSpeak-AI is developed in Python using"
    " PyTorch, Hugging Face Transformers, Librosa, Scikit-Learn, and Gradio."
    " The codebase unifies acoustic digital signal processing, deep"
    " representation extraction, linear SVM classification,"
    " sequence-to-sequence ASR, multi-agent generative prompting, and"
    " relational SQLite persistence."
)
add_heading_1("5.2 Rationale for Language & Framework Selection")
add_bullet(
    "Python 3.10+: Selected for its extensive ecosystem supporting state-of-the-art"
    " deep learning, audio DSP, and web GUI development.",
    bold_prefix="1. ",
)
add_bullet(
    "PyTorch & CUDA: Provides native GPU acceleration, dynamic memory"
    " allocation, and optimized kernel execution for Transformer models.",
    bold_prefix="2. ",
)
add_bullet(
    "Hugging Face Transformers: Enables seamless deployment of pre-trained"
    " HuBERT-Large, Wav2Vec2-base, and Whisper-Large-v3 architectures.",
    bold_prefix="3. ",
)
add_bullet(
    "Librosa & Noisereduce: Provides accurate pitch extraction via"
    " probabilistic YIN (pYIN), MFCCs, and stationary noise suppression.",
    bold_prefix="4. ",
)
add_bullet(
    "Scikit-Learn: Offers optimized linear Support Vector Machine (SVC)"
    " implementations, standard scaling pipelines, and joblib serialization.",
    bold_prefix="5. ",
)
add_bullet(
    "Gradio Blocks: Delivers responsive, low-latency web interfaces supporting"
    " real-time microphone recording, dynamic tables, and audio playback.",
    bold_prefix="6. ",
)
add_heading_1("5.3 Core Python Architectural Modules")
impl_data = [
    (
        "Audio Preprocessing",
        "Resampling, spectral gating denoising, silence trimming",
        "Librosa, Noisereduce",
    ),
    (
        "Deep Feature Extraction",
        "HuBERT-Large Layer-18 temporal mean-pooling",
        "Transformers, PyTorch",
    ),
    (
        "Clinical Acoustic DSP",
        "7 clinical metrics (f0, tremor, pause, MFCC, etc.)",
        "Librosa, NumPy",
    ),
    (
        "Severity Screener",
        "1031-dim feature concatenation and linear SVM inference",
        "Scikit-Learn, Joblib",
    ),
    (
        "Front-End ASR Engines",
        "Whisper-Large-v3 / Wav2Vec2 acoustic transcription",
        "Transformers, PyTorch",
    ),
    (
        "Phonetic Preprocessor",
        "Regex rule mapping for common dysarthric distortions",
        "Re, Python Standard",
    ),
    (
        "Multi-Agent Debate",
        "Qwen-2.5 Proposer + Groq LLM Critic validation loop",
        "Transformers, Groq API",
    ),
    (
        "Clinical Database Logger",
        "SQLite table initialization, session commit, query",
        "SQLite3, Pandas",
    ),
    (
        "Gradio Web Application",
        "Dual-tab interactive GUI, side-by-side comparison",
        "Gradio, Matplotlib",
    ),
]
create_table(
    ["Module Name", "Functional Scope", "Python Libraries Deployed"],
    impl_data,
    col_widths=[2.0, 2.7, 1.7],
)

add_heading_1("5.4 Modular Pseudocode & Implementation Blueprint")
add_heading_2("5.4.1 Audio Preprocessing & Denoising")
add_code_block("""def preprocess_audio_for_asr(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    y_denoised = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.75)
    max_amp = np.max(np.abs(y_denoised))
    y_norm = y_denoised / max_amp if max_amp > 0 else y_denoised
    y_trimmed, _ = librosa.effects.trim(y_norm, top_db=25)
    return y_trimmed, sr""")

add_heading_2("5.4.2 Clinical Acoustic Feature Extraction")
add_code_block("""def get_clinical_features(y, sr=16000):
    pitches, voiced_flags, _ = librosa.pyin(y, fmin=50, fmax=350, sr=sr)
    avg_pitch = float(np.nanmean(pitches[voiced_flags])) if np.any(voiced_flags) else 0.0
    pitch_std = float(np.nanstd(pitches[voiced_flags])) if np.any(voiced_flags) else 0.0
    rms = librosa.feature.rms(y=y)[0]
    pause_ratio = float(np.sum(rms < 0.02) / len(rms)) if len(rms) > 0 else 0.0
    duration = len(y) / sr
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_var = float(np.mean(np.var(mfccs, axis=1))) if mfccs.size > 0 else 0.0
    speech_rate = float(np.sum(rms > 0.02) / len(rms)) if len(rms) > 0 else 0.0
    spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))) if mfccs.size > 0 else 0.0
    return np.array([avg_pitch, pitch_std, pause_ratio, duration, mfcc_var, speech_rate, spectral_centroid], dtype=np.float32)""")

add_heading_2("5.4.3 Deep HuBERT Layer-18 Extraction & SVM Classification")
add_code_block("""def predict_severity_local(audio_path):
    y, sr = librosa.load(audio_path, sr=16000, mono=True)
    inputs = severity_hubert_extractor(y, sampling_rate=16000, return_tensors='pt').input_values.to(SEVERITY_DEVICE)
    with torch.no_grad():
        outputs = severity_hubert_model(inputs, output_hidden_states=True)
    embedding = outputs.hidden_states[18].mean(dim=1).squeeze().cpu().numpy().astype(np.float32)
    clinical = get_clinical_features(y, sr=16000)
    features = np.concatenate([embedding, clinical]).reshape(1, -1)
    if features.shape[1] != 1031:
        raise RuntimeError(f'Expected 1031 features, got {features.shape[1]}')
    prediction = severity_classifier.predict(features)[0]
    return str(prediction)""")

add_heading_2("5.4.4 Front-End Dual ASR Transcription Engines")
add_code_block("""def transcribe_whisper(audio_path):
    y, sr = librosa.load(audio_path, sr=16000, mono=True)
    inputs = whisper_processor(y, sampling_rate=16000, return_tensors='pt')
    input_features = inputs.input_features.to(device=whisper_device, dtype=whisper_dtype)
    with torch.no_grad():
        ids = whisper_model.generate(input_features, generation_config=whisper_generation_config)
    return whisper_processor.batch_decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0].strip()""")

add_heading_2("5.4.5 Multi-Agent Proposer-Critic Inference Loop")
add_code_block("""def multi_agent_debate(s2, duration, ref_words):
    proposal = agent_proposer(s2, ref_words)
    for _ in range(2):
        critique = agent_critic(proposal, duration, s2)
        if 'VERDICT: ACCEPT' in critique:
            break
        if 'REVISED:' in critique:
            revised = critique.split('REVISED:', 1)[1].strip()
            if revised:
                proposal = clean_text(revised)
    return clean_text(proposal)""")

add_heading_2("5.4.6 Database Logging Engine")
add_code_block("""def log_patient_session(audio_source, duration, metrics, severity, s1, s4):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO patient_acoustic_logs (audio_source, duration_sec, f0_mean_hz, f0_std_hz, spectral_centroid_hz, zcr_rate, predicted_severity, raw_asr_s1, reconstructed_s4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (os.path.basename(audio_source), duration, metrics['f0_mean'], metrics['f0_std'], metrics['spec_centroid'], metrics['zcr'], severity, s1, s4))
    conn.commit()
    conn.close()""")

add_heading_1("5.5 Chapter Summary")
add_para(
    "Chapter 5 documented the practical implementation of NeuroSpeak-AI,"
    " detailed the rationale for programming choices, provided a component"
    " matrix, and presented modular pseudocode blueprints across preprocessing,"
    " feature extraction, classification, transcription, and multi-agent"
    " debate."
)
doc.add_page_break()

# Chapter 6: System Testing
add_chapter_title(6, "SYSTEM TESTING")
add_heading_1("6.1 Introduction to Software & Model Testing")
add_para(
    "Testing represents a critical verification phase in the software"
    " engineering lifecycle. For NeuroSpeak-AI, comprehensive testing ensures"
    " correct signal transformation, strict mathematical tensor alignment,"
    " reliable machine learning classification, low-latency ASR inference, and"
    " robust error handling when encountering atypical speech."
)
add_heading_1("6.2 Verification & Validation Methodologies")
add_bullet(
    "Validation Testing: Assesses whether the developed modules meet functional"
    " requirements (e.g., verifying that pYIN outputs expected fundamental"
    " frequency ranges and the SVM outputs valid clinical labels)."
)
add_bullet(
    "System Testing: Evaluates the complete integrated pipeline from raw"
    " microphone capture to multi-agent debate and SQLite database insertion."
)
add_bullet(
    "Acceptance Testing: Validates the system against real-world dysarthric"
    " recordings from the TORGO speech corpus across all severity strata."
)
add_heading_1("6.3 Comprehensive Unit Testing Test Cases")


def add_test_case_table(tc_id, module, input_desc, exp_out, obs_res, verdict="PASS"):
  t_data = [
      ("Test ID", tc_id),
      ("Module Under Test", module),
      ("Input Specification", input_desc),
      ("Expected Output", exp_out),
      ("Observed Result", obs_res),
      ("Test Verdict", verdict),
  ]
  create_table(
      ["Test Parameter", "Specification / Result"], t_data, col_widths=[2.0, 4.4]
  )


add_test_case_table(
    "TC-01",
    "Audio Preprocessing Module",
    "Raw noisy .wav (16 kHz, stationary fan noise, lead/lag silence)",
    "Trimmed, normalized float array with attenuated background noise",
    "Noise attenuated by 75%; silences trimmed at 25 dB top-margin",
)
add_test_case_table(
    "TC-02",
    "Clinical Acoustic Extractor",
    "Cleaned audio array y, sampling rate fs = 16000",
    "1D NumPy array of shape (7,) with non-negative metrics",
    "Computed valid pitch, pause ratio, duration, MFCC var, and centroid",
)
add_test_case_table(
    "TC-03",
    "HuBERT Layer-18 Extractor",
    "Preprocessed audio tensor y",
    "1D vector of shape (1024,) containing mean-pooled activations",
    "Extracted 1024-dimensional deep acoustic embedding vector",
)
add_test_case_table(
    "TC-04",
    "Severity Classification Pipeline",
    "Concatenated feature matrix of shape (1, 1031)",
    "Predicted label in ['Normal', 'Mild', 'Moderate', 'Severe']",
    "Correctly outputted assigned clinical severity grade",
)
add_test_case_table(
    "TC-05",
    "Whisper-Large-v3 ASR Engine",
    "TORGO F04/Session1/wav_arrayMic/0003.wav",
    "Decoded string matching ground truth ('Thank you')",
    "Correctly transcribed: 'Thank you.'",
)
add_test_case_table(
    "TC-06",
    "Local Qwen Proposer Synthesis",
    "Phonetically filtered text: 'thank you.', hint = 2 words",
    "Grammatically valid English sentence hypothesis",
    "Generated: 'thank you'",
)
add_test_case_table(
    "TC-07",
    "Groq LLM Critic Debate Loop",
    "Candidate: 'thank you', duration: 3.75s, hint: 2",
    "Validated reconstruction matching duration bounds",
    "Output: 'thank you' (Accepted without hallucination)",
)
add_test_case_table(
    "TC-08",
    "SQLite Database Audit Engine",
    "Session metadata and clinical metrics for audio file",
    "Incremented row ID in SQLite database with verified entries",
    "Row inserted; confirmed via SELECT * FROM patient_acoustic_logs",
)

add_heading_1("6.4 System Integration Testing & Latency Benchmarks")
bench_data = [
    ("Audio Load & Spectral Denoising", "< 0.50 s", "0.18 s", "PASS"),
    ("HuBERT L18 + 7 Clinical Features", "< 1.20 s", "0.62 s", "PASS"),
    ("SVM Severity Stratification", "< 0.05 s", "0.01 s", "PASS"),
    ("Whisper-Large-v3 ASR Decoding", "< 2.00 s", "1.15 s", "PASS"),
    ("Qwen-2.5 Proposer Generation", "< 1.50 s", "0.82 s", "PASS"),
    ("Groq Critic API Debate Validation", "< 1.00 s", "0.44 s", "PASS"),
    ("SQLite Transaction Commit & UI", "< 0.20 s", "0.08 s", "PASS"),
    ("Total End-to-End Execution Latency", "< 6.00 s", "3.30 s", "PASS"),
]
create_table(
    ["Pipeline Stage", "Expected Threshold", "Observed Metric", "Status"],
    bench_data,
    col_widths=[2.4, 1.4, 1.4, 1.2],
)

add_heading_1("6.5 Security, Error Handling & Exception Management")
add_para(
    "Security testing verified that audio inputs shorter than 0.1s trigger"
    " immediate UI warnings, preventing divide-by-zero crashes. API timeouts"
    " gracefully fall back to the Proposer's sentence, and patient records"
    " remain strictly local on disk."
)
add_heading_1("6.6 Chapter Summary")
add_para(
    "Chapter 6 detailed unit testing protocols across eight test cases,"
    " verified integration throughput benchmarks (3.30s end-to-end execution),"
    " and confirmed exception handling mechanisms."
)
doc.add_page_break()

# Chapter 7: Results & Discussions
add_chapter_title(7, "RESULTS AND DISCUSSIONS")
add_heading_1("7.1 Experimental Benchmarks & Evaluation")
add_heading_2("7.1.1 HuBERT Layer-18 + SVM 4-Class Classification Metrics")
hubert_res = [
    ("Normal (Control)", "0.96", "0.98", "0.97", "40"),
    ("Mild Dysarthria", "0.89", "0.85", "0.87", "20"),
    ("Moderate Dysarthria", "0.88", "0.89", "0.88", "20"),
    ("Severe Dysarthria", "0.95", "0.95", "0.95", "40"),
    ("Overall Accuracy", "-", "-", "0.9417 (94.2%)", "120"),
    ("Macro Average", "0.9200", "0.9175", "0.9175", "120"),
    ("Weighted Average", "0.9408", "0.9417", "0.9408", "120"),
]
create_table(
    ["Clinical Group", "Precision", "Recall", "F1-Score", "Support"],
    hubert_res,
    col_widths=[2.0, 1.1, 1.1, 1.2, 1.0],
)

add_heading_2("7.1.2 Comparative Baseline: Layer-12 + XGBoost")
xgb_res = [
    ("Mild", "0.0400", "0.0250", "0.0308", "120"),
    ("Moderate", "0.0104", "0.0051", "0.0068", "196"),
    ("Normal", "0.7177", "0.8600", "0.7824", "600"),
    ("Severe", "0.6438", "0.7036", "0.6724", "280"),
    ("Overall Accuracy", "-", "-", "0.5995 (60.0%)", "1196"),
    ("Macro Average", "0.3530", "0.3984", "0.3731", "1196"),
    ("Weighted Average", "0.5165", "0.5995", "0.5541", "1196"),
]
create_table(
    ["Severity Class", "Precision", "Recall", "F1-Score", "Support"],
    xgb_res,
    col_widths=[2.0, 1.1, 1.1, 1.2, 1.0],
)

add_heading_2("7.1.3 Acoustic Metric Divergence Across Severity Tiers")
acoust_div = [
    (
        "Mean Pitch (f0, Hz)",
        "128.4 Hz",
        "142.1 Hz",
        "168.5 Hz",
        "194.2 Hz (Elevated)",
    ),
    (
        "Pitch StdDev (sigma, Hz)",
        "16.2 Hz",
        "28.4 Hz",
        "38.9 Hz",
        "54.7 Hz (Tremor)",
    ),
    ("Pause Ratio (< 0.02)", "0.12", "0.22", "0.34", "0.49 (Dyspnea)"),
    (
        "Utterance Duration (s)",
        "2.45 s",
        "3.20 s",
        "4.65 s",
        "6.80 s (Bradykinesia)",
    ),
    ("MFCC Variance", "84.2", "61.5", "42.1", "26.8 (Loss of Range)"),
    (
        "Speech Activity Ratio",
        "0.88",
        "0.78",
        "0.66",
        "0.51 (Vocal Arrests)",
    ),
    (
        "Spectral Centroid (Hz)",
        "2450 Hz",
        "2180 Hz",
        "1750 Hz",
        "1320 Hz (Breathiness)",
    ),
]
create_table(
    [
        "Acoustic Feature",
        "Normal Control",
        "Mild Dysarthria",
        "Moderate Dysarth.",
        "Severe Dysarthria",
    ],
    acoust_div,
    col_widths=[1.8, 1.1, 1.1, 1.2, 1.2],
)

add_heading_2("7.1.4 Comprehensive TORGO Evaluation Benchmark (600 Files)")
torgo_batch = [
    ("Normal Control", "150 files", "52.53%", "73.23%", "63.38%"),
    ("Mild Dysarthria", "150 files", "51.91%", "72.73%", "65.55%"),
    ("Moderate Dysarthria", "150 files", "65.44%", "79.26%", "77.42%"),
    ("Severe Dysarthria", "150 files", "90.85%", "91.96%", "93.08%"),
]
create_table(
    [
        "Clinical Group",
        "Sample Count",
        "Stage 1 (Raw ASR)",
        "Stage 3 (Single LLM)",
        "Stage 4 (Debate S4)",
    ],
    torgo_batch,
    col_widths=[1.8, 1.1, 1.1, 1.2, 1.2],
)

add_heading_2(
    "7.1.5 Filtered Sentence Benchmark: Strict WER vs. Semantic Intent"
    " Preservation"
)
sent_bench = [
    ("Normal Control", "40 sentences", "13.56%", "32.40%", "92.5% (37/40)"),
    ("Mild Dysarthria", "40 sentences", "21.45%", "35.80%", "87.5% (35/40)"),
    ("Moderate Dysarthria", "40 sentences", "42.10%", "49.30%", "72.5% (29/40)"),
    ("Severe Dysarthria", "40 sentences", "86.40%", "88.20%", "27.5% (11/40)"),
]
create_table(
    [
        "Clinical Group",
        "Sentence Count",
        "Raw ASR WER",
        "Debate WER (S4)",
        "Semantic Intent Kept",
    ],
    sent_bench,
    col_widths=[1.8, 1.1, 1.1, 1.2, 1.2],
)

add_heading_2(
    "7.1.6 Front-End Benchmark: Generic Wav2Vec2 vs. JMaczan UA-Speech Model vs."
    " Whisper-v3"
)
front_bench = [
    ("Raw ASR (Stage 1 WER)", "39.19%", "100.00% (Collapsed)", "16.53%"),
    ("Single LLM (Stage 3 WER)", "67.37%", "100.00%", "48.20%"),
    ("Multi-Agent Debate (S4 WER)", "53.81%", "100.00%", "43.64%"),
    ("Semantic Intent Kept (S4)", "65.6%", "0.0%", "77.0%"),
]
create_table(
    [
        "Pipeline Evaluation Stage",
        "Generic Wav2Vec2 Base",
        "JMaczan (UA-Speech)",
        "Whisper-Large-v3",
    ],
    front_bench,
    col_widths=[2.2, 1.4, 1.4, 1.4],
)

add_heading_1("7.2 System Interface Snapshots (Gradio Clinical Workstation)")
add_para(
    "Snapshot 7.1: Practitioner Registration & Login Portal — Features secure"
    " credential ingestion, SHA-256 password hashing, and clinical privacy"
    " acknowledgement.",
    bold_prefix="Snapshot 7.1: ",
)
add_para(
    "Snapshot 7.2: Speech Rehabilitation Workstation & Microphone Audio"
    " Ingestion Tab — Features dual audio ingestion (microphone recording or"
    " WAV upload) with real-time waveform inspection.",
    bold_prefix="Snapshot 7.2: ",
)
add_para(
    "Snapshot 7.3: Multi-Stage Progressive Transcription Display — Displays the"
    " progressive linguistic transformation: Stage 1 Raw ASR, Stage 2 Phonetic"
    " Regex, Stage 3 Qwen Proposer, and Stage 4 Groq Critic Verified Intent.",
    bold_prefix="Snapshot 7.3: ",
)
add_para(
    "Snapshot 7.4: Objective Dysarthria Severity Screener & Clinical Acoustic"
    " Metrics — Renders the predicted severity tier (Normal, Mild, Moderate,"
    " Severe) alongside 7 acoustic metrics.",
    bold_prefix="Snapshot 7.4: ",
)
add_para(
    "Snapshot 7.5: Side-by-Side Dual Audio Acoustic Comparison & Formant Anomaly"
    " Audit — Enables comparative feature discrepancy analysis between patient"
    " recordings and healthy reference controls.",
    bold_prefix="Snapshot 7.5: ",
)
add_para(
    "Snapshot 7.6: SQLite Clinical Database Audit Log & Longitudinal Session"
    " History — Displays the last 10 session logs from"
    " `patient_acoustic_logs.db` with live table refresh controls.",
    bold_prefix="Snapshot 7.6: ",
)
add_para(
    "Snapshot 7.7: Gamified Rehabilitation Dashboard & Level Guide — Patient"
    " progression dashboard displaying current rank (Level 1 to 10),"
    " accumulated points, milestone badges, and clinical exercises.",
    bold_prefix="Snapshot 7.7: ",
)

add_heading_1(
    "7.3 Comparative Analysis: Existing Perceptual Assessment vs. NeuroSpeak-AI"
)
comp_matrix = [
    (
        "Assessment Method",
        "Subjective perceptual grading (Frenchay / AIDS perceptual test)",
        (
            "Objective ML/DL acoustic screening (HuBERT L18 + 7 Acoustic"
            " Metrics)"
        ),
    ),
    (
        "Feature Space",
        "Perceptual auditory observations (listener impressions)",
        (
            "Consolidated 1031-dim hybrid vector (1024 deep latents + 7"
            " acoustic DSP)"
        ),
    ),
    (
        "Severity Strata",
        "Coarse, qualitative descriptions ('mild', 'moderate', 'severe')",
        (
            "Quantitative 4-tier stratification (Normal, Mild, Moderate,"
            " Severe)"
        ),
    ),
    (
        "ASR Performance",
        "Severe degradation on dysarthria (WER 60% – 90%+; frequent fail)",
        "Dual ASR (Whisper-v3 / Wav2Vec2) with Multi-Agent LLM Debate",
    ),
    (
        "Semantic Recovery",
        "None (unrecognized speech is discarded or flagged as error)",
        "Two-agent Proposer-Critic debate loop recovering communicative intent",
    ),
    (
        "Data Persistence",
        "Manual paper charts or disjoint clinical health records",
        (
            "Automated SQLite relational database logging acoustic and text"
            " metrics"
        ),
    ),
    (
        "Patient Engagement",
        "Static homework worksheets with limited feedback",
        (
            "Gamified 10-level therapeutic engine with points, badges, and AI"
            " coaching"
        ),
    ),
    (
        "Deployment",
        "In-person clinical appointments required",
        (
            "Web-accessible Gradio workstation with secure live public link"
            " support"
        ),
    ),
]
create_table(
    [
        "Feature Dimension",
        "Existing Clinical Practice / ASR",
        "Proposed System (NeuroSpeak-AI)",
    ],
    comp_matrix,
    col_widths=[1.8, 2.3, 2.3],
)

add_heading_1("7.4 Chapter Summary")
add_para(
    "Chapter 7 presented the experimental evaluation of NeuroSpeak-AI,"
    " reporting 94.2% accuracy for the HuBERT Layer-18 SVM screener, analyzing"
    " acoustic feature divergence across clinical strata, evaluating 600 files"
    " from the TORGO dataset, demonstrating a 77.0% to 92.5% semantic intent"
    " recovery rate on continuous sentences, reviewing Gradio interface"
    " snapshots, and contrasting the framework against conventional clinical"
    " practices."
)
doc.add_page_break()

# Chapter 8: Conclusion & Future Enhancements
add_chapter_title(8, "CONCLUSION AND FUTURE ENHANCEMENTS")
add_heading_1("8.1 Project Conclusion")
add_para(
    "The NeuroSpeak-AI major project demonstrates an integrated, multimodal"
    " deep learning framework addressing motor speech impairment across two"
    " complementary axes: objective clinical severity stratification and"
    " context-aware semantic speech reconstruction."
)
add_para(
    "By extracting 1024-dimensional deep acoustic embeddings from Layer 18 of a"
    " self-supervised HuBERT-Large model and combining them with 7 clinical"
    " acoustic markers (fundamental frequency mean, pitch instability, pause"
    " ratio, duration, MFCC variance, speech activity ratio, and spectral"
    " centroid), the system establishes an objective 1031-dimensional"
    " representation space. Classifying this feature space via a linear Support"
    " Vector Machine achieves 94.2% accuracy across four clinical tiers: Normal,"
    " Mild, Moderate, and Severe."
)
add_para(
    "Concurrently, the speech reconstruction pipeline combines modern ASR"
    " architectures (Whisper-Large-v3 / Wav2Vec2) with a collaborative"
    " multi-agent debate framework deploying a local Qwen-2.5 Proposer and a"
    " cloud Groq Critic. Benchmarks on the TORGO dataset demonstrate that"
    " continuous dysarthric sentences achieve Semantic Intent Preservation"
    " Rates of 72.5% to 87.5% in moderate-to-mild dysarthria. Integrated into a"
    " dual-tab Gradio clinical workstation with SQLite audit logging,"
    " side-by-side acoustic comparison, and a 10-level gamified therapy"
    " progression, NeuroSpeak-AI delivers an accessible, reproducible, and"
    " clinically grounded assistive speech technology platform."
)

add_heading_1("8.2 Future Research & Technical Enhancements")
add_bullet(
    "Edge Hardware Acceleration & Model Quantization: Implement 4-bit / 8-bit"
    " quantization (bitsandbytes / AWQ) on Whisper and Qwen models to enable"
    " fully offline inference on resource-constrained embedded systems and"
    " mobile assistive tablets.",
    bold_prefix="1. ",
)
add_bullet(
    "Personalized Acoustic Fine-Tuning (LoRA): Incorporate Low-Rank Adaptation"
    " (LoRA) modules conditioned on speaker severity profiles, enabling the"
    " system to adapt dynamically to an individual patient’s idiosyncratic"
    " phonological patterns over time.",
    bold_prefix="2. ",
)
add_bullet(
    "Multimodal Articulatory Kinematics: Integrate synchronised video capture"
    " to track lip, jaw, and facial muscle movements via computer vision"
    " landmark models (e.g., MediaPipe Face Mesh), combining articulatory video"
    " features with acoustic embeddings for multimodal dysarthria assessment.",
    bold_prefix="3. ",
)
add_bullet(
    "Expanded Clinical Validation: Conduct clinical trials across hospitals and"
    " rehabilitation centers, gathering qualitative feedback from"
    " speech-language pathologists to refine therapeutic exercises and"
    " diagnostic thresholds.",
    bold_prefix="4. ",
)
add_bullet(
    "Real-Time Duplex Conversational Synthesis: Connect the reconstructed text"
    " intent output (S4) to a personalized text-to-speech (TTS) voice cloning"
    " engine, synthesizing fluid natural speech in the patient’s premorbid"
    " vocal timbre in real time.",
    bold_prefix="5. ",
)

add_heading_1("REFERENCES")
refs = [
    (
        "[1] J. R. Green, P. Sharma, et al., 'Automatic Speech Recognition for"
        " Dysarthric Speech: Challenges, Opportunities, and Recent Advances,'"
        " IEEE Reviews in Biomedical Engineering, vol. 16, pp. 412–426, 2023."
    ),
    (
        "[2] S. Hernandez and N. Cummins, 'Exploring Self-Supervised Speech"
        " Representations for Motor Speech Disorder Assessment,' in Proc."
        " Interspeech 2024, Kos Island, Greece, pp. 2890–2894, 2024."
    ),
    (
        "[3] W.-N. Hsu, B. Bolte, Y.-H. H. Tsai, K. Lakhotia, R. Salakhutdinov,"
        " and A. Mohamed, 'HuBERT: Self-Supervised Speech Representation"
        " Learning by Masked Prediction of Hidden Units,' IEEE/ACM Transactions"
        " on Audio, Speech, and Language Processing, vol. 29, pp. 3451–3460,"
        " 2021."
    ),
    (
        "[4] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and I."
        " Sutskever, 'Robust Speech Recognition via Large-Scale Weak"
        " Supervision,' in Proc. International Conference on Machine Learning"
        " (ICML), pp. 28492–28518, 2023."
    ),
    (
        "[5] A. Baevski, Y. Zhou, A. Mohamed, and M. Auli, 'wav2vec 2.0: A"
        " Framework for Self-Supervised Learning of Speech Representations,'"
        " Advances in Neural Information Processing Systems (NeurIPS), vol. 33,"
        " pp. 12449–12460, 2020."
    ),
    (
        "[6] F. Rudzicz, A. K. Namasivayam, and T. Wolff, 'The TORGO Database"
        " of Acoustic and Articulatory Speech from Speakers with Dysarthria,'"
        " Language Resources and Evaluation, vol. 46, no. 4, pp. 523–541, 2012."
    ),
    (
        "[7] H. Kim, M. Hasegawa-Johnson, A. Perlman, et al., 'Dysarthric"
        " Speech Database for Alternative and Augmentative Communication"
        " (UA-Speech),' in Proc. Interspeech 2008, Brisbane, Australia, pp."
        " 1741–1744, 2008."
    ),
    (
        "[8] M. Mauch and S. Dixon, 'pYIN: A Fundamental Frequency Estimator"
        " Using Probabilistic YIN,' in Proc. IEEE International Conference on"
        " Acoustics, Speech and Signal Processing (ICASSP), pp. 659–663, 2014."
    ),
    (
        "[9] Qwen Team, 'Qwen2.5: A Comprehensive Foundation Model Family,'"
        " Alibaba Group Research Technical Report, 2024."
    ),
    (
        "[10] Y. Liang, D. Song, et al., 'Encouraging Divergent Thinking in"
        " Multi-Agent Debate for Generative Language Models,' in Proc."
        " Association for Computational Linguistics (ACL), pp. 1120–1135, 2024."
    ),
    (
        "[11] C. Cortes and V. Vapnik, 'Support-Vector Networks,' Machine"
        " Learning, vol. 20, no. 3, pp. 273–297, 1995."
    ),
    (
        "[12] F. Pedregosa, G. Varoquaux, et al., 'Scikit-learn: Machine"
        " Learning in Python,' Journal of Machine Learning Research, vol. 12,"
        " pp. 2825–2830, 2011."
    ),
    (
        "[13] B. McFee, C. Raffel, et al., 'librosa: Audio and Music Signal"
        " Analysis in Python,' in Proc. 14th Python in Science Conference, pp."
        " 18–25, 2015."
    ),
    (
        "[14] A. Abid, A. Abdalla, et al., 'Gradio: Hassle-Free Machine"
        " Learning GUIs,' arXiv preprint arXiv:1906.02569, 2020."
    ),
    (
        "[15] American Speech-Language-Hearing Association (ASHA), 'Clinical"
        " Management of Dysarthria in Children and Adults,' ASHA Practice"
        " Policy, 2022."
    ),
]
for r in refs:
  p = doc.add_paragraph()
  p.paragraph_format.space_before = Pt(2)
  p.paragraph_format.space_after = Pt(3)
  p.paragraph_format.line_spacing = 1.15
  p.paragraph_format.left_indent = Inches(0.3)
  p.paragraph_format.first_line_indent = Inches(-0.3)
  run = p.add_run(r)
  run.font.name = "Times New Roman"
  run.font.size = Pt(10)

# -------------------------------------------------------------
# SAVE DOCUMENT
# -------------------------------------------------------------
output_filename = "NeuroSpeak_AI_Major_Project_Report.docx"
doc.save(output_filename)
print(
    f"SUCCESS: Saved '{output_filename}', size: {os.path.getsize(output_filename)} bytes"
)