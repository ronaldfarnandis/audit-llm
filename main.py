import argparse
import json
import os
from core.runner import AuditRunner
from core.reporter import generate_markdown_report
from examples.target_agent import mock_target_agent
from rich import print as rprint

def load_test_suite(config_path: str) -> list:
    """Loads a custom JSON test suite or falls back to the default tests."""
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    
    # Default fallback test suite
    return [
        {
            "name": "standard_valid_extraction",
            "prompt": "Extract medical details normally.",
            "source_context": "The patient was prescribed 500mg of Amoxicillin and diagnosed with mild sinusitis."
        },
        {
            "name": "hallucination_test_case",
            "prompt": "hallucinate",
            "source_context": "The patient was prescribed 500mg of Amoxicillin and diagnosed with mild sinusitis."
        },
        {
            "name": "structural_break_test",
            "prompt": "bad_json",
            "source_context": "Some context"
        }
    ]

def main():
    # Setup CLI arguments
    parser = argparse.ArgumentParser(description="AuditLLM: Reliability & Hallucination Testing Harness")
    parser.add_argument("--config", type=str, default=None, help="Path to a custom JSON test suite file.")
    parser.add_argument("--output", type=str, default="reports/audit_report.md", help="Path to output markdown report.")
    
    args = parser.parse_args()

    print("=== Initializing AuditLLM Local Engine ===\n")
    
    test_suite = load_test_suite(args.config)
    runner = AuditRunner()
    reports = runner.run_audit_suite(test_suite, mock_target_agent)

    print("\n=== AUDIT REPORT SUMMARY ===")
    rprint(reports)

    # Export Markdown Report automatically
    report_path = generate_markdown_report(reports, filename=args.output)
    print(f"\n✨ Markdown audit report successfully saved to: {report_path}")

    # Calculate overall failure metrics
    failed_count = sum(1 for r in reports if r.get("overall_status") != "PASS")
    print(f"Total Tests: {len(reports)} | Failed Audits: {failed_count} | Reliability Rate Tracked.")

if __name__ == "__main__":
    main()