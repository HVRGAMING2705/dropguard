// Node parity check: mirrors index.html calc() using model.json weights.
const fs = require("fs");
const m = JSON.parse(fs.readFileSync("model.json", "utf8"));
const samples = JSON.parse(fs.readFileSync("parity_samples.json", "utf8"));
let maxDiff = 0;
for (const s of samples) {
  let z = m.intercept;
  for (let j = 0; j < 7; j++) z += ((s.inputs[j] - m.means[j]) / m.stds[j]) * m.coef[j];
  const p = 1 / (1 + Math.exp(-z)) * 100;
  const diff = Math.abs(p - s.prob_dropout_pct);
  maxDiff = Math.max(maxDiff, diff);
  console.log(JSON.stringify(s.inputs), p.toFixed(2), "vs python", s.prob_dropout_pct.toFixed(2), "diff", diff.toFixed(6));
}
console.log("max diff:", maxDiff, maxDiff < 0.01 ? "PASS" : "FAIL");
