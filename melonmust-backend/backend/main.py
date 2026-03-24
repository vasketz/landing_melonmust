import os
from fastapi import FastAPI
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
ADMIN_EMAIL = os.getenv("EMAIL_USER")  # donde recibes los leads

resend.api_key = RESEND_API_KEY

# =========================
# APP
# =========================
app = FastAPI()

# =========================
# CORS (DEBUG)
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
# EMAIL CON RESEND
# =========================
async def send_email(lead: Lead):
    resend.Emails.send({
        "from": "onboarding@resend.dev",  # luego cambias a tu dominio
        "to": ADMIN_EMAIL,
        "subject": "🚀 Nuevo Lead - MelonMust",
        "html": f"""
        <h2>Nuevo Lead Recibido</h2>
        <p><b>Nombre:</b> {lead.firstName} {lead.lastName}</p>
        <p><b>Email:</b> {lead.email}</p>
        <p><b>Teléfono:</b> {lead.phone}</p>
        <p><b>Monto:</b> {lead.amount}</p>
        <p><b>Negocio:</b> {lead.business}</p>
        """
    })

# =========================
# FIX PREFLIGHT
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
        return {"status": "success"}
    except Exception as e:
        print("EMAIL ERROR ❌:", e)
        return {"status": "error", "detail": str(e)}
