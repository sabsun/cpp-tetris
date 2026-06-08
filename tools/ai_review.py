#!/usr/bin/env python

import json
import subprocess
import sys
import time
import urllib2

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3-coder:480b-cloud"

MAX_DIFF_SIZE = 12000
MAX_FILE_SIZE = 15000


def get_staged_diff():
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--cached"]
        )

        if len(diff) > MAX_DIFF_SIZE:
            diff = diff[:MAX_DIFF_SIZE]

        return diff

    except Exception:
        return ""


def get_staged_files():
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"]
        )

        files = []

        for line in output.splitlines():
            line = line.strip()

            if not line:
                continue

            if (
                line.endswith(".cpp")
                or line.endswith(".h")
                or line.endswith(".hpp")
                or line.endswith(".c")
            ):
                files.append(line)

        return files

    except Exception:
        return []


def get_file_content(filename):
    try:
        content = subprocess.check_output(
            ["git", "show", ":" + filename]
        )

        if len(content) > MAX_FILE_SIZE:
            content = content[:MAX_FILE_SIZE]

        return content

    except Exception:
        return ""


def build_context():
    diff_text = get_staged_diff()

    files = get_staged_files()

    context = []

    context.append(
        "================ DIFF ================\n"
    )

    context.append(diff_text)

    for filename in files:
        context.append(
            "\n\n=========== FILE: %s ===========\n"
            % filename
        )

        context.append(
            get_file_content(filename)
        )

    return "".join(context)


def build_prompt(context):
    return """
You are a senior C++ reviewer.

You will receive:

1. Git diff
2. Full content of modified files

Review the change carefully.

Focus on:

* bug introduction
* null pointer issues
* memory leaks
* resource leaks
* use-after-free
* double free
* buffer overflow
* security vulnerabilities
* race conditions
* broken logic
* dead code

Ignore:

* formatting
* comments
* naming
* TODO
* FIXME

Review using BOTH:

* the diff
* the file contents

Return ONLY valid JSON.

PASS:

{"status":"PASS","issues":[]}

FAIL:

{"status":"FAIL","issues":["reason"]}

Code Context:

%s
""" % context


def parse_ai_response(text):
    text = text.strip()

    if text == "PASS":
        return {
            "status": "PASS",
            "issues": [],
        }

    try:
        return json.loads(text)

    except Exception:
        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:
            try:
                return json.loads(
                    text[start:end + 1]
                )

            except Exception:
                pass

        return {
            "status": "FAIL",
            "issues": [
                "AI reviewer returned invalid JSON",
            ],
        }


def run_ai_review():
    review_context = build_context()

    if not review_context.strip():
        return {
            "status": "PASS",
            "issues": [],
        }

    sys.stderr.write(
        "Review context size: %d bytes\n"
        % len(review_context)
    )
    payload = {
        "model": MODEL,
        "prompt": build_prompt(review_context),
        "stream": False,
    }
    sys.stderr.write("\n===== PAYLOAD START =====\n")
    sys.stderr.write(json.dumps(payload, indent=2))
    sys.stderr.write("\n===== PAYLOAD END =====\n")

    try:
        req = urllib2.Request(
            OLLAMA_URL,
            json.dumps(payload),
            {
                "Content-Type": "application/json",
            },
        )

        start = time.time()

        response = urllib2.urlopen(
            req,
            timeout=60
        )

        elapsed = time.time() - start

        sys.stderr.write(
            "AI review took %.2f seconds\n"
            % elapsed
        )

        result = json.loads(
            response.read()
        )

        text = result.get(
            "response",
            ""
        )

        return parse_ai_response(text)

    except Exception as e:
        return {
            "status": "FAIL",
            "issues": [
                "AI review error: %s" % str(e),
            ],
        }


if __name__ == "__main__":
    result = run_ai_review()

    print(
        json.dumps(
            result,
            ensure_ascii=True
        )
    )