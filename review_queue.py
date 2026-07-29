import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Define thresholds for auto-approve vs. human review
THRESHOLDS = {
    "exact_match_scorer": 0.50,
    "completeness_scorer": 0.80,
}

def needs_human_review(scores):
    """
    Check if any metric score falls below threshold.
    Returns (True, reason) if human review is required.
    """
    for metric, threshold in THRESHOLDS.items():
        score_value = scores.get(metric, 1.0)
        if score_value < threshold:
            return True, f"{metric} score ({score_value:.2f}) below threshold ({threshold})"
    return False, "All scores meet or exceed threshold"


def check_trace_for_review(trace_id):
    """
    Evaluate trace metric scores to determine review queue placement.
    """
    # Example 1: High quality response (Auto-Approved)
    good_scores = {
        "exact_match_scorer": 1.00,
        "completeness_scorer": 1.00,
    }
    
    # Example 2: Low quality response (Pending Human Review)
    bad_scores = {
        "exact_match_scorer": 0.33,
        "completeness_scorer": 1.00,
    }
    
    print("=" * 60)
    print("AI Tool Monitoring Assistant - Human Review Queue Checker")
    print("=" * 60)
    
    # Check good trace
    print(f"\n[Trace 1: {trace_id}_good] Evaluating scores...")
    needs_review, reason = needs_human_review(good_scores)
    if needs_review:
        print(f"Status: 🔴 PENDING HUMAN REVIEW")
        print(f"Reason: {reason}")
    else:
        print(f"Status: 🟢 AUTO-APPROVED")
        print(f"Reason: {reason}")
    
    # Check bad trace
    print(f"\n[Trace 2: {trace_id}_bad] Evaluating scores...")
    needs_review, reason = needs_human_review(bad_scores)
    if needs_review:
        print(f"Status: 🔴 PENDING HUMAN REVIEW")
        print(f"Reason: {reason}")
    else:
        print(f"Status: 🟢 AUTO-APPROVED")
        print(f"Reason: {reason}")
    
    print("\n✓ Review queue threshold evaluation complete!")


if __name__ == "__main__":
    check_trace_for_review("trace_sample_001")