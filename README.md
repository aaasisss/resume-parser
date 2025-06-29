# Resume Parser API

A FastAPI-based backend for parsing resumes, extracting structured information, and matching resumes to job descriptions.

## Features

- Parse resumes (PDF, base64) and extract structured data (skills, education, experience, etc.)
- Match resumes to job descriptions and provide feedback
- CORS enabled for local frontend development

## Project Structure

```
resume-parser/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── endpoints.py
│   │   └── models/
│   │       └── resume.py
│   ├── core/
│   │   └── config.py
│   ├── services/
│   │   └── resume_parser.py
│   ├── utils/
│   │   └── pdf_utils.py
│   └── models/
│       └── schemas.py
├── requirements.txt
└── README.md
```

## Quickstart

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**

   ```bash
   uvicorn app.main:app --reload
   ```

3. **API Endpoints:**
   - `POST /parse-resume` — Parse a resume PDF and extract information
   - `POST /parse-match-resume` — Match a resume to a job description
   - `POST /analyse-resume` — Analyse a resume for feedback
   - `GET /healthcheck` — Health check endpoint

## Models

See [`api/models/resume.py`](app/api/models/resume.py) for request and response models.

## Development

- Python 3.10+
- FastAPI
- Pydantic

## License

MIT
