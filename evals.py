from braintrust import Eval, init
from groq import Groq
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv(override=True)

GROQ_KEY = os.getenv("GROQ_API_KEY")
BRAINTRUST_KEY = os.getenv("BRAINTRUST_API_KEY")

if not BRAINTRUST_KEY or not GROQ_KEY:
    raise ValueError("Missing API keys! Ensure GROQ_API_KEY and BRAINTRUST_API_KEY are set in .env")

# 2. Initialize Braintrust
init(
    project="ai-monitoring-assistant",
    api_key=BRAINTRUST_KEY
)

# 3. Initialize Groq Client
client = Groq(api_key=GROQ_KEY)

# 4. Define the Agent Task Function
def customer_support_task(input_text):
    """
    Calls the live Groq Llama 3.3 model with the test query.
    """
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant for Elchai. Answer questions clearly and concisely."
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content

# 5. Evaluation Dataset
eval_dataset = [
    {
        "input": "How do I reset my password?",
        "expected": "Go to Settings > Account > Reset Password",
    },
    {
        "input": "What's your refund policy?",
        "expected": "30-day money-back guarantee",
    },
    {
        "input": "How can I contact support?",
        "expected": "support@elchai.com or 1-800-555-0123",
    },
    {
        "input": "Can I get a refund?",
        "expected": "Yes, within 30 days",
    },
    {
        "input": "What are your hours?",
        "expected": "Monday-Friday, 9am-5pm EST",
    },
]

# 6. Define Custom Scorer Functions
def exact_match_scorer(input, output, expected):
    keywords = expected.lower().split()
    matched = sum(1 for word in keywords if word in output.lower())
    return matched / len(keywords) if keywords else 1.0

def completeness_scorer(input, output, expected):
    return 1.0 if len(output.strip()) > 10 else 0.0

# 7. Run the Evaluation
if __name__ == "__main__":
    print("=" * 60)
    print("Running Customer Support Evaluation on Braintrust...")
    print("=" * 60)

    Eval(
        name="ai-monitoring-assistant",
        data=eval_dataset,
        task=customer_support_task,
        scores=[exact_match_scorer, completeness_scorer],
    )

    print("\n✓ Evaluation complete!")
    print("View results under Experiments/Evals at: https://www.braintrust.dev/app")