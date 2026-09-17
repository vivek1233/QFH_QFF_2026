#!/usr/bin/env python3
"""
IBM Quantum Safe Workshop — Lab 3: Crypto-Agile Microservice Gateway Architecture
==================================================================================
This script demonstrates how to architect a modern enterprise microservice gateway
with dynamic "Crypto-Agility". It allows seamless switching between:
- Classical Mode (RSA-2048 / ECDSA P-256)
- Hybrid Mode (X25519 + ML-KEM-768)
- Pure Post-Quantum Mode (ML-KEM-768 + ML-DSA-65)

Through runtime policy updates WITHOUT restarting or recompiling services.
"""

import os
import json
import secrets
import hashlib
from typing import Dict, Any

class CryptoPolicy:
    CLASSICAL = "CLASSICAL_LEGACY"
    HYBRID = "HYBRID_QUANTUM_SAFE"
    POST_QUANTUM = "PURE_POST_QUANTUM"

class CryptoAgileGateway:
    def __init__(self, policy: str = CryptoPolicy.HYBRID):
        self.policy = policy
        self.session_table: Dict[str, Dict[str, Any]] = {}
        print(f"[*] Initialized Gateway with Active Policy: {self.policy}")

    def update_policy(self, new_policy: str):
        """Dynamic runtime policy transition (Crypto-Agility)."""
        old_policy = self.policy
        self.policy = new_policy
        print(f"[!] Policy Shift: {old_policy} ➔ {self.policy} (Zero Downtime)")

    def authenticate_request(self, client_id: str, payload: bytes) -> Dict[str, Any]:
        """Processes an incoming API request under the currently enforced cryptographic policy."""
        session_id = secrets.token_hex(8)
        
        if self.policy == CryptoPolicy.CLASSICAL:
            # RSA-2048 + ECDH P-256
            kem_algo = "ECDH-P256"
            sig_algo = "RSA-2048"
            key_size = 256
            quantum_safe = False
        elif self.policy == CryptoPolicy.HYBRID:
            # Dual X25519 + ML-KEM-768
            kem_algo = "Hybrid-X25519-ML-KEM-768"
            sig_algo = "Dual-ECDSA-ML-DSA-65"
            key_size = 1184 + 32
            quantum_safe = True
        elif self.policy == CryptoPolicy.POST_QUANTUM:
            # Pure NIST Standards
            kem_algo = "ML-KEM-768 (FIPS 203)"
            sig_algo = "ML-DSA-65 (FIPS 204)"
            key_size = 1184
            quantum_safe = True
        else:
            raise ValueError("Unknown cryptographic policy.")

        session_record = {
            "session_id": session_id,
            "client_id": client_id,
            "policy_enforced": self.policy,
            "key_exchange_algorithm": kem_algo,
            "signature_algorithm": sig_algo,
            "is_quantum_resistant": quantum_safe,
            "derived_session_key": hashlib.sha256(payload + self.policy.encode()).hexdigest()
        }
        self.session_table[session_id] = session_record
        return session_record

if __name__ == "__main__":
    print("================================================================================")
    print("   IBM Quantum Safe Workshop — Lab 3: Crypto-Agile Microservice Gateway         ")
    print("================================================================================\n")

    gateway = CryptoAgileGateway(policy=CryptoPolicy.CLASSICAL)
    
    # 1. Processing under legacy policy
    print("\n--- 1. Processing Traffic under CLASSICAL Mode ---")
    res1 = gateway.authenticate_request("Service_A_PaymentService", b"GET /v1/account-balance")
    print(json.dumps(res1, indent=2))

    # 2. Transitioning live to HYBRID Mode
    print("\n--- 2. Seamless Migration to HYBRID Mode ---")
    gateway.update_policy(CryptoPolicy.HYBRID)
    res2 = gateway.authenticate_request("Service_B_HealthcareSync", b"POST /v2/patient-records")
    print(json.dumps(res2, indent=2))

    # 3. Transitioning to Pure Post-Quantum Mode
    print("\n--- 3. Upgrading to PURE POST-QUANTUM (FIPS 203/204) ---")
    gateway.update_policy(CryptoPolicy.POST_QUANTUM)
    res3 = gateway.authenticate_request("Service_C_CoreBanking", b"POST /v3/settlement-wire")
    print(json.dumps(res3, indent=2))

    print("\n[+] Crypto-Agility demonstration finished successfully.")
