from fastapi import FastAPI, APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from database import engine, SessionLocal
from typing import Annotated

from sqlalchemy.orm import Session
import shutil
from pathlib import Path
import os
from crew import CkdV3
import auth

import agentops
from auth import get_current_user
from fastapi import FastAPI, status, Depends, HTTPException
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import auth
from auth import get_current_user
from analysis import router as analysis_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",  # Default Vite
                   "http://localhost:5175",  # Your current Vite
                   "http://localhost:3000",  # CRA fallback,
                   "*",
                   ],   # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(analysis_router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]



@app.get("/",status_code=status.HTTP_200_OK)
async def user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return {"User":user}
