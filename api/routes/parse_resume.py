from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.models.resume import ResumeParseRequest
from api.utils.resume_utils import extract_text_from_pdf, build_parse_prompt, call_local_model
from api.llm_clients import openai_client, gemini_models
import base64

router = APIRouter()

@router.post("/parse-resume")
async def parse_resume(req: ResumeParseRequest):
    try:
        base64_data = req.resume_pdf_base64
        pdf_bytes = base64.b64decode(base64_data)

        resume_text = extract_text_from_pdf(pdf_bytes)
        if not resume_text:
            raise ValueError("No text extracted from PDF.")

        prompt = build_parse_prompt(resume_text)

        if req.mode == "openai":
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            parsed = response.choices[0].message.content

        elif req.mode == "google":
            response = gemini_models['pro'].generate_content(prompt)
            parsed = response.text

        elif req.mode == "local":
            resume_text = extract_text_from_pdf(pdf_bytes)
            if not resume_text:
                raise ValueError("No text extracted from PDF.")
            parsed = call_local_model(build_parse_prompt(resume_text))

        else:
            raise HTTPException(status_code=400, detail="Unsupported mode")

        return JSONResponse(content={"status": "done", "result": parsed})

    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

