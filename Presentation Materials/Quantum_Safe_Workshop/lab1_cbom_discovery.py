#!/usr/bin/env python3
"""
IBM Quantum Safe Workshop — Lab 1: Cryptographic Discovery & CBOM Generation
=============================================================================
This script scans source code and software artifacts for classical and
quantum-vulnerable cryptographic algorithms, computes vulnerability metrics,
and exports an OWASP CycloneDX-compliant Cryptographic Bill of Materials (CBOM).

References:
- OWASP CycloneDX CBOM Specification: https://cyclonedx.org/capabilities/cbom/
- IBM Quantum Safe Explorer Architecture & zCDI concepts
"""

import os
import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any

# Cryptographic ruleset defining quantum vulnerability and post-quantum status
CRYPTO_SIGNATURES = [
    {
        "pattern": r"\b(RSA|rsa|RSACryptoServiceProvider|RSA_PKCS1_OAEP_PADDING)\b",
        "algorithm": "RSA",
        "category": "Asymmetric / Public-Key",
        "quantum_status": "Vulnerable (Shor's Algorithm)",
        "security_level": "Broken by CRQC",
        "replacement": "ML-KEM (FIPS 203) for key encapsulation or ML-DSA (FIPS 204) for signing",
        "risk_score": 9.5
    },
    {
        "pattern": r"\b(ECDSA|ecdsa|secp256k1|secp256r1|prime256v1|ECDH|ecdh)\b",
        "algorithm": "Elliptic Curve Cryptography (ECC / ECDSA / ECDH)",
        "category": "Asymmetric / Elliptic Curve",
        "quantum_status": "Vulnerable (Shor's Algorithm)",
        "security_level": "Broken by CRQC",
        "replacement": "ML-KEM (FIPS 203) or ML-DSA (FIPS 204)",
        "risk_score": 9.5
    },
    {
        "pattern": r"\b(DiffieHellman|DHKeyExchange|dh_compute_key)\b",
        "algorithm": "Diffie-Hellman",
        "category": "Asymmetric Key Exchange",
        "quantum_status": "Vulnerable (Shor's Algorithm)",
        "security_level": "Broken by CRQC",
        "replacement": "ML-KEM-768 / Hybrid X25519+ML-KEM",
        "risk_score": 9.0
    },
    {
        "pattern": r"\b(AES_128|AES-128|AES128|AES/CBC/PKCS5Padding)\b",
        "algorithm": "AES-128",
        "category": "Symmetric Block Cipher",
        "quantum_status": "Weakened (Grover's Algorithm reduces effective strength to 64 bits)",
        "security_level": "Marginal under Grover",
        "replacement": "AES-256 (maintains 128-bit quantum security)",
        "risk_score": 6.0
    },
    {
        "pattern": r"\b(AES_256|AES-256|AES256|AES/GCM/NoPadding)\b",
        "algorithm": "AES-256",
        "category": "Symmetric Block Cipher",
        "quantum_status": "Quantum Safe",
        "security_level": "128-bit Post-Quantum Secure",
        "replacement": "None Required",
        "risk_score": 1.0
    },
    {
        "pattern": r"\b(DES|3DES|TripleDES|DESede)\b",
        "algorithm": "Triple-DES (3DES)",
        "category": "Legacy Symmetric Cipher",
        "quantum_status": "Deprecated & Quantum Vulnerable",
        "security_level": "Critically Insecure",
        "replacement": "AES-256-GCM",
        "risk_score": 10.0
    },
    {
        "pattern": r"\b(SHA1|SHA-1|md5|MD5)\b",
        "algorithm": "SHA-1 / MD5",
        "category": "Cryptographic Hash Function",
        "quantum_status": "Legacy Broken (Classical Collision Attacks)",
        "security_level": "Insecure",
        "replacement": "SHA-256 / SHA-384 / SHA-3 / SHAKE-256",
        "risk_score": 8.5
    },
    {
        "pattern": r"\b(ML-KEM|Kyber|ML-KEM-512|ML-KEM-768|ML-KEM-1024)\b",
        "algorithm": "ML-KEM (CRYSTALS-Kyber)",
        "category": "Post-Quantum Key Encapsulation (FIPS 203)",
        "quantum_status": "Quantum Safe (NIST Standard)",
        "security_level": "NIST Security Categories 1, 3, 5",
        "replacement": "Target Standard",
        "risk_score": 0.0
    },
    {
        "pattern": r"\b(ML-DSA|Dilithium|ML-DSA-44|ML-DSA-65|ML-DSA-87)\b",
        "algorithm": "ML-DSA (CRYSTALS-Dilithium)",
        "category": "Post-Quantum Digital Signature (FIPS 204)",
        "quantum_status": "Quantum Safe (NIST Standard)",
        "security_level": "NIST Security Categories 2, 3, 5",
        "replacement": "Target Standard",
        "risk_score": 0.0
    }
]

