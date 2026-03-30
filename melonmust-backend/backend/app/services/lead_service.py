from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.services.encryption import encrypt
from app.services.scoring import calculate_score

def create_lead(db: Session, data: dict):
    score = calculate_score(
        int(data["amount"]),
        data.get("business"),
        data["phone"]
    )

    lead = Lead(
        first_name=data.get("firstName"),
        last_name=data.get("lastName"),
        email_encrypted=encrypt(data.get("email")),
        phone_encrypted=encrypt(data.get("phone")),
        amount=int(data.get("amount")),
        business=data.get("business"),
        score=score
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead

