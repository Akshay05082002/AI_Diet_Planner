# ============================================================
#  MODEL ACCURACY — TRAIN + CHART
#  Dataset : Iris (built-in, no download needed)
#  Models  : Logistic Regression, Random Forest, SVM, KNN, Decision Tree
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

# ─────────────────────────────────────────────
#  1. LOAD & SPLIT DATA
# ─────────────────────────────────────────────
print("=" * 55)
print("  LOADING IRIS DATASET")
print("=" * 55)

iris   = load_iris()
X, y   = iris.data, iris.target
labels = iris.target_names          # ['setosa', 'versicolor', 'virginica']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Scale features (important for SVM / KNN / LR)
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

print(f"  Total samples : {len(X)}")
print(f"  Training set  : {len(X_train)}")
print(f"  Test set      : {len(X_test)}")
print(f"  Classes       : {list(labels)}\n")

# ─────────────────────────────────────────────
#  2. DEFINE MODELS
# ─────────────────────────────────────────────
models = {
    "Logistic Reg":    LogisticRegression(max_iter=300, random_state=42),
    "Random Forest":   RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM":             SVC(kernel="rbf", probability=True, random_state=42),
    "KNN":             KNeighborsClassifier(n_neighbors=5),
    "Decision Tree":   DecisionTreeClassifier(max_depth=5, random_state=42),
}

COLORS = {
    "Logistic Reg":  "#00d4ff",
    "Random Forest": "#10b981",
    "SVM":           "#a855f7",
    "KNN":           "#f59e0b",
    "Decision Tree": "#f43f5e",
}

# ─────────────────────────────────────────────
#  3. TRAIN & COLLECT METRICS
# ─────────────────────────────────────────────
results   = {}   # final metric scores
cv_scores = {}   # cross-validation accuracy per fold
lc_data   = {}   # learning curve data

print("=" * 55)
print("  TRAINING MODELS")
print("=" * 55)

for name, model in models.items():
    # --- train ---
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # --- metrics ---
    acc  = accuracy_score(y_test, y_pred) * 100
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0) * 100
    rec  = recall_score(y_test, y_pred, average="weighted", zero_division=0) * 100
    f1   = f1_score(y_test, y_pred, average="weighted", zero_division=0) * 100
    cm   = confusion_matrix(y_test, y_pred)

    results[name] = {
        "Accuracy":  acc,
        "Precision": prec,
        "Recall":    rec,
        "F1 Score":  f1,
        "CM":        cm,
    }

    # --- 5-fold cross-validation ---
    cv = cross_val_score(model, np.vstack([X_train, X_test]),
                         np.concatenate([y_train, y_test]),
                         cv=5, scoring="accuracy") * 100
    cv_scores[name] = cv

    # --- learning curve (train-size vs accuracy) ---
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train, y_train,
        train_sizes=np.linspace(0.2, 1.0, 8),
        cv=5, scoring="accuracy", n_jobs=-1
    )
    lc_data[name] = {
        "sizes":  train_sizes,
        "train":  train_scores.mean(axis=1) * 100,
        "val":    val_scores.mean(axis=1) * 100,
    }

    print(f"  ✓  {name:<16}  Acc={acc:.1f}%  F1={f1:.1f}%  CV={cv.mean():.1f}±{cv.std():.1f}%")

print()

# ─────────────────────────────────────────────
#  4. PRINT BEST MODEL REPORT
# ─────────────────────────────────────────────
best_name = max(results, key=lambda n: results[n]["Accuracy"])
best_model = models[best_name]
print("=" * 55)
print(f"  BEST MODEL → {best_name}  ({results[best_name]['Accuracy']:.1f}%)")
print("=" * 55)
print(classification_report(
    y_test, best_model.predict(X_test),
    target_names=labels
))

# ─────────────────────────────────────────────
#  5. PLOT DASHBOARD
# ─────────────────────────────────────────────
DARK   = "#08081a"
PANEL  = "#0f0f22"
GRID   = "#1e1e38"
TICK   = "#6b6b9b"
LABEL  = "#9898c0"
WHITE  = "#e8e8f8"

def style(ax, title=""):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_edgecolor(GRID)
    ax.tick_params(colors=TICK, labelsize=8)
    ax.yaxis.label.set_color(LABEL)
    ax.xaxis.label.set_color(LABEL)
    ax.grid(color=GRID, linewidth=0.6, linestyle="--")
    if title:
        ax.set_title(title, color=WHITE, fontsize=11,
                     fontweight="bold", pad=10)

fig = plt.figure(figsize=(20, 14), facecolor=DARK)
fig.suptitle(
    "MODEL ACCURACY DASHBOARD  —  Iris Dataset",
    color="white", fontsize=20, fontweight="bold",
    fontfamily="monospace", y=0.97,
)

gs = gridspec.GridSpec(
    2, 3, figure=fig,
    hspace=0.45, wspace=0.35,
    left=0.06, right=0.97, top=0.91, bottom=0.07,
)

model_names = list(results.keys())
clrs        = [COLORS[n] for n in model_names]

# ── Panel A : Final Accuracy (horizontal bar) ─────────────────────────────
ax_a = fig.add_subplot(gs[0, 0])
style(ax_a, "Final Test Accuracy (%)")

accs = [results[n]["Accuracy"] for n in model_names]
bars = ax_a.barh(model_names, accs, color=clrs, height=0.55, edgecolor="none")
for bar, val, name in zip(bars, accs, model_names):
    ax_a.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
              f"{val:.1f}%", va="center", color=COLORS[name],
              fontsize=9, fontweight="bold")
    if name == best_name:
        bar.set_edgecolor("white")
        bar.set_linewidth(1.3)

