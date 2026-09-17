#!/usr/bin/env python3
"""
IBM Quantum Safe Workshop — Automated Grader & Assessment Engine
=================================================================
This script tests the student implementation in `student_assignment.py`
and outputs a graded scorecard from 0 to 100 points with diagnostic logs.
"""

import sys
import secrets
import hashlib
from student_assignment import (
    classify_crypto_algorithm,
    derive_hybrid_session_key,
    verify_mldsa_signature,
    AgileSecurityEngine
)

def run_grader():
    score = 0
    max_score = 100
    print("================================================================================")
    print("     IBM Quantum Safe Workshop -- Automated Student Assessment Grader           ")
    print("================================================================================\n")

    # --------------------------------------------------------------------------
    # TEST 1: Algorithm Classification (25 Points)
    # --------------------------------------------------------------------------
    print("[*] Testing Task 1: CBOM Vulnerability Classifier...")
    try:
        t1_rsa = classify_crypto_algorithm("RSA-2048")
        t1_ecc = classify_crypto_algorithm("ECDSA_P256")
        t1_aes = classify_crypto_algorithm("AES", key_size=128)
        t1_kem = classify_crypto_algorithm("ML-KEM-768")
        t1_dsa = classify_crypto_algorithm("ML-DSA-65")

        assert t1_rsa["is_quantum_vulnerable"] is True, "RSA should be marked vulnerable"
        assert t1_rsa["recommended_action"] == "Migrate to ML-KEM"
        assert t1_ecc["is_quantum_vulnerable"] is True, "ECC should be marked vulnerable"
        assert t1_aes["is_quantum_vulnerable"] is True, "AES-128 should be marked vulnerable"
        assert t1_kem["is_quantum_vulnerable"] is False, "ML-KEM-768 is Quantum Safe"
        assert t1_kem["nist_standard_category"] == "FIPS 203"
        assert t1_dsa["nist_standard_category"] == "FIPS 204"

        print("    [+] PASS: All algorithm risk classifications correct (+25 pts)")
        score += 25
    except Exception as e:
        print(f"    [-] FAIL: Task 1 error: {e}")

    # --------------------------------------------------------------------------
    # TEST 2: Hybrid Key Derivation (25 Points)
    # --------------------------------------------------------------------------
    print("\n[*] Testing Task 2: Hybrid Key Derivation (HKDF)...")
    try:
        c_secret = secrets.token_bytes(32)
        pq_secret = secrets.token_bytes(32)
        derived1 = derive_hybrid_session_key(c_secret, pq_secret)
        derived2 = derive_hybrid_session_key(c_secret, pq_secret)

        assert len(derived1) == 32, "Derived key must be exactly 32 bytes (256-bit)"
        assert derived1 == derived2, "Key derivation must be deterministic"

        # Check entropy contribution
        diff_pq = secrets.token_bytes(32)
        derived3 = derive_hybrid_session_key(c_secret, diff_pq)
        assert derived1 != derived3, "Changing PQ secret must yield a different key"

        print(f"    [+] PASS: Hybrid session key successfully generated: {derived1.hex()[:16]}... (+25 pts)")
        score += 25
    except Exception as e:
        print(f"    [-] FAIL: Task 2 error: {e}")

    # --------------------------------------------------------------------------
    # TEST 3: Post-Quantum Signature Verification (25 Points)
    # --------------------------------------------------------------------------
    print("\n[*] Testing Task 3: Post-Quantum ML-DSA Signature Verification...")
    try:
        valid_payload = b"TRANSFER $50,000 FROM VAULT A"
        valid_sig = secrets.token_bytes(3293)
        valid_pub = secrets.token_bytes(1952)

        res_valid = verify_mldsa_signature(valid_payload, valid_sig, valid_pub)
        res_invalid_len = verify_mldsa_signature(valid_payload, valid_sig[:100], valid_pub)
        res_empty_payload = verify_mldsa_signature(b"", valid_sig, valid_pub)

        assert res_valid is True, "Valid signature dimensions must pass"
        assert res_invalid_len is False, "Truncated signature must fail"
        assert res_empty_payload is False, "Empty payload must fail"

        print("    [+] PASS: ML-DSA-65 validation logic strictly enforced (+25 pts)")
        score += 25
    except Exception as e:
        print(f"    [-] FAIL: Task 3 error: {e}")

    # --------------------------------------------------------------------------
    # TEST 4: Crypto-Agility Policy Engine (25 Points)
    # --------------------------------------------------------------------------
    print("\n[*] Testing Task 4: Crypto-Agile Dynamic Policy Switcher...")
    try:
        engine = AgileSecurityEngine(initial_policy="CLASSICAL")
        cs1 = engine.get_cipher_suite()
        assert cs1["key_exchange"] == "ECDH-P256"

        engine.set_policy("HYBRID")
        cs2 = engine.get_cipher_suite()
        assert "ML-KEM" in cs2["key_exchange"] and "X25519" in cs2["key_exchange"]

        engine.set_policy("POST_QUANTUM")
        cs3 = engine.get_cipher_suite()
        assert cs3["key_exchange"] == "ML-KEM-768"
        assert cs3["signature"] == "ML-DSA-65"

        print("    [+] PASS: State machine handled dynamic policy transitions (+25 pts)")
        score += 25
    except Exception as e:
        print(f"    [-] FAIL: Task 4 error: {e}")

    # --------------------------------------------------------------------------
    # FINAL SCORECARD
    # --------------------------------------------------------------------------
    print("\n================================================================================")
    print(f"                   FINAL SCORE: {score} / {max_score} POINTS                     ")
    print("================================================================================")
    if score == 100:
        print("  [#] EXCELLENT! You have achieved 100% Mastery in Quantum Safe Implementation!")
        print("  [#] Certified for Post-Quantum Migration Architecture (FIPS 203/204)")
    elif score >= 75:
        print("  [*] PROFICIENT: Passing grade achieved. Review failed test cases.")
    else:
        print("  [!] NEEDS REVISION: Please review the TODOs in student_assignment.py and re-run.")
    print("================================================================================\n")
    return score

if __name__ == "__main__":
    score = run_grader()
    sys.exit(0 if score >= 75 else 1)
