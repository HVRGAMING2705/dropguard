import json
m = json.load(open("model.json"))
means, stds, coef, icpt = m["means"], m["stds"], m["coef"], m["intercept"]
mt = m["metrics"]
acc, auc, base, dr = mt["cv_accuracy"], mt["cv_auc"], mt["baseline_accuracy"], mt["dropout_rate"]
DOMAIN = "dropguard.vercel.app"
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DropGuard — Student Dropout Risk Predictor | AI/ML Project</title>
<meta name="description" content="DropGuard estimates a student's dropout risk from attendance, GPA, assignment completion, backlogs, study hours, part-time work hours and fee stress, using a logistic regression model trained on 900 synthetic student records.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="DropGuard — Student Dropout Risk Predictor">
<meta property="og:description" content="Enter a student's profile and instantly get a dropout-risk score, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="DropGuard — Student Dropout Risk Predictor">
<meta name="twitter:description" content="Logistic regression dropout-risk predictor. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"DropGuard","applicationCategory":"EducationalApplication","description":"Student dropout risk predictor using logistic regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input,select{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:20px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:2em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
</style>
</head>
<body>
<h1>&#127891; DropGuard — Student Dropout Risk Predictor</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A logistic regression model trained on 900 synthetic student records estimates dropout risk from attendance, previous GPA, assignment completion, backlogs, study hours, part-time work hours and fee stress. 5-fold CV: <b>accuracy = {acc:.1%}</b>, AUC = {auc:.2f} vs an always-continuing baseline of {base:.1%}.</p>
<label>Attendance (%)</label><input id="att" type="number" value="78" min="40" max="100">
<label>Previous GPA (0–10)</label><input id="gpa" type="number" value="7.2" min="4" max="10" step="0.1">
<label>Assignments completed (%)</label><input id="assign" type="number" value="70" min="20" max="100">
<label>Backlogs (subjects)</label><input id="backlogs" type="number" value="1" min="0" max="5">
<label>Study hours per week</label><input id="study" type="number" value="12" min="0" max="35">
<label>Part-time work hours per week</label><input id="parttime" type="number" value="5" min="0" max="25">
<label>Fee / financial stress?</label><select id="fee"><option value="0" selected>No</option><option value="1">Yes</option></select>
<button onclick="predict()">Check Dropout Risk</button>
<button onclick="tryRisky()">Try an at-risk profile</button>
<div id="result"></div>
<p class="note">How it works: the inputs are standardised with the training means and standard deviations, multiplied by the model&apos;s learned coefficients and passed through a sigmoid. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try a sample: an average student — 78% attendance, 7.2 GPA, 70% assignments, 1 backlog, 12 study hours &rarr; about 30.51% dropout risk. An at-risk one — 55% attendance, 5.0 GPA, 30% assignments, 4 backlogs, 3 study hours, 20 part-time hours, fee stress &rarr; about 99.83% dropout risk. A strong student — 95% attendance, 9.0 GPA, 95% assignments, no backlogs, 25 study hours &rarr; about 0.62% risk.</p>
<p class="note">This is a classroom demo on synthetic data, to flag students who may need support early — not a real academic decision.</p>
<p><a href="https://github.com/HVRGAMING2705/dropguard">View source on GitHub</a></p>
<script>
const MEANS = {json.dumps(means)};
const STDS = {json.dumps(stds)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function calc(){{
  const v = [parseFloat(document.getElementById("att").value), parseFloat(document.getElementById("gpa").value), parseFloat(document.getElementById("assign").value), parseFloat(document.getElementById("backlogs").value), parseFloat(document.getElementById("study").value), parseFloat(document.getElementById("parttime").value), parseFloat(document.getElementById("fee").value)];
  let z = INTERCEPT;
  for (let j = 0; j < 7; j++) z += ((v[j]-MEANS[j])/STDS[j]) * COEF[j];
  return 1/(1+Math.exp(-z)) * 100;
}}
function show(p){{
  const verdict = p >= 50 ? "&#9888; HIGH RISK — this student may need support soon: mentoring, attendance follow-up and fee help." : (p >= 25 ? "&#9888; MEDIUM RISK — worth a check-in before small problems grow." : "&#9989; LOW RISK — looks on track to continue.");
  const el = document.getElementById("result");
  el.style.display = "block";
  el.innerHTML = "<b>" + p.toFixed(2) + "% dropout risk</b><br>" + verdict;
}}
function predict(){{ show(calc()); }}
function tryRisky(){{
  document.getElementById("att").value = 55; document.getElementById("gpa").value = 5.0; document.getElementById("assign").value = 30; document.getElementById("backlogs").value = 4; document.getElementById("study").value = 3; document.getElementById("parttime").value = 20; document.getElementById("fee").value = 1; show(calc());
}}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — DropGuard</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on DropGuard.</p><p><a href="https://{DOMAIN}/">Back to DropGuard</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>\n""")
open("README.md", "w").write(f"""# DropGuard — Student Dropout Risk Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — attendance %, previous GPA, assignments completed %, backlogs, study hours/week, part-time work hours/week, fee stress — trained on 900 synthetic student records (seed 42).

- 5-fold CV accuracy: {acc:.1%}, AUC: {auc:.2f} (always-continuing baseline: {base:.1%})
- Dropout rate in training data: {dr:.1%}
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
""")
print("site files written, acc", acc, "auc", auc)
