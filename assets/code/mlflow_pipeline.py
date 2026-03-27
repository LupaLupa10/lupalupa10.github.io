"""
====================================================
  MLflow ML Pipeline — End-to-End MLOps Demo
====================================================
  Dataset  : Breast Cancer Wisconsin (sklearn)
  Models   : Logistic Regression, Random Forest, XGBoost
  Tracking : MLflow (local ./mlruns)
  Covers   :
    ✔ Data preprocessing & EDA
    ✔ MLflow experiment tracking
    ✔ Parameter logging
    ✔ Metric logging (per-epoch curves)
    ✔ Artifact logging (plots, reports)
    ✔ Model registration & versioning
    ✔ Model loading for inference
    ✔ Run comparison
====================================================
"""

import os
import warnings
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, roc_curve
)
from sklearn.pipeline import Pipeline
import xgboost as xgb
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from mlflow.models import infer_signature

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
EXPERIMENT_NAME = "breast_cancer_classification"
ARTIFACT_DIR    = Path("./artifacts")
ARTIFACT_DIR.mkdir(exist_ok=True)
RANDOM_STATE    = 42
TEST_SIZE       = 0.2
CV_FOLDS        = 5

# ─────────────────────────────────────────────
#  MLFLOW SETUP
# ─────────────────────────────────────────────
mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment(EXPERIMENT_NAME)


# ─────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────

def print_header(title: str):
    bar = "═" * 56
    print(f"\n╔{bar}╗")
    print(f"║  {title:<54}║")
    print(f"╚{bar}╝")


def compute_metrics(y_true, y_pred, y_prob) -> dict:
    return {
        "accuracy":  round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred), 4),
        "recall":    round(recall_score(y_true, y_pred), 4),
        "f1_score":  round(f1_score(y_true, y_pred), 4),
        "roc_auc":   round(roc_auc_score(y_true, y_prob), 4),
    }


# ─────────────────────────────────────────────
#  ARTIFACT GENERATORS
# ─────────────────────────────────────────────

