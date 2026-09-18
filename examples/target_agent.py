import time

def mock_target_agent(prompt: str) -> dict:
    """
    Simulates a target LLM agent. 
    It intentionally behaves differently based on the prompt to test your auditor's error detection.
    """
    if "fail_latency" in prompt:
        time.sleep(2.5)

    if "bad_json" in prompt:
        return {"raw_output": "Here is your data: name: John Doe, age: thirty"} # Invalid schema
    
    if "hallucinate" in prompt:
        return {
            "summary": "The patient was prescribed 500mg of Penicillin and diagnosed with acute bronchitis.",
            "confidence": 0.99
        }

    return {
        "summary": "The patient was prescribed 500mg of Amoxicillin and diagnosed with mild sinusitis.",
        "confidence": 0.95
    }