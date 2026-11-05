from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "dropguard.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "DropGuard — Student Dropout Risk Predictor", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that flags students at risk of dropping out early, so support can reach them in time"])
add(1, "The Problem", ["Some students quietly fall behind — low attendance, backlogs and fee pressure pile up", "By the time a dropout happens, it is often too late to help", "Colleges spot trouble late because warning signs sit in separate records", "An early, simple risk score lets mentors act before a student gives up"])
add(2, "The Solution — DropGuard", ["Enter a student's profile: attendance, GPA, assignments, backlogs, study and work hours, fee stress", "A trained model returns a dropout-risk percentage and a risk level", "Below 25% looks low risk, 25–50% medium risk, above 50% high risk", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset and model training", "Logistic regression (C = 1.0) on standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 900 synthetic student records (seed 42), 7 features", "Inputs -> standardisation (training mean and standard deviation) -> logistic regression -> model.json", "model.json ships with the site; JavaScript applies the same formula and a sigmoid", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter a student profile and press Check Dropout Risk", "Average student: 78% attendance, 7.2 GPA, 70% assignments, 1 backlog -> about 30.51% risk (medium)", "At-risk student: 55% attendance, 5.0 GPA, 30% assignments, 4 backlogs, fee stress -> about 99.83% risk (high)", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation accuracy: 73.4%", "AUC: 0.80 — the model ranks at-risk students well above on-track ones", "Baseline (always guessing continuing): 61.1% accuracy", "Browser demo matches Python predictions exactly on all test samples"])
add(7, "Future Scope", ["Train on real, anonymised college records with permission", "Add features like hostel distance, health and mentorship history", "Add a mentor dashboard that lists high-risk students for follow-up", "Add explanations: which factor pushed the risk score up most"])
add(8, "Thank You", ["DropGuard — Student Dropout Risk Predictor", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/dropguard", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_DropGuard_2026-11-05.pptx")
print("slides:", len(prs.slides._sldIdLst))
