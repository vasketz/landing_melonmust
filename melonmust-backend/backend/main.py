import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from pydantic import BaseModel
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
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego restringes a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "ok"}

# =========================
# MODELO (para JSON)
# =========================
class Lead(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    amount: str
    business: str | None = None

# =========================
# EMAIL
# =========================
async def send_email(data: dict):
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
        """
    })

    print("RESEND RESPONSE:", response)

# =========================
# FIX PREFLIGHT
# =========================
@app.options("/lead")
async def options_lead():
    return Response(status_code=200)

# =========================
# ENDPOINT (JSON + FILE)
# =========================
@app.post("/lead")
async def create_lead(request: Request):

    content_type = request.headers.get("content-type", "")

    try:
        # =========================
        # CASO 1: JSON (lo que ya tienes funcionando)
        # =========================
        if "application/json" in content_type:
            data = await request.json()
            print("NEW LEAD (JSON):", data)

            await send_email(data)

            return {"status": "success"}

        # =========================
        # CASO 2: FORMDATA (con archivo)
        # =========================
        elif "multipart/form-data" in content_type:
            form = await request.form()

            data = dict(form)
            file = form.get("file")

            print("NEW LEAD (FORM):", data)

            # guardar archivo si existe
            if file and isinstance(file, UploadFile):
                contents = await file.read()

                os.makedirs("uploads", exist_ok=True)

                file_path = f"uploads/{file.filename}"

                with open(file_path, "wb") as f:
                    f.write(contents)

                print(f"FILE SAVED: {file_path}")

            await send_email(data)

            return {"status": "success"}

        else:
            return {"status": "error", "detail": "Unsupported content type"}

    except Exception as e:
        print("ERROR ❌:", e)
        return {"status": "error", "detail": str(e)}
