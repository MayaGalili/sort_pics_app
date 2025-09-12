# Setup Instructions for Picture Sorting Application

This guide will help you set up the Picture Sorting Application using UV (similar to your spotifyAgent setup).

## Prerequisites

- Python 3.8 or higher
- UV package manager

## Installation

### 1. Install UV

If you don't have UV installed, install it first:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Clone and Setup Project

```bash
git clone <your-repo-url>
cd sort_pics_app
```

### 3. Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
uv sync

# Or install only production dependencies
uv sync --no-dev
```

This will:
- Create a virtual environment
- Install all dependencies from `pyproject.toml`
- Generate a `uv.lock` file for reproducible builds

## Running the Application

### Using UV (Recommended)

```bash
# Run the application
uv run python src/main.py

# Or use the convenience script
python run_app.py
```

### Using Traditional Python

```bash
# Activate the virtual environment first
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows

# Then run the application
python src/main.py
```

## Running Tests

### Using UV (Recommended)

```bash
# Run all tests
uv run pytest tests/ -v

# Or use the convenience script
python run_tests_uv.py

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

### Using Traditional Python

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run tests
pytest tests/ -v
```

## Development

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Add with specific version
uv add "package-name>=1.0.0"
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific dependency
uv add package-name@latest
```

### Code Formatting and Linting

```bash
# Format code with black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/

# Lint with flake8
uv run flake8 src/ tests/

# Type checking with mypy
uv run mypy src/
```

## Project Structure

```
sort_pics_app/
├── pyproject.toml          # UV configuration and dependencies
├── uv.lock                 # Lock file for reproducible builds
├── requirements.txt        # Legacy requirements (kept for compatibility)
├── .gitignore             # Git ignore rules
├── run_app.py             # UV-based app runner
├── run_tests_uv.py        # UV-based test runner
├── src/
│   ├── main.py            # Main Flask application
│   └── templates/
│       └── index.html     # Web interface template
├── tests/                 # Test suite
│   ├── test_app.py        # Application tests
│   ├── test_html_template.py  # Template tests
│   └── conftest.py        # Pytest fixtures
└── htmlcov/               # Coverage reports (generated)
```

## Environment Variables

Create a `.env` file for any environment-specific configuration:

```bash
# .env
FLASK_ENV=development
FLASK_DEBUG=True
```

## Troubleshooting

### UV Not Found
```bash
# Make sure UV is in your PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Or reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Virtual Environment Issues
```bash
# Remove existing environment and recreate
rm -rf .venv
uv sync
```

### Dependency Conflicts
```bash
# Update lock file
uv lock --upgrade
uv sync
```

## Comparison with spotifyAgent

This setup follows the same patterns as your [spotifyAgent repository](https://github.com/MayaGalili/spotifyAgent):

- ✅ `pyproject.toml` for dependency management
- ✅ `uv.lock` for reproducible builds
- ✅ UV-based development workflow
- ✅ Similar project structure and scripts
- ✅ Development dependencies separated from production
- ✅ Modern Python packaging standards

## Next Steps

1. Run `uv sync` to install dependencies
2. Run `python run_app.py` to start the application
3. Open `http://localhost:5001` in your browser
4. Run `python run_tests_uv.py` to verify everything works
