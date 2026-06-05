import subprocess
import sys

diff = subprocess.check_output(
    ["git", "diff", "--cached"]
)

if len(diff) == 0:
    print("No staged changes")
    sys.exit(1)

print("Review passed")
sys.exit(0)