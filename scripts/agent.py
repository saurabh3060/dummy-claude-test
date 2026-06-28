import os
import requests

# Read Jira issue from workflow env variables
summary = os.getenv("ISSUE_SUMMARY", "")
description = os.getenv("ISSUE_DESCRIPTION", "")

# Read existing file
with open("src/greeting.js", "r") as f:
    current_code = f.read()

# PROMPT GOES HERE
prompt = f"""
You are a senior JavaScript developer.

Jira Issue Summary:
{summary}

Jira Issue Description:
{description}

Current file: src/greeting.js

Existing code:

{current_code}

Update the code to satisfy the Jira requirement.

Return ONLY the complete updated JavaScript file.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }
)

updated_code = response.json()["response"]

# Save modified file
with open("src/greeting.js", "w") as f:
    f.write(updated_code)

print("File updated successfully")
