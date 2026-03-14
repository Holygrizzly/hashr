from fastapi import APIRouter, Request, Header
from pathlib import Path
from web3 import Web3
import os

from .payment import verify_payment

router = APIRouter(prefix="/contract", tags=["contracts"])

VERSION = Path("VERSION").read_text().strip()

RPC_URL = os.getenv("ETH_RPC_URL", "https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC_URL))


@router.post("/analyze")
def analyze_contract(
    payload: dict,
    request: Request,
    X_402_payment: str | None = Header(None, alias="X-402-Payment"),
):
    verify_payment(job_id="contract_analyze", request=request, x_402_payment=X_402_payment)

    address = payload.get("address")

    if not address:
        return {"error": "contract address required"}

    code = w3.eth.get_code(address).hex()

    dangerous_opcodes = [
        "selfdestruct",
        "suicide",
        "delegatecall",
        "callcode",
    ]
    dangerous_opcode_detected = False
    for opcode in dangerous_opcodes:
        if opcode in code.lower():
            dangerous_opcode_detected = True
            break

    owner_address = None
    ownership_renounced = False
    try:
        owner_abi = [
            {
                "constant": True,
                "inputs": [],
                "name": "owner",
                "outputs": [{"name": "", "type": "address"}],
                "type": "function",
            }
        ]
        contract = w3.eth.contract(address=address, abi=owner_abi)
        owner_address = contract.functions.owner().call()
        if owner_address == "0x0000000000000000000000000000000000000000":
            ownership_renounced = True
    except Exception:
        owner_address = None

    has_code = code != "0x"
    code_size = len(code)

    proxy_pattern = "delegatecall" in code.lower()
    owner_pattern = "owner" in code.lower()

    honeypot_pattern = False
    suspicious_terms = [
        "revert",
        "require",
        "assert",
        "stop",
    ]
    for term in suspicious_terms:
        if term in code.lower():
            honeypot_pattern = True
            break

    implementation_address = None
    try:
        slot = "0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC"
        raw = w3.eth.get_storage_at(address, slot).hex()
        if raw and raw != "0x":
            implementation_address = "0x" + raw[-40:]
    except Exception:
        implementation_address = None

    upgradeable_proxy = False
    if implementation_address and not ownership_renounced:
        upgradeable_proxy = True

    erc20_functions = [
        "70a08231",  # balanceOf
        "a9059cbb",  # transfer
        "095ea7b3",  # approve
        "23b872dd",  # transferFrom
    ]
    erc20_detected = False
    for sig in erc20_functions:
        if sig in code.lower():
            erc20_detected = True
            break

    verified_contract = False
    metadata_markers = [
        "a2646970667358",  # solc metadata prefix
        "solc",
        "ipfs",
    ]
    for marker in metadata_markers:
        if marker in code.lower():
            verified_contract = True
            break

    tax_pattern = False
    tax_keywords = [
        "tax",
        "fee",
        "maxsell",
        "maxsellamount",
        "maxtransaction",
        "tradingenabled",
    ]
    for keyword in tax_keywords:
        if keyword in code.lower():
            tax_pattern = True
            break

    risk_score = 0
    if not has_code:
        risk_score += 50
    if proxy_pattern:
        risk_score += 20
    if dangerous_opcode_detected:
        risk_score += 30
    if owner_pattern:
        risk_score += 10
    if honeypot_pattern:
        risk_score += 20
    if tax_pattern:
        risk_score += 20
    if not verified_contract:
        risk_score += 5
    if upgradeable_proxy:
        risk_score += 20

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 20:
        risk_level = "medium"
    else:
        risk_level = "low"

    flags = {
        "no_code": not has_code,
        "proxy_pattern": proxy_pattern,
        "ownership_pattern": owner_pattern,
        "honeypot_pattern": honeypot_pattern,
        "token_tax_pattern": tax_pattern,
        "erc20_detected": erc20_detected,
        "verified_contract": verified_contract,
        "dangerous_opcode": dangerous_opcode_detected,
        "upgradeable_proxy": upgradeable_proxy,
        "owner_detected": owner_address is not None,
        "ownership_renounced": ownership_renounced,
        "proxy_implementation_detected": implementation_address is not None,
    }

    return {
        "service": "hashr",
        "version": VERSION,
        "analysis": {
            "address": address,
            "has_code": has_code,
            "code_size": code_size,
            "proxy_pattern_detected": proxy_pattern,
            "ownership_pattern_detected": owner_pattern,
            "implementation_address": implementation_address,
            "owner_address": owner_address,
            "ownership_renounced": ownership_renounced,
            "erc20_detected": erc20_detected,
            "verified_contract": verified_contract,
            "dangerous_opcode_detected": dangerous_opcode_detected,
            "upgradeable_proxy_detected": upgradeable_proxy,
            "token_tax_pattern_detected": tax_pattern,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "flags": flags,
            "status": "basic-security-analysis",
        },
    }
