import time
from pydantic import BaseModel
from core.checker import check_structural_integrity, check_latency
from judges.llm_judge import LLMJudge

class AgentOutputSchema(BaseModel):
    summary: str
    confidence: float

class AuditRunner:
    def __init__(self):
        self.judge = LLMJudge()

    def run_audit_suite(self, test_cases: list, target_func) -> list:
        audit_reports = []

        for idx, test in enumerate(test_cases):
            print(f"Running audit test case {idx + 1}/{len(test_cases)}: {test['name']}")
            
            start_time = time.time()
            try:
                output = target_func(test["prompt"])
            except Exception as e:
                audit_reports.append({
                    "test_name": test["name"],
                    "overall_status": "CRITICAL_FAILURE",
                    "error": str(e)
                })
                continue

            # 1. Deterministic Checks
            schema_result = check_structural_integrity(output, AgentOutputSchema)
            latency_result = check_latency(start_time, max_latency_sec=2.0)

            # 2. Semantic Judge Checks (Only run if schema passed)
            semantic_result = {"passed": True, "details": "Skipped due to schema failure"}
            if schema_result["passed"] and "source_context" in test:
                semantic_result = self.judge.evaluate_faithfulness(
                    source_context=test["source_context"],
                    agent_claim=output.get("summary", "")
                )

            # Aggregate results
            test_passed = schema_result["passed"] and latency_result["passed"] and semantic_result["passed"]

            audit_reports.append({
                "test_name": test["name"],
                "overall_status": "PASS" if test_passed else "FAIL",
                "checks": {
                    "schema": schema_result,
                    "latency": latency_result,
                    "semantic_faithfulness": semantic_result
                }
            })

        return audit_reports