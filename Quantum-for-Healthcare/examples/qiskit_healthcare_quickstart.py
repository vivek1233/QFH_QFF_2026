"""
Qiskit Healthcare Quick-Start Example
=======================================
Quantum for Healthcare — Quantum for Humanity
https://github.com/vivekiniitm-stack/Quantum-for-humanity

This script demonstrates:
  1. VQE ground-state energy of H2 (drug discovery foundation)
  2. ICU allocation optimisation with QAOA

Learning source: https://learning.quantum.ibm.com
"""

import numpy as np

# ─── 1. VQE DRUG DISCOVERY (H₂ MOLECULE) ─────────────────────────────────────

print("=" * 55)
print("  PART 1: VQE Drug Discovery — H₂ Molecule")
print("=" * 55)

try:
    from qiskit_nature.second_q.drivers import PySCFDriver
    from qiskit_nature.second_q.mappers import JordanWignerMapper
    from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
    from qiskit_nature.second_q.algorithms import GroundStateEigensolver
    from qiskit_algorithms import VQE, NumPyMinimumEigensolver
    from qiskit_algorithms.optimizers import SLSQP
    from qiskit.primitives import Estimator

    driver  = PySCFDriver(atom='H 0 0 0; H 0 0 0.735', basis='sto3g')
    problem = driver.run()
    mapper  = JordanWignerMapper()

    # Classical FCI reference
    fci_solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
    fci_result = fci_solver.solve(problem)
    fci_energy = fci_result.total_energies[0]

    # VQE
    ansatz = UCCSD(
        num_spatial_orbitals=problem.num_spatial_orbitals,
        num_particles=problem.num_particles,
        mapper=mapper,
        initial_state=HartreeFock(
            num_spatial_orbitals=problem.num_spatial_orbitals,
            num_particles=problem.num_particles,
            mapper=mapper
        )
    )
    vqe = VQE(estimator=Estimator(), ansatz=ansatz, optimizer=SLSQP(maxiter=300))
    vqe_solver = GroundStateEigensolver(mapper, vqe)
    vqe_result = vqe_solver.solve(problem)
    vqe_energy = vqe_result.total_energies[0]

    print(f"\n  H₂ VQE Energy:  {vqe_energy:.6f} Hartree")
    print(f"  FCI Reference:  {fci_energy:.6f} Hartree")
    error_mha = abs(vqe_energy - fci_energy) * 1000
    print(f"  Error:          {error_mha:.4f} mHa  (threshold: 1 mHa)")
    if error_mha < 1.0:
        print("  ✅  Chemical accuracy achieved!")

except ImportError:
    print("  ⚠️  qiskit-nature / pyscf not installed.")
    print("  Run: pip install qiskit-nature pyscf")


# ─── 2. ICU ALLOCATION WITH QAOA ─────────────────────────────────────────────

print("\n" + "=" * 55)
print("  PART 2: QAOA ICU Allocation Optimisation")
print("=" * 55)

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

# 6-patient ICU problem
patients = [
    ('P01', 'Sepsis',      9.5, 0.92, 5),
    ('P02', 'Cardiac',     9.8, 0.88, 4),
    ('P03', 'Trauma',      8.5, 0.85, 7),
    ('P04', 'Resp. Fail.', 8.0, 0.80, 6),
    ('P05', 'Eclampsia',   9.0, 0.91, 4),
    ('P06', 'Paed. Fever', 7.0, 0.95, 2),
]
ids      = [p[0] for p in patients]
severity = np.array([p[2] for p in patients])
benefit  = np.array([p[3] for p in patients])
days     = np.array([p[4] for p in patients])
ICU_BEDS, MAX_DAYS = 2, 10

qp = QuadraticProgram('ICU')
for pid in ids:
    qp.binary_var(name=pid)
qp.minimize(linear={ids[i]: -(severity[i] * benefit[i]) for i in range(len(ids))})
qp.linear_constraint(linear={ids[i]: 1 for i in range(len(ids))}, sense='<=', rhs=ICU_BEDS, name='beds')
qp.linear_constraint(linear={ids[i]: int(days[i]) for i in range(len(ids))}, sense='<=', rhs=MAX_DAYS, name='days')

# Classical
exact = MinimumEigenOptimizer(NumPyMinimumEigensolver())
r_exact = exact.solve(qp)
admitted_c = [ids[i] for i, x in enumerate(r_exact.x) if x > 0.5]
print(f"\n  Classical optimal: {admitted_c}")

# QAOA
converter = QuadraticProgramToQubo()
qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(maxiter=200), reps=2)
r_qaoa_qubo = MinimumEigenOptimizer(qaoa).solve(converter.convert(qp))
r_qaoa = converter.interpret(r_qaoa_qubo)
admitted_q = [ids[i] for i, x in enumerate(r_qaoa.x) if x > 0.5]
print(f"  QAOA quantum:     {admitted_q}")


if __name__ == "__main__":
    print("\n✅ Quantum Healthcare Quick-Start complete.")
    print("   Next steps:")
    print("   - Open notebooks/ for detailed tutorials")
    print("   - Visit https://learning.quantum.ibm.com for IBM Quantum Learning")
    print("   - Join Discord: https://discord.gg/UgF3PaEax")
