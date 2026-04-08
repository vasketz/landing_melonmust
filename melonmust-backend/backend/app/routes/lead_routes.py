import os
import uuid
import re
from time import time
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.lead_service import create_lead

router = APIRouter()

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = ["application/pdf", "image/png", "image/jpeg"]
ALLOWED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]

os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# RATE LIMIT
# =========================
requests_log = {}

def get_client_ip(request: Request):
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

def rate_limit(ip):
    now = time()
    if ip not in requests_log:
        requests_log[ip] = []

    requests_log[ip] = [t for t in requests_log[ip] if now - t < 60]

    if len(requests_log[ip]) >= 10:
        return False

    requests_log[ip].append(now)
    return True

# =========================
# DB
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# PREFLIGHT
# =========================
@router.options("/lead")
async def options_lead():
    return Response(status_code=200)

# =========================
# SANITIZE
# =========================
def sanitize(value: str):
    if not value:
        return ""
    return re.sub(r"[<>]", "", value).strip()

# =========================
# VALIDATION
# =========================
def validate_data(data: dict):
    email = data.get("email", "")
    phone = data.get("phone", "")
    amount = data.get("amount", "")

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return "Invalid email"

    if len(phone) < 7:
        return "Invalid phone"

    try:
        amount = int(amount)
        if amount <= 0:
            return "Invalid amount"
    except:
        return "Invalid amount"

    return None

# =========================
# ENDPOINT
# =========================
@router.post("/lead")
async def create_lead_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = get_client_ip(request)

    if not rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests")

    content_type = request.headers.get("content-type", "")

    try:
        # =========================
        # JSON
        # =========================
        if "application/json" in content_type:
            data = await request.json()

            data = {k: sanitize(v) for k, v in data.items()}

            error = validate_data(data)
            if error:
                raise HTTPException(status_code=400, detail=error)

            print("NEW LEAD (JSON):", data)

            lead = create_lead(db, data)

            from app.main import send_email
            await send_email(data)

            return {"status": "success", "lead_id": lead.id, "score": lead.score}

        # =========================
        # FORMDATA
        # =========================
        elif "multipart/form-data" in content_type:
            form = await request.form()

            data = {}
            file = None

            for key, value in form.items():
                if key == "file":
                    file = value
                else:
                    data[key] = sanitize(value)

            error = validate_data(data)
            if error:
                raise HTTPException(status_code=400, detail=error)

            print("NEW LEAD (FORM):", data)

            file_bytes = None
            file_name = None

            if file:
                ext = os.path.splitext(file.filename)[1].lower()

                if file.content_type not in ALLOWED_TYPES:
                    raise HTTPException(status_code=400, detail="Invalid file type")

                if ext not in ALLOWED_EXTENSIONS:
                    raise HTTPException(status_code=400, detail="Invalid file extension")

                contents = await file.read()

                if len(contents) > MAX_FILE_SIZE:
                    raise HTTPException(status_code=400, detail="File too large")

                filename = f"{uuid.uuid4()}{ext}"
                file_path = os.path.join(UPLOAD_DIR, filename)

                with open(file_path, "wb") as f:
                    f.write(contents)

                print("FILE SAVED:", file_path)

                file_bytes = contents
                file_name = file.filename

            lead = create_lead(db, data)

            from app.main import send_email
            await send_email(data, file_bytes, file_name)

            return {"status": "success", "lead_id": lead.id, "score": lead.score}

        else:
            raise HTTPException(status_code=415, detail="Unsupported content type")

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR ❌:", e)
        raise HTTPException(status_code=500, detail="Internal server error")