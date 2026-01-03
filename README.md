# ☁️ Cloud Failure Predictor & Auto-Healing Assistant

Cloud systems fail. Latency spikes, CPU overloads, memory leaks, and queuing issues can push services to outage.  
This project predicts **cloud service failures in advance** using Machine Learning and automatically suggests **self-healing actions** to prevent incidents.

🔗 **Live Web App (Local Deploy)**  
Run locally and instantly predict outages, visualize trends, and get automated remediation actions.

---

## 🚀 Features
- 🧠 ML model predicts cloud failure probability
- 📊 Visual history & risk trend chart
- ⚠️ Risk classification: LOW | MEDIUM | HIGH
- 🤖 Auto-healing recommendations
- 🎯 Built for SRE / DevOps / Cloud Reliability

---

## 🧠 Tech Stack
| Component | Tech |
|----------|------|
| Backend | Python, Flask |
| ML Model | RandomForest |
| Frontend | HTML, CSS, JS, Chart.js |
| Persistence | Session-based history |
| Deployment | Local / Cloud-ready |

---

## 📸 UI Preview
![UI Preview](https://github.com/Viraj-Pathak/cloud-failure-predictor/blob/main/docs/ui.png)

---

## 🏗️ How It Works
1️⃣ Input live cloud metrics  
2️⃣ System predicts failure probability for next 10 minutes  
3️⃣ Assigns risk level  
4️⃣ Displays charts  
5️⃣ Provides automated system mitigation actions  

---

## 📥 Installation

### 1️⃣ Clone Repo
```bash
git clone https://github.com/Viraj-Pathak/cloud-failure-predictor.git
cd cloud-failure-predictor
