import os
import requests

# Read Jira details from GitHub Action
issue_key = os.getenv("ISSUE_KEY", "NO-KEY")
summary = os.getenv("ISSUE_SUMMARY", "")
description = os.getenv("ISSUE_DESCRIPTION", "")

print(f"Processing Jira Ticket: {issue_key}")
print(f"Summary: {summary}")

# File to modify
file_path = "src/greeting.js"

# Read existing code
with open(file_path, "r", encoding="utf-8") as f:
    current_code = f.read()

# Build prompt
prompt = f"""
You are a senior JavaScript developer.

Jira Ticket: {issue_key}

Summary:
{summary}

Description:
{description}

Current file path:
{file_path}

Current source code:

{current_code}

Task:
Update the code according to the Jira ticket.

Rules:
1. Keep existing functionality unless ticket requires changes.
2. Return ONLY raw JavaScript code.
3. Do not return markdown.
4. Do not explain anything.
"""

print("Sending prompt to Ollama...")

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False
    },
    timeout=600
)

response.raise_for_status()

updated_code = response.json()["response"].strip()

print("Received response from Ollama")

# Save updated file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(updated_code)

print(f"{file_path} updated successfully.")
