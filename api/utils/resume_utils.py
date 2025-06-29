import pdfplumber
import requests
import json
import io
import re
import fitz  
import base64

from api.models.resume import JobMatchResponse, ParsedResumeResponse

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error extracting PDF text: {e}")

def convert_pdf_to_png_base64(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(0)  # first page
    pix = page.get_pixmap(dpi=150)  # decent resolution
    png_bytes = pix.tobytes("png")
    return base64.b64encode(png_bytes).decode("utf-8")


def build_parse_prompt(resume_text: str) -> str:
    return f"""
Extract the following structured information from this resume:

- Full Name
- Email
- Phone
- Socials such as LinkedIn, GitHub, etc. (if any)
- Skills (comma separated)
- Work Experience: for each job, include:
    - Job Title
    - Company
    - Start Date
    - End Date
    - Description
- Education: for each entry, include:
    - Degree
    - Institution
    - Dates
    - Major (if applicable)

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond in JSON format only. Follow this structure:
{ParsedResumeResponse.model_json_schema()}
"""


def build_match_prompt(resume_json: dict, job_description: str) -> str:
    return f"""
Compare the following resume data with the job description. Return:

1. A match score from 0 to 1.
2. A short explanation of the strengths and gaps.
3. Key matched skills and unmatched requirements.

Resume:
{json.dumps(resume_json, indent=2)}

Job Description:
\"\"\"
{job_description}
\"\"\"

Respond in JSON format only. Follow this structure:
{JobMatchResponse.model_json_schema()}
"""


def build_analyze_prompt() -> str:
    return (
        "Please evaluate the visual design of this resume."
        "Comment on formatting, fonts, spacing, layout, colors, and overall design quality. "
        "Suggest specific improvements to make it look more professional and easier to read."
    )


def call_local_model(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:12b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )
    result = response.json()
    return result["message"]["content"]
