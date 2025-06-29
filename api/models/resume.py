from pydantic import BaseModel

class WorkExperience(BaseModel):
    company: str
    job_title: str
    start_date: str
    end_date: str
    description: str

class Education(BaseModel):
    institution: str
    degree: str
    start_date: str
    end_date: str
    major: str 

class ParsedResumeResponse(BaseModel):
    name: str
    email: str
    phone: str
    socials: dict[str, str] 
    skills: list[str]
    education: list[Education]
    experience: list[WorkExperience]  
    certifications: list[str]
    projects: str

class JobMatchRequest(BaseModel):
    resume_pdf_base64: str
    job_description: str
    mode: str


class MatchedSkills(BaseModel):
    resume_skills: list[str]
    job_description_requirements: list[str]


class JobMatchResponse(BaseModel):
    match_score: float
    strengths_and_gaps: str
    matched_skills: MatchedSkills
    unmatched_requirements: list[str]


class ResumeParseRequest(BaseModel):
    mode: str  
    resume_pdf_base64: str

class ResumeVisualFeedbackRequest(BaseModel):
    resume_pdf_base64: str
    mode: str = "openai" 
