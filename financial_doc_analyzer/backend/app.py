import os
import uuid
import logging
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from io import StringIO
from typing import Optional, Dict, Any

import aiofiles
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Depends,
    BackgroundTasks,
    Header,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from bson import ObjectId  # Import ObjectId for MongoDB queries

load_dotenv()  # load .env if present

# ----------------------------
# Configuration (env)
# ----------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))
UPLOAD_BASE = Path(os.getenv("UPLOAD_BASE", "./knowledge/uploaded_pdfs")).resolve()
CREW_LOG_DIR = Path(os.getenv("CREW_LOG_DIR", "./logs")).resolve()

UPLOAD_BASE.mkdir(parents=True, exist_ok=True)
CREW_LOG_DIR.mkdir(parents=True, exist_ok=True)

# === ALLOWED USERS CONFIGURATION (Registration Filter) ===
ALLOWED_USERS = {
    "admin@example.com",
    "test@example.com",
    "bhupati@example.com"
}
# =========================================================

# ----------------------------
# DB / Auth setup
# ----------------------------
client = AsyncIOMotorClient(MONGO_URI)
db = client.financial_app  # database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(title="Financial Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",  # Default Vite
                   "http://localhost:5175",  # Your current Vite
                   "http://localhost:3000",  # CRA fallback,
                   "*",
                   ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Helper types / models
