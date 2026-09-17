#!/usr/bin/env python3
"""
IBM Quantum Safe Workshop — Graded Student Assignment
======================================================
Welcome to the hands-on implementation challenge!
Complete the 4 tasks below marked with TODOs.

When finished, run:
    python lab_grader.py
to automatically test and grade your implementation out of 100 points.

Tasks:
- Task 1: Implement CBOM Vulnerability Classifier (25 pts)
- Task 2: Implement Hybrid Key Derivation (HKDF) (25 pts)
- Task 3: Implement Post-Quantum Signature Verification (25 pts)
- Task 4: Implement Crypto-Agile Dynamic Policy Switcher (25 pts)
"""

import hashlib
import hmac
from typing import Dict, Any, Tuple

# ==============================================================================
# TASK 1: CBOM Vulnerability Classifier (25 Points)
# ==============================================================================
def classify_crypto_algorithm(algorithm_name: str, key_size: int = 0) -> Dict[str, Any]:
    """
    Given an algorithm name (e.g. 'RSA', 'AES', 'ML-KEM-768', '3DES', 'ECDSA'):
    Return a dictionary with:
    - 'is_quantum_vulnerable': bool (True for RSA, ECDSA, ECDH, DiffieHellman, 3DES, or AES with key_size < 256)
    - 'nist_standard_category': str ('FIPS 203', 'FIPS 204', 'Legacy', 'Deprecated', or 'Quantum Safe')
    - 'recommended_action': str ('Migrate to ML-KEM', 'Migrate to ML-DSA', 'Upgrade to AES-256', 'None')
    """
    algo = algorithm_name.upper().strip()
    
    # STUDENT IMPLEMENTATION:
    if "RSA" in algo or "DIFFIE" in algo or "DH" in algo:
        return {
            "is_quantum_vulnerable": True,
            "nist_standard_category": "Legacy",
            "recommended_action": "Migrate to ML-KEM"
        }
    elif "ECDSA" in algo or "ECC" in algo or "SECP" in algo:
        return {
            "is_quantum_vulnerable": True,
            "nist_standard_category": "Legacy",
            "recommended_action": "Migrate to ML-DSA"
        }
    elif "3DES" in algo or "DES" in algo:
        return {
            "is_quantum_vulnerable": True,
            "nist_standard_category": "Deprecated",
            "recommended_action": "Upgrade to AES-256"
        }
    elif "AES" in algo:
        if key_size < 256 and key_size > 0:
            return {
                "is_quantum_vulnerable": True,
                "nist_standard_category": "Legacy",
                "recommended_action": "Upgrade to AES-256"
            }
        else:
            return {
                "is_quantum_vulnerable": False,
                "nist_standard_category": "Quantum Safe",
                "recommended_action": "None"
            }
    elif "ML-KEM" in algo or "KYBER" in algo:
        return {
            "is_quantum_vulnerable": False,
            "nist_standard_category": "FIPS 203",
            "recommended_action": "None"
        }
    elif "ML-DSA" in algo or "DILITHIUM" in algo:
        return {
            "is_quantum_vulnerable": False,
            "nist_standard_category": "FIPS 204",
            "recommended_action": "None"
        }
    else:
        return {
            "is_quantum_vulnerable": True,
            "nist_standard_category": "Legacy",
            "recommended_action": "Migrate to ML-KEM"
        }


# ==============================================================================
# TASK 2: Hybrid Key Derivation (HKDF) (25 Points)
# ==============================================================================
def derive_hybrid_session_key(classical_ecdh_secret: bytes, pq_mlkem_secret: bytes, salt: bytes = b"QFF2026-SALT") -> bytes:
    """
    Implements hybrid key derivation by combining classical + post-quantum secrets:
    1. Extract: PRK = HMAC-SHA256(salt, classical_ecdh_secret + pq_mlkem_secret)
    2. Expand: OKM = HMAC-SHA256(PRK, b"HYBRID-SESSION-KEY-V1" + b"\x01")
    Return the 32-byte derived symmetric key.
    """
    if not classical_ecdh_secret or not pq_mlkem_secret:
        raise ValueError("Both secrets must be non-empty bytes")
    
    combined = classical_ecdh_secret + pq_mlkem_secret
    prk = hmac.new(salt, combined, hashlib.sha256).digest()
    derived_key = hmac.new(prk, b"HYBRID-SESSION-KEY-V1\x01", hashlib.sha256).digest()
    return derived_key


# ==============================================================================
# TASK 3: Post-Quantum Signature Verification (25 Points)
# ==============================================================================
def verify_mldsa_signature(payload: bytes, signature: bytes, public_key: bytes) -> bool:
    """
    Validates an ML-DSA-65 (FIPS 204) signature:
    - Signature length must be exactly 3,293 bytes
    - Public key length must be exactly 1,952 bytes
    - Payload must not be empty
    Returns True if valid, False otherwise.
    """
    if not payload:
        return False
    if len(signature) != 3293:
        return False
    if len(public_key) != 1952:
        return False
    return True


# ==============================================================================
# TASK 4: Crypto-Agile Dynamic Policy Switcher (25 Points)
# ==============================================================================
class AgileSecurityEngine:
    """
    Stateful engine enforcing cryptographic policies dynamically:
    Supported modes: 'CLASSICAL', 'HYBRID', 'POST_QUANTUM'
    """
    def __init__(self, initial_policy: str = "CLASSICAL"):
        self.policy = initial_policy

    def set_policy(self, new_policy: str) -> None:
        if new_policy not in ["CLASSICAL", "HYBRID", "POST_QUANTUM"]:
            raise ValueError("Invalid policy mode")
        self.policy = new_policy

    def get_cipher_suite(self) -> Dict[str, str]:
        """Returns the active cipher suite mapping based on the current policy."""
        if self.policy == "CLASSICAL":
            return {
                "key_exchange": "ECDH-P256",
                "signature": "RSA-2048",
                "symmetric": "AES-128-GCM"
            }
        elif self.policy == "HYBRID":
            return {
                "key_exchange": "X25519+ML-KEM-768",
                "signature": "ECDSA+ML-DSA-65",
                "symmetric": "AES-256-GCM"
            }
        elif self.policy == "POST_QUANTUM":
            return {
                "key_exchange": "ML-KEM-768",
                "signature": "ML-DSA-65",
                "symmetric": "AES-256-GCM"
            }
        else:
            raise ValueError("Unknown policy")
