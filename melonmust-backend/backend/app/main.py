import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import resend

from app.routes import lead_routes
from app.db import Base, engine

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
    allow_origins=["https://landing-melonmust.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DB INIT
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# ROUTES
# =========================
app.include_router(lead_routes.router)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "ok"}

# =========================
# EMAIL (NO SE TOCA)
# =========================
async def send_email(data: dict, file_bytes=None, filename=None):

    attachments = []

    if file_bytes and filename:
        attachments.append({
            "filename": filename,
            "content": base64.b64encode(file_bytes).decode()
        })

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
        """,
        "attachments": attachments if attachments else None
    })

    print("RESEND RESPONSE:", response)