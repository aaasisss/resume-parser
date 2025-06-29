# README.md

# Resume Parser

This project is a Resume Parser application built using FastAPI. It provides functionalities to parse resumes from PDF files, match them with job descriptions, and extract structured information.

## Project Structure

```
resume-parser
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── endpoints.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── resume_parser.py
│   │   ├── job_matcher.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── pdf_utils.py
│   │   ├── prompt_builder.py
│   │   ├── json_utils.py
│   └── models
│       ├── __init__.py
│       ├── schemas.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd resume-parser
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- **Parse Resume**: Upload a PDF resume to extract structured information.
- **Match Job**: Compare a resume with a job description to get a match score and insights.
- **WebSocket Match**: Use WebSocket to send a resume and job description for real-time matching.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.