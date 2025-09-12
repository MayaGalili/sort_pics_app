#!/usr/bin/env python3
"""
UV-based test runner for Picture Sorting Application
"""
import subprocess
import sys
import os


def run_tests_with_uv():
    """Run tests using UV"""
    print("🧪 Running Picture Sorting Application Tests with UV")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run pytest with UV
    cmd = [
        "uv", "run", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ UV not found. Please install UV first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False


def run_specific_test(test_name):
    """Run a specific test with UV"""
    cmd = ["uv", "run", "pytest", f"tests/{test_name}", "-v"]
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        print(f"Running specific test: {test_name}")
        run_specific_test(test_name)
    else:
        success = run_tests_with_uv()
        sys.exit(0 if success else 1)
