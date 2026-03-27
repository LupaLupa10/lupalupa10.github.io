---
layout: post
title: MLflow Pipeline End-to-End MLOps Demo
date: 2026-03-27 10:00:00-0600
description: end-to-end MLflow pipeline for preprocessing, training, tracking, and model comparison
tags: code ai quantitative
categories: research-notes
giscus_comments: false
related_posts: false
published: true
---

This example packages an end-to-end ML pipeline around the Breast Cancer Wisconsin dataset using MLflow for experiment tracking, model logging, artifact management, and comparison across multiple classifiers.

It covers:

1. Data loading and exploratory analysis
2. Training for Logistic Regression, Random Forest, and XGBoost
3. Metric logging, artifacts, and model registration with MLflow
4. Simple inference on the best-performing run

You can download the full source here: [mlflow_pipeline.py]({{ '/assets/code/mlflow_pipeline.py' | relative_url }}).

Here is a small excerpt from the pipeline setup:

{% highlight python %}
EXPERIMENT_NAME = "breast_cancer_classification"
ARTIFACT_DIR = Path("./artifacts")
ARTIFACT_DIR.mkdir(exist_ok=True)
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment(EXPERIMENT_NAME)
{% endhighlight %}

And the script finishes by comparing runs and pointing you to the MLflow UI:

{% highlight python %}
print_header("DONE — MLflow Summary")
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
print(f"  Experiment ID : {experiment.experiment_id}")
print(f"  Tracking URI  : {mlflow.get_tracking_uri()}")
print(f"  Runs logged   : {len(run_ids)}")
print()
print("  To launch the MLflow UI, run:")
print("  mlflow ui --port 5000")
{% endhighlight %}
