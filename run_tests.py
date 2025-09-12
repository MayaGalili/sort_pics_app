#!/usr/bin/env python3
"""
Test runner script for the Picture Sorting Application
"""
import subprocess
import sys
import os


def run_tests():
    """Run all tests with pytest"""
    print("🧪 Running Picture Sorting Application Tests")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
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


def run_specific_test(test_name):
    """Run a specific test"""
    cmd = [sys.executable, "-m", "pytest", f"tests/{test_name}", "-v"]
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        print(f"Running specific test: {test_name}")
        run_specific_test(test_name)
    else:
        success = run_tests()
        sys.exit(0 if success else 1)
