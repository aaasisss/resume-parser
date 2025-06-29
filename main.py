from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from api.routes import analyse_resume, parse_match_resume, parse_resume

app = FastAPI()

origins = ["http://localhost:5173", 
           "http://127.0.0.1:5173", 
           "http://localhost:3000"
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    ) 

app.include_router(parse_resume.router)
app.include_router(parse_match_resume.router)
app.include_router(analyse_resume.router)



@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})
