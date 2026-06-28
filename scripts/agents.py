import os

issue = os.environ["ISSUE_DESCRIPTION"]

files = []

for root, dirs, filenames in os.walk("."):
    for f in filenames:
        if f.endswith((".py", ".js", ".ts", ".java")):
            files.append(os.path.join(root, f))
