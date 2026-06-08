import os
import subprocess
import requests

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434",
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3-coder:480b-cloud",
)


def run(cmd):
    return subprocess.check_output(
        cmd,
        shell=True,
        text=True,
    ).strip()


def get_changed_files():
    try:
        files = run("git diff --name-only HEAD~1 HEAD")
        return [f for f in files.splitlines() if f]
    except Exception:
        return []


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def ask_ollama(prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )

    response.raise_for_status()

    return response.json()["response"]


def main():
    print("Checking Ollama...")

    tags = requests.get(
        f"{OLLAMA_URL}/api/tags",
        timeout=10,
    )

    tags.raise_for_status()

    print("Ollama reachable")

    files = get_changed_files()

    if not files:
        print("No changed files found")
        return

    print(f"Files under review: {len(files)}")

    for file in files:
        if not (
            file.endswith(".py")
            or file.endswith(".cpp")
            or file.endswith(".c")
            or file.endswith(".h")
            or file.endswith(".hpp")
        ):
            continue

        print(f"Reviewing {file}")

        content = read_file(file)

        if not content:
            continue

        prompt = f"""
You are a senior software engineer.

Review this file and provide:

1. Bugs
2. Security issues
3. Performance issues
4. Code quality improvements
5. Overall summary

File: {file}

Code:

```text
{content[:15000]}
"""

        try:
            review = ask_ollama(prompt)

            print("=" * 80)
            print(file)
            print("=" * 80)
            print(review)
            print()

        except Exception as e:
            print(f"Failed to review {file}: {e}")
            print()


if __name__ == "__main__":
    main()