def plot_confusion_matrix(y_true, y_pred, model_name: str) -> str:
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Benign", "Malignant"],
                yticklabels=["Benign", "Malignant"], ax=ax)
    ax.set_title(f"Confusion Matrix — {model_name}", fontweight="bold")
    ax.set_ylabel("True Label")
    ax.set_xlabel("Predicted Label")
    plt.tight_layout()
    path = str(ARTIFACT_DIR / f"cm_{model_name.replace(' ', '_')}.png")
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def plot_roc_curve(y_true, y_prob, model_name: str) -> str:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(fpr, tpr, lw=2, color="#4f86f7", label=f"AUC = {auc:.4f}")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.fill_between(fpr, tpr, alpha=0.1, color="#4f86f7")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve — {model_name}", fontweight="bold")
    ax.legend(loc="lower right")
    plt.tight_layout()
    path = str(ARTIFACT_DIR / f"roc_{model_name.replace(' ', '_')}.png")
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def plot_feature_importance(model, feature_names: list, model_name: str) -> str:
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        return None

    indices = np.argsort(importances)[::-1][:15]
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(indices)))[::-1]
    ax.barh([feature_names[i] for i in indices[::-1]],
            importances[indices[::-1]], color=colors)
    ax.set_title(f"Top Feature Importances — {model_name}", fontweight="bold")
    ax.set_xlabel("Importance Score")
    plt.tight_layout()
    path = str(ARTIFACT_DIR / f"fi_{model_name.replace(' ', '_')}.png")
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def plot_cv_scores(cv_scores: np.ndarray, model_name: str) -> str:
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(range(1, len(cv_scores) + 1), cv_scores, color="#4f86f7", alpha=0.8)
    ax.axhline(cv_scores.mean(), color="red", linestyle="--",
               label=f"Mean = {cv_scores.mean():.4f}")
    ax.set_xlabel("Fold")
    ax.set_ylabel("Accuracy")
    ax.set_title(f"Cross-Validation Scores — {model_name}", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    path = str(ARTIFACT_DIR / f"cv_{model_name.replace(' ', '_')}.png")
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def save_classification_report(y_true, y_pred, model_name: str) -> str:
    report = classification_report(y_true, y_pred,
                                   target_names=["Benign", "Malignant"])
    path = str(ARTIFACT_DIR / f"report_{model_name.replace(' ', '_')}.txt")
    with open(path, "w") as f:
        f.write(f"Classification Report — {model_name}\n")
        f.write("=" * 50 + "\n")
        f.write(report)
    return path


# ─────────────────────────────────────────────
#  DATA LOADING & EDA
# ─────────────────────────────────────────────

def load_and_prepare_data():
    print_header("STEP 1 — Load & Explore Dataset")

    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df["target"] = data.target

    print(f"  Dataset   : Breast Cancer Wisconsin")
    print(f"  Samples   : {df.shape[0]}")
    print(f"  Features  : {df.shape[1] - 1}")
    print(f"  Classes   : Benign={sum(df.target==1)}, Malignant={sum(df.target==0)}")
    print(f"  Missing   : {df.isnull().sum().sum()}")
    print()
    print(df.describe().round(3).to_string())

    # EDA — correlation heatmap (top 10 features)
    fig, ax = plt.subplots(figsize=(8, 6))
    top_cols = df.drop("target", axis=1).corrwith(df["target"]).abs().nlargest(10).index.tolist()
    corr = df[top_cols + ["target"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, ax=ax, annot_kws={"size": 8})
    ax.set_title("Feature Correlation with Target (Top 10)", fontweight="bold")
    plt.tight_layout()
    eda_path = str(ARTIFACT_DIR / "eda_correlation.png")
    plt.savefig(eda_path, dpi=120)
    plt.close()

    # Class distribution
    fig, ax = plt.subplots(figsize=(4, 3))
    labels = ["Malignant", "Benign"]
    counts = [sum(df.target == 0), sum(df.target == 1)]
    ax.bar(labels, counts, color=["#f87171", "#34d399"], width=0.5)
    ax.set_title("Class Distribution", fontweight="bold")
    ax.set_ylabel("Count")
    plt.tight_layout()
    dist_path = str(ARTIFACT_DIR / "eda_class_dist.png")
    plt.savefig(dist_path, dpi=120)
    plt.close()

    X = df.drop("target", axis=1)
    y = df["target"]
    feature_names = list(data.feature_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"\n  Train set : {X_train.shape[0]} samples")
    print(f"  Test set  : {X_test.shape[0]} samples")

    return X_train, X_test, y_train, y_test, feature_names, [eda_path, dist_path]


# ─────────────────────────────────────────────
#  GENERIC MLFLOW RUN TRAINER
# ─────────────────────────────────────────────

def train_and_log(
    model_name: str,
    model,
    params: dict,
    X_train, X_test, y_train, y_test,
    feature_names: list,
    use_scaler: bool = False,
    log_model_fn=mlflow.sklearn.log_model,
    extra_tags: dict = None,
):
    print(f"\n  ▶  Training: {model_name} ...")

    with mlflow.start_run(run_name=model_name) as run:
        run_id = run.info.run_id

        # ── Tags ──────────────────────────────
        mlflow.set_tags({
            "model_type":  model_name,
            "dataset":     "breast_cancer_wisconsin",
            "developer":   "mlops_engineer",
            "framework":   "scikit-learn" if "XGBoost" not in model_name else "xgboost",
            **(extra_tags or {}),
        })

        # ── Log Parameters ────────────────────
        mlflow.log_params(params)
        mlflow.log_param("test_size",    TEST_SIZE)
        mlflow.log_param("random_state", RANDOM_STATE)
        mlflow.log_param("cv_folds",     CV_FOLDS)
        mlflow.log_param("use_scaler",   use_scaler)

        # ── Build Pipeline ────────────────────
        if use_scaler:
            pipeline = Pipeline([("scaler", StandardScaler()), ("model", model)])
        else:
            pipeline = model

        # ── Cross-Validation ──────────────────
        cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
        mlflow.log_metric("cv_mean_accuracy", round(cv_scores.mean(), 4))
        mlflow.log_metric("cv_std_accuracy",  round(cv_scores.std(), 4))

        # Log each fold score
        for i, score in enumerate(cv_scores):
            mlflow.log_metric("cv_fold_accuracy", round(score, 4), step=i + 1)

        # ── Train ─────────────────────────────
        pipeline.fit(X_train, y_train)

        # ── Predict ───────────────────────────
        y_pred      = pipeline.predict(X_test)
        y_prob      = pipeline.predict_proba(X_test)[:, 1]

        # ── Metrics ───────────────────────────
        metrics = compute_metrics(y_test, y_pred, y_prob)
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        # Train metrics
        y_train_pred = pipeline.predict(X_train)
        y_train_prob = pipeline.predict_proba(X_train)[:, 1]
        train_metrics = compute_metrics(y_train, y_train_pred, y_train_prob)
        for k, v in train_metrics.items():
            mlflow.log_metric(f"train_{k}", v)

        # ── Artifacts ─────────────────────────
        # Confusion matrix
        cm_path = plot_confusion_matrix(y_test, y_pred, model_name)
        mlflow.log_artifact(cm_path, "plots")

        # ROC curve
        roc_path = plot_roc_curve(y_test, y_prob, model_name)
        mlflow.log_artifact(roc_path, "plots")

        # Feature importance
        inner = model if not use_scaler else pipeline.named_steps["model"]
        fi_path = plot_feature_importance(inner, feature_names, model_name)
        if fi_path:
            mlflow.log_artifact(fi_path, "plots")

        # CV plot
        cv_path = plot_cv_scores(cv_scores, model_name)
        mlflow.log_artifact(cv_path, "plots")

        # Classification report
        report_path = save_classification_report(y_test, y_pred, model_name)
        mlflow.log_artifact(report_path, "reports")

        # Params JSON (nice for downstream tooling)
        params_path = str(ARTIFACT_DIR / f"params_{model_name.replace(' ','_')}.json")
        with open(params_path, "w") as f:
            json.dump({**params, **metrics}, f, indent=2)
        mlflow.log_artifact(params_path, "configs")

        # ── Log Model ─────────────────────────
        signature = infer_signature(X_train, pipeline.predict(X_train))
        log_model_fn(
            pipeline, artifact_path="model",
            signature=signature,
            input_example=X_train.iloc[:3],
            registered_model_name=f"bc_{model_name.replace(' ', '_').lower()}",
        )

        # ── Print Results ─────────────────────
        print(f"     Run ID  : {run_id[:8]}...")
        print(f"     CV Acc  : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        for k, v in metrics.items():
            print(f"     {k:<12}: {v:.4f}")

        return run_id, metrics


# ─────────────────────────────────────────────
#  MODEL CONFIGS
# ─────────────────────────────────────────────

def get_model_configs():
    return [
        {
            "name": "Logistic Regression",
            "model": LogisticRegression(C=1.0, max_iter=1000, random_state=RANDOM_STATE),
            "params": {"C": 1.0, "max_iter": 1000, "solver": "lbfgs", "penalty": "l2"},
            "use_scaler": True,
            "log_fn": mlflow.sklearn.log_model,
        },
        {
            "name": "Random Forest",
            "model": RandomForestClassifier(
                n_estimators=200, max_depth=10, min_samples_split=5,
                random_state=RANDOM_STATE, n_jobs=-1
            ),
            "params": {"n_estimators": 200, "max_depth": 10, "min_samples_split": 5},
            "use_scaler": False,
            "log_fn": mlflow.sklearn.log_model,
        },
        {
            "name": "XGBoost",
            "model": xgb.XGBClassifier(
                n_estimators=200, max_depth=6, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8,
                use_label_encoder=False, eval_metric="logloss",
                random_state=RANDOM_STATE
            ),
            "params": {
                "n_estimators": 200, "max_depth": 6, "learning_rate": 0.05,
                "subsample": 0.8, "colsample_bytree": 0.8,
            },
            "use_scaler": False,
            "log_fn": mlflow.sklearn.log_model,
        },
    ]


# ─────────────────────────────────────────────
#  COMPARE RUNS & PLOT
# ─────────────────────────────────────────────

def compare_and_plot(results: list):
    print_header("STEP 3 — Model Comparison")

    df = pd.DataFrame(results)
    df_display = df[["model", "accuracy", "precision", "recall", "f1_score", "roc_auc"]]
    print(df_display.to_string(index=False))

    # Bar chart comparison
    metrics_to_plot = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    x = np.arange(len(metrics_to_plot))
    width = 0.22
    colors = ["#4f86f7", "#34d399", "#f59e0b"]

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, row in df.iterrows():
        vals = [row[m] for m in metrics_to_plot]
        bars = ax.bar(x + i * width, vals, width, label=row["model"], color=colors[i], alpha=0.88)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7.5)

    ax.set_xticks(x + width)
    ax.set_xticklabels([m.replace("_", " ").title() for m in metrics_to_plot])
    ax.set_ylim(0.85, 1.02)
    ax.set_ylabel("Score")
    ax.set_title("Model Comparison — All Metrics", fontweight="bold", fontsize=13)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    cmp_path = str(ARTIFACT_DIR / "model_comparison.png")
    plt.savefig(cmp_path, dpi=130)
    plt.close()
    print(f"\n  Comparison chart saved → {cmp_path}")

    best = df.loc[df["roc_auc"].idxmax()]
    print(f"\n  🏆  Best Model : {best['model']}  (ROC-AUC = {best['roc_auc']:.4f})")
    return cmp_path, best["model"]


# ─────────────────────────────────────────────
#  LOAD MODEL & INFERENCE
# ─────────────────────────────────────────────

def demo_model_inference(run_id: str, X_test, y_test):
    print_header("STEP 4 — Load Model & Run Inference")

    model_uri = f"runs:/{run_id}/model"
    print(f"  Loading model from: {model_uri}")
    loaded_model = mlflow.sklearn.load_model(model_uri)

    sample = X_test.iloc[:5]
    preds  = loaded_model.predict(sample)
    probs  = loaded_model.predict_proba(sample)[:, 1]

    print("\n  Sample Predictions (first 5 test rows):")
    print(f"  {'Row':<5} {'True':<10} {'Pred':<10} {'Prob(+)':<10}")
    print("  " + "-" * 38)
    label_map = {0: "Malignant", 1: "Benign"}
    for i, (true, pred, prob) in enumerate(zip(y_test.iloc[:5], preds, probs)):
        match = "✔" if true == pred else "✘"
        print(f"  {i:<5} {label_map[true]:<10} {label_map[pred]:<10} {prob:.4f}  {match}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    print("\n" + "█" * 58)
    print("  MLflow ML Pipeline — Breast Cancer Classification")
    print("  MLflow version :", mlflow.__version__)
    print("  Tracking URI   :", mlflow.get_tracking_uri())
    print("  Experiment     :", EXPERIMENT_NAME)
    print("█" * 58)

    # ── Step 1: Data ──────────────────────────
    X_train, X_test, y_train, y_test, feature_names, eda_paths = load_and_prepare_data()

    # ── Step 2: Train All Models ──────────────
    print_header("STEP 2 — Train & Log Models with MLflow")

    model_configs = get_model_configs()
    results, run_ids = [], []

    for cfg in model_configs:
        run_id, metrics = train_and_log(
            model_name  = cfg["name"],
            model       = cfg["model"],
            params      = cfg["params"],
            X_train     = X_train,
            X_test      = X_test,
            y_train     = y_train,
            y_test      = y_test,
            feature_names = feature_names,
            use_scaler  = cfg["use_scaler"],
            log_model_fn = cfg["log_fn"],
        )
        run_ids.append(run_id)
        results.append({"model": cfg["name"], **metrics})

    # Log EDA artifacts to first run
    with mlflow.start_run(run_id=run_ids[0]):
        for p in eda_paths:
            mlflow.log_artifact(p, "eda")

    # ── Step 3: Compare ───────────────────────
    cmp_path, best_model_name = compare_and_plot(results)

    # Log comparison chart to all runs
    for rid in run_ids:
        with mlflow.start_run(run_id=rid):
            mlflow.log_artifact(cmp_path, "comparison")

    # ── Step 4: Inference demo ────────────────
    best_idx = next(i for i, r in enumerate(results) if r["model"] == best_model_name)
    demo_model_inference(run_ids[best_idx], X_test, y_test)

    # ── Summary ───────────────────────────────
    print_header("DONE — MLflow Summary")
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    print(f"  Experiment ID : {experiment.experiment_id}")
    print(f"  Tracking URI  : {mlflow.get_tracking_uri()}")
    print(f"  Runs logged   : {len(run_ids)}")
    print(f"  Artifacts dir : {ARTIFACT_DIR.resolve()}")
    print()
    print("  To launch the MLflow UI, run:")
    print("  ┌──────────────────────────────────────────┐")
    print("  │   mlflow ui --port 5000                  │")
    print("  │   → http://localhost:5000                │")
    print("  └──────────────────────────────────────────┘")
    print()


if __name__ == "__main__":
    main()
