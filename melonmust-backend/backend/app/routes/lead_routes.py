import os
import uuid
from time import time
from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services.lead_service import create_lead

router = APIRouter()

# =========================
# CONFIG FILES
# =========================
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = ["application/pdf", "image/png", "image/jpeg"]

os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# RATE LIMIT
# =========================
requests_log = {}

def rate_limit(ip):
    now = time()
    if ip not in requests_log:
        requests_log[ip] = []

    requests_log[ip] = [t for t in requests_log[ip] if now - t < 60]

    if len(requests_log[ip]) > 10:
        return False

    requests_log[ip].append(now)
    return True

# =========================
# DB DEPENDENCY
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
# VALIDACIONES
# =========================
def validate_data(data: dict):
    if "@" not in data.get("email", ""):
        return "Invalid email"

    if len(data.get("phone", "")) < 7:
        return "Invalid phone"

    try:
        int(data.get("amount", 0))
    except:
        return "Invalid amount"

    return None

# =========================
# ENDPOINT PRINCIPAL
# =========================
@router.post("/lead")
async def create_lead_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host

    # 🔒 RATE LIMIT
    if not rate_limit(client_ip):
        return {"status": "error", "detail": "Too many requests"}

    content_type = request.headers.get("content-type", "")

    try:
        # =========================
        # JSON
        # =========================
        if "application/json" in content_type:
            data = await request.json()

            error = validate_data(data)
            if error:
                return {"status": "error", "detail": error}

            print("NEW LEAD (JSON):", data)

            # 🔥 DB
            lead = create_lead(db, data)

            # 🔥 EMAIL (reutiliza tu lógica)
            from app.main import send_email
            await send_email(data)

            return {
                "status": "success",
                "lead_id": lead.id,
                "score": lead.score
            }

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
                    data[key] = value

            error = validate_data(data)
            if error:
                return {"status": "error", "detail": error}

            print("NEW LEAD (FORM):", data)

            file_bytes = None
            file_name = None

            if file:

                if file.content_type not in ALLOWED_TYPES:
                    return {"status": "error", "detail": "Invalid file type"}

                contents = await file.read()

                if len(contents) > MAX_FILE_SIZE:
                    return {"status": "error", "detail": "File too large"}

                # guardar archivo
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4()}{ext}"
                file_path = os.path.join(UPLOAD_DIR, filename)

                with open(file_path, "wb") as f:
                    f.write(contents)

                print("FILE SAVED:", file_path)

                file_bytes = contents
                file_name = file.filename

            # 🔥 DB
            lead = create_lead(db, data)

            # 🔥 EMAIL
            from app.main import send_email
            await send_email(data, file_bytes, file_name)

            return {
                "status": "success",
                "lead_id": lead.id,
                "score": lead.score
            }

        else:
            return {"status": "error", "detail": "Unsupported content type"}

    except Exception as e:
        print("ERROR ❌:", e)
        return {"status": "error", "detail": "Internal server error"}
    