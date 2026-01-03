import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("models", "failure_model.joblib")

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

def smart_failure_risk(cpu, memory, disk, latency, error_rate, queue):
    score = 0

    # CPU impact
    if cpu > 85:
        score += 20
    elif cpu > 70:
        score += 10

    # Memory impact
    if memory > 85:
        score += 20
    elif memory > 70:
        score += 10

    # Disk IO
    if disk > 120:
        score += 15
    elif disk > 90:
        score += 10

    # Latency
    if latency > 300:
        score += 20
    elif latency > 150:
        score += 10

    # Error rate
    if error_rate > 5:
        score += 25
    elif error_rate > 2:
        score += 15

    # Queue length
    if queue > 100:
        score += 15
    elif queue > 50:
        score += 10

    # Cap 100
    score = min(score, 100)
    return score

def predict_failure(metrics):
    cpu, memory, disk, latency, error_rate, queue = metrics

    # Try ML model first if exists
    ml_prob = 0
    if model:
        prob = model.predict_proba([metrics])[0][1] * 100
        ml_prob = round(prob, 2)

    # Smart engine
    rule_prob = smart_failure_risk(cpu, memory, disk, latency, error_rate, queue)

    # Final probability = best of both
    final_prob = max(rule_prob, ml_prob)

    return round(final_prob, 2)
