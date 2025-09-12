#!/usr/bin/env python3
"""
UV-based application runner for Picture Sorting Application
"""
import subprocess
import sys
import os


def run_with_uv():
    """Run the application using UV"""
    print("🚀 Starting Picture Sorting Application with UV")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run the app with UV
    cmd = ["uv", "run", "python", "src/main.py"]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("❌ UV not found. Please install UV first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)


if __name__ == "__main__":
    run_with_uv()
