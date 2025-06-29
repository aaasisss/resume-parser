from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import google.generativeai as genai
import base64, requests

from api.models.resume import ResumeVisualFeedbackRequest
from api.utils.resume_utils import build_analyze_prompt, convert_pdf_to_png_base64
from api.llm_clients import openai_client, gemini_models

router = APIRouter()

@router.websocket("/ws/analyze-visual")
async def analyze_visual_resume(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json({"status": "pending", "result": "Waiting for resume PDF..."})
        data : ResumeVisualFeedbackRequest = await websocket.receive_json()
        base64_pdf = data["resume_pdf_base64"]
        mode = data.get("mode", "local").lower()

        if not base64_pdf:
            raise ValueError("Missing resume_pdf_base64")

        await websocket.send_json({"status": "pending", "result": "Rendering PDF to image..."})
        pdf_bytes = base64.b64decode(base64_pdf.split(",")[-1])
        img_base64 = convert_pdf_to_png_base64(pdf_bytes)

        await websocket.send_json({"status": "pending", "result": f"Sending to {mode} model for visual feedback..."})
        prompt_text = build_analyze_prompt()
        
        if mode == "openai":
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                        ],
                    }
                ],  
            )
            result = response.choices[0].message.content

        elif mode == "google":
            response = gemini_models['pro'].generate_content([
                prompt_text,
                genai.upload_image(base64.b64decode(img_base64), mime_type="image/png")
            ])
            result = response.text

        elif mode == "local":
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llava-llama3",
                "prompt": prompt_text,
                "images": [img_base64],
                "stream": False
            })
            result = response.json().get("response", "No response from local model.")

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        await websocket.send_json({"status": "done", "result": result})

    except WebSocketDisconnect:
        print("WebSocket disconnected.")
    except Exception as e:
        await websocket.send_json({"status": "error", 'result': str(e)})
