# IBM Quantum Safe Hands-On Workshop & Lab Guide

Welcome to the **IBM Quantum Safe Hands-On Workshop**. This repository contains production-grade Python scripts, a hands-on lab pipeline, and an automated grading engine for testing post-quantum cryptographic implementations.

---

## 🎯 Workshop Objectives
1. **Discover**: Perform static cryptographic discovery across codebases and generate an OWASP CycloneDX-compliant **Cryptographic Bill of Materials (CBOM)**.
2. **Observe**: Evaluate cryptographic posture against NIST FIPS 203, 204, and 205 post-quantum standards.
3. **Transform**: Implement **ML-KEM-768** (FIPS 203) key encapsulation, **Hybrid X25519+ML-KEM** key derivation, and **ML-DSA-65** (FIPS 204) digital signatures.
4. **Crypto-Agility**: Build a zero-downtime microservice security gateway capable of switching between Classical, Hybrid, and Pure Post-Quantum policies.

---

## 📁 Workshop Files & Structure

| File | Purpose | Description |
| :--- | :--- | :--- |
| `IBM_Quantum_Safe_Masterclass_and_Workshop.pptx` | Presentation Deck | 10-slide masterclass presentation with speaker notes |
| `lab1_cbom_discovery.py` | Lab 1: Discovery Engine | Scans files and generates `cbom_output.json` |
| `lab2_hybrid_kem_mldsa.py` | Lab 2: Post-Quantum Crypto | ML-KEM-768 encapsulation, Hybrid HKDF, and ML-DSA-65 |
| `lab3_crypto_agile_api.py` | Lab 3: Crypto-Agility | Microservice API gateway with dynamic cipher switching |
| `student_assignment.py` | Student Assignment | Hands-on challenge file with implementation tasks |
| `lab_grader.py` | Automated Grader | Tests student code and outputs scores (0–100 pts) |

---

## 🚀 Running the Hands-On Labs

### Lab 1: Run Cryptographic Discovery & Generate CBOM
```bash
python lab1_cbom_discovery.py
```
*Output*: Generates `cbom_output.json` containing standardized cryptographic assets and risk scores.

### Lab 2: Run Hybrid Key Exchange & ML-DSA Signatures
```bash
python lab2_hybrid_kem_mldsa.py
```
*Output*: Generates lattice keypairs, encapsulates a shared secret, computes master hybrid keys, and verifies post-quantum digital signatures.

### Lab 3: Run Crypto-Agile Microservice Gateway
```bash
python lab3_crypto_agile_api.py
```
*Output*: Demonstrates live, zero-downtime cipher transitions across Classical, Hybrid, and Pure Post-Quantum modes.

---

## 🏆 Graded Student Assessment

To run the automated grader and receive a final score (0–100 points):

```bash
python lab_grader.py
```

### Grading Rubric (100 Points Total)
- **Task 1 (25 pts)**: CBOM Algorithm Vulnerability Classifier (`classify_crypto_algorithm`)
- **Task 2 (25 pts)**: Hybrid Key Derivation Function (`derive_hybrid_session_key`)
- **Task 3 (25 pts)**: Post-Quantum Digital Signature Verification (`verify_mldsa_signature`)
- **Task 4 (25 pts)**: Crypto-Agile State Machine (`AgileSecurityEngine`)

---

## 📚 Official References
1. **NIST FIPS 203 (Aug 2024)**: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM / CRYSTALS-Kyber)
2. **NIST FIPS 204 (Aug 2024)**: Module-Lattice-Based Digital Signature Standard (ML-DSA / CRYSTALS-Dilithium)
3. **NIST FIPS 205 (Aug 2024)**: Stateless Hash-Based Digital Signature Standard (SLH-DSA / SPHINCS+)
4. **IBM Quantum Safe Documentation**: [ibm.com/quantum/quantum-safe](https://www.ibm.com/quantum/quantum-safe)
5. **IBM Z Crypto Discovery & Inventory (zCDI)**: [IBM Documentation](https://www.ibm.com/docs/en/z-crypto-discovery-inventory)
6. **OWASP CycloneDX CBOM Standard**: [cyclonedx.org/capabilities/cbom/](https://cyclonedx.org/capabilities/cbom/)
