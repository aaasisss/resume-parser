
import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.llm_clients import openai_client, gemini_models
from api.models.resume import JobMatchRequest
from api.utils.resume_utils import (
    build_match_prompt,
    build_parse_prompt,
    call_local_model,
    extract_text_from_pdf
)

router = APIRouter()

@router.websocket("/ws/match-job")
async def websocket_match_job(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json({"status": "pending", "result":"Waiting for input..."})
        data : JobMatchRequest  = await websocket.receive_json()

        base64_pdf = data['resume_pdf_base64']
        job_description = data['job_description']
        mode = data.get("mode", "local").lower()

        if not base64_pdf or not job_description:
            raise ValueError("Missing required fields.")

        await websocket.send_json({"status": "pending", "result": "Extracting PDF..."})
        pdf_bytes = base64.b64decode(base64_pdf)
        resume_text = extract_text_from_pdf(pdf_bytes)

        await websocket.send_json({"status": "pending", "result": f"Sending to {mode} model to parse resume..."})
        prompt = build_parse_prompt(resume_text)

        if mode == "openai":
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            parsed = response.choices[0].message.content

        elif mode == "google":
            response = gemini_models['pro'].generate_content(prompt)
            parsed = response.text

        elif mode == "local":
            parsed = call_local_model(prompt)

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        await websocket.send_json({"status":"pending", "result": "Matching job..."})
        match_prompt = build_match_prompt(parsed, job_description)

        if mode == "openai":
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": match_prompt}]
            )
            match_result = response.choices[0].message.content

        elif mode == "google":
            response = gemini_models['pro'].generate_content(match_prompt)
            match_result = response.text

        elif mode == "local":
            match_result = call_local_model(match_prompt)

        await websocket.send_json({"status": "done", "result": match_result})

    except WebSocketDisconnect:
        print("WebSocket disconnected.")
    except Exception as e:
        await websocket.send_json({"status": "error", "result": str(e)})
