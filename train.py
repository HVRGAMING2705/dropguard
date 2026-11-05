import json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score

rng = np.random.default_rng(42)
n = 900
att = np.clip(rng.normal(78, 12, n), 40, 100)
gpa = np.clip(rng.normal(7.4, 1.3, n), 4.0, 10.0)
assign = np.clip(rng.normal(72, 18, n), 20, 100)
backlogs = rng.choice([0, 1, 2, 3, 4, 5], n, p=[0.45, 0.25, 0.15, 0.08, 0.04, 0.03]).astype(float)
study = np.clip(rng.normal(12, 6, n), 0, 35)
parttime = np.clip(rng.exponential(5, n), 0, 25)
fee = rng.binomial(1, 0.30, n).astype(float)
logit = (-1.6 - 0.06*(att-75) - 0.65*(gpa-7) - 0.025*(assign-70)
         + 0.7*backlogs - 0.08*(study-12) + 0.07*parttime + 1.0*fee
         + rng.normal(0, 0.4, n))
p = 1/(1+np.exp(-logit))
y = (rng.random(n) < p).astype(int)
X = np.column_stack([att, gpa, assign, backlogs, study, parttime, fee]).astype(float)
names = ["attendance_pct", "prev_gpa", "assignments_pct", "backlogs", "study_hours_week", "parttime_hours_week", "fee_stress"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu) / sd
model = LogisticRegression(C=1.0, max_iter=1000).fit(Xs, y)
skf = StratifiedKFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=1000), Xs, y, cv=skf)
proba_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=1000), Xs, y, cv=skf, method="predict_proba")[:, 1]
acc = float(accuracy_score(y, pred_cv)); auc = float(roc_auc_score(y, proba_cv))
base = float(max(y.mean(), 1-y.mean()))
print(f"CV accuracy={acc:.3f} AUC={auc:.3f} baseline={base:.3f} dropout_rate={y.mean():.3f} n={n}")
print("coef", model.coef_, "intercept", model.intercept_)
mj = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
      "coef": model.coef_[0].tolist(), "intercept": float(model.intercept_[0]),
      "metrics": {"cv_accuracy": acc, "cv_auc": auc, "baseline_accuracy": base, "dropout_rate": float(y.mean()), "n": n}}
with open("model.json", "w") as f: json.dump(mj, f, indent=1)

def predict_raw(*v):
    v = np.array(v, dtype=float)
    z = (v - mu) / sd
    lg = float(model.intercept_[0] + z @ model.coef_[0])
    return 1/(1+np.exp(-lg))
samples = [[95, 9.0, 95, 0, 25, 0, 0], [55, 5.0, 30, 4, 3, 20, 1],
           [78, 7.2, 70, 1, 12, 5, 0], [68, 6.5, 55, 2, 8, 12, 1],
           [88, 8.0, 85, 0, 15, 0, 1]]
for s in samples: print(s, round(predict_raw(*s)*100, 2), "%")
with open("parity_samples.json", "w") as f:
    json.dump([{"inputs": s, "prob_dropout_pct": predict_raw(*s)*100} for s in samples], f, indent=1)
