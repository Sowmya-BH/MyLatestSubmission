from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import os
# from financial_advisor.src.financial_advisor.crew import CkdV3

from crew import CkdV3

import agentops
import auth
from auth import get_current_user

import agentops

router = APIRouter(
    prefix="/analysis",
    tags=["financial-analysis"]
)

# Directory to save uploaded files
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploaded_files"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload-and-analyze")
async def upload_and_analyze(
    user: dict = Depends(get_current_user),   # 🔐 JWT protected
    file: UploadFile = File(...),
    input_field: str = Form(...),
    user_query: str = Form(...)
):
    """
    Upload PDF/DOCX → Run CkdV3 Crew → Return analysis result
    """

    # --------------------------------------------------------------------
    # 1. SAVE THE UPLOADED FILE
    # --------------------------------------------------------------------
    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")


    # --------------------------------------------------------------------
    # 2. AGENTOPS — Proper tracing (NO end_session())
    # --------------------------------------------------------------------
    agentops.init(os.getenv("AGENTOPS_API_KEY"))
    agentops.start_trace("financial_analysis")


    # --------------------------------------------------------------------
    # 3. PREPARE CREWAI INPUTS
    # --------------------------------------------------------------------
    inputs = {
        "pdf_path": str(file_path),
        "input_field": input_field,
        "user_query": user_query,
    }

    try:
        # Run the Crew
        crew = CkdV3().crew()
        result = crew.kickoff(inputs=inputs)

        # End trace properly
        agentops.end_trace()

        return {
            "status": "success",
            "filename": file.filename,
            "pdf_path": str(file_path),
            "final_answer": result.output,   # ← CrewAI final summary
        }

    except Exception as e:
        agentops.end_trace()
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

# @router.get("/agentops-dashboard")
# async def get_agentops_dashboard(user: dict = Depends(get_current_user)):
#     """Return session dashboard URL for frontend visualization"""
#     url = agentops.get_session_dashboard_link()
#     if not url:
#         raise HTTPException(status_code=404, detail="No active session found")
#     return {"dashboard_url": url}
