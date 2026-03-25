import os
from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
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
# STATIC FILES (CLAVE)
# =========================
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
# MODELO (JSON)
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
        {
            f"<p><b>Statement:</b> <a href='{data.get('file_url')}'>View File</a></p>"
            if data.get("file_url") else ""
        }
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
# ENDPOINT
# =========================
@app.post("/lead")
async def create_lead(request: Request):

    content_type = request.headers.get("content-type", "")

    try:
        # =========================
        # JSON (lo actual)
        # =========================
        if "application/json" in content_type:
            data = await request.json()
            print("NEW LEAD (JSON):", data)

            await send_email(data)

            return {"status": "success"}

        # =========================
        # FORMDATA (con archivo)
        # =========================
        elif "multipart/form-data" in content_type:
            form = await request.form()

            data = dict(form)
            file = form.get("file")

            print("NEW LEAD (FORM):", data)

            if file and isinstance(file, UploadFile):
                contents = await file.read()

                filename = file.filename.replace(" ", "_")
                file_path = f"uploads/{filename}"

                with open(file_path, "wb") as f:
                    f.write(contents)

                # 🔥 CLAVE: generar URL pública
                file_url = f"https://landing-melonmust.onrender.com/uploads/{filename}"

                # 🔥 CLAVE: agregar al data
                data["file_url"] = file_url

                print(f"FILE SAVED: {file_path}")
                print(f"FILE URL: {file_url}")

            await send_email(data)

            return {"status": "success"}

        else:
            return {"status": "error", "detail": "Unsupported content type"}

    except Exception as e:
        print("ERROR ❌:", e)
        return {"status": "error", "detail": str(e)}
