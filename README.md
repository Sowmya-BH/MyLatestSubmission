# 📄 `README.md`

# **Financial Report Analyst — AI-Powered Document Analysis Platform**

An end-to-end AI system for analyzing financial documents using **CrewAI**, **AgentOps**, **FastAPI**, **React**, and **TailwindCSS**.

This project allows users to:

✅ Upload PDFs or DOCX financial files
✅ Extract structured financial data
✅ Ask custom analysis queries
✅ Run a multi-agent CrewAI pipeline
✅ View summary + extracted data
✅ Authenticate using JWT login
✅ Track agent performance using AgentOps

---

## 🚀 **Tech Stack**

### **Backend**

* **FastAPI**
* **JWT Authentication**
* **SQLite + SQLAlchemy ORM**
* **CrewAI (Multi-agent framework)**
* **DoclingTool (PDF parsing)**
* **AgentOps (Trace & monitoring)**

### **Frontend**

* **React (Vite)**
* **React Router**
* **TailwindCSS**
* **Protected routes**
* **File Upload + Analysis UI**

---

# 🔐 **Authentication Flow (JWT)**

1. User logs in using `/auth/token`
2. Backend validates credentials (SQLite DB)
3. JWT token returned to frontend
4. Token stored in `localStorage`
5. All analysis requests include:

```
Authorization: Bearer <token>
```

6. Backend validates token using `get_current_user`

---

# 📡 **Backend API Documentation**

### **POST** `/auth/token`

Authenticate and get JWT token.

### **POST** `/auth/`

Create user (development-only).

---

## 📄 **POST** `/analysis/upload-and-analyze`

Uploads document + runs full CrewAI pipeline.

### **Request (multipart/form-data)**

| Field       | Type       | Description           |
| ----------- | ---------- | --------------------- |
| file        | UploadFile | PDF or DOCX           |
| input_field | string     | Data field to extract |
| user_query  | string     | Summarization     |

### **Response**

```json
{
  "status": "success",
  "filename": "file.pdf",
  "final_answer": "Financial summary here..."
}
```

```
---
┌──────────────────────────┐
│        React UI          │
│ - Login page             │
│ - File upload (PDF/DOCX) │
│ - Show analysis results  │
└──────────────┬───────────┘
               │  fetch()
               ▼
       ┌────────────────────────┐
       │        FastAPI         │
       │ /auth/token (JWT)      │
       │ /analysis/upload       │
       │ run CkdV3 crew         │
       └─────────────┬──────────┘
                     │ inputs={}
                     ▼
           ┌───────────────────┐
           │      CrewAI       │
           │ docling_agent     │
           │ JSON extractor    │
           │ financial agent   │
           │ parse+analyze     │
           └───────┬──────────┘
                   │ tracing
                   ▼
          ┌───────────────────┐
          │     AgentOps      │
          │ start_trace()     │
          │ end_trace()       │
          └───────────────────┘

Future:
SQLite for storage
```
# 🤖 **CrewAI Pipeline**

Your `CkdV3` Crew consists of:

### ✓ **Docling Agent**

Extracts structured content from PDF
Uses:

* `DoclingTool`
* `FileWriterTool`

### ✓ **JSON Data Extractor**

Extracts numeric fields based on `input_field`

### ✓ **Financial Analyst Agent**

Writes human-readable summary

### ✓ Tasks:

* `parse_pdf`
* `parse_json`
* `answer_query`

---

# 📊 **AgentOps Integration**

AgentOps tracks execution traces for:

* Individual calls
* Agent performance
* Pipeline timing

Your FastAPI endpoint uses:

```python
agentops.init(API_KEY)
agentops.start_trace("financial_analysis")
...
agentops.end_trace()
```

---

# 💻 **Frontend Overview**

## **Login Page**

* Tailwind UI login form
* Calls `/auth/token`
* Redirects to `/analysis`

## **Analysis Page**

* Upload PDF
* Enter input field
* Enter custom query
* Sends request to backend
* Displays CrewAI output

---

# 🛠️ **Setup Instructions**

## **Backend Setup**

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8001
```

Make sure to set env variables:

```
AGENTOPS_API_KEY=xxxx
GEMINI_API_KEY=xxxx
OPENAI_API_KEY=xxxx
```

---

## **Frontend Setup**

```sh
cd frontend
npm install
npm run dev
```

Default URL:

```
http://localhost:5173
```

---

# 🧪 Example Login Credentials

```
username: bhupati
password: test1234
```

---

# 🚀 Future Enhancements

* PDF text preview
* Display AgentOps dashboard link in UI
* Add history of analyzed documents
* Improved summarization via RAG + MongoDB Vector Store


