#!/usr/bin/env python

import os
import subprocess
import sys
import time

IGNORE_FILES = [
    "tools/review_agent.py",
]

IGNORE_PREFIXES = [
    "reviews/",
]
SOURCE_EXTENSIONS = [
".cpp",
".h",
".hpp",
".c"
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
        return subprocess.check_output(
            ["git", "show", ":" + filename]
        )
    except Exception:
        return ""


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

        if "password =" in content:
            errors.append(
                "%s contains possible hardcoded password" % filename
            )

        if "secret =" in content:
            errors.append(
                "%s contains possible hardcoded secret" % filename
            )

    return errors


def write_report(errors):
    if not os.path.exists("reviews"):
        os.makedirs("reviews")

    filename = "reviews/review_%d.md" % int(time.time())

    with open(filename, "w") as f:
        f.write("# Review Report\n\n")

        if errors:
            f.write("Status: FAIL\n\n")

            for error in errors:
                f.write("- %s\n" % error)
        else:
            f.write("Status: PASS\n")

    print("Review report written: %s" % filename)


def main():
    print("Collecting staged files...")

    files = get_staged_files()

    print("Files under review: %d" % len(files))

    for filename in files:
        print(" - %s" % filename)

    errors = run_checks(files)

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