ax_a.set_xlim(70, 105)
ax_a.set_xlabel("Accuracy (%)", fontsize=9)
ax_a.tick_params(axis="y", labelcolor=WHITE, labelsize=9)

# ── Panel B : Multi-Metric Grouped Bar ────────────────────────────────────
ax_b = fig.add_subplot(gs[0, 1])
style(ax_b, "Metrics Comparison")

metric_keys  = ["Accuracy", "Precision", "Recall", "F1 Score"]
metric_clrs  = ["#00d4ff", "#a855f7", "#f59e0b", "#10b981"]
x   = np.arange(len(model_names))
w   = 0.18
off = np.linspace(-(len(metric_keys)-1)/2,
                  (len(metric_keys)-1)/2,
                  len(metric_keys)) * w

for i, (metric, mc) in enumerate(zip(metric_keys, metric_clrs)):
    vals = [results[n][metric] for n in model_names]
    ax_b.bar(x + off[i], vals, width=w, color=mc,
             label=metric, alpha=0.85, edgecolor="none")

ax_b.set_xticks(x)
ax_b.set_xticklabels(
    [n.replace(" ", "\n") for n in model_names],
    color=WHITE, fontsize=8
)
ax_b.set_ylim(70, 105)
ax_b.set_ylabel("Score (%)", fontsize=9)
ax_b.legend(framealpha=0, labelcolor=metric_clrs,
            fontsize=8, loc="lower right", ncol=2)

# ── Panel C : Cross-Validation Box Plot ───────────────────────────────────
ax_c = fig.add_subplot(gs[0, 2])
style(ax_c, "5-Fold Cross-Validation")

cv_values = [cv_scores[n] for n in model_names]
bp = ax_c.boxplot(
    cv_values,
    patch_artist=True,
    medianprops=dict(color="white", linewidth=2),
    whiskerprops=dict(color=TICK),
    capprops=dict(color=TICK),
    flierprops=dict(marker="o", color=TICK, markersize=4),
)
for patch, color in zip(bp["boxes"], clrs):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax_c.set_xticks(range(1, len(model_names) + 1))
ax_c.set_xticklabels(
    [n.replace(" ", "\n") for n in model_names],
    color=WHITE, fontsize=8
)
ax_c.set_ylabel("CV Accuracy (%)", fontsize=9)
ax_c.set_ylim(70, 105)

# ── Panel D : Learning Curves (best model) ────────────────────────────────
ax_d = fig.add_subplot(gs[1, 0])
style(ax_d, f"Learning Curve  —  {best_name}")

lc   = lc_data[best_name]
bc   = COLORS[best_name]
ax_d.plot(lc["sizes"], lc["train"], color=bc,
          linewidth=2, marker="o", markersize=5, label="Train")
ax_d.plot(lc["sizes"], lc["val"], color=bc,
          linewidth=2, marker="s", markersize=5,
          linestyle="--", alpha=0.7, label="Validation")
ax_d.fill_between(lc["sizes"], lc["train"], lc["val"],
                  alpha=0.1, color=bc)
ax_d.set_xlabel("Training Samples", fontsize=9)
ax_d.set_ylabel("Accuracy (%)", fontsize=9)
ax_d.set_ylim(70, 105)
ax_d.legend(framealpha=0, labelcolor=[bc, bc], fontsize=9)

# ── Panel E : Confusion Matrix (best model) ───────────────────────────────
ax_e = fig.add_subplot(gs[1, 1])
ax_e.set_facecolor(PANEL)
ax_e.set_title(f"Confusion Matrix  —  {best_name}",
               color=WHITE, fontsize=11, fontweight="bold", pad=10)

cm    = results[best_name]["CM"]
bc    = COLORS[best_name]
im    = ax_e.imshow(cm, cmap="Blues", aspect="auto")
ticks = range(len(labels))
ax_e.set_xticks(ticks); ax_e.set_xticklabels(labels, color=WHITE, fontsize=9)
ax_e.set_yticks(ticks); ax_e.set_yticklabels(labels, color=WHITE, fontsize=9)
ax_e.set_xlabel("Predicted", fontsize=9, color=LABEL)
ax_e.set_ylabel("Actual",    fontsize=9, color=LABEL)
for sp in ax_e.spines.values():
    sp.set_edgecolor(GRID)
for i in range(len(labels)):
    for j in range(len(labels)):
        ax_e.text(j, i, str(cm[i, j]), ha="center", va="center",
                  color="white" if cm[i, j] > cm.max() / 2 else TICK,
                  fontsize=13, fontweight="bold")

# ── Panel F : CV Mean ± Std Bar ───────────────────────────────────────────
ax_f = fig.add_subplot(gs[1, 2])
style(ax_f, "CV Mean ± Std Accuracy")

means = [cv_scores[n].mean() for n in model_names]
stds  = [cv_scores[n].std()  for n in model_names]

bars2 = ax_f.bar(model_names, means, color=clrs, alpha=0.8,
                  edgecolor="none", width=0.55)
ax_f.errorbar(model_names, means, yerr=stds,
              fmt="none", color="white", capsize=6,
              linewidth=1.5, capthick=1.5)

for bar, mean in zip(bars2, means):
    ax_f.text(bar.get_x() + bar.get_width() / 2,
              mean + max(stds) + 0.5,
              f"{mean:.1f}%", ha="center",
              color=WHITE, fontsize=8, fontweight="bold")

ax_f.set_xticklabels(
    [n.replace(" ", "\n") for n in model_names],
    color=WHITE, fontsize=8
)
ax_f.set_ylim(70, 105)
ax_f.set_ylabel("CV Accuracy (%)", fontsize=9)

# ── Save ──────────────────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accuracy_chart.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"\n  Chart saved → {out}")
plt.show()
