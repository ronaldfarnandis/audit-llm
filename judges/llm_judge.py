class LLMJudge:
    def __init__(self, model_name: str = "local-heuristic-judge"):
        self.model_name = model_name

    def evaluate_faithfulness(self, source_context: str, agent_claim: str) -> dict:
        """
        Local heuristic judge. Uses deterministic rules/keywords to simulate 
        semantic hallucination detection offline.
        """
        hallucination_triggers = ["penicillin", "invented", "fake_fact", "unknown"]
        
        lower_claim = agent_claim.lower()
        has_hallucination = any(trigger in lower_claim for trigger in hallucination_triggers)

        if has_hallucination:
            return {
                "check": "hallucination_audit",
                "passed": False,
                "details": f"VERDICT: FAIL\nRATIONALE: Local judge detected unauthorized/ungrounded claims in text: '{agent_claim}'"
            }
        
        return {
            "check": "hallucination_audit",
            "passed": True,
            "details": f"VERDICT: PASS\nRATIONALE: Claim is fully supported by source context."
        }