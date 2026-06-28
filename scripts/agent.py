import os
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

issue_key = os.getenv("ISSUE_KEY", "NO-KEY")
summary = os.getenv("ISSUE_SUMMARY", "")
description = os.getenv("ISSUE_DESCRIPTION", "")

print(f"Processing {issue_key}")

# ------------------------------------------
# Read repository files
# ------------------------------------------

repo_context = []

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv"
}

EXCLUDED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif",
    ".pdf", ".zip", ".exe"
}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

    for file in files:

        ext = os.path.splitext(file)[1]

        if ext in EXCLUDED_EXTENSIONS:
            continue

        path = os.path.join(root, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            repo_context.append({
                "path": path,
                "content": content[:8000]   # avoid huge prompts
            })

        except Exception:
            pass

# ------------------------------------------
# Prompt
# ------------------------------------------

prompt = f"""
You are an expert software engineer.

Jira Ticket: {issue_key}

Summary:
{summary}

Description:
{description}

Repository files:

{json.dumps(repo_context, indent=2)}

Your task:

1. Analyze the Jira ticket.
2. Decide which existing files should be modified.
3. Create new files if required.
4. Return ALL required file changes.

IMPORTANT:

Return ONLY valid JSON.

Format:

{{
  "files": [
    {{
      "path": "src/example.js",
      "content": "full file contents"
    }},
    {{
      "path": "src/newFile.js",
      "content": "new file contents"
    }}
  ]
}}

Rules:
- Include complete file contents.
- Do not return markdown.
- Do not explain.
- Return valid JSON only.
"""

print("Sending prompt to Ollama...")

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    },
    timeout=900
)

response.raise_for_status()

result = response.json()["response"]

print(result)

# ------------------------------------------
# Parse JSON
# ------------------------------------------

try:
    data = json.loads(result)

except json.JSONDecodeError:
    print("Invalid JSON returned by model")
    exit(1)

# ------------------------------------------
# Write files
# ------------------------------------------

updated = []

for file_info in data.get("files", []):

    path = file_info["path"]
    content = file_info["content"]

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    updated.append(path)

print("\nUpdated files:")
for f in updated:
    print("-", f)
