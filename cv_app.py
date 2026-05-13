#!/usr/bin/env python3
"""
CV Manager — by Md. Mahfuzur Rahman
=================================
Cross-platform (Windows / Ubuntu / Mac)
• Full GUI forms for all sections
• JSON data storage
• PDF export matching original portfolio layout
• Photo support
Run: python3 cv_app.py
"""

from email.mime import text
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont
import json, os, sys, shutil, re
from datetime import datetime
from pathlib import Path

# ── Try importing PDF library ─────────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm, cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable, Image as RLImage,
                                    KeepTogether)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    from reportlab.platypus.flowables import Flowable
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from PIL import Image as PILImage, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# ── Data file ─────────────────────────────────────────────────────────────────
DATA_FILE = Path(__file__).parent / "cv_data.json"

DEFAULT_DATA = {
    "personal": {
        "name": "Md. Mahfuzur Rahman",
        
        "dob": "6-Nov-1982",
        "nationality": "Bangladeshi",
        "nid": "6419049579",
        "email": "mh0e@icloud.com",
        "phone": "+8801941718855",
        "address": "House: 115, Block: B, West of Baunia Bazar Main Road,\nBaunia, Thana: Turag, Dhaka, Bangladesh",
        "about": ("With over two and a half decades forging expertise in construction, telecoms, and real estate, "
                  "Md. Mahfuzur Rahman leads high-performing teams to surpass goals, wielding construction mastery "
                  "and meticulous oversight. He orchestrates projects, budgets, and schedules with precision, ensuring "
                  "flawless daily operations across civil and mechanical domains. A seasoned Project Manager with a "
                  "proven record of success, Md. Mahfuzur Rahman delivers excellence — every project a testament to leadership."),
        "summary": ("Accomplished Civil Engineer & Project Manager with 25+ years across high-rise commercial, institutional, "
                    "and governmental developments. Portfolio includes East West University campus, Shahjalal International "
                    "Airport Terminal-3, Finance Square, and LankaBangla Corporate HQ."),
        "photo": ""
    },
    "experience": [
        {"company": "SPACEZERO LTD. | VOLUMEZERO LTD.", "period": "Aug 2023 – Continue",
         "title": "AGM – Planning & Management",
         "duties": "Strategic Alignment, Multi-Project Oversight, Resource Management, Standardization, Risk Management, Compliance, Reporting",
         "projects": "ST The September | LankaBangla CHO | Finance Square"},
        {"company": "SPACEZERO LTD. | VOLUMEZERO LTD.", "period": "2019 – Aug 2023",
         "title": "AGM – Construction",
         "duties": "Project Management, Budget Analysis & Cost Control, Time and Materials Management, Construction Management, Co-Ordination",
         "projects": "LankaBangla CHO | Finance Square | Shimanto Tower"},
        {"company": "RANGDHANU MEDIA LTD.", "period": "2016 – 2019",
         "title": "Project Manager (rep. Volumezero Ltd.)",
         "duties": "Project Management, Scheduling, Budget and cost, Tender Documentation, Vendor Finalization",
         "projects": "Rangdhanu TV Bhaban (Nexus TV)"},
        {"company": "HASHEM REAL ESTATE LIMITED.", "period": "2014 – 2016",
         "title": "Project Manager (rep. Volumezero Ltd.)",
         "duties": "Project Management, Scheduling, Budget and cost, Tender Documentation, Vendor Finalization",
         "projects": "Jahanara Dynasty"},
        {"company": "MIKA GROUP", "period": "2012 – 2014",
         "title": "Project Manager (rep. Volumezero Ltd.)",
         "duties": "Project Management, Scheduling, Budget and cost, Documentation, Vendor Selection",
         "projects": "Mika Cornerstone"},
        {"company": "EASTWEST UNIVERSITY.", "period": "2009 – 2012",
         "title": "Assistant Engineer",
         "duties": "Project Scheduling, Follow up with Contractor, Checking Bills",
         "projects": "East-West University Permanent Campus"},
        {"company": "ORASINVEST BANGLADESH LTD. (MOBISERVE)", "period": "2005 – 2009",
         "title": "Senior Engineer (Co-Ordinator)",
         "duties": "Project Planning & Scheduling, Resource Allocation, BOQ and Budget Preparation",
         "projects": "300+ Mobile Telecom Projects – Banglalik"},
        {"company": "URBAN HOMES LTD.", "period": "2001 – 2005",
         "title": "Site Engineer to Project Engineer",
         "duties": "Site supervision, structural & finishing oversight, construction management",
         "projects": "Regent Heights | Niketo Heights | Khoshmahal Heights | Mouobash"},
    ],
    "education": [
        {"degree": "S.S.C.", "institution": "B.A.F. Shaheen College, Kurmitola, Dhaka", "year": "1997", "notes": ""},
        {"degree": "Diploma in CE", "institution": "Dhaka Polytechnic Institute, Tejgaon, Dhaka", "year": "2000", "notes": ""},
        {"degree": "B.Sc. in CSE", "institution": "Uttara University, Uttara, Dhaka", "year": "2014", "notes": ""},
    ],
    "skills": [
        {"category": "PMC", "skill": "Project Management", "level": "Expert"},
        {"category": "PMC", "skill": "Project Analysis", "level": "Expert"},
        {"category": "PMC", "skill": "Project Planning", "level": "Expert"},
        {"category": "PMC", "skill": "Project Supervision", "level": "Expert"},
        {"category": "COST & BUDGET", "skill": "Estimation & Costing", "level": "Expert"},
        {"category": "COST & BUDGET", "skill": "Budget Preparation", "level": "Expert"},
        {"category": "COST & BUDGET", "skill": "Schedule", "level": "Expert"},
        {"category": "COST & BUDGET", "skill": "Tender Documentation", "level": "Expert"},
        {"category": "COMPUTER", "skill": "Advance Excel with VBA", "level": "Expert"},
        {"category": "COMPUTER", "skill": "All Office tools", "level": "Expert"},
        {"category": "COMPUTER", "skill": "AutoCAD", "level": "Advanced"},
        {"category": "COMPUTER", "skill": "Photoshop", "level": "Intermediate"},
        {"category": "COMPUTER", "skill": "HTML / CSS", "level": "Intermediate"},
        {"category": "COMPUTER", "skill": "PHP / MySql / Java", "level": "Intermediate"},
        {"category": "COMPUTER", "skill": "Windows & Linux", "level": "Proficient"},
    ],
    "training": [
        {"name": "PMP Training", "institute": "PM Aspire", "trainer": "Mr. Abdullah",
         "year": "2022", "location": "Kurmitola, Dhaka"},
    ],
    "certifications": [
        {"name": "PMP Training Certificate", "body": "PM Aspire Institute", "year": "2022", "notes": "Project Management Professional Training"},
    ],
    "projects": [
        {"name": "ST The September", "company": "SPACEZERO LTD.", "land": "15 Katha",
         "client": "SimpleTree", "location": "Tejgaon Industrial area", "brief": "10 Storied, 03 Basements",
         "duties": "", "designer": "", "year": "2023"},
        {"name": "LankaBangla CHO", "company": "SPACEZERO LTD.", "land": "1 Bigha",
         "client": "LankaBangla Finance", "location": "Tejgaon Industrial area", "brief": "12 Storied, 04 Basements",
         "duties": "", "designer": "", "year": "2020"},
        {"name": "Finance Square", "company": "SPACEZERO LTD.", "land": "10 Katha",
         "client": "Canadian University", "location": "Gulshan-2, Dhaka", "brief": "20 Storied, 04 Basements",
         "duties": "", "designer": "", "year": "2021"},
        {"name": "East-West University Campus", "company": "EASTWEST UNIVERSITY", "land": "7.5 Bigha",
         "client": "EastWest University", "location": "Aftabnagar, Dhaka",
         "brief": "Multiple Buildings 2-9 Storied, 2 Basement",
         "duties": "Project Scheduling, Follow up with Contractor, Checking Bills",
         "designer": "Arch. Bashirul Haque", "year": "2012"},
    ]
}

# ── Load / Save data ──────────────────────────────────────────────────────────
def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                # merge missing keys
                for k, v in DEFAULT_DATA.items():
                    if k not in d:
                        d[k] = v
                return d
        except:
            pass
    return dict(DEFAULT_DATA)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Colour palette ────────────────────────────────────────────────────────────
