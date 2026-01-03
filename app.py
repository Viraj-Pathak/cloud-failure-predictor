from flask import Flask, render_template, request
from model_utils import predict_failure
from datetime import datetime

app = Flask(__name__)

HISTORY = []

def add_to_history(risk, level, metrics):
    HISTORY.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "risk": round(risk, 2),
        "level": level,
        "cpu": metrics[0],
        "memory": metrics[1],
        "latency": metrics[3],
        "error": metrics[4],
        "queue": metrics[5]
    })
    if len(HISTORY) > 10:
        HISTORY.pop(0)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    level = None
    recommendation = None

    if request.method == "POST":
        cpu = float(request.form["cpu"])
        memory = float(request.form["memory"])
        disk_io = float(request.form["disk_io"])
        latency = float(request.form["net_latency"])
        error_rate = float(request.form["error_rate"])
        queue = float(request.form["queue_length"])

        metrics = [cpu, memory, disk_io, latency, error_rate, queue]

        # ML Score
        ml_score = predict_failure(metrics)

        # Hybrid Risk Model (Rule + ML)
        risk = ml_score

        if cpu > 85 or memory > 90:
            risk += 25

        if latency > 300 or error_rate > 5:
            risk += 20

        if queue > 100:
            risk += 15

        if disk_io > 140:
            risk += 10

        risk = max(0, min(risk, 100))
        result = round(risk, 2)

        # Risk Levels
        if result >= 80:
            level = "HIGH"
            recommendation = (
                "🚨 Auto-Scale services, restart impacted nodes, "
                "enable rate limiting, and trigger incident workflow."
            )
        elif result >= 50:
            level = "MEDIUM"
            recommendation = (
                "⚠️ Monitor closely, scale resources gradually, "
                "clear queue backlogs, optimize services."
            )
        else:
            level = "LOW"
            recommendation = "✅ System stable. Continue monitoring."

        add_to_history(result, level, metrics)

    return render_template(
        "index.html",
        result=result,
        level=level,
        recommendation=recommendation,
        history=HISTORY
    )


if __name__ == "__main__":
    app.run(debug=True)
