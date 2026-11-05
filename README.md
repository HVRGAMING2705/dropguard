# DropGuard — Student Dropout Risk Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — attendance %, previous GPA, assignments completed %, backlogs, study hours/week, part-time work hours/week, fee stress — trained on 900 synthetic student records (seed 42).

- 5-fold CV accuracy: 73.4%, AUC: 0.80 (always-continuing baseline: 61.1%)
- Dropout rate in training data: 38.9%
- Live demo: https://dropguard.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
