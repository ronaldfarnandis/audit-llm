import time
from typing import Dict, Any, Type
from pydantic import BaseModel, ValidationError

def check_structural_integrity(response_data: Any, expected_schema: Type[BaseModel]) -> Dict[str, Any]:
    """Validates if the output matches a strict Pydantic schema."""
    if not isinstance(response_data, dict):
        return {
            "check": "schema_validation",
            "passed": False,
            "error": "Output is not a valid JSON object dictionary."
        }
    
    try:
        expected_schema(**response_data)
        return {"check": "schema_validation", "passed": True, "error": None}
    except ValidationError as e:
        return {
            "check": "schema_validation",
            "passed": False,
            "error": str(e)
        }

def check_latency(start_time: float, max_latency_sec: float = 2.0) -> Dict[str, Any]:
    """Ensures the agent meets performance SLAs."""
    duration = time.time() - start_time
    passed = duration <= max_latency_sec
    return {
        "check": "latency_sla",
        "passed": passed,
        "duration_sec": round(duration, 3),
        "error": None if passed else f"Latency {duration:.2f}s exceeded threshold {max_latency_sec}s"
    }