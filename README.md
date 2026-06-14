# Resume Scanner

A web-based application for scanning and extracting information from PDF resumes.

## Features

- Upload PDF resumes
- Extract and parse resume data
- Display structured resume information
- Flask-based web interface

## Setup

1. Ensure Python 3.x is installed
2. Create a virtual environment:
   ```
   python -m venv resume
   resume\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install flask pdfplumber pillow pdfminer.six pypdfium2
   ```

4. Run the application:
   ```
   python resume.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `resume.py` - Main Flask application
- `templates/` - HTML templates
- `uploads/` - Directory for uploaded PDF files
- `resume/` - Virtual environment

## License

This project is open source and available under the MIT License.
