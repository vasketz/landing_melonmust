import re

def calculate_score(amount: int, business: str, phone: str):
    score = 0

    if amount >= 50000:
        score += 50
    elif amount >= 10000:
        score += 30
    else:
        score += 10
    
    if business:
        score += 20

    if re.match(r"^\+?\d{10, 15}$", phone):
        score += 30

    return score
