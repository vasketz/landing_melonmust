import aiosmtplib
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

origins = [
	"https://melonmust.com"
	"https://www.melonmust.com"
	"https://melonmust.vercel.app"
]


async def send_email(lead):
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = EMAIL_USER
    message["Subject"] = "🚀 Nuevo Lead - MelonMust from react landing"

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
        password=EMAIL_PASSWORD,  # ⚠️ no tu password normal
    )

# ✅ PRIMERO creas la app
app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok"}

# CORS (para React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# modelo
class Lead(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    amount: str
    business: str | None = None


# endpoint
@app.post("/lead")
async def create_lead(lead: Lead):
    print("NEW LEAD:", lead)

    try:
        await send_email(lead)
        print("EMAIL SENT ✅")
    except Exception as e:
        print("EMAIL ERROR ❌:", e)

    return {"message": "Lead saved"}