BG_SIDEBAR = "#E8EAF0"
BG_WHITE   = "#FFFFFF"
NAVY       = "#1B3A5C"
TEAL       = "#2E86AB"
GOLD       = "#D4A843"
DARK       = "#2C3E50"
GREY_TEXT  = "#7F8C8D"
LIGHT_GREY = "#F5F5F5"
RED        = "#C0392B"
GREEN      = "#1B5E20"
BTN_FG     = "#FFFFFF"

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════
class CVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CV Manager — by Md. Mahfuzur Rahman")
        self.root.geometry("1100x750")
        self.root.configure(bg=NAVY)
        self.root.minsize(900, 600)

        self.data = load_data()
        self._build_ui()

    def _build_ui(self):
        # ── Top banner ────────────────────────────────────────────────────────
        banner = tk.Frame(self.root, bg=NAVY, height=60)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(banner, text="  CV MANAGER", font=("Calibri", 22, "bold"),
                 bg=NAVY, fg="white").pack(side="left", padx=16, pady=10)
        tk.Label(banner, text="Md. Mahfuzur Rahman",
                 font=("Calibri", 11), bg=NAVY, fg=GOLD).pack(side="left", pady=10)

        # Export button top right
        tk.Button(banner, text="  Export PDF  ", font=("Calibri", 11, "bold"),
                  bg=GREEN, fg="white", relief="flat", cursor="hand2",
                  command=self.export_pdf, padx=10, pady=4).pack(side="right", padx=16, pady=12)
        tk.Button(banner, text="  Save Data  ", font=("Calibri", 11, "bold"),
                  bg=TEAL, fg="white", relief="flat", cursor="hand2",
                  command=self._save, padx=10, pady=4).pack(side="right", padx=4, pady=12)

        

        # ── Main body ─────────────────────────────────────────────────────────
        body = tk.Frame(self.root, bg=LIGHT_GREY)
        body.pack(fill="both", expand=True)

        # Left nav
        nav = tk.Frame(body, bg=NAVY, width=200)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)

        # Right content
        self.content = tk.Frame(body, bg=LIGHT_GREY)
        self.content.pack(side="left", fill="both", expand=True)

        # ── Nav buttons ───────────────────────────────────────────────────────
        self.pages = {}
        nav_items = [
            ("👤  Personal Info",   "personal",      self.show_personal),
            ("💼  Experience",      "experience",    self.show_experience),
            ("🎓  Education",       "education",     self.show_education),
            ("🛠   Skills",         "skills",        self.show_skills),
            ("📜  Training",        "training",      self.show_training),
            ("🏆  Certifications",  "certifications",self.show_certifications),
            ("🏗   Projects",       "projects",      self.show_projects),
        ]

        tk.Label(nav, text="SECTIONS", font=("Calibri", 9, "bold"),
                 bg=NAVY, fg=GOLD).pack(pady=(20, 8))

        self.nav_btns = {}
        for label, key, cmd in nav_items:
            btn = tk.Button(nav, text=label, font=("Calibri", 11),
                            bg=NAVY, fg="white", relief="flat",
                            anchor="w", padx=16, pady=10,
                            activebackground=TEAL, activeforeground="white",
                            cursor="hand2", command=cmd)
            btn.pack(fill="x", padx=4, pady=1)
            self.nav_btns[key] = btn

        tk.Frame(nav, bg="#2D4F6B", height=1).pack(fill="x", pady=16)

        # ── Utility buttons ───────────────────────────────────────────────────
        tk.Label(nav, text="UTILITIES", font=("Calibri", 9, "bold"),
                 bg=NAVY, fg=GOLD).pack(pady=(20, 8))

        tk.Button(nav, text="🗑   Clean CV", font=("Calibri", 11),
                  bg=RED, fg="white", relief="flat",
                  anchor="w", padx=16, pady=10,
                  activebackground="#A00000", activeforeground="white",
                  cursor="hand2", command=self.clean_cv).pack(fill="x", padx=4, pady=1)

        tk.Button(nav, text="📥   Import PDF", font=("Calibri", 11),
                  bg=GREEN, fg="white", relief="flat",
                  anchor="w", padx=16, pady=10,
                  activebackground="#008000", activeforeground="white",
                  cursor="hand2", command=self.import_from_pdf).pack(fill="x", padx=4, pady=1)
        
        rights_label = tk.Label(nav, font=("Calibri", 9, "italic"), fg="Light Blue", text="@ All rights reserved by Mahfuz",
                            bg=NAVY,  anchor="e", wraplength=100 )
                                
        rights_label.pack(side="right", padx=50, pady=50)

        tk.Frame(nav, bg="#2D4F6B", height=1).pack(fill="x", pady=16)

        # Show first page
        self.show_personal()

    def _set_active_nav(self, key):
        for k, btn in self.nav_btns.items():
            btn.configure(bg=TEAL if k == key else NAVY)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _save(self):
        save_data(self.data)
        self.status_var.set(f"✓ Saved {datetime.now().strftime('%H:%M:%S')}")
        messagebox.showinfo("Saved", "CV data saved successfully!")

    # ── Scrollable frame helper ───────────────────────────────────────────────
    def _scrollable(self, parent):
        outer = tk.Frame(parent, bg=LIGHT_GREY)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=LIGHT_GREY, highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=LIGHT_GREY)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120),"units"))
        return frame

    def _section_title(self, parent, title, subtitle=""):
        hdr = tk.Frame(parent, bg=NAVY)
        hdr.pack(fill="x", padx=20, pady=(20, 0))
        tk.Label(hdr, text=f"  {title}", font=("Calibri", 16, "bold"),
                 bg=NAVY, fg="white", pady=10).pack(side="left")
        if subtitle:
            tk.Label(hdr, text=subtitle, font=("Calibri", 10),
                     bg=NAVY, fg=GOLD).pack(side="right", padx=12)
        tk.Frame(parent, bg=GOLD, height=2).pack(fill="x", padx=20)

    def _field(self, parent, label, var_or_text, row, col=0, wide=False,
               multiline=False, height=3, choices=None, colspan=1):
        """Render a labelled field"""
        cspan = 2 if wide else colspan
        lf = tk.Frame(parent, bg=BG_WHITE)
        lf.grid(row=row, column=col, columnspan=cspan, sticky="ew",
                padx=6, pady=4)
        tk.Label(lf, text=label, font=("Calibri", 9, "bold"),
                 bg=BG_WHITE, fg=NAVY, anchor="w").pack(anchor="w", padx=4, pady=(4,1))

        if choices:
            cb = ttk.Combobox(lf, values=choices, font=("Calibri", 10),
                              textvariable=var_or_text, state="normal")
            cb.pack(fill="x", padx=4, pady=(0,4))
            return cb
        elif multiline:
            txt = tk.Text(lf, height=height, font=("Calibri", 10),
                          relief="solid", bd=1, wrap="word",
                          bg="#FAFAFA")
            txt.pack(fill="x", padx=4, pady=(0,4))
            if isinstance(var_or_text, str):
                txt.insert("1.0", var_or_text)
            return txt
        else:
            e = tk.Entry(lf, textvariable=var_or_text, font=("Calibri", 10),
                         relief="solid", bd=1, bg="#FAFAFA")
            e.pack(fill="x", padx=4, pady=(0,4))
            return e

    def _btn(self, parent, text, cmd, color=TEAL, row=0, col=0):
        b = tk.Button(parent, text=text, command=cmd,
                      font=("Calibri", 10, "bold"), bg=color, fg="white",
                      relief="flat", padx=14, pady=6, cursor="hand2",
                      activebackground=DARK, activeforeground="white")
        b.grid(row=row, column=col, padx=6, pady=8, sticky="w")
        return b

    def clean_cv(self):
        """Reset CV data to empty/fresh state."""
        if not messagebox.askyesno("Confirm Clean CV",
                                   "This will clear all saved CV data and reset the app to a fresh state.\n\n"
                                   "This cannot be undone. Continue?"):
            return

        self.data = {
            "personal": {
                "name": "", "dob": "", "nationality": "", "nid": "",
                "email": "", "phone": "", "address": "", "about": "",
                "summary": "", "photo": ""
            },
            "experience": [],
            "education": [],
            "skills": [],
            "training": [],
            "certifications": [],
            "projects": []
        }

        save_data(self.data)
        self.status_var.set("🗑 CV cleaned - all data reset")
        messagebox.showinfo("CV Cleaned", "CV has been reset to a fresh blank state.")
        self.show_personal()

    def import_from_pdf(self):
        """Import CV data from a previously exported PDF."""
        if not HAS_PDFPLUMBER:
            messagebox.showerror("Missing Library",
                                 "PDF import requires the 'pdfplumber' package.\n"
                                 "Install it with: pip install pdfplumber")
            return

        pdf_file = filedialog.askopenfilename(
            title="Select exported CV PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not pdf_file:
            return

        try:
            extracted_data = self._parse_pdf_data(pdf_file)
            extracted_data = self._ai_refine_import(extracted_data)
            if not extracted_data:
                raise ValueError("No structured data could be extracted from this PDF.")
            self._show_import_preview(extracted_data)
        except Exception as exc:
            messagebox.showerror("Import Error", f"Unable to import PDF:\n{exc}")

    def _parse_pdf_data(self, pdf_path):
        """Smartly parse exported CV PDF into structured data with advanced AI-like techniques."""
        import pdfplumber

        extracted = {
            "personal": {},
            "experience": [],
            "education": [],
            "skills": [],
            "training": [],
            "certifications": [],
            "projects": []
        }

        def section_key(line):
            text = line.upper()
            patterns = [
                (r"\bpersonal\b", "personal"),
                (r"\b(work\s+)?experience\b", "experience"),
                (r"\beducation\b", "education"),
                (r"\bskills\b", "skills"),
                (r"\btraining\b", "training"),
                (r"\b(certifications?|credentials?)\b", "certifications"),
                (r"\bprojects?\b", "projects"),
            ]
            for pattern, key in patterns:
                if re.search(pattern, text, re.I):
                    return key
            return None

        def normalize_line(line):
            return re.sub(r"\s+", " ", line.strip())

        def is_period_line(line):
            """Detect if line contains date range."""
            return bool(re.search(r"(\d{1,2}\s*[/-]\s*)?(\d{4}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*(–|-|to|through)\s*(\d{1,2}\s*[/-]\s*)?(\d{4}|present|current|ongoing)", line, re.I))

        def extract_dates(text):
            """Extract date range from text."""
            match = re.search(r"(\d{4}|present|current).*(–|-|to).*(\d{4}|present|current)", text, re.I)
            return match.group(0) if match else ""

        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])

        lines = [normalize_line(l) for l in text.splitlines() if normalize_line(l)]
        current_section = None
        current_entry = None
        i = 0

        while i < len(lines):
            line = lines[i]
            
            new_section = section_key(line)
            if new_section:
                current_section = new_section
                current_entry = None
                i += 1
                continue

            if not current_section:
                i += 1
                continue

            # ── Personal Section ──────────────────────────────────────────────
            if current_section == "personal":
                self._extract_personal_data(line, extracted["personal"])
                i += 1
                continue

            # ── Experience Section (Advanced) ─────────────────────────────────
            if current_section == "experience":
                if is_period_line(line):
                    period = extract_dates(line)
                    current_entry = {"company": "", "period": period, "title": "", "duties": "", "projects": ""}
                    extracted["experience"].append(current_entry)
                    i += 1
                    continue

                if current_entry is None or (line and not line[0].isspace() and line[0].isupper()):
                    if current_entry and not current_entry["company"]:
                        current_entry["company"] = line
                    else:
                        current_entry = {"company": line, "period": "", "title": "", "duties": "", "projects": ""}
                        extracted["experience"].append(current_entry)
                    i += 1
                    continue

                if current_entry:
                    if re.search(r"\b(as|as a|role|position|title|designation):\s*", line, re.I):
                        current_entry["title"] = re.sub(r".*?:\s*", "", line, flags=re.I)
                    elif re.search(r"\b(responsibilities?|duties?|tasks?|achievements?):", line, re.I):
                        current_entry["duties"] = line
                        i += 1
                        while i < len(lines) and lines[i] and (lines[i][0].isspace() or lines[i].startswith("•") or lines[i].startswith("-")):
                            current_entry["duties"] += " " + lines[i].strip()
                            i += 1
                        continue
                    elif re.search(r"\b(projects?|skills used):", line, re.I):
                        current_entry["projects"] = line
                    else:
                        if current_entry["title"]:
                            if current_entry["duties"]:
                                current_entry["duties"] += " " + line
                            else:
                                current_entry["duties"] = line
                        elif not current_entry["title"]:
                            current_entry["title"] = line
                i += 1
                continue

            # ── Education Section (Advanced) ──────────────────────────────────
            if current_section == "education":
                degree_match = re.search(r"(s\.s\.c|h\.s\.c|diploma|b\.?sc|m\.?sc|mba|phd|ba|bbs|b\.?tech|m\.?tech)", line, re.I)
                if degree_match or re.search(r"\d{4}", line):
                    current_entry = {"degree": "", "institution": "", "year": "", "grade": ""}
                    extracted["education"].append(current_entry)
                    if degree_match:
                        current_entry["degree"] = line
                    i += 1
                    continue

                if current_entry:
                    if re.search(r"(university|college|institute|school|academy)", line, re.I):
                        if not current_entry["institution"]:
                            current_entry["institution"] = line
                    elif re.search(r"\b(gpa|grade|result|score|mark):\s*", line, re.I):
                        current_entry["grade"] = re.sub(r".*?:\s*", "", line)
                    elif re.search(r"\d{4}", line):
                        if not current_entry["year"]:
                            current_entry["year"] = re.search(r"\d{4}", line).group(0)
                    elif not current_entry["degree"]:
                        current_entry["degree"] = line
                    elif not current_entry["institution"]:
                        current_entry["institution"] = line
                i += 1
                continue

            # ── Skills Section (Advanced) ─────────────────────────────────────
            if current_section == "skills":
                skill_line = line
                separators = [r"[•\-]", r",", r";", r"\|"]
                for sep in separators:
                    if re.search(sep, skill_line):
                        tokens = re.split(sep, skill_line)
                        for token in tokens:
                            token = token.strip()
                            if token and len(token) > 1:
                                skill_cat = ""
                                if re.search(r"(language|programming|code)", token, re.I):
                                    skill_cat = "Programming"
                                elif re.search(r"(data|database|sql|nosql)", token, re.I):
                                    skill_cat = "Data"
                                elif re.search(r"(design|ui|ux|graphic)", token, re.I):
                                    skill_cat = "Design"
                                extracted["skills"].append({"category": skill_cat, "skill": token, "level": ""})
                        break
                else:
                    if skill_line and len(skill_line) > 2:
                        extracted["skills"].append({"category": "", "skill": skill_line, "level": ""})
                i += 1
                continue

            # ── Training Section ──────────────────────────────────────────────
            if current_section == "training":
                if not current_entry:
                    current_entry = {"name": line, "institute": "", "trainer": "", "year": "", "location": ""}
                    extracted["training"].append(current_entry)
                else:
                    if re.search(r"(institute|organization|provider):\s*", line, re.I):
                        current_entry["institute"] = re.sub(r".*?:\s*", "", line)
                    elif re.search(r"\d{4}", line):
                        current_entry["year"] = re.search(r"\d{4}", line).group(0)
                    elif not current_entry["institute"]:
                        current_entry["institute"] = line
                i += 1
                continue

            # ── Certifications Section ────────────────────────────────────────
            if current_section == "certifications":
                if not current_entry:
                    current_entry = {"name": line, "body": "", "year": "", "notes": ""}
                    extracted["certifications"].append(current_entry)
                else:
                    if re.search(r"(issuer|issuing|body|organization|authority):\s*", line, re.I):
                        current_entry["body"] = re.sub(r".*?:\s*", "", line)
                    elif re.search(r"\d{4}", line):
                        current_entry["year"] = re.search(r"\d{4}", line).group(0)
                    elif not current_entry["body"]:
                        current_entry["body"] = line
                i += 1
                continue

            # ── Projects Section ──────────────────────────────────────────────
            if current_section == "projects":
                if not current_entry or (line and line[0].isupper() and not current_entry.get("name")):
                    current_entry = {"name": line, "company": "", "year": "", "land": "", "client": "", "location": "", "brief": "", "designer": "", "duties": ""}
                    extracted["projects"].append(current_entry)
                else:
                    if re.search(r"(company|organization|client):\s*", line, re.I):
                        current_entry["company"] = re.sub(r".*?:\s*", "", line)
                    elif re.search(r"(brief|description|summary|overview):\s*", line, re.I):
                        current_entry["brief"] = re.sub(r".*?:\s*", "", line)
                    elif re.search(r"\d{4}", line):
                        if not current_entry["year"]:
                            current_entry["year"] = re.search(r"\d{4}", line).group(0)
                    elif not current_entry["company"]:
                        current_entry["company"] = line
                i += 1
                continue

            i += 1

        return extracted

    def _ai_refine_import(self, extracted):
        """Multi-pass AI refinement for parsed PDF data using advanced heuristics."""
        def clean_text(value):
            return re.sub(r"\s+", " ", value or "").strip()

        def is_likely_job_title(text):
            """Detect if text is likely a job title."""
            job_keywords = r"\b(manager|engineer|developer|architect|consultant|director|officer|analyst|specialist|coordinator|lead|head|supervisor|lead|principal|senior|junior|executive|assistant|associate|director|president|ceo|cto|cfo)\b"
            return bool(re.search(job_keywords, text, re.I))

        def extract_key_value(text):
            """Try to extract key: value pairs."""
            match = re.match(r"^([^:]+):\s*(.+)$", text)
            return match.groups() if match else (None, None)

        # ── Pass 1: Clean all text ────────────────────────────────────────────
        for sec in ["experience", "education", "projects", "training", "certifications"]:
            for item in extracted.get(sec, []):
                for k, v in item.items():
                    item[k] = clean_text(v)
        
        for key, value in extracted.get("personal", {}).items():
            extracted["personal"][key] = clean_text(value)

        # ── Pass 2: Deduplicate and categorize skills ─────────────────────────
        seen_skills = {}
        cleaned_skills = []
        for skill in extracted.get("skills", []):
            text = skill.get("skill", "").lower()
            if not text or len(text) < 2:
                continue
            if text not in seen_skills:
                seen_skills[text] = True
                cat = skill.get("category", "")
                if not cat:
                    if re.search(r"\b(python|java|c\+\+|javascript|ruby|php|swift|kotlin|go|rust)\b", text, re.I):
                        cat = "Programming Languages"
                    elif re.search(r"\b(sql|mongodb|postgresql|mysql|firebase|dynamodb|cassandra)\b", text, re.I):
                        cat = "Databases"
                    elif re.search(r"\b(aws|azure|gcp|docker|kubernetes|terraform|jenkins)\b", text, re.I):
                        cat = "DevOps & Cloud"
                    elif re.search(r"\b(react|angular|vue|django|flask|spring|nodejs|express)\b", text, re.I):
                        cat = "Frameworks"
                    elif re.search(r"\b(figma|adobe|sketch|photoshop|illustrator|xd|ui|ux)\b", text, re.I):
                        cat = "Design"
                    elif re.search(r"\b(git|svn|github|gitlab|bitbucket)\b", text, re.I):
                        cat = "Version Control"
                    elif re.search(r"\b(communication|leadership|teamwork|problem.?solving|analytical)\b", text, re.I):
                        cat = "Soft Skills"
                cleaned_skills.append({"category": cat, "skill": skill.get("skill"), "level": ""})
        extracted["skills"] = cleaned_skills

        # ── Pass 3: Refine experience entries ──────────────────────────────────
        for exp in extracted.get("experience", []):
            # Try to extract job title if missing
            if not exp["title"] and exp["company"]:
                if is_likely_job_title(exp["company"]):
                    exp["title"] = exp["company"]
                    exp["company"] = ""
            
            # Try to separate company and period from combined field
            if exp["company"] and "|" in exp["company"] and not exp["period"]:
                parts = [clean_text(p) for p in exp["company"].split("|")]
                exp["company"] = parts[0]
                if len(parts) > 1:
                    exp["period"] = parts[1]
            
            # Extract period from duties if not present
            if not exp["period"] and exp["duties"]:
                period_match = re.search(r"(\d{4}\s*(–|-|to)\s*\d{4}|\d{4}\s*(–|-|to)\s*(present|current))", exp["duties"])
                if period_match:
                    exp["period"] = period_match.group(0)
            
            # Clean up duties
            exp["duties"] = re.sub(r"^(duties?:|responsibilities?:|achievements?:)\s*", "", exp["duties"], flags=re.I).strip()
            exp["projects"] = re.sub(r"^(projects?:|skills? used:)\s*", "", exp["projects"], flags=re.I).strip()

        # ── Pass 4: Refine education entries ──────────────────────────────────
        for edu in extracted.get("education", []):
            # Try to parse combined degree/institution/year
            if edu["degree"] and not edu["institution"] and "," in edu["degree"]:
                parts = [clean_text(p) for p in edu["degree"].split(",")]
                edu["degree"] = parts[0]
                if len(parts) > 1:
                    edu["institution"] = parts[1]
            
            # Extract year from degree if not present
            if not edu["year"]:
                year_match = re.search(r"(19|20)\d{2}", edu["degree"])
                if year_match:
                    edu["year"] = year_match.group(0)
                    edu["degree"] = re.sub(year_match.group(0), "", edu["degree"]).strip(" ,")
            
            # Extract GPA from grade field
            gpa_match = re.search(r"(gpa|grade|score):\s*([\d.]+)", edu["grade"], re.I)
            if gpa_match:
                edu["grade"] = gpa_match.group(2)

        # ── Pass 5: Refine project entries ────────────────────────────────────
        for proj in extracted.get("projects", []):
            if proj["name"] and not proj["company"] and ("," in proj["name"] or "|" in proj["name"]):
                sep = "," if "," in proj["name"] else "|"
                parts = [clean_text(p) for p in proj["name"].split(sep)]
                proj["name"] = parts[0]
                if len(parts) > 1:
                    proj["company"] = parts[1]
            
            # Extract year from brief if present
            if not proj["year"] and proj["brief"]:
                year_match = re.search(r"(19|20)\d{2}", proj["brief"])
                if year_match:
                    proj["year"] = year_match.group(0)

        # ── Pass 6: Refine training entries ───────────────────────────────────
        for train in extracted.get("training", []):
            if train["name"] and not train["institute"] and "," in train["name"]:
                parts = [clean_text(p) for p in train["name"].split(",")]
                train["name"] = parts[0]
                if len(parts) > 1:
                    train["institute"] = parts[1]

        # ── Pass 7: Refine certification entries ───────────────────────────────
        for cert in extracted.get("certifications", []):
            if cert["name"] and not cert["body"] and "," in cert["name"]:
                parts = [clean_text(p) for p in cert["name"].split(",")]
                cert["name"] = parts[0]
                if len(parts) > 1:
                    cert["body"] = parts[1]

        return extracted

    def _build_ai_summary(self):
        personal = self.data.get("personal", {})
        experience = self.data.get("experience", [])
        education = self.data.get("education", [])
        skills = self.data.get("skills", [])

        pieces = []
        if personal.get("name"):
            pieces.append(f"{personal['name']} is a seasoned professional")
        if experience:
            top_roles = []
            for exp in experience[:2]:
                title = exp.get("title") or exp.get("company")
                if title:
                    top_roles.append(title)
            if top_roles:
                pieces.append(f"with experience as {', '.join(top_roles)}")
        if education:
            pieces.append(f"holding qualifications such as {education[0].get('degree','a relevant degree')}")
        if skills:
            top_skills = [s.get("skill") for s in skills if s.get("skill")][:5]
            if top_skills:
                pieces.append(f"skilled in {', '.join(top_skills[:5])}")

        summary = ". ".join(pieces).strip()
        if summary and not summary.endswith("."):
            summary += "."
        return summary or "Experienced professional with a strong CV profile, ready to contribute to new opportunities."

    def _extract_personal_data(self, line, personal_dict):
        if ':' not in line:
            return
        key, value = [part.strip() for part in line.split(':', 1)]
        lower = key.lower()
        if 'name' in lower:
            personal_dict['name'] = value
        elif 'email' in lower or 'e-mail' in lower:
            personal_dict['email'] = value
        elif 'phone' in lower or 'contact' in lower:
            personal_dict['phone'] = value
        elif 'nationality' in lower:
            personal_dict['nationality'] = value
        elif 'date of birth' in lower or 'dob' in lower:
            personal_dict['dob'] = value
        elif 'national id' in lower or 'nid' in lower:
            personal_dict['nid'] = value
        elif 'address' in lower:
            personal_dict['address'] = value

    def _show_import_preview(self, extracted_data):
        preview = tk.Toplevel(self.root)
        preview.title("Import Preview")
        preview.geometry("850x650")
        preview.configure(bg=BG_WHITE)

        tk.Label(preview, text="📥 Import Preview", font=("Calibri", 16, "bold"),
                 bg=BG_WHITE, fg=NAVY).pack(pady=14)

        outer = tk.Frame(preview, bg=BG_WHITE)
        outer.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(outer, bg=BG_WHITE, highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=BG_WHITE)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        row = 0
        for section, data in extracted_data.items():
            tk.Label(frame, text=section.upper(), font=("Calibri", 12, "bold"),
                     bg=BG_WHITE, fg=NAVY).grid(row=row, column=0, sticky="w", pady=(12,4))
            row += 1
            if isinstance(data, dict):
                for key, value in data.items():
                    if value:
                        tk.Label(frame, text=f"  {key}: {value}", font=("Calibri", 10),
                                 bg=BG_WHITE, fg=DARK).grid(row=row, column=0, sticky="w")
                        row += 1
            else:
                for item in data:
                    item_text = ", ".join([f"{k}: {v}" for k, v in item.items() if v]) if isinstance(item, dict) else str(item)
                    tk.Label(frame, text=f"  • {item_text}", font=("Calibri", 10),
                             bg=BG_WHITE, fg=DARK, wraplength=780, justify="left").grid(row=row, column=0, sticky="w", pady=2)
                    row += 1

        btn_frame = tk.Frame(preview, bg=BG_WHITE)
        btn_frame.pack(fill="x", padx=20, pady=12)

        def do_import():
            self.data = extracted_data
            save_data(self.data)
            self.status_var.set("📥 PDF data imported")
            messagebox.showinfo("Import Complete", "PDF data imported successfully.")
            preview.destroy()
            self.show_personal()

        tk.Button(btn_frame, text="  ✅ Import Data  ", command=do_import,
                  font=("Calibri", 11, "bold"), bg=TEAL, fg="white",
                  relief="flat", padx=20, pady=8, cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_frame, text="  ❌ Cancel  ", command=preview.destroy,
                  font=("Calibri", 11), bg=LIGHT_GREY, fg=DARK,
                  relief="flat", padx=20, pady=8, cursor="hand2").pack(side="left")

    def _edit_entry(self, section, idx):
        item = self.data[section][idx]
        modal = tk.Toplevel(self.root)
        modal.title("Edit entry")
        modal.geometry("650x520")
        modal.configure(bg=BG_WHITE)

        field_map = {
            'experience': [
                ('company', 'Company'), ('period', 'Period'), ('title', 'Job Title'),
                ('duties', 'Duties'), ('projects', 'Projects')
            ],
            'education': [
                ('degree', 'Degree'), ('institution', 'Institution'),
                ('year', 'Year'), ('grade', 'Grade/Notes')
            ],
            'skills': [
                ('category', 'Category'), ('skill', 'Skill'), ('level', 'Level')
            ],
            'training': [
                ('name', 'Training Name'), ('institute', 'Institute'),
                ('trainer', 'Trainer'), ('year', 'Year'), ('location', 'Location / Notes')
            ],
            'certifications': [
                ('name', 'Certification Name'), ('body', 'Issuing Body'),
                ('year', 'Year'), ('notes', 'Notes')
            ],
            'projects': [
                ('name', 'Project Name'), ('company', 'Company'), ('year', 'Year'),
                ('land', 'Land Area'), ('client', 'Client'), ('location', 'Location'),
                ('brief', 'Project Brief'), ('designer', 'Designed By'), ('duties', 'Duties')
            ]
        }

        entries = {}
        row = 0
        for key, label in field_map.get(section, []):
            tk.Label(modal, text=label, font=("Calibri", 10, "bold"),
                     bg=BG_WHITE, fg=NAVY).grid(row=row, column=0, sticky="w", padx=16, pady=(12 if row==0 else 4,2))
            if key in ['duties', 'projects', 'brief', 'grade', 'notes', 'location']:
                txt = tk.Text(modal, height=3, font=("Calibri", 10), relief="solid", bd=1, bg="#FAFAFA", wrap="word")
                txt.grid(row=row, column=1, sticky="ew", padx=16, pady=(12 if row==0 else 4,2))
                txt.insert('1.0', item.get(key, ''))
                entries[key] = txt
            else:
                var = tk.StringVar(value=item.get(key, ''))
                tk.Entry(modal, textvariable=var, font=("Calibri", 10), relief="solid", bd=1, bg="#FAFAFA").grid(row=row, column=1, sticky="ew", padx=16, pady=(12 if row==0 else 4,2))
                entries[key] = var
            row += 1

        modal.columnconfigure(1, weight=1)

        def save_edit():
            for key, widget in entries.items():
                if isinstance(widget, tk.Text):
                    item[key] = widget.get('1.0', 'end-1c').strip()
                else:
                    item[key] = widget.get().strip()
            save_data(self.data)
            self.status_var.set(f"✓ Updated {section} entry")
            modal.destroy()
            getattr(self, f"show_{section}")()

        tk.Button(modal, text="  Save Changes  ", command=save_edit,
                  font=("Calibri", 11, "bold"), bg=TEAL, fg="white",
                  relief="flat", padx=18, pady=8, cursor="hand2").grid(row=row, column=0, padx=16, pady=16, sticky="w")
        tk.Button(modal, text="  Cancel  ", command=modal.destroy,
                  font=("Calibri", 11), bg=LIGHT_GREY, fg=DARK,
                  relief="flat", padx=18, pady=8, cursor="hand2").grid(row=row, column=1, padx=16, pady=16, sticky="e")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: PERSONAL INFO
    # ══════════════════════════════════════════════════════════════════════════
    def show_personal(self):
        self._set_active_nav("personal")
        self._clear_content()
        self._section_title(self.content, "👤 Personal Information", "All fields auto-saved")

        sf = self._scrollable(self.content)
        card = tk.Frame(sf, bg=BG_WHITE, bd=1, relief="solid")
        card.pack(fill="x", padx=20, pady=16)
        card.columnconfigure(1, weight=1); card.columnconfigure(3, weight=1)

        p = self.data["personal"]
        v = {k: tk.StringVar(value=p.get(k,"")) for k in
             ["name","dob","nationality","nid","email","phone"]}

        self._field(card,"Full Name *",           v["name"],       0, 0, False)
        
        self._field(card,"Date of Birth",         v["dob"],        1, 0, False)
        self._field(card,"Nationality",           v["nationality"],1, 2, False)
        self._field(card,"National ID No.",       v["nid"],        2, 0, False)
        self._field(card,"Email Address *",       v["email"],      2, 2, False)
        self._field(card,"Contact No.",           v["phone"],      3, 0, False, colspan=2)

        # Address multiline
        addr_frame = tk.Frame(card, bg=BG_WHITE)
        addr_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=6, pady=4)
        tk.Label(addr_frame, text="Address", font=("Calibri",9,"bold"),
                 bg=BG_WHITE, fg=NAVY).pack(anchor="w", padx=4)
        addr_txt = tk.Text(addr_frame, height=3, font=("Calibri",10),
                           relief="solid", bd=1, bg="#FAFAFA", wrap="word")
        addr_txt.insert("1.0", p.get("address",""))
        addr_txt.pack(fill="x", padx=4, pady=(0,4))

        # About Me
        about_frame = tk.Frame(card, bg=BG_WHITE)
        about_frame.grid(row=5, column=0, columnspan=4, sticky="ew", padx=6, pady=4)
        tk.Label(about_frame, text="About Me", font=("Calibri",9,"bold"),
                 bg=BG_WHITE, fg=NAVY).pack(anchor="w", padx=4)
        about_txt = tk.Text(about_frame, height=5, font=("Calibri",10),
                            relief="solid", bd=1, bg="#FAFAFA", wrap="word")
        about_txt.insert("1.0", p.get("about",""))
        about_txt.pack(fill="x", padx=4, pady=(0,4))

        # Summary
        summ_frame = tk.Frame(card, bg=BG_WHITE)
        summ_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=6, pady=4)
        tk.Label(summ_frame, text="Professional Summary", font=("Calibri",9,"bold"),
                 bg=BG_WHITE, fg=NAVY).pack(anchor="w", padx=4)
        summ_txt = tk.Text(summ_frame, height=4, font=("Calibri",10),
                           relief="solid", bd=1, bg="#FAFAFA", wrap="word")
        summ_txt.insert("1.0", p.get("summary",""))
        summ_txt.pack(fill="x", padx=4, pady=(0,4))

        # Photo
        photo_frame = tk.Frame(card, bg=BG_WHITE)
        photo_frame.grid(row=7, column=0, columnspan=4, sticky="ew", padx=6, pady=4)
        tk.Label(photo_frame, text="Profile Photo", font=("Calibri",9,"bold"),
                 bg=BG_WHITE, fg=NAVY).pack(anchor="w", padx=4)
        photo_path_var = tk.StringVar(value=p.get("photo",""))
        ph_row = tk.Frame(photo_frame, bg=BG_WHITE)
        ph_row.pack(fill="x", padx=4)
        tk.Entry(ph_row, textvariable=photo_path_var, font=("Calibri",9),
                 relief="solid", bd=1, bg="#FAFAFA", state="readonly",
                 width=50).pack(side="left", pady=4)

        def browse_photo():
            fp = filedialog.askopenfilename(
                title="Select Profile Photo",
                filetypes=[("Images","*.jpg *.jpeg *.png *.bmp")])
            if fp:
                photo_path_var.set(fp)
        tk.Button(ph_row, text=" Browse Photo ", command=browse_photo,
                  font=("Calibri",9,"bold"), bg=TEAL, fg="white",
                  relief="flat", cursor="hand2").pack(side="left", padx=8)

        def clear_photo():
            photo_path_var.set("")
        tk.Button(ph_row, text="Clear", command=clear_photo,
                  font=("Calibri",9), bg=LIGHT_GREY, fg=DARK,
                  relief="flat", cursor="hand2").pack(side="left")

        # Buttons
        btn_row = tk.Frame(card, bg=BG_WHITE)
        btn_row.grid(row=8, column=0, columnspan=4, sticky="w", padx=6, pady=12)

        def save_personal():
            if not v["name"].get().strip():
                messagebox.showerror("Required","Full Name is required"); return
            if not v["email"].get().strip():
                messagebox.showerror("Required","Email is required"); return
            for k in ["name","dob","nationality","nid","email","phone"]:
                self.data["personal"][k] = v[k].get().strip()
            self.data["personal"]["address"] = addr_txt.get("1.0","end-1c").strip()
            self.data["personal"]["about"]   = about_txt.get("1.0","end-1c").strip()
            self.data["personal"]["summary"] = summ_txt.get("1.0","end-1c").strip()
            self.data["personal"]["photo"]   = photo_path_var.get().strip()
            save_data(self.data)
            self.status_var.set("✓ Personal info saved")
            messagebox.showinfo("Saved","Personal information saved!")

        def generate_ai_summary():
            summary = self._build_ai_summary()
            summ_txt.delete("1.0", "end")
            summ_txt.insert("1.0", summary)
            self.data["personal"]["summary"] = summary
            save_data(self.data)
            self.status_var.set("🧠 AI summary generated")
            messagebox.showinfo("AI Summary", "A professional summary has been generated. Review and adjust it as needed.")

        tk.Button(btn_row, text="  Save Personal Info  ", command=save_personal,
                  font=("Calibri",11,"bold"), bg=NAVY, fg="white",
                  relief="flat", padx=14, pady=8, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_row, text="  🧠 Generate AI Summary  ", command=generate_ai_summary,
                  font=("Calibri",11,"bold"), bg=GOLD, fg=DARK,
                  relief="flat", padx=14, pady=8, cursor="hand2").pack(side="left", padx=4)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: EXPERIENCE
    # ══════════════════════════════════════════════════════════════════════════
    def show_experience(self):
        self._set_active_nav("experience")
        self._clear_content()
        self._section_title(self.content, "💼 Work Experience")

        sf = self._scrollable(self.content)

        # ── Add new entry form ────────────────────────────────────────────────
        add_card = tk.LabelFrame(sf, text="  ➕  Add New Experience Entry  ",
                                  font=("Calibri",11,"bold"), bg=BG_WHITE,
                                  fg=NAVY, bd=2, relief="groove")
        add_card.pack(fill="x", padx=20, pady=(16,8))
        add_card.columnconfigure(1,weight=1); add_card.columnconfigure(3,weight=1)

        ev = {k: tk.StringVar() for k in ["company","period","title"]}
        titles = ["AGM – Planning & Management","AGM – Construction","Project Manager",
                  "Senior Project Engineer","Assistant Engineer","Site Engineer",
                  "Senior Engineer (Co-Ordinator)","Site Engineer to Project Engineer","Other"]

        tk.Label(add_card,text="Company *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=0,sticky="w",padx=8,pady=(10,2))
        tk.Entry(add_card,textvariable=ev["company"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=0,column=1,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Period *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=2,sticky="w",padx=8,pady=(10,2))
        tk.Entry(add_card,textvariable=ev["period"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=0,column=3,sticky="ew",padx=8,pady=(10,2))

        tk.Label(add_card,text="Job Title *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=1,column=0,sticky="w",padx=8,pady=4)
        ttk.Combobox(add_card,textvariable=ev["title"],values=titles,font=("Calibri",10)).grid(row=1,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        tk.Label(add_card,text="Duties & Responsibilities",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=2,column=0,sticky="nw",padx=8,pady=4)
        duties_txt = tk.Text(add_card,height=4,font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA",wrap="word")
        duties_txt.grid(row=2,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        tk.Label(add_card,text="Projects",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=3,column=0,sticky="nw",padx=8,pady=4)
        projects_txt = tk.Text(add_card,height=2,font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA",wrap="word")
        projects_txt.grid(row=3,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        def add_exp():
            if not ev["company"].get().strip(): messagebox.showerror("Required","Company is required"); return
            if not ev["period"].get().strip():  messagebox.showerror("Required","Period is required");  return
            if not ev["title"].get().strip():   messagebox.showerror("Required","Job Title is required"); return
            entry = {"company":ev["company"].get().strip(), "period":ev["period"].get().strip(),
                     "title":ev["title"].get().strip(),
                     "duties":duties_txt.get("1.0","end-1c").strip(),
                     "projects":projects_txt.get("1.0","end-1c").strip()}
            self.data["experience"].append(entry)
            save_data(self.data)
            self.status_var.set(f"✓ Added: {entry['company']}")
            for k in ev.values(): k.set("")
            duties_txt.delete("1.0","end"); projects_txt.delete("1.0","end")
            self.show_experience()

        btn_row2 = tk.Frame(add_card, bg=BG_WHITE)
        btn_row2.grid(row=4, column=0, columnspan=4, sticky="w", padx=8, pady=10)
        tk.Button(btn_row2, text="  ➕ Add Experience  ", command=add_exp,
                  font=("Calibri",11,"bold"), bg=GOLD, fg=DARK,
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")

        # ── Existing entries ──────────────────────────────────────────────────
        tk.Label(sf, text="  Existing Experience Entries", font=("Calibri",12,"bold"),
                 bg=LIGHT_GREY, fg=NAVY).pack(anchor="w", padx=20, pady=(16,4))

        for i, exp in enumerate(self.data["experience"]):
            self._exp_card(sf, exp, i)

    def _exp_card(self, parent, exp, idx):
        card = tk.Frame(parent, bg=BG_WHITE, bd=1, relief="solid")
        card.pack(fill="x", padx=20, pady=4)

        hdr = tk.Frame(card, bg=NAVY)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  {exp['company']}", font=("Calibri",10,"bold"),
                 bg=NAVY, fg="white", pady=6).pack(side="left")
        tk.Label(hdr, text=f"{exp['period']}  ", font=("Calibri",9),
                 bg=NAVY, fg=GOLD).pack(side="right")

        body = tk.Frame(card, bg=BG_WHITE)
        body.pack(fill="x", padx=12, pady=8)
        tk.Label(body, text=exp.get("title",""), font=("Calibri",10,"italic"),
                 bg=BG_WHITE, fg=DARK).pack(anchor="w")
        if exp.get("duties"):
            tk.Label(body, text=f"Duties: {exp['duties']}", font=("Calibri",9),
                     bg=BG_WHITE, fg=GREY_TEXT, wraplength=700,
                     justify="left").pack(anchor="w", pady=2)
        if exp.get("projects"):
            tk.Label(body, text=f"Projects: {exp['projects']}", font=("Calibri",9),
                     bg=BG_WHITE, fg=TEAL, wraplength=700,
                     justify="left").pack(anchor="w")

        btn_row = tk.Frame(card, bg=BG_WHITE)
        btn_row.pack(anchor="e", padx=8, pady=4)

        def edit_exp(i=idx):
            self._edit_entry("experience", i)

        def delete_exp(i=idx):
            if messagebox.askyesno("Delete", f"Delete entry for {self.data['experience'][i]['company']}?"):
                self.data["experience"].pop(i)
                save_data(self.data)
                self.show_experience()

        tk.Button(btn_row, text=" ✎ Edit ", command=edit_exp,
                  font=("Calibri",8), bg=LIGHT_GREY, fg=TEAL,
                  relief="flat", cursor="hand2").pack(side="right", padx=4)
        tk.Button(btn_row, text=" 🗑 Delete ", command=delete_exp,
                  font=("Calibri",8), bg=LIGHT_GREY, fg=RED,
                  relief="flat", cursor="hand2").pack(side="right")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: EDUCATION
    # ══════════════════════════════════════════════════════════════════════════
    def show_education(self):
        self._set_active_nav("education")
        self._clear_content()
        self._section_title(self.content, "🎓 Education & Qualifications")
        sf = self._scrollable(self.content)

        add_card = tk.LabelFrame(sf, text="  ➕  Add Education  ",
                                  font=("Calibri",11,"bold"), bg=BG_WHITE, fg=NAVY, bd=2, relief="groove")
        add_card.pack(fill="x", padx=20, pady=(16,8))
        add_card.columnconfigure(1,weight=1); add_card.columnconfigure(3,weight=1)

        degrees = ["S.S.C.","H.S.C.","Diploma in CE","Diploma in EEE", "Diploma in CSE", "Diploma in Mechanical",
                   "B.Sc. in CE","B.Sc. in CSE","B.Sc. in EEE", "BSC", "BA","BBS", "B.Sc in Mechanical",
                   "B.Sc. in Architecture","M.Sc.","MBA","PhD","Other"]
        ev = {k: tk.StringVar() for k in ["degree","institution","year","notes"]}

        tk.Label(add_card,text="Degree *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=0,sticky="w",padx=8,pady=(10,2))
        ttk.Combobox(add_card,textvariable=ev["degree"],values=degrees,font=("Calibri",10)).grid(row=0,column=1,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Year *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=2,sticky="w",padx=8,pady=(10,2))
        tk.Entry(add_card,textvariable=ev["year"],font=("Calibri",10),width=10,relief="solid",bd=1,bg="#FAFAFA").grid(row=0,column=3,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Institution *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=1,column=0,sticky="w",padx=8,pady=4)
        tk.Entry(add_card,textvariable=ev["institution"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=1,column=1,columnspan=3,sticky="ew",padx=8,pady=4)
        tk.Label(add_card,text="Notes",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=2,column=0,sticky="w",padx=8,pady=4)
        tk.Entry(add_card,textvariable=ev["notes"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=2,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        def add_edu():
            if not ev["degree"].get().strip(): messagebox.showerror("Required","Degree is required"); return
            if not ev["institution"].get().strip(): messagebox.showerror("Required","Institution is required"); return
            entry = {k:ev[k].get().strip() for k in ev}
            self.data["education"].append(entry)
            save_data(self.data); self.show_education()

        tk.Button(add_card,text="  ➕ Add Education  ",command=add_edu,
                  font=("Calibri",11,"bold"),bg=TEAL,fg="white",
                  relief="flat",padx=12,pady=6,cursor="hand2").grid(row=3,column=0,columnspan=4,sticky="w",padx=8,pady=10)

        tk.Label(sf,text="  Existing Education Entries",font=("Calibri",12,"bold"),
                 bg=LIGHT_GREY,fg=NAVY).pack(anchor="w",padx=20,pady=(16,4))
        for i,edu in enumerate(self.data["education"]):
            self._list_card(sf, edu.get("degree",""), edu.get("institution",""),
                            edu.get("year",""), edu.get("notes",""), i, "education")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: SKILLS
    # ══════════════════════════════════════════════════════════════════════════
    def show_skills(self):
        self._set_active_nav("skills")
        self._clear_content()
        self._section_title(self.content, "🛠 Skills")
        sf = self._scrollable(self.content)

        add_card = tk.LabelFrame(sf, text="  ➕  Add Skill  ",
                                  font=("Calibri",11,"bold"), bg=BG_WHITE, fg=NAVY, bd=2, relief="groove")
        add_card.pack(fill="x", padx=20, pady=(16,8))
        add_card.columnconfigure(1,weight=1); add_card.columnconfigure(3,weight=1)

        cats = ["PMC","COST & BUDGET","COMPUTER","LANGUAGE","OTHER"]
        levels = ["Expert","Advanced","Intermediate","Basic","Proficient"]
        ev = {k: tk.StringVar() for k in ["category","skill","level"]}
        ev["level"].set("Expert")

        tk.Label(add_card,text="Category *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=0,sticky="w",padx=8,pady=(10,2))
        ttk.Combobox(add_card,textvariable=ev["category"],values=cats,font=("Calibri",10)).grid(row=0,column=1,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Proficiency",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=2,sticky="w",padx=8,pady=(10,2))
        ttk.Combobox(add_card,textvariable=ev["level"],values=levels,font=("Calibri",10),state="readonly").grid(row=0,column=3,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Skill Name *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=1,column=0,sticky="w",padx=8,pady=4)
        tk.Entry(add_card,textvariable=ev["skill"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=1,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        def add_skill():
            if not ev["skill"].get().strip(): messagebox.showerror("Required","Skill name is required"); return
            entry = {"category":ev["category"].get().strip(),"skill":ev["skill"].get().strip(),"level":ev["level"].get().strip()}
            self.data["skills"].append(entry)
            save_data(self.data); self.show_skills()

        tk.Button(add_card,text="  ➕ Add Skill  ",command=add_skill,
                  font=("Calibri",11,"bold"),bg=NAVY,fg="white",
                  relief="flat",padx=12,pady=6,cursor="hand2").grid(row=2,column=0,columnspan=4,sticky="w",padx=8,pady=10)

        # Skills table
        tk.Label(sf,text="  Current Skills",font=("Calibri",12,"bold"),bg=LIGHT_GREY,fg=NAVY).pack(anchor="w",padx=20,pady=(16,4))
        tbl = tk.Frame(sf,bg=BG_WHITE,bd=1,relief="solid")
        tbl.pack(fill="x",padx=20,pady=4)
        for j,h in enumerate(["Category","Skill","Level","Action"]):
            tk.Label(tbl,text=h,font=("Calibri",9,"bold"),bg=NAVY,fg="white",
                     anchor="w",padx=8,pady=6).grid(row=0,column=j,sticky="ew")
        tbl.columnconfigure(1,weight=1)
        for i,sk in enumerate(self.data["skills"]):
            bg2 = BG_WHITE if i%2==0 else "#F8F9FA"
            tk.Label(tbl,text=sk.get("category",""),font=("Calibri",9),bg=bg2,anchor="w",padx=8,pady=5).grid(row=i+1,column=0,sticky="ew")
            tk.Label(tbl,text=sk.get("skill",""),font=("Calibri",9),bg=bg2,anchor="w",padx=8).grid(row=i+1,column=1,sticky="ew")
            lv = sk.get("level","")
            lv_color = {"Expert":GREEN,"Advanced":TEAL,"Intermediate":GOLD,"Basic":GREY_TEXT,"Proficient":DARK}.get(lv,DARK)
            tk.Label(tbl,text=lv,font=("Calibri",9,"bold"),bg=bg2,fg=lv_color,padx=8).grid(row=i+1,column=2,sticky="ew")
            def del_sk(i=i):
                self.data["skills"].pop(i); save_data(self.data); self.show_skills()
            tk.Button(tbl,text="✕",command=del_sk,font=("Calibri",9),
                      bg=bg2,fg=RED,relief="flat",cursor="hand2").grid(row=i+1,column=3,padx=4)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: TRAINING
    # ══════════════════════════════════════════════════════════════════════════
    def show_training(self):
        self._set_active_nav("training")
        self._clear_content()
        self._section_title(self.content, "📜 Professional Training")
        sf = self._scrollable(self.content)

        add_card = tk.LabelFrame(sf,text="  ➕  Add Training  ",font=("Calibri",11,"bold"),
                                  bg=BG_WHITE,fg=NAVY,bd=2,relief="groove")
        add_card.pack(fill="x",padx=20,pady=(16,8))
        add_card.columnconfigure(1,weight=1); add_card.columnconfigure(3,weight=1)

        ev = {k: tk.StringVar() for k in ["name","institute","trainer","year","location"]}
        for row3,(lbl,key,col) in enumerate([("Training Name *","name",0),("Year","year",2),
                                            ("Institute *","institute",0),("Trainer","trainer",2),
                                            ("Location / Notes","location",0)]):
            tk.Label(add_card,text=lbl,font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=row3,column=col,sticky="w",padx=8,pady=(8 if row3==0 else 4,2))
            span = 3 if key=="location" else 1
            tk.Entry(add_card,textvariable=ev[key],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=row3,column=col+1,columnspan=span,sticky="ew",padx=8,pady=(8 if row3==0 else 4,2))

        def add_train():
            if not ev["name"].get().strip(): messagebox.showerror("Required","Training name required"); return
            entry = {k:ev[k].get().strip() for k in ev}
            self.data["training"].append(entry)
            save_data(self.data); self.show_training()

        tk.Button(add_card,text="  ➕ Add Training  ",command=add_train,
                  font=("Calibri",11,"bold"),bg=GOLD,fg=DARK,
                  relief="flat",padx=12,pady=6,cursor="hand2").grid(row=5,column=0,columnspan=4,sticky="w",padx=8,pady=10)

        tk.Label(sf,text="  Current Training",font=("Calibri",12,"bold"),bg=LIGHT_GREY,fg=NAVY).pack(anchor="w",padx=20,pady=(16,4))
        for i,tr in enumerate(self.data["training"]):
            self._list_card(sf,tr.get("name",""),tr.get("institute",""),tr.get("year",""),
                            f"Trainer: {tr.get('trainer','')}  Location: {tr.get('location','')}",i,"training")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: CERTIFICATIONS
    # ══════════════════════════════════════════════════════════════════════════
    def show_certifications(self):
        self._set_active_nav("certifications")
        self._clear_content()
        self._section_title(self.content, "🏆 Certifications")
        sf = self._scrollable(self.content)

        add_card = tk.LabelFrame(sf,text="  ➕  Add Certification  ",font=("Calibri",11,"bold"),
                                  bg=BG_WHITE,fg=NAVY,bd=2,relief="groove")
        add_card.pack(fill="x",padx=20,pady=(16,8))
        add_card.columnconfigure(1,weight=1); add_card.columnconfigure(3,weight=1)

        ev = {k: tk.StringVar() for k in ["name","body","year","notes"]}
        tk.Label(add_card,text="Certification Name *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=0,sticky="w",padx=8,pady=(10,2))
        tk.Entry(add_card,textvariable=ev["name"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=0,column=1,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Year",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=0,column=2,sticky="w",padx=8,pady=(10,2))
        tk.Entry(add_card,textvariable=ev["year"],font=("Calibri",10),width=10,relief="solid",bd=1,bg="#FAFAFA").grid(row=0,column=3,sticky="ew",padx=8,pady=(10,2))
        tk.Label(add_card,text="Issuing Body *",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=1,column=0,sticky="w",padx=8,pady=4)
        tk.Entry(add_card,textvariable=ev["body"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=1,column=1,columnspan=3,sticky="ew",padx=8,pady=4)
        tk.Label(add_card,text="Notes",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=2,column=0,sticky="w",padx=8,pady=4)
        tk.Entry(add_card,textvariable=ev["notes"],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=2,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        def add_cert():
            if not ev["name"].get().strip(): messagebox.showerror("Required","Certification name required"); return
            entry = {k:ev[k].get().strip() for k in ev}
            self.data["certifications"].append(entry)
            save_data(self.data); self.show_certifications()

        tk.Button(add_card,text="  ➕ Add Certification  ",command=add_cert,
                  font=("Calibri",11,"bold"),bg=GOLD,fg=DARK,
                  relief="flat",padx=12,pady=6,cursor="hand2").grid(row=3,column=0,columnspan=4,sticky="w",padx=8,pady=10)

        tk.Label(sf,text="  Current Certifications",font=("Calibri",12,"bold"),bg=LIGHT_GREY,fg=NAVY).pack(anchor="w",padx=20,pady=(16,4))
        for i,ct in enumerate(self.data["certifications"]):
            self._list_card(sf,ct.get("name",""),ct.get("body",""),ct.get("year",""),ct.get("notes",""),i,"certifications")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE: PROJECTS
    # ══════════════════════════════════════════════════════════════════════════
    def show_projects(self):
        self._set_active_nav("projects")
        self._clear_content()
        self._section_title(self.content, "🏗 Projects")
        sf = self._scrollable(self.content)

        add_card = tk.LabelFrame(sf,text="  ➕  Add Project  ",font=("Calibri",11,"bold"),
                                  bg=BG_WHITE,fg=NAVY,bd=2,relief="groove")
        add_card.pack(fill="x",padx=20,pady=(16,8))
        add_card.columnconfigure(1,weight=1); add_card.columnconfigure(3,weight=1)

        ev = {k: tk.StringVar() for k in ["name","company","land","client","location","brief","designer","year"]}
        fields4 = [("Project Name *","name",0,0),("Year","year",0,2),
                   ("Company *","company",1,0),("Land Area","land",1,2),
                   ("Client","client",2,0),("Location","location",2,2),
                   ("Project Brief","brief",3,0),("Designed By","designer",3,2)]
        for lbl,key,row4,col4 in fields4:
            tk.Label(add_card,text=lbl,font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=row4,column=col4,sticky="w",padx=8,pady=(10 if row4==0 else 4,2))
            tk.Entry(add_card,textvariable=ev[key],font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA").grid(row=row4,column=col4+1,sticky="ew",padx=8,pady=(10 if row4==0 else 4,2))

        tk.Label(add_card,text="Duties",font=("Calibri",9,"bold"),bg=BG_WHITE,fg=NAVY).grid(row=4,column=0,sticky="nw",padx=8,pady=4)
        duties2 = tk.Text(add_card,height=3,font=("Calibri",10),relief="solid",bd=1,bg="#FAFAFA",wrap="word")
        duties2.grid(row=4,column=1,columnspan=3,sticky="ew",padx=8,pady=4)

        def add_proj():
            if not ev["name"].get().strip(): messagebox.showerror("Required","Project name required"); return
            entry = {k:ev[k].get().strip() for k in ev}
            entry["duties"] = duties2.get("1.0","end-1c").strip()
            self.data["projects"].append(entry)
            save_data(self.data); self.show_projects()

        tk.Button(add_card,text="  ➕ Add Project  ",command=add_proj,
                  font=("Calibri",11,"bold"),bg=TEAL,fg="white",
                  relief="flat",padx=12,pady=6,cursor="hand2").grid(row=5,column=0,columnspan=4,sticky="w",padx=8,pady=10)

        tk.Label(sf,text="  Current Projects",font=("Calibri",12,"bold"),bg=LIGHT_GREY,fg=NAVY).pack(anchor="w",padx=20,pady=(16,4))
        for i,pj in enumerate(self.data["projects"]):
            self._list_card(sf,pj.get("name",""),pj.get("company",""),pj.get("year",""),
                            f"{pj.get('client','')} | {pj.get('location','')} | {pj.get('brief','')}",i,"projects")

    # ── Generic list card ─────────────────────────────────────────────────────
    def _list_card(self, parent, title, sub, meta, detail, idx, section):
        card = tk.Frame(parent, bg=BG_WHITE, bd=1, relief="solid")
        card.pack(fill="x", padx=20, pady=3)
        hdr = tk.Frame(card, bg=TEAL)
        hdr.pack(fill="x")
        tk.Label(hdr,text=f"  {title}",font=("Calibri",10,"bold"),bg=TEAL,fg="white",pady=5).pack(side="left")
        tk.Label(hdr,text=f"{meta}  ",font=("Calibri",9),bg=TEAL,fg=LIGHT_GREY).pack(side="right")
        body = tk.Frame(card, bg=BG_WHITE)
        body.pack(fill="x", padx=12, pady=6)
        if sub: tk.Label(body,text=sub,font=("Calibri",9),bg=BG_WHITE,fg=DARK).pack(anchor="w")
        if detail: tk.Label(body,text=detail,font=("Calibri",8),bg=BG_WHITE,fg=GREY_TEXT,wraplength=700,justify="left").pack(anchor="w",pady=2)
        btn_row = tk.Frame(card, bg=BG_WHITE)
        btn_row.pack(anchor="e", padx=8, pady=4)
        def edit_item(i=idx, s=section):
            self._edit_entry(s, i)
        def del_item(i=idx, s=section):
            if messagebox.askyesno("Delete","Delete this entry?"):
                self.data[s].pop(i); save_data(self.data)
                getattr(self, f"show_{s}")()
        tk.Button(btn_row, text=" ✎ Edit ", command=edit_item,
                  font=("Calibri",8), bg=LIGHT_GREY, fg=TEAL,
                  relief="flat", cursor="hand2").pack(side="right", padx=4)
        tk.Button(btn_row, text=" 🗑 Delete ", command=del_item,
                  font=("Calibri",8),bg=LIGHT_GREY,fg=RED,
                  relief="flat",cursor="hand2").pack(side="right")

    # ══════════════════════════════════════════════════════════════════════════
    # PDF EXPORT
    # ══════════════════════════════════════════════════════════════════════════
    def export_pdf(self):
        if not HAS_PDF:
            messagebox.showerror("Missing Library",
                "reportlab is not installed.\nRun: pip install reportlab"); return

        fp = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"CV_{self.data['personal'].get('name','').replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            filetypes=[("PDF","*.pdf")],
            title="Save CV as PDF")
        if not fp: return

        try:
            generate_pdf(self.data, fp)
            messagebox.showinfo("PDF Exported", f"CV saved to:\n{fp}")
            # Try to open
            import subprocess, platform
            if platform.system() == "Windows": os.startfile(fp)
            elif platform.system() == "Darwin": subprocess.run(["open", fp])
            else: subprocess.run(["xdg-open", fp])
        except Exception as e:
            messagebox.showerror("Export Error", str(e))


# ══════════════════════════════════════════════════════════════════════════════
# PDF GENERATION  (matching original PDF layout)
# ══════════════════════════════════════════════════════════════════════════════
def generate_pdf(data, filepath):
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    
    # Register Calibri-like font using DejaVu Sans TTF files
    try:
        pdfmetrics.registerFont(TTFont('Calibri', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-Italic', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-BoldItalic', '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'))
    except Exception as e:
        # Fallback to standard fonts if TTF registration fails
        print(f"Warning: Could not register Calibri fonts: {e}")

    W, H = A4   # 210 x 297 mm
    c = rl_canvas.Canvas(filepath, pagesize=A4)

    # Colors - Remove all gold elements
    COL_NAVY     = colors.HexColor("#1B3A5C")
    COL_TEAL     = colors.HexColor("#2E86AB")
    COL_DARK     = colors.HexColor("#2C3E50")
    COL_GREY     = colors.HexColor("#7F8C8D")
    COL_TEXT     = colors.HexColor("#4A4A4A")
    COL_BG       = colors.HexColor("#DCE1E4")
    COL_WHITE    = colors.white

    # Layout - Two column design
    TOP_MARGIN = 15 * mm
    BOTTOM_MARGIN = 8 * mm   # reduced bottom margin

    MARGIN = TOP_MARGIN  # keep old references working
    LEFT_COL_X = MARGIN
    LEFT_COL_W = 65 * mm
    RIGHT_COL_X = LEFT_COL_X + LEFT_COL_W + 15 * mm
    RIGHT_COL_W = W - RIGHT_COL_X - MARGIN
    LINE_HEIGHT = 4.5 * mm

    page = 1
    def new_page():
        nonlocal y, page
        c.showPage()
        page += 1
        
        y = H - TOP_MARGIN
        c.setFillColor(COL_BG)
        c.rect(LEFT_COL_X - 20*mm, TOP_MARGIN - 20*mm ,
           LEFT_COL_W + 22*mm, H + 2*TOP_MARGIN,
               stroke=0, fill=1)
        
        
        y = H - 1.5*TOP_MARGIN
        c.setStrokeColor(COL_GREY)
        c.setLineWidth(1.25)
        c.line(LEFT_COL_X -20*mm, y, W , y)
        y -= LINE_HEIGHT * 1.2
        return y       
        
    def ensure_space(needed_space=30*mm):
        nonlocal y
        if y - needed_space < TOP_MARGIN:
            y = new_page()
        return y
    
    def draw_text_block(x, y, text, w, size=10, color=COL_TEXT, leading=5, align='left'):
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
        
        alignment = TA_LEFT
        if align == 'right':
            alignment = TA_RIGHT
        elif align == 'center':
            alignment = TA_CENTER
        elif align == 'justify':
            alignment = TA_JUSTIFY
            
        style = ParagraphStyle("t", fontName="Calibri", fontSize=size,
                               leading=leading, textColor=color, alignment=alignment)
        p = Paragraph(text.replace("\n","<br/>"), style)
        aw, ah = p.wrapOn(c, w, 999*mm)
        if y - ah < MARGIN:
            y = new_page()
        p.drawOn(c, x, y - ah)
        return y - ah - 2*mm
    
    def draw_text_block1(x, y, text, w, size=10, color=COL_TEXT, leading=5, align='left'):
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
        
        alignment = TA_LEFT
        if align == 'right':
            alignment = TA_RIGHT
        elif align == 'center':
            alignment = TA_CENTER
        elif align == 'justify':
            alignment = TA_JUSTIFY
            
        style = ParagraphStyle("t", fontName="Calibri-Bold", fontSize=size,
                               leading=leading, textColor=color, alignment=alignment)
        p = Paragraph(text.replace("\n","<br/>"), style)
        aw, ah = p.wrapOn(c, w, 999*mm)
        if y - ah < MARGIN:
            y = new_page()
        p.drawOn(c, x, y - ah)
        return y - ah - 2*mm

    # Start position
    y = H - TOP_MARGIN

    # Grey sidebar background
    c.setFillColor(COL_BG)
    c.rect(LEFT_COL_X - 20*mm, TOP_MARGIN - 20*mm ,
           LEFT_COL_W + 22*mm, H + 2*TOP_MARGIN,
           stroke=0, fill=1)

    # ── HEADER: Title only ───────────────────────────────────────────────────
  
    y = H - 1.5*TOP_MARGIN
    c.setStrokeColor(COL_GREY)
    c.setLineWidth(1.25)
    c.line(LEFT_COL_X -20*mm, y, W , y)
    y -= LINE_HEIGHT * 1.2

    # Photo area
    photo_path = data["personal"].get("photo","")
    if photo_path and os.path.exists(photo_path) and HAS_PIL:
        try:
            c.drawImage(photo_path, LEFT_COL_X + 5*mm, H - 75*mm,
                        width=LEFT_COL_W - 10*mm, height=50*mm,
                        preserveAspectRatio=True, mask="auto")
        except:
            pass
    else:
        c.setFillColor(colors.HexColor("#D0D4E0"))
        c.rect(LEFT_COL_X + 5*mm, H - 75*mm, LEFT_COL_W - 10*mm, 50*mm, fill=1, stroke=0)
        c.setFont("Calibri", 8); c.setFillColor(COL_GREY)
        c.drawCentredString(LEFT_COL_X + LEFT_COL_W/2 - 5*mm, H - 45*mm, "[ PHOTO ]")

    ensure_space(35*mm)
    # ── ABOUT ME Section ─────────────────────────────────────────────────────
    c.setFont("Calibri-Bold", 13)
    c.setFillColor(COL_NAVY)
    c.drawString(RIGHT_COL_X - 10*mm, y, "ABOUT ME")
    y -= LINE_HEIGHT * 1.5

    # Name under About Me (as requested)
    c.setFont("Calibri-Bold", 15)
    c.setFillColor(COL_DARK)
    c.drawString(RIGHT_COL_X - 10*mm, y, data["personal"].get("name",""))
    y -= LINE_HEIGHT * 1.2

    # About text
    y = draw_text_block(RIGHT_COL_X - 10*mm, y, data["personal"].get("about",""), 
                       RIGHT_COL_W + 15*mm, size=9, leading=12, align='justify')
    y -= LINE_HEIGHT 

    ensure_space(25*mm)
    # ── PERSONAL INFORMATION (Two Column Layout) ────────────────────────────
    c.setFont("Calibri-Bold", 11)
    c.setFillColor(COL_GREY)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "PERSONAL INFORMATION")
    y -= LINE_HEIGHT * 1.2
    
    
    # Left column - Labels in grey sidebar
    
    left_y = y
    labels = ["Date of Birth", "Nationality", "National ID", "Email", "Phone", "Address"]
    for label in labels:
        c.setFont("Calibri", 10)
        c.setFillColor(COL_DARK)
        c.drawRightString(LEFT_COL_X + 65*mm, left_y, label + ":")
        left_y -= LINE_HEIGHT * 1.25
        
    
    # Right column - Values
    
    right_y = y
    values = [
        data["personal"].get("dob",""),
        data["personal"].get("nationality",""),
        data["personal"].get("nid",""),
        data["personal"].get("email",""),
        data["personal"].get("phone",""),
        
    ]
    
    for value in values:
        c.setFont("Calibri", 10)
        c.setFillColor(COL_DARK)
        c.drawString(RIGHT_COL_X - 10*mm, right_y, str(value))
        right_y -= LINE_HEIGHT *1.25

        # Handle address separately with line breaks
    address = data["personal"].get("address","")
    for line in address.split("\n"):
        c.setFont("Calibri", 10)
        c.setFillColor(COL_DARK)
        c.drawString(RIGHT_COL_X - 10*mm, right_y, line)
        right_y -= LINE_HEIGHT * 1


    y = min(left_y, right_y) - LINE_HEIGHT * .5

    
    # ── EDUCATION (Two Column Layout) ───────────────────────────────────────
    c.setFont("Calibri-Bold", 11)
    c.setFillColor(COL_GREY)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "EDUCATIONAL QUALIFICATION")
    y -= LINE_HEIGHT * -.2

    for edu in data["education"]:
      

      # Degree name on left sidebar
      y -= LINE_HEIGHT * 1.5
      c.setFont("Calibri", 10)
      c.setFillColor(COL_DARK)
      c.drawRightString(LEFT_COL_X + 65*mm, y, edu.get("degree",""))

      # Institution on the same vertical level (right column)
      y -= LINE_HEIGHT * -1
      c.setFont("Calibri", 10)
      c.setFillColor(COL_TEXT)
      # Draw institution at same y, don’t update y yet
      draw_text_block(RIGHT_COL_X - 10*mm, y, edu.get("institution",""), RIGHT_COL_W, size=11, leading=11)

      # Now move down for year
      y -= LINE_HEIGHT * 2
      c.setFont("Calibri", 9)
      c.setFillColor(COL_GREY)
      c.drawString(RIGHT_COL_X - 10*mm, y, "Year: " + str(edu.get("year","")))

      # Extra spacing before next entry
    y -= LINE_HEIGHT 

    # ── TRAINING ────────────────────────────────────────────────────────────
    if data["training"]:
        ensure_space(25*mm)
        y -= LINE_HEIGHT * 0.5
        c.setFont("Calibri-Bold", 11)
        c.setFillColor(COL_GREY)
        c.drawRightString(LEFT_COL_X + 65*mm, y, "TRAINING")
        y -= LINE_HEIGHT * 1.5

        for tr in data["training"]:
            ensure_space(15*mm)
            c.setFont("Calibri-Bold", 10)
            c.setFillColor(COL_GREY)
            c.drawRightString(LEFT_COL_X + 65*mm, y, tr.get("name",""))
            
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_GREY)
            c.drawString(RIGHT_COL_X - 10*mm, y, tr.get("institute",""))
            y -= LINE_HEIGHT 

            ensure_space(15*mm)
            c.setFont("Calibri", 10)
            c.setFillColor(COL_GREY)
            c.drawRightString(LEFT_COL_X + 65*mm, y, "Trainer")
            
            
            c.setFont("Calibri-Bold", 9)
            c.setFillColor(COL_GREY)
            c.drawString(RIGHT_COL_X - 10*mm, y, tr.get("trainer",""))
            y -= LINE_HEIGHT * 1.5
    y -= LINE_HEIGHT * 0.5
    # ── CERTIFICATIONS ──────────────────────────────────────────────────────
    if data["certifications"]:
        ensure_space(25*mm)
        y -= LINE_HEIGHT * 0.5
        c.setFont("Calibri-Bold", 11)
        c.setFillColor(COL_NAVY)
        c.drawRightString(LEFT_COL_X + 65*mm, y, "CERTIFICATIONS")
        y -= LINE_HEIGHT * 1.2

        for cert in data["certifications"]:
            ensure_space(20*mm)
            c.setFont("Calibri-Bold", 10)
            c.setFillColor(COL_DARK)
            c.drawString(RIGHT_COL_X, y, cert.get("name",""))
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_GREY)
            c.drawRightString(W - MARGIN, y, str(cert.get("year","")))
            y -= LINE_HEIGHT * 0.8
            
            if cert.get("body"):
                c.setFont("Calibri", 9)
                c.setFillColor(COL_TEXT)
                c.drawString(RIGHT_COL_X - 10*mm, y, cert.get("body",""))
                y -= LINE_HEIGHT

    # ── SKILLS ──────────────────────────────────────────────────────────────
    if data["skills"]:
     ensure_space(25*mm)
    c.setFont("Calibri-Bold", 11)
    c.setFillColor(COL_GREY)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "SKILLS & SPECIALIZATION")
    

    current_cat = ""
    for sk in data["skills"]:
        ensure_space(20*mm)
        cat = sk.get("category","")

        if cat != current_cat:
            current_cat = cat
            # Extra spacing before new category
            y -= LINE_HEIGHT * 1.3
            # Draw category on the left
            c.setFont("Calibri-Bold", 10)
            c.setFillColor(COL_GREY)
            c.drawRightString(LEFT_COL_X + 65*mm, y, cat.upper())

            # Draw first skill on the same line (right side)
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            c.drawString(RIGHT_COL_X - 10*mm, y, "• " + sk.get("skill",""))

        else:
            # Normal spacing for subsequent skills
            y -= LINE_HEIGHT * 1.2
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            c.drawString(RIGHT_COL_X - 10*mm, y, "• " + sk.get("skill",""))

    y -= LINE_HEIGHT
            


    ensure_space(35*mm)
    # ── PROFESSIONAL EXPERIENCE ─────────────────────────────────────────────
    c.setFont("Calibri-Bold", 11)
    c.setFillColor(COL_DARK)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "PROFESSIONAL EXPERIENCE")
    y -= LINE_HEIGHT * 1.2




    for exp in data["experience"]:
        company = exp.get("company","")
        
        # Save starting y
        y_start = y

        # Draw company block (handles wrapping/splitting)
        y_after = draw_text_block1(
        LEFT_COL_X, y, company,
        w=65*mm, size=10, color=COL_GREY,
        leading=LINE_HEIGHT, align='right'
        )

        # If company consumed only one line, keep title aligned on same baseline
        if abs(y_start - y_after) <= LINE_HEIGHT :
            y_title = y_start   # same line as first company line
        else:
            y_title = y_after   # below multi-line company
    
        ensure_space(30*mm)
        
                # Job title
        y -= LINE_HEIGHT * .8
        c.setFont("Calibri-Bold", 10)
        c.setFillColor(COL_TEXT)
        c.drawString(RIGHT_COL_X - 10*mm, y, exp.get("title",""))
        y -= LINE_HEIGHT * 1.7
        

        c.setFont("Calibri", 10)
        c.setFillColor(COL_GREY)
        c.drawRightString(LEFT_COL_X + 65*mm, y, exp.get("period",""))
        y -= LINE_HEIGHT * 1.2
        
        
        # Duties
        if exp.get("duties"):
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y, "Responsibility:")
            y -= LINE_HEIGHT * -.7
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y, exp["duties"], 
                               RIGHT_COL_W , size=10, leading=12)
        y -= LINE_HEIGHT 
        # Projects
        if exp.get("projects"):
            c.setFont("Calibri-Bold", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y, "Projects:")
            y -= LINE_HEIGHT * -.7
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y, exp["projects"], 
                               RIGHT_COL_W , size=10, leading=12)
        
        y -= LINE_HEIGHT

        ensure_space(35*mm)
    # ── Projects ─────────────────────────────────────────────
    c.setFont("Calibri-Bold", 11)
    c.setFillColor(COL_DARK)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "PROJECTS")
    y -= LINE_HEIGHT * .5

    for pj in data["projects"]:
        name = pj.get("name","")
        company = pj.get("company","")
        
        
        # Calculate space needed for this project
        project_height = LINE_HEIGHT * 5  # header + spacing
        if pj.get("land"): project_height += LINE_HEIGHT 
        if pj.get("client"): project_height += LINE_HEIGHT 
        if pj.get("location"): project_height += LINE_HEIGHT 
        if pj.get("brief"): project_height += LINE_HEIGHT 
        if pj.get("designer"): project_height += LINE_HEIGHT 
        
        # Check if we need to start a new page
        if y - project_height < TOP_MARGIN:
            y = new_page()
        
        # Save starting y
        y_start = y

        # Draw project name block (handles wrapping/splitting)
        y_after = draw_text_block1(
            LEFT_COL_X, y, name,
            w=65*mm, size=10, color=COL_GREY,
            leading=9, align='right'
        )

        # Always align company on the same baseline as the first line of project name
        y_company = y_start

        # Company and period on the same line
        c.setFont("Calibri-Bold", 10)
        c.setFillColor(COL_TEXT)
        c.drawString(RIGHT_COL_X - 10*mm, y_company + LINE_HEIGHT * -.9, company)
        
        y -= LINE_HEIGHT * 1.45

        # Land Area
        if pj.get("land"):
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y - LINE_HEIGHT * .8, "Land Area:")
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y - LINE_HEIGHT *.2, pj["land"], 
                               RIGHT_COL_W , size=10, leading=12)

        # Client
        if pj.get("client"):
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y - LINE_HEIGHT * .8, "Client:")
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y - LINE_HEIGHT *.2, pj["client"], 
                               RIGHT_COL_W , size=10, leading=12)
        
        # Location
        if pj.get("location"):
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y - LINE_HEIGHT * .8, "Location:")
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y - LINE_HEIGHT *.2, pj["location"], 
                               RIGHT_COL_W , size=10, leading=12)

        # Project brief
        if pj.get("brief"):
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y - LINE_HEIGHT * .8, "Project Brief:")
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y - LINE_HEIGHT *.2, pj["brief"], 
                               RIGHT_COL_W , size=10, leading=12)
        
        # Designer
        if pj.get("designer"):
            c.setFont("Calibri-Bold", 9)
            c.setFillColor(COL_TEAL)
            c.drawRightString(LEFT_COL_X + 65*mm, y - LINE_HEIGHT * .8, "Designed By:")
            
            c.setFont("Calibri", 9)
            c.setFillColor(COL_TEXT)
            y = draw_text_block(RIGHT_COL_X - 10*mm, y - LINE_HEIGHT *.2, pj["designer"], 
                               RIGHT_COL_W , size=10, leading=12)

        y -= LINE_HEIGHT * .3
            

    # ── WORK UNDERTAKEN ──────────────────────────────────────────────────────
    if data["personal"].get("summary"):
        summary_text = data["personal"].get("summary","")

    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY

    summary_style = ParagraphStyle(
        "sum",
        fontName="Calibri",
        fontSize=10,
        leading=12,
        textColor=COL_TEXT,
        alignment=TA_JUSTIFY
    )

    p_sum = Paragraph(summary_text.replace("\n","<br/>"), summary_style)
    aw_sum, ah_sum = p_sum.wrapOn(c, RIGHT_COL_W + 10*mm, 999*mm)

    ensure_space(ah_sum + LINE_HEIGHT)

    # First heading line + summary aligned
    c.setFont("Calibri-Bold", 10)
    c.setFillColor(COL_NAVY)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "WORK UNDERTAKEN")
    p_sum.drawOn(c, RIGHT_COL_X - 10*mm, y - ah_sum + LINE_HEIGHT * 0.8)

    # Move down for the other heading lines
    y -= LINE_HEIGHT * 1.25
    c.drawRightString(LEFT_COL_X + 65*mm, y, "THAT BEST ILLUSTRATES YOUR")
    y -= LINE_HEIGHT * 1.25
    c.drawRightString(LEFT_COL_X + 65*mm, y, "CAPABILITY")

    # Update y after summary block
    y = y - ah_sum - LINE_HEIGHT

        
    # ── DECLARATION ─────────────────────────────────────────────────────────
    declaration = ("I, the undersigned, certify that, to the best of my knowledge and belief, "
                   "this curriculum vitae correctly describes me, my qualifications, and my experience. "
                   "I understand that willful misstatement described herein may lead to my disqualification "
                   "or dismissal, if engaged.")
    decl_style = ParagraphStyle("decl", fontName="Calibri", fontSize=9,
                                leading=12, textColor=COL_TEXT, alignment=TA_JUSTIFY)
    p_decl = Paragraph(declaration.replace("\n","<br/>"), decl_style)
    aw_decl, ah_decl = p_decl.wrapOn(c, RIGHT_COL_W + 10*mm, 999*mm)
    ensure_space(ah_decl + LINE_HEIGHT * 1)
    y -= LINE_HEIGHT 
    c.setFont("Calibri-Bold", 10)
    c.setFillColor(COL_NAVY)
    c.drawRightString(LEFT_COL_X + 65*mm, y, "CERTIFICATION")
    y -= LINE_HEIGHT * -.8
    p_decl.drawOn(c, RIGHT_COL_X - 10*mm, y - ah_decl)
    y = y - ah_decl - LINE_HEIGHT * 1.2
    
    # Signature section
    y -= LINE_HEIGHT * 8
    c.setFont("Calibri", 10)
    c.setFillColor(COL_TEXT)
    c.drawString(RIGHT_COL_X, y, "Signature:")
    c.drawString(RIGHT_COL_X + 40*mm, y, "________________________")
    y -= LINE_HEIGHT
    
    c.drawString(RIGHT_COL_X, y, "Date:")
    c.drawString(RIGHT_COL_X + 40*mm, y, datetime.now().strftime("%d / %m / %Y"))
    y -= LINE_HEIGHT
    
    c.drawString(RIGHT_COL_X, y, "Name:")
    c.drawString(RIGHT_COL_X + 40*mm, y, data["personal"].get("name",""))
    
    

    c.save()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = CVApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
