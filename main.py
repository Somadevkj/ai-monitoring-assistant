from braintrust import init_logger
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

GROQ_KEY = os.getenv("GROQ_API_KEY")
BRAINTRUST_KEY = os.getenv("BRAINTRUST_API_KEY")

if not BRAINTRUST_KEY or not GROQ_KEY:
    raise ValueError("Missing API keys! Ensure GROQ_API_KEY and BRAINTRUST_API_KEY are set in .env")

# 1. Initialize Logger directly with your project name and API key
logger = init_logger(
    project="ai-monitoring-assistant",
    api_key=BRAINTRUST_KEY
)

client = Groq(api_key=GROQ_KEY)

def customer_support_agent(user_query: str) -> str:
    """
    AI agent that logs directly to Braintrust via logger.log()
    """
    # Call Groq (Llama 3.3 70B)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant for Elchai. Answer questions clearly and concisely."
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=500,
    )
    
    output_text = response.choices[0].message.content
    
    # 2. Directly log input and output to Braintrust Logger
    logger.log(
        input=user_query,
        output=output_text,
        metadata={"model": "llama-3.3-70b-versatile"}
    )
    
    return output_text

if __name__ == "__main__":
    print("=" * 60)
    print("AI Tool Monitoring Assistant - Direct Logging Test")
    print("=" * 60)
    
    test_queries = [
        "How do I reset my password?",
        "What is your refund policy?",
        "How can I contact support?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Test {i}] Sending query: '{query}'...")
        reply = customer_support_agent(query)
        print(f"Response: {reply}")
        print("-" * 60)
    
    # 3. Explicitly flush the logger object
    print("\nSyncing logs to Braintrust servers...")
    logger.flush()
    print("✓ Success! Log sync complete.")