#!/usr/bin/env python

import json
import os
import re
import subprocess
import sys
import time

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"-----BEGIN PRIVATE KEY-----",
    r"github_pat_",
    r"ghp_[A-Za-z0-9]+",
    r"Bearer\s+[A-Za-z0-9\-_\.]+",
]

IGNORE_FILES = [
    "tools/review_agent.py",
]

IGNORE_PREFIXES = [
    "reviews/",
]

SOURCE_EXTENSIONS = [
    ".cpp",
    ".c",
    ".h",
    ".hpp",
]


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

            valid_extension = False

            for ext in SOURCE_EXTENSIONS:
                if line.endswith(ext):
                    valid_extension = True
                    break

            if not valid_extension:
                continue

            skip = False

            if line in IGNORE_FILES:
                skip = True

            for prefix in IGNORE_PREFIXES:
                if line.startswith(prefix):
                    skip = True
                    break

            if not skip:
                files.append(line)

        return files

    except Exception as e:
        print("Failed to get staged files")
        print(str(e))
        sys.exit(1)


def get_staged_content(filename):
    try:
        content = subprocess.check_output(
            ["git", "show", ":" + filename]
        )

        if not isinstance(content, str):
            content = content.decode("utf-8", "ignore")

        return content

    except Exception:
        return ""


def check_secret_patterns(content):
    matches = []

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content):
            matches.append(pattern)

    return matches


def run_checks(files):
    errors = []

    for filename in files:
        content = get_staged_content(filename)

        if not content:
            continue

        if "TODO" in content:
            errors.append(
                "%s contains TODO" % filename
            )

        if "FIXME" in content:
            errors.append(
                "%s contains FIXME" % filename
            )

        secret_matches = check_secret_patterns(content)

        for match in secret_matches:
            errors.append(
                "%s contains secret pattern: %s"
                % (filename, match)
            )

    return errors


def write_report(errors):
    if not os.path.exists("reviews"):
        os.makedirs("reviews")

    filename = "reviews/review_%d.md" % int(time.time())

    f = open(filename, "w")

    f.write("# Review Report\n\n")

    if errors:
        f.write("Status: FAIL\n\n")
        
        f.write("## Issues\n\n")

        for error in errors:
            f.write("- %s\n" % error)
    else:
        f.write("Status: PASS\n")

    f.close()

    print("Review report written: %s" % filename)


def run_ai_review():
    try:
        output = subprocess.check_output(
            ["python", "tools/ai_review.py"]
        )

        return json.loads(output)

    except Exception as e:
        return {
            "status": "FAIL",
            "issues": [
                "AI review execution failed: %s" % str(e)
            ],
        }


def main():
    print("Collecting staged files...")

    files = get_staged_files()

    print("Files under review: %d" % len(files))

    for filename in files:
        print(" - %s" % filename)

    if len(files) == 0:
        print("")
        print("No source files staged")
        sys.exit(0)

    errors = run_checks(files)

    print("")
    print("Running AI review...")

    ai_result = run_ai_review()

    if ai_result.get("status") == "FAIL":
        for issue in ai_result.get("issues", []):
            errors.append(
                "AI Review: %s" % issue
            )

    write_report(errors)

    if errors:
        print("")
        print("Review failed:")
        print("")

        for error in errors:
            print("- %s" % error)

        sys.exit(1)

    print("")
    print("Review passed")

    sys.exit(0)


if __name__ == "__main__":
    main()