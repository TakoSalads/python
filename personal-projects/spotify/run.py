import subprocess
import sys

# List of required packages
REQUIRED_PACKAGES = ["spotipy", "Flask", "python-dotenv"]

def install_missing_packages():
    """Checks for missing packages and installs them."""
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_missing_packages()
    import main  # Assuming your script is named 'main.py'
