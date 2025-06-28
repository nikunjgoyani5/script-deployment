# gpt_runner.py
import openai
import sys
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = sys.argv[1]

USAGE_FILE = "usage.json"
MAX_DOLLARS = 10
COST_PER_1K_TOKENS = 0.002

# Load usage
if os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, "r") as f:
        usage = json.load(f)
else:
    usage = {"total_tokens": 0}

def estimate_cost(tokens):
    return (tokens / 1000) * COST_PER_1K_TOKENS

def log_tokens(tokens):
    usage["total_tokens"] += tokens
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)

try:
    estimated_cost = estimate_cost(usage["total_tokens"])
    if estimated_cost >= MAX_DOLLARS:
        print("Error: Usage cap reached ($10). Halting execution.")
        sys.exit(1)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    tokens_used = response['usage']['total_tokens']
    log_tokens(tokens_used)
    result = response['choices'][0]['message']['content']
    print(result)

except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
