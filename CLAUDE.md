# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
- Run application: `python app.py` (Runs on port 5001 by default)
- Install dependencies: `pip install -r requirements.txt`

### Testing
- Run all tests: `pytest`
- Run a specific test file: `pytest tests/test_file.py`
- Run a specific test function: `pytest tests/test_file.py::test_function`

## Architecture and Structure

### High-Level Architecture
The project is a Flask web application following a traditional monolithic structure:
- **Routing & Logic**: Handled in `app.py`.
- **Data Persistence**: SQLite database management located in `database/db.py`.
- **Frontend**: Jinja2 templates in `templates/` and static assets in `static/`.

### Key Directories
- `database/`: Contains database connection and initialization logic.
- `static/`: CSS, JavaScript, and images.
- `templates/`: HTML templates for the user interface.

### Project State
The application is currently in a skeletal state. Many routes in `app.py` (e.g., `/logout`, `/profile`, `/expenses/add`) are placeholders intended for future implementation.
