"""Run the complete, repeatable static-site build and quality checks."""

from pathlib import Path
import subprocess
import sys


SCRIPTS = Path(__file__).resolve().parent

for script in ("sync_shared_layout.py", "modernize_site.py", "add_image_dimensions.py", "audit_site.py"):
    subprocess.run([sys.executable, str(SCRIPTS / script)], check=True)

print("Build complete: shared layout synchronized and all quality checks passed.")