# ----------------------------
class UserCreate(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ----------------------------
# JWT helpers
# ----------------------------
def create_access_token(sub: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": sub, "exp": int(expire.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Simple dependency that expects Authorization: Bearer <token>.
    Returns user dict from DB or raises 401.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # remove sensitive fields before returning
    user.pop("password", None)
    return user


# ----------------------------
# Log capture for Crew / agentops
# ----------------------------
class LogCapture:
    """
    Capture Python logging to a memory buffer string. Use start() before Crew run,
    stop() after run, then get_text() to retrieve logs.
    """

    def __init__(self):
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self._logger = None

    def start(self, logger_name: str = None):
        # attach to a logger; if none provided attach to root
        self._logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(self.handler)

    def stop(self):
        if self._logger:
            try:
                self._logger.removeHandler(self.handler)
            except Exception:
                pass

    def get_text(self) -> str:
        return self.stream.getvalue()


# ----------------------------
# Auth endpoints
# ----------------------------
@app.post("/auth/register", response_model=TokenOut)
async def register(payload: UserCreate):
    # Enforce ALLOWED_USERS Check
    if payload.username not in ALLOWED_USERS:
        raise HTTPException(status_code=403, detail="User not authorized for registration.")

    existing = await db.users.find_one({"username": payload.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # NOTE: Password hash is still required for the DB even if password check is skipped later.
    hashed = get_password_hash(payload.password)
    user_doc = {"username": payload.username, "password": hashed, "created_at": datetime.utcnow()}
    await db.users.insert_one(user_doc)
    token = create_access_token(sub=payload.username)
    return {"access_token": token}


@app.post("/auth/login", response_model=TokenOut)
async def login(payload: UserCreate):
    user = await db.users.find_one({"username": payload.username})

    if not user:
        # If user isn't found, deny access.
        raise HTTPException(status_code=401, detail="Invalid username.")

    # === MODIFIED: BYPASS PASSWORD VERIFICATION (SECURITY RISK!) ===
    # This allows login with just the correct registered username.

    # Since we verified the user exists, we generate a token.
    token = create_access_token(sub=payload.username)
    return {"access_token": token}


# ----------------------------
# Upload endpoint
# ----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    # ensure file is pdf
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # build a safe unique name
    unique_name = f"{uuid.uuid4()}--{os.path.basename(file.filename)}"
    dest_path = UPLOAD_BASE / unique_name

    # save to disk
    try:
        async with aiofiles.open(dest_path, "wb") as out_file:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await out_file.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store file: {e}")

    # store metadata in mongo
    doc = {
        "owner": user["username"],
        "orig_filename": file.filename,
        "saved_path": str(dest_path),
        "uploaded_at": datetime.utcnow(),
        "analysis_status": "uploaded",
        "result_summary": None,
        "crew_logs": None,
    }
    res = await db.documents.insert_one(doc)
    return {"id": str(res.inserted_id), "filename": file.filename, "saved_path": str(dest_path)}


# ----------------------------
# List user documents
# ----------------------------
@app.get("/documents")
async def list_documents(user=Depends(get_current_user)):
    cursor = db.documents.find({"owner": user["username"]}).sort("uploaded_at", -1)
    docs = []
    async for d in cursor:
        d["id"] = str(d["_id"])
        d.pop("_id", None)
        docs.append(d)
    return docs


# ----------------------------
# Background runner for Crew kickoff
# ----------------------------
def run_crew_background(pdf_path: str, doc_id: str, username: str):
    """
    Runs Crew synchronously in a background thread/process using a captured log.
    Updates Mongo document with results and logs.
    """
    capture = LogCapture()
    capture.start()

    try:
        # Dynamically import crew to avoid startup-time import issues
        from crew import CkdV3  # replace with your crew module/class

        crew_instance = CkdV3()  # instantiate the crew class
        # Kickoff expects a mapping of inputs
        inputs = {"pdf_path": pdf_path, "input_field": None, "user_query": None}

        result = crew_instance.crew().kickoff(inputs=inputs)
        # Save result to DB
        update_doc = {
            "analysis_status": "done",
            "result_summary": str(result),
            "crew_logs": capture.get_text(),
            "completed_at": datetime.utcnow(),
        }
    except Exception as e:
        tb = traceback.format_exc()
        update_doc = {
            "analysis_status": "failed",
            "result_summary": f"Error: {e}\n{tb}",
            "crew_logs": capture.get_text() + "\n\n" + traceback.format_exc(),
            "completed_at": datetime.utcnow(),
        }
    finally:
        capture.stop()

    # update DB (create client inside this thread)
    try:
        client_local = AsyncIOMotorClient(MONGO_URI)
        db_local = client_local.financial_app
        # convert doc_id to ObjectId when updating
        db_local.documents.update_one({"_id": ObjectId(doc_id)}, {"$set": update_doc})
        client_local.close()
    except Exception:
        # best-effort only
        logging.exception("Failed to update document after crew run")


# ----------------------------
# Analyze endpoint
# ----------------------------
@app.post("/analyze/{doc_id}")
async def analyze_document(doc_id: str, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    # verify ownership
    doc = await db.documents.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.get("owner") != user["username"]:
        raise HTTPException(status_code=403, detail="Not allowed to analyze this document")

    # mark running
    await db.documents.update_one({"_id": ObjectId(doc_id)},
                                  {"$set": {"analysis_status": "running", "started_at": datetime.utcnow()}})

    # schedule crew run
    background_tasks.add_task(run_crew_background, doc["saved_path"], doc_id, user["username"])

    return {"message": "analysis scheduled", "document_id": doc_id}


# ----------------------------
# Direct query endpoint (keyword + semantic query)
# ----------------------------
@app.post("/query")
async def query_document(payload: dict, user=Depends(get_current_user)):
    """
    payload example:
    {
        "pdf_path": "/abs/path/to/file.pdf",
        "input_field": "Total gross profit",    # optional keyword
        "user_query": "Summarize performance in one paragraph"  # optional semantic query
    }
    This runs Crew synchronously and returns the result. If you prefer background, wrap in BackgroundTasks.
    """
    pdf_path = payload.get("pdf_path")
    if not pdf_path:
        raise HTTPException(status_code=400, detail="pdf_path required")

    # optionally check ownership if you want – omitted for direct-run endpoint.
    from crew import CkdV3

    try:
        crew_instance = CkdV3()
        inputs = {
            "pdf_path": pdf_path,
            "input_field": payload.get("input_field"),
            "user_query": payload.get("user_query"),
        }
        result = crew_instance.crew().kickoff(inputs=inputs)
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew execution failed: {e}")


# ----------------------------
# Get logs & result
# ----------------------------
@app.get("/results/{doc_id}")
async def get_results(doc_id: str, user=Depends(get_current_user)):
    doc = await db.documents.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.get("owner") != user["username"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    # return status + summary + small logs
    return {
        "status": doc.get("analysis_status"),
        "summary": doc.get("result_summary"),
        "crew_logs": (doc.get("crew_logs") or "")[:20_000],  # avoid huge payloads
        "saved_path": doc.get("saved_path"),
    }


# ----------------------------
# Simple health endpoint
# ----------------------------
@app.get("/health")
async def health():
    # quick DB ping
    try:
        await client.admin.command("ping")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
