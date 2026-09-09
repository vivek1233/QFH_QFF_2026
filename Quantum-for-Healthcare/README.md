# 🏥 Quantum for Healthcare
### A Sub-Project of [Quantum for Humanity](https://github.com/vivekiniitm-stack/Quantum-for-humanity)

> *Accelerating drug discovery, personalising medicine, and optimising healthcare delivery with the power of quantum computing.*

---

## 🌐 Overview

**Quantum for Healthcare** applies quantum algorithms to medicine and public health — from simulating molecular interactions for drug discovery, to optimising hospital logistics, to quantum-enhanced medical imaging. This sub-project houses research notebooks, algorithm implementations, and educational resources for quantum healthcare applications.

---

## 🎯 Mission

- Accelerate drug discovery for neglected tropical diseases (TB, malaria, dengue)
- Enable quantum-powered personalised medicine and genomics
- Optimise healthcare resource allocation for underserved populations
- Advance quantum-enhanced medical imaging and diagnostics

---

## 📁 Repository Structure

```
Quantum-for-Healthcare/
├── README.md                              ← You are here
├── notebooks/
│   ├── 01_quantum_drug_discovery_vqe.ipynb
│   ├── 02_quantum_protein_folding.ipynb
│   ├── 03_quantum_medical_imaging_qml.ipynb
│   └── 04_hospital_resource_optimisation.ipynb
├── resources/
│   ├── quantum_healthcare_roadmap.md
│   └── references.md
└── examples/
    └── qiskit_healthcare_quickstart.py
```

---

## 🔬 Core Topics

### 1. Drug Discovery via Quantum Chemistry (VQE)
The **Variational Quantum Eigensolver (VQE)** computes the ground-state energy of molecular Hamiltonians — enabling accurate simulation of drug-target binding energies that are intractable classically.

**Target diseases:** Tuberculosis, Malaria, Dengue, Cancer  
**Key algorithms:** VQE, UCCSD ansatz, Quantum Phase Estimation  
**Qiskit modules:** `qiskit_nature`, `qiskit_algorithms`  
**Notebook:** [`01_quantum_drug_discovery_vqe.ipynb`](notebooks/01_quantum_drug_discovery_vqe.ipynb)

---

### 2. Quantum Protein Folding
Protein folding is an NP-hard problem critical for understanding disease mechanisms and designing therapeutic proteins. Quantum optimisation offers new approaches beyond classical AlphaFold.

**Key algorithms:** QAOA, Quantum Annealing, Lattice protein model  
**Qiskit modules:** `qiskit_research` (protein folding)  
**Notebook:** [`02_quantum_protein_folding.ipynb`](notebooks/02_quantum_protein_folding.ipynb)

---

### 3. Quantum ML for Medical Imaging
Quantum kernel methods and QNNs applied to MRI/CT scan classification — detecting tumours, anomalies, and disease markers faster than classical deep learning on quantum hardware.

**Key algorithms:** Quantum SVM, QNN, Quantum CNN  
**Qiskit modules:** `qiskit_machine_learning`  
**Notebook:** [`03_quantum_medical_imaging_qml.ipynb`](notebooks/03_quantum_medical_imaging_qml.ipynb)

---

### 4. Hospital Resource Optimisation (QfH Focus)
Quantum optimisation for hospital bed allocation, surgical scheduling, ambulance routing, and supply chain management — maximising patient outcomes with limited healthcare resources.

**Application areas:** Rural hospitals, disaster response, pandemic surge capacity  
**Key algorithms:** QAOA, Quantum Integer Programming  
**Notebook:** [`04_hospital_resource_optimisation.ipynb`](notebooks/04_hospital_resource_optimisation.ipynb)

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install qiskit qiskit-nature qiskit-algorithms qiskit-machine-learning
pip install pyscf  # classical quantum chemistry backend
pip install jupyter matplotlib numpy scipy
```

### Run on IBM Quantum
```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_IBM_QUANTUM_TOKEN")
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print(f"Running on: {backend.name}")
```

### Launch Notebooks
```bash
git clone https://github.com/vivekiniitm-stack/Quantum-for-humanity.git
cd Quantum-for-humanity/Quantum-for-Healthcare/notebooks
jupyter notebook
```

---

## 📚 Key References & Learning Resources

| Resource | Link |
|---|---|
| IBM Quantum Learning | https://learning.quantum.ibm.com |
| Qiskit Nature (Chemistry) | https://qiskit-community.github.io/qiskit-nature/ |
| Ground State Energies with VQE | https://learning.quantum.ibm.com/tutorial/variational-quantum-eigensolver |
| Quantum Protein Folding (IBM) | https://arxiv.org/abs/2212.01930 |
| Drug Discovery with Quantum | https://arxiv.org/abs/2210.12765 |
| Quantum ML for Medical Imaging | https://arxiv.org/abs/2103.14146 |

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/quantum-genomics`
3. Commit your changes: `git commit -m 'Add quantum genomics notebook'`
4. Push and open a Pull Request

### Contribution Areas
- Disease-specific drug discovery notebooks (HIV, Dengue, Cancer)
- Quantum genomics and personalised medicine
- Medical imaging datasets and benchmarks
- Clinical trial optimisation
- Translations and educational materials

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) in the root repository.

---

## 🌍 Part of Quantum for Humanity

This project is a sub-project of **[Quantum for Humanity](https://github.com/vivekiniitm-stack/Quantum-for-humanity)** — an organisation dedicated to applying quantum science for the betterment of all people.

**Other sub-projects:**
- 💹 [Quantum for Finance](../Quantum-for-Finance/README.md)

---

*#QuantumForHumanity #QuantumHealthcare #DrugDiscovery #Qiskit #IBMQuantum*
