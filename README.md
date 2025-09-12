# Picture Sorting Application

A web-based application for automatically organizing and sorting pictures into structured directories by date and category.

## Features
- **Web Interface**: User-friendly Flask-based web application
- **Directory Selection**: Easy selection of source directories containing pictures
- **Automatic Organization**: Sort pictures by date and category
- **Structured Output**: Create organized folder hierarchy for better photo management

## Planned Features (Future Development)
- Date-based sorting into `YYYY-MM-DD` folders
- Automatic categorization into:
  - **People** - Photos containing people
  - **Views** - Buildings, skies, nature scenes
  - **Special** - Screenshots, receipts, etc.
- Daily summary generation
- Image analysis and classification

## System Requirements
- Python 3.8 or higher
- Internet connection (for future image classification features)

## Installation

### Using UV (Recommended)
1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Install dependencies: `uv sync`
3. Run the application: `uv run python src/main.py`

### Using pip (Alternative)
1. Install Python 3.8 or newer
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python src/main.py`

## Usage
1. Run the application:
```bash
# Using UV (recommended)
uv run python src/main.py
# Or use the convenience script
python run_app.py

# Using traditional Python
python src/main.py
```
2. Open your web browser and go to `http://localhost:5001`
3. Enter the full path to your pictures directory
4. Click "Create Sorted Directory" to create the organized folder structure

## Development
See `SETUP.md` for detailed development setup instructions including testing, formatting, and dependency management.

## Current Implementation
The application currently provides:
- Web interface for directory selection
- Creation of a `sorted_pictures` subdirectory in the selected location
- Foundation for future sorting and categorization features

## Planned Directory Structure
```
source_directory/
    ├── sorted_pictures/
    │   ├── YYYY-MM-DD/
    │   │   ├── people/
    │   │   ├── views/
    │   │   ├── special/
    │   │   └── summary.txt
    │   └── ...
    └── original_pictures/
```

## Development Status
This application is currently in early development. The core web interface and directory creation functionality is implemented, with sorting and categorization features planned for future releases.