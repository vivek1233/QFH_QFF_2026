"""
Qiskit Finance Quick-Start Example
===================================
Quantum for Finance — Quantum for Humanity
https://github.com/vivekiniitm-stack/Quantum-for-humanity

This script demonstrates a minimal end-to-end quantum finance workflow:
  1. Portfolio Optimisation with QAOA
  2. Connect to IBM Quantum hardware (optional)

Learning source: https://learning.quantum.ibm.com
"""

import numpy as np

# ─── 1. PORTFOLIO OPTIMISATION (LOCAL SIMULATOR) ──────────────────────────────

from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

# Asset universe
assets = ["AAPL", "MSFT", "GOOGL", "AMZN"]
mu    = np.array([0.12, 0.10, 0.15, 0.08])   # expected returns
sigma = np.array([                             # covariance matrix
    [0.10, 0.02, 0.01, 0.03],
    [0.02, 0.08, 0.02, 0.01],
    [0.01, 0.02, 0.12, 0.02],
    [0.03, 0.01, 0.02, 0.06],
])

# Build portfolio problem
portfolio = PortfolioOptimization(
    expected_returns=mu,
    covariances=sigma,
    risk_factor=0.5,
    budget=2,
)
qp = portfolio.to_quadratic_program()

# ── Classical baseline ────────────────────────────────────────────────────────
print("=== Classical Exact Solver ===")
exact = MinimumEigenOptimizer(NumPyMinimumEigensolver())
result_exact = exact.solve(qp)
selected = [assets[i] for i, x in enumerate(result_exact.x) if x > 0.5]
print(f"Optimal portfolio: {selected}  |  Objective: {result_exact.fval:.4f}\n")

# ── QAOA on local simulator ───────────────────────────────────────────────────
print("=== QAOA (Qiskit Sampler Simulator) ===")
qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(maxiter=200), reps=2)
result_qaoa = MinimumEigenOptimizer(qaoa).solve(qp)
selected_q = [assets[i] for i, x in enumerate(result_qaoa.x) if x > 0.5]
print(f"QAOA portfolio:    {selected_q}  |  Objective: {result_qaoa.fval:.4f}\n")


# ─── 2. CONNECT TO IBM QUANTUM HARDWARE (OPTIONAL) ────────────────────────────
#
# Uncomment the block below and replace YOUR_IBM_QUANTUM_TOKEN to run on
# a real IBM Quantum processor.
#
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as IBMSampler
#
# QiskitRuntimeService.save_account(
#     channel="ibm_quantum",
#     token="YOUR_IBM_QUANTUM_TOKEN",
#     overwrite=True,
# )
# service = QiskitRuntimeService()
# backend = service.least_busy(operational=True, simulator=False)
# print(f"Running on: {backend.name}")
#
# sampler = IBMSampler(mode=backend)
# qaoa_hw = QAOA(sampler=sampler, optimizer=COBYLA(maxiter=100), reps=1)
# result_hw = MinimumEigenOptimizer(qaoa_hw).solve(qp)
# selected_hw = [assets[i] for i, x in enumerate(result_hw.x) if x > 0.5]
# print(f"IBM Quantum portfolio: {selected_hw}  |  Objective: {result_hw.fval:.4f}")


if __name__ == "__main__":
    print("✅ Quantum Finance Quick-Start complete.")
    print("   Next steps:")
    print("   - Open notebooks/ for detailed tutorials")
    print("   - Visit https://learning.quantum.ibm.com for IBM Quantum Learning")
    print("   - Join Discord: https://discord.gg/UgF3PaEax")
