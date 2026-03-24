import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv

# =========================
# ENV
# =========================
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# =========================
# APP
# =========================
app = FastAPI()

# =========================
# CORS (DEBUG ABIERTO)
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
# MODELO
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
async def send_email(lead: Lead):
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = EMAIL_USER
    message["Subject"] = "🚀 Nuevo Lead - MelonMust"

    message.set_content(f"""
Nuevo lead recibido:

Nombre: {lead.firstName} {lead.lastName}
Email: {lead.email}
Teléfono: {lead.phone}
Monto: {lead.amount}
Negocio: {lead.business}
""")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=EMAIL_USER,
        password=EMAIL_PASSWORD,
    )

# =========================
# FIX PREFLIGHT (CLAVE)
# =========================
@app.options("/lead")
async def options_lead():
    return Response(status_code=200)

# =========================
# ENDPOINT
# =========================
@app.post("/lead")
async def create_lead(lead: Lead):
    print("NEW LEAD:", lead)

    try:
        await send_email(lead)
        print("EMAIL SENT ✅")
    except Exception as e:
        print("EMAIL ERROR ❌:", e)

    return {"message": "Lead saved"}
