import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def generate_synthetic_data(n_samples: int = 5000) -> pd.DataFrame:
    """
    Generate synthetic infrastructure metrics and failure labels.
    """
    cpu = np.random.beta(a=2, b=5, size=n_samples) * 100           # percent
    memory = np.random.beta(a=2, b=4, size=n_samples) * 100        # percent
    disk_io = np.random.gamma(shape=2, scale=30, size=n_samples)   # MB/s
    net_latency = np.random.gamma(shape=2, scale=20, size=n_samples)  # ms
    error_rate = np.random.exponential(scale=1.5, size=n_samples)  # percent of requests failing
    queue_length = np.random.poisson(lam=10, size=n_samples)       # messages in queue

    # base risk score with some noise
    risk_score = (
        0.4 * (cpu / 100)
        + 0.35 * (memory / 100)
        + 0.1 * (net_latency / 300)
        + 0.1 * (error_rate / 10)
        + 0.05 * (queue_length / 50)
    )

    noise = np.random.normal(loc=0.0, scale=0.05, size=n_samples)
    risk_score = risk_score + noise

    # failure if risk_score above threshold or very extreme values
    failure = (
        (risk_score > 0.75)
        | (cpu > 92)
        | (memory > 93)
        | (net_latency > 350)
        | (error_rate > 12)
    ).astype(int)

    df = pd.DataFrame(
        {
            "cpu": cpu,
            "memory": memory,
            "disk_io": disk_io,
            "net_latency": net_latency,
            "error_rate": error_rate,
            "queue_length": queue_length,
            "failure_within_10min": failure,
        }
    )

    return df


def train_model():
    print("Generating synthetic infrastructure dataset...")
    df = generate_synthetic_data(8000)
    print(df.head())

    X = df[
        ["cpu", "memory", "disk_io", "net_latency", "error_rate", "queue_length"]
    ]
    y = df["failure_within_10min"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=RANDOM_SEED,
        class_weight="balanced",
        n_jobs=-1,
    )

    print("Training RandomForest model...")
    clf.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "failure_model.joblib")
    joblib.dump(clf, model_path)

    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    train_model()
