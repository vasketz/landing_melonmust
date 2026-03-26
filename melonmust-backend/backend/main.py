import os
import uuid
from time import time
from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv
import resend

# =========================
# ENV
# =========================
load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
ADMIN_EMAIL = os.getenv("EMAIL_USER")

resend.api_key = RESEND_API_KEY

# =========================
# APP
# =========================
app = FastAPI()

# =========================
# CORS (RESTRINGIDO)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://landing-melonmust.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CONFIG
# =========================
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
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

    # limpiar requests antiguos
    requests_log[ip] = [t for t in requests_log[ip] if now - t < 60]

    if len(requests_log[ip]) > 10:
        return False

    requests_log[ip].append(now)
    return True

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "ok"}

# =========================
# EMAIL
# =========================
async def send_email(data: dict, file_path: str = None):

    file_section = ""
    if file_path:
        file_section = f"<p><b>File saved internally:</b> {file_path}</p>"

    response = resend.Emails.send({
        "from": "MelonMust <onboarding@resend.dev>",
        "to": ADMIN_EMAIL,
        "subject": "🚀 Nuevo Lead - MelonMust",
        "html": f"""
        <h2>Nuevo Lead Recibido</h2>
        <p><b>Nombre:</b> {data.get('firstName')} {data.get('lastName')}</p>
        <p><b>Email:</b> {data.get('email')}</p>
        <p><b>Teléfono:</b> {data.get('phone')}</p>
        <p><b>Monto:</b> {data.get('amount')}</p>
        <p><b>Negocio:</b> {data.get('business')}</p>
        {file_section}
        """
    })

    print("RESEND RESPONSE:", response)

# =========================
# PREFLIGHT
# =========================
@app.options("/lead")
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
# ENDPOINT
# =========================
@app.post("/lead")
async def create_lead(request: Request):

    # 🔒 RATE LIMIT
    client_ip = request.client.host
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

            await send_email(data)

            return {"status": "success"}

        # =========================
        # FORMDATA (FILE)
        # =========================
        elif "multipart/form-data" in content_type:
            form = await request.form()

            data = {}
            file = None

            for key, value in form.items():
                if isinstance(value, UploadFile):
                    file = value
                else:
                    data[key] = value

            error = validate_data(data)
            if error:
                return {"status": "error", "detail": error}

            print("NEW LEAD (FORM):", data)

            file_path = None

            if file and isinstance(file, UploadFile):

                # VALIDAR TIPO
                if file.content_type not in ALLOWED_TYPES:
                    return {"status": "error", "detail": "Invalid file type"}

                contents = await file.read()

                # VALIDAR TAMAÑO
                if len(contents) > MAX_FILE_SIZE:
                    return {"status": "error", "detail": "File too large"}

                # NOMBRE SEGURO
                filename = f"{uuid.uuid4()}.dat"
                file_path = os.path.join(UPLOAD_DIR, filename)

                with open(file_path, "wb") as f:
                    f.write(contents)

                print("FILE SAVED:", file_path)

            await send_email(data, file_path)

            return {"status": "success"}

        else:
            return {"status": "error", "detail": "Unsupported content type"}

    except Exception as e:
        print("ERROR ❌:", e)
        return {"status": "error", "detail": "Internal server error"}