def scan_file_for_crypto(file_path: str) -> List[Dict[str, Any]]:
    """Inspects a single source file for cryptographic invocations."""
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line_no, line in enumerate(lines, start=1):
                for rule in CRYPTO_SIGNATURES:
                    match = re.search(rule["pattern"], line, re.IGNORECASE)
                    if match:
                        findings.append({
                            "algorithm": rule["algorithm"],
                            "matched_text": match.group(0),
                            "category": rule["category"],
                            "quantum_status": rule["quantum_status"],
                            "security_level": rule["security_level"],
                            "replacement": rule["replacement"],
                            "risk_score": rule["risk_score"],
                            "file": os.path.relpath(file_path),
                            "line_number": line_no,
                            "snippet": line.strip()
                        })
    except Exception as e:
        print(f"[!] Error scanning {file_path}: {e}")
    return findings

def generate_cbom(target_dir: str, project_name: str = "Enterprise_Microservice_Core") -> Dict[str, Any]:
    """Scans an entire directory tree and compiles an OWASP CycloneDX CBOM structure."""
    all_findings = []
    files_scanned = 0

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith((".py", ".java", ".c", ".cpp", ".js", ".ts", ".go", ".cs", ".yaml", ".json")):
                full_path = os.path.join(root, file)
                findings = scan_file_for_crypto(full_path)
                all_findings.extend(findings)
                files_scanned += 1

    # Aggregate metrics
    vuln_count = sum(1 for f in all_findings if f["risk_score"] >= 6.0)
    safe_count = sum(1 for f in all_findings if f["risk_score"] == 0.0)
    avg_risk = sum(f["risk_score"] for f in all_findings) / max(len(all_findings), 1)

    cbom_data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:{hashlib.md5(project_name.encode()).hexdigest()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": {
                "name": project_name,
                "type": "application",
                "version": "1.0.0"
            },
            "tools": [
                {
                    "vendor": "IBM Quantum Safe / Quantum for Humanity",
                    "name": "CBOM Discovery Scanner",
                    "version": "2026.1"
                }
            ],
            "summary": {
                "files_scanned": files_scanned,
                "total_crypto_assets": len(all_findings),
                "quantum_vulnerable_assets": vuln_count,
                "quantum_safe_assets": safe_count,
                "composite_risk_score": round(avg_risk, 2)
            }
        },
        "cryptographicAssets": all_findings
    }
    return cbom_data

if __name__ == "__main__":
    print("================================================================================")
    print("  IBM Quantum Safe Discovery — Cryptographic Bill of Materials (CBOM) Engine   ")
    print("================================================================================")
    
    # Run scan on the current codebase
    scan_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    print(f"[*] Initiating discovery scan on: {scan_path}\n")
    
    cbom = generate_cbom(scan_path, "QFF2026_Enterprise_Platform")
    
    output_cbom_path = os.path.join(os.path.dirname(__file__), "cbom_output.json")
    with open(output_cbom_path, "w", encoding="utf-8") as out:
        json.dump(cbom, out, indent=2)
        
    print(f"[+] Scan Complete!")
    print(f"    - Files Analyzed:          {cbom['metadata']['summary']['files_scanned']}")
    print(f"    - Crypto Assets Found:     {cbom['metadata']['summary']['total_crypto_assets']}")
    print(f"    - Quantum Vulnerable:      {cbom['metadata']['summary']['quantum_vulnerable_assets']}")
    print(f"    - Quantum Safe Certified:  {cbom['metadata']['summary']['quantum_safe_assets']}")
    print(f"    - Enterprise Risk Index:   {cbom['metadata']['summary']['composite_risk_score']} / 10.0")
    print(f"\n[+] Standardized CBOM JSON exported to: {output_cbom_path}")
