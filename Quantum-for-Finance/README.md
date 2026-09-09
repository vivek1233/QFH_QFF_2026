# 💹 Quantum for Finance
### A Sub-Project of [Quantum for Humanity](https://github.com/vivekiniitm-stack/Quantum-for-humanity)

> *Harnessing the power of quantum computing to democratise financial systems, improve risk modelling, and build a more equitable global economy.*

---

## 🌐 Overview

**Quantum for Finance** applies quantum algorithms to real-world financial challenges — from portfolio optimisation and derivative pricing to fraud detection and financial inclusion for underserved communities. This sub-project houses research notebooks, algorithm implementations, and educational resources for quantum finance applications.

---

## 🎯 Mission

- Bring quantum-accelerated financial modelling to researchers and practitioners
- Develop open-source tools for quantum risk, optimisation, and simulation in finance
- Apply quantum finance to humanitarian goals: financial inclusion, microfinance risk, and equitable access to capital markets

---

## 📁 Repository Structure

```
Quantum-for-Finance/
├── README.md                          ← You are here
├── notebooks/
│   ├── 01_quantum_portfolio_optimisation.ipynb
│   ├── 02_quantum_monte_carlo_pricing.ipynb
│   ├── 03_quantum_fraud_detection.ipynb
│   └── 04_financial_inclusion_qaoa.ipynb
├── resources/
│   ├── quantum_finance_roadmap.md
│   └── references.md
└── examples/
    └── qiskit_finance_quickstart.py
```

---

## 🔬 Core Topics

### 1. Portfolio Optimisation (QAOA / VQE)
Quantum approximate optimisation applied to the Markowitz portfolio selection problem. Encode asset weights as binary variables and minimise risk-adjusted returns on IBM Quantum hardware.

**Key algorithms:** QAOA, VQE, Quantum Annealing  
**Qiskit modules:** `qiskit_optimization`, `qiskit_finance`  
**Notebook:** [`01_quantum_portfolio_optimisation.ipynb`](notebooks/01_quantum_portfolio_optimisation.ipynb)

---

### 2. Quantum Monte Carlo for Derivative Pricing
Quantum Amplitude Estimation (QAE) provides a quadratic speedup over classical Monte Carlo methods for pricing financial derivatives (options, swaps, CDOs).

**Key algorithms:** Quantum Amplitude Estimation (QAE), Grover search  
**Qiskit modules:** `qiskit_finance`, `qiskit_algorithms`  
**Notebook:** [`02_quantum_monte_carlo_pricing.ipynb`](notebooks/02_quantum_monte_carlo_pricing.ipynb)

---

### 3. Quantum Machine Learning for Fraud Detection
Quantum kernel methods and Quantum Neural Networks (QNNs) applied to transaction classification and anomaly detection in financial datasets.

**Key algorithms:** Quantum SVM (QSVM), QNN, Quantum Kernel Estimation  
**Qiskit modules:** `qiskit_machine_learning`  
**Notebook:** [`03_quantum_fraud_detection.ipynb`](notebooks/03_quantum_fraud_detection.ipynb)

---

### 4. Financial Inclusion via Quantum Optimisation (QfH Focus)
Quantum optimisation models for microfinance credit scoring, optimising last-mile financial service distribution, and risk-pooling for unbanked populations.

**Application areas:** Jan Dhan (India), M-Pesa (Africa), microfinance  
**Key algorithms:** QAOA, Quantum Integer Programming  
**Notebook:** [`04_financial_inclusion_qaoa.ipynb`](notebooks/04_financial_inclusion_qaoa.ipynb)

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install qiskit qiskit-finance qiskit-optimization qiskit-machine-learning
pip install jupyter matplotlib numpy pandas
```

### Run on IBM Quantum
```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Load your IBM Quantum account
QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_IBM_QUANTUM_TOKEN")
service = QiskitRuntimeService()

# Select a backend
backend = service.least_busy(operational=True, simulator=False)
print(f"Running on: {backend.name}")
```

### Launch Notebooks
```bash
git clone https://github.com/vivekiniitm-stack/Quantum-for-humanity.git
cd Quantum-for-humanity/Quantum-for-Finance/notebooks
jupyter notebook
```

---

## 📚 Key References & Learning Resources

| Resource | Link |
|---|---|
| IBM Quantum Learning — Finance | https://learning.quantum.ibm.com |
| Qiskit Finance Tutorials | https://qiskit-community.github.io/qiskit-finance/ |
| Quantum Computing for Finance (Woerner & Egger, 2019) | https://arxiv.org/abs/1907.03044 |
| Option Pricing using QAE (Stamatopoulos et al., 2020) | https://arxiv.org/abs/1905.02666 |
| QAOA for Portfolio Optimisation | https://arxiv.org/abs/1911.05759 |
| Qiskit Textbook — Quantum ML | https://learn.qiskit.org/course/machine-learning |

---

## 🤝 Contributing

We welcome contributions from quantum researchers, financial engineers, and social impact practitioners.

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/quantum-credit-scoring`
3. Commit your changes: `git commit -m 'Add quantum credit scoring notebook'`
4. Push and open a Pull Request

### Contribution Areas
- New application notebooks (ESG scoring, climate finance, insurance)
- Improved implementations of existing algorithms
- Translations and educational materials
- Real-world dataset integrations

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) in the root repository.

---

## 🌍 Part of Quantum for Humanity

This project is a sub-project of **[Quantum for Humanity](https://github.com/vivekiniitm-stack/Quantum-for-humanity)** — an organisation dedicated to applying quantum science for the betterment of all people.

**Other sub-projects:**
- 🏥 [Quantum for Healthcare](../Quantum-for-Healthcare/README.md)

---

*#QuantumForHumanity #QuantumFinance #Qiskit #IBMQuantum*
