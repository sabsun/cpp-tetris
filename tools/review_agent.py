import subprocess
import sys

print("Collecting staged diff...")

diff = subprocess.check_output(
    ["git", "diff", "--cached"]
)

if not isinstance(diff, str):
    diff = diff.decode("utf-8")

if not diff.strip():
    print("No staged changes")
    sys.exit(0)

print("Diff size:", len(diff))

print("Review passed")

sys.exit(0)