import os
import json
import requests
import sys
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

print("=" * 80)
print("AI AGENT STARTED")
print("=" * 80)

# -------------------------------------------------------------------
# Read Jira details
# -------------------------------------------------------------------

issue_key = os.getenv("ISSUE_KEY", "NO-KEY")
summary = os.getenv("ISSUE_SUMMARY", "")
description = os.getenv("ISSUE_DESCRIPTION", "")

print(f"[INFO] ISSUE_KEY        : {issue_key}")
print(f"[INFO] ISSUE_SUMMARY   : {summary}")
print(f"[INFO] ISSUE_DESCRIPTION length: {len(description)}")

# -------------------------------------------------------------------
# Read repository files
# -------------------------------------------------------------------

repo_context = []

SOURCE_DIR = "./src"

print(f"[INFO] Looking for source files inside: {SOURCE_DIR}")

if not os.path.exists(SOURCE_DIR):
    print(f"[WARNING] {SOURCE_DIR} folder does not exist")
else:

    for root, dirs, files in os.walk(SOURCE_DIR):

        print(f"[DEBUG] Entering folder: {root}")

        for file in files:

            path = os.path.join(root, file)

            print(f"[DEBUG] Reading file: {path}")

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                print(f"[DEBUG] Read {len(content)} chars from {path}")

                repo_context.append({
                    "path": path,
                    "content": content[:3000]
                })

            except Exception as e:
                print(f"[ERROR] Failed reading {path}")
                print(e)

print(f"[INFO] Total files discovered: {len(repo_context)}")

for f in repo_context:
    print(f"[INFO] Included file: {f['path']}")

# -------------------------------------------------------------------
# Build prompt
# -------------------------------------------------------------------

print("[INFO] Building prompt")

prompt = f"""
You are an expert software engineer.

Jira Ticket: {issue_key}

Summary:
{summary}

Description:
{description}

Repository files:

{json.dumps(repo_context, indent=2)}

Task:
1. Analyze the Jira ticket.
2. Modify existing files if needed.
3. Create new files if needed.
4. Return ALL changed files.

Return ONLY valid JSON.

Example:

{{
  "files": [
    {{
      "path": "src/Login.js",
      "content": "complete file contents"
    }},
    {{
      "path": "src/Login.css",
      "content": "complete css contents"
    }}
  ]
}}

Rules:
- Return complete file contents.
- No markdown.
- No explanation.
- JSON only.
"""

print(f"[INFO] Prompt size: {len(prompt)} characters")

# -------------------------------------------------------------------
# Call Ollama
# -------------------------------------------------------------------

print("[INFO] Sending request to Ollama")
start = time.time()

try:

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=900
    )

    elapsed = round(time.time() - start, 2)

    print(f"[INFO] Ollama response received in {elapsed} seconds")
    print(f"[INFO] HTTP Status: {response.status_code}")

    response.raise_for_status()

except Exception as e:
    print("[ERROR] Failed calling Ollama")
    print(e)
    sys.exit(1)

# -------------------------------------------------------------------
# Parse response
# -------------------------------------------------------------------

print("[INFO] Parsing model response")

try:
    result = response.json()["response"]

    print(f"[INFO] Model response length: {len(result)}")

except Exception as e:
    print("[ERROR] Could not extract response")
    print(e)
    print(response.text)
    sys.exit(1)

print("=" * 80)
print("MODEL OUTPUT")
print("=" * 80)
print(result[:5000])
print("=" * 80)

# -------------------------------------------------------------------
# Convert JSON
# -------------------------------------------------------------------

try:
    data = json.loads(result)

    print("[INFO] JSON parsed successfully")

except Exception as e:

    print("[ERROR] Invalid JSON from model")
    print(e)

    with open("ollama_raw_output.txt", "w") as f:
        f.write(result)

    print("[INFO] Saved raw output to ollama_raw_output.txt")

    sys.exit(1)

# -------------------------------------------------------------------
# Write files
# -------------------------------------------------------------------

updated_files = []

for file_info in data.get("files", []):

    path = file_info["path"]
    content = file_info["content"]

    print(f"[INFO] Writing file: {path}")

    try:

        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        updated_files.append(path)

        print(f"[SUCCESS] Updated {path}")

    except Exception as e:

        print(f"[ERROR] Failed writing {path}")
        print(e)

print("=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"Files updated: {len(updated_files)}")

for f in updated_files:
    print(f" - {f}")

if len(updated_files) == 0:
    print("[WARNING] No files updated")

print("=" * 80)
print("AI AGENT FINISHED")
print("=" * 80)
