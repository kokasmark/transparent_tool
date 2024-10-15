import subprocess
import sys

# List of dependencies to install
dependencies = [
    "pywin32",
    "pynput",
    "keyboard",
    "pywebview"
]

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

if __name__ == '__main__':
    for dependency in dependencies:
        try:
            install(dependency)
            print(f"Successfully installed {dependency}.")
        except Exception as e:
            print(f"Failed to install {dependency}: {e